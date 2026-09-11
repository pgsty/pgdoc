"""Small adversarial books exercise identity, includes and conservative matching."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'bin/check_doc_alignment.py'
spec = importlib.util.spec_from_file_location('alignment', SCRIPT)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


class AlignmentTests(unittest.TestCase):
    def compare(self, en, zh, extra_en=None, extra_zh=None):
        with tempfile.TemporaryDirectory(prefix='alignment-test-', dir=SCRIPT.parents[1] / 'tmp') as tmp:
            root = Path(tmp)
            books = []
            for side, doc, extra in [('en', en, extra_en), ('zh', zh, extra_zh)]:
                directory = root / side
                directory.mkdir()
                for rel, text in {'postgres.sgml': doc, **(extra or {})}.items():
                    path = directory / rel
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(text)
                books.append(m.Book(directory).parse())
            return m.Alignment(*books).run()

    def codes(self, a):
        return {f['code'] for f in a.findings}

    def test_equal_counts_missing_and_extra_ids(self):
        a = self.compare('<book id="b"><chapter id="wanted"/></book>',
                         '<book id="b"><chapter id="other"/></book>')
        self.assertEqual(len(a.en.nodes), len(a.zh.nodes))
        self.assertIn('missing_id', self.codes(a))
        self.assertIn('extra_id', self.codes(a))

    def test_duplicate_xml_id(self):
        a = self.compare('<book><anchor xml:id="x"/></book>',
                         '<book><anchor xml:id="x"/><anchor id="x"/></book>')
        f = next(f for f in a.findings if f['code'] == 'duplicate_id')
        self.assertEqual(len(f['details']['occurrences']), 2)

    def test_parent_level_and_sibling_order(self):
        en = '<book id="b"><chapter id="a"><sect1 id="x"/><sect1 id="y"/></chapter><chapter id="c"/></book>'
        zh = '<book id="b"><chapter id="c"><sect2 id="x"/></chapter><chapter id="a"><sect1 id="y"/></chapter></book>'
        a = self.compare(en, zh)
        self.assertTrue({'node_kind', 'parent_or_level', 'sibling_order'} <= self.codes(a))

    def test_same_parent_reverse_order(self):
        a = self.compare('<book id="b"><section id="x"/><section id="y"/></book>',
                         '<book id="b"><section id="y"/><section id="x"/></book>')
        self.assertIn('sibling_order', self.codes(a))

    def test_single_anonymous_titles_are_translations(self):
        a = self.compare('<book id="b"><title>Database architecture</title><section><title>Storage</title></section></book>',
                         '<book id="b"><title>数据库架构</title><section><title>存储</title></section></book>')
        self.assertEqual(a.findings, [])
        self.assertEqual(len(a.titles), 2)
        self.assertTrue(all(t['semantic_status'] == 'not_automatically_verified' for t in a.titles))

    def test_anonymous_repeated_sections_are_not_forced_by_ordinal(self):
        en = '<book id="b"><section><title>One</title></section><section><title>Two</title></section></book>'
        zh = '<book id="b"><section><title>二</title></section><section><title>一</title></section></book>'
        a = self.compare(en, zh)
        self.assertIn('anonymous_alignment', self.codes(a))
        self.assertEqual(len(a.titles), 0)

    def test_anonymous_between_identified_neighbors(self):
        en = '<book id="b"><anchor id="x"/><informaltable><tgroup cols="1"><tbody><row><entry>Yes</entry></row></tbody></tgroup></informaltable><anchor id="y"/></book>'
        a = self.compare(en, en.replace('Yes', '是'))
        self.assertEqual(len(a.tables), 1)
        self.assertNotIn('boolean_fact', self.codes(a))
        self.assertEqual(len(a.tables[0]['paired_rows']), 1)

    def test_cross_file_parameter_and_general_entities(self):
        entry = '<!DOCTYPE book [<!ENTITY % files SYSTEM "filelist.sgml">%files;]><book id="b">&chapter;</book>'
        extra = {'filelist.sgml': '<!ENTITY chapter SYSTEM "sub/ch.sgml">',
                 'sub/ch.sgml': '<chapter id="c">\n<title>Title</title>\n&section;</chapter>',
                 'sub/section.sgml': '<section id="s"><title>Nested</title></section>'}
        extra['filelist.sgml'] += '<!ENTITY section SYSTEM "sub/section.sgml">'
        a = self.compare(entry, entry, extra, extra)
        self.assertTrue(a.en.complete, a.en.errors)
        self.assertEqual(a.findings, [])
        ch = next(n for n in a.en.nodes if n.ident == 'c')
        self.assertEqual((ch.file, ch.line), ('sub/ch.sgml', 1))
        self.assertEqual(next(n for n in a.en.nodes if n.tag == 'title').line, 2)
        self.assertEqual({e['to'] for e in a.en.edges}, {'filelist.sgml', 'sub/ch.sgml', 'sub/section.sgml'})

    def test_declared_but_unused_entity_is_not_included(self):
        en = '<!DOCTYPE book [<!ENTITY unused SYSTEM "absent.sgml">]><book id="b"/>'
        a = self.compare(en, en)
        self.assertTrue(a.en.complete)
        self.assertFalse(a.en.edges)

    def test_missing_included_file_and_undefined_entity_fail(self):
        for entry in ['<!DOCTYPE book [<!ENTITY missing SYSTEM "absent.sgml">]><book>&missing;</book>',
                      '<book>&undefined;</book>']:
            a = self.compare(entry, '<book/>')
            self.assertFalse(a.en.complete)
            self.assertTrue(a.en.errors)
            self.assertFalse(a.pairs)

    def test_comments_and_cdata_not_markup(self):
        en = '<book id="b"><!-- <section id="fake"/> &missing; --><programlisting><![CDATA[<section id="not-an-id"/> &unknown;]]></programlisting></book>'
        a = self.compare(en, en)
        self.assertTrue(a.en.complete, a.en.errors)
        self.assertEqual([n.ident for n in a.en.nodes if n.ident], ['b'])
        self.assertEqual(a.en.events, {'comments': 1, 'cdata': 1})

    def test_internal_references_are_book_wide(self):
        en = '<book id="b"><section id="x"/><para><xref linkend="x"/></para></book>'
        a = self.compare(en, en.replace('linkend="x"', 'linkend="gone"'))
        self.assertIn('unresolved_reference', self.codes(a))

    def test_table_missing_function_row_overload_and_boolean(self):
        def row(name, typ, fact):
            return f'<row><entry><para role="func_signature"><function>{name}</function>(<type>{typ}</type>)</para></entry><entry>{fact}</entry></row>'
        def table(rows):
            return '<book id="b"><table id="t"><title>Functions</title><tgroup cols="2"><tbody>' + rows + '</tbody></tgroup></table></book>'
        en = table(row('array_agg', 'anyarray', 'Yes') + row('array_agg', 'anynonarray', 'Yes') + row('new_fn', 'text', 'No'))
        zh = table(row('array_agg', 'anyarray', 'No') + row('array_agg', 'anynonarray', 'No'))
        a = self.compare(en, zh)
        self.assertTrue({'table_shape', 'table_function_identifiers', 'boolean_fact'} <= self.codes(a))
        self.assertEqual(sum(f['code'] == 'boolean_fact' for f in a.findings), 2)
        self.assertEqual(a.tables[0]['function_delta']['missing'], {'new_fn': 1})

    def test_style_attributes_not_byte_compared(self):
        en = '<book id="b"><table id="t" frame="all"><title>Example</title><tgroup cols="1"><tbody><row><entry align="left">X</entry></row></tbody></tgroup></table></book>'
        zh = en.replace('frame="all"', 'frame="none"').replace('align="left"', 'align="center"').replace('Example', '示例')
        a = self.compare(en, zh)
        self.assertEqual(a.findings, [])

    def test_cals_column_names_are_local_aliases(self):
        en = '<book id="b"><table id="t"><tgroup cols="2"><colspec colname="a"/><colspec colname="b"/><tbody><row><entry namest="a" nameend="b">X</entry></row></tbody></tgroup></table></book>'
        zh = en.replace('colname="a"', 'colname="left"').replace('colname="b"', 'colname="right"').replace('namest="a"', 'namest="left"').replace('nameend="b"', 'nameend="right"')
        self.assertNotIn('cell_span', self.codes(self.compare(en, zh)))
        invalid = en.replace('nameend="b"', 'nameend="unknown"')
        self.assertIn('table_grid_invalid', self.codes(self.compare(en, invalid)))

    def test_existing_reference_retarget_is_detected(self):
        en = '<book id="b"><anchor id="x"/><anchor id="y"/><para><xref linkend="x"/></para></book>'
        a = self.compare(en, en.replace('linkend="x"', 'linkend="y"'))
        self.assertIn('internal_reference_targets', self.codes(a))
        self.assertNotIn('unresolved_reference', self.codes(a))

    def test_cals_namest_without_nameend_matches_docbook_single_column(self):
        en = '<book id="b"><table id="t"><tgroup cols="4"><colspec colname="last" colnum="4"/><tbody><row><entry namest="last">X</entry></row></tbody></tgroup></table></book>'
        a = self.compare(en, en.replace('namest="last"', 'colname="last"'))
        self.assertNotIn('table_grid_invalid', self.codes(a))
        self.assertNotIn('cell_span', self.codes(a))
        table = next(n for n in a.en.nodes if n.tag == 'table')
        self.assertEqual(list(m.table_grid(table).values()), [(4, 4, 0)])
        invalid = en.replace('namest="last"', 'namest="unknown"')
        self.assertIn('table_grid_invalid', self.codes(self.compare(en, invalid)))
        overflow = en.replace('</entry></row>', '</entry><entry>Y</entry></row>')
        self.assertIn('table_grid_invalid', self.codes(self.compare(en, overflow)))

    def test_namespace_aliased_xinclude_is_explicitly_incomplete(self):
        entry = '<book xmlns:files="http://www.w3.org/2001/XInclude"><files:include href="missing.xml"/></book>'
        a = self.compare(entry, entry)
        self.assertFalse(a.en.complete)
        self.assertIn('Unsupported XInclude', a.en.errors[0])

    def test_catalog_function_reference_is_not_function_definition(self):
        en = '<book id="b"><table id="t"><tgroup cols="1"><tbody><row><entry><para><structfield>field</structfield> <type>int</type></para><para>Calls <function>internal_fn</function>.</para></entry></row></tbody></tgroup></table></book>'
        a = self.compare(en, en.replace('<function>internal_fn</function>', '内部函数'))
        self.assertNotIn('table_function_identifiers', self.codes(a))

    def test_standard_reference_titles_pair_without_ordinal_assumption(self):
        en = '<book id="b"><refentry id="r"><refsect1><title>Description</title></refsect1><refsect1><title>Examples</title></refsect1></refentry></book>'
        zh = '<book id="b"><refentry id="r"><refsect1><title>示例</title></refsect1><refsect1><title>描述</title></refsect1></refentry></book>'
        a = self.compare(en, zh)
        self.assertIn('sibling_order', self.codes(a))
        self.assertNotIn('anonymous_alignment', self.codes(a))

    def test_ambiguity_and_incomplete_inputs_cannot_return_zero(self):
        self.assertEqual(m.exit_status(False, True, {}), 2)
        self.assertEqual(m.exit_status(True, True, {'ambiguous': 1}), 3)
        self.assertEqual(m.exit_status(True, True, {'definite': 1, 'ambiguous': 1}), 1)
        self.assertEqual(m.exit_status(True, True, {'review': 1}), 0)

    def test_translated_function_table_header_is_not_signature_defect(self):
        en = '<book id="b"><table id="t"><tgroup cols="1"><thead><row><entry><para role="func_signature">Function</para></entry></row></thead><tbody><row><entry><para role="func_signature"><function>f</function>()</para></entry></row></tbody></tgroup></table></book>'
        a = self.compare(en, en.replace('>Function<', '>函数<'))
        self.assertEqual(a.findings, [])

    def test_plain_english_cell_is_not_a_definite_missing_identifier(self):
        en = '<book id="b"><table id="t"><tgroup cols="1"><tbody><row><entry>Serializable</entry></row></tbody></tgroup></table></book>'
        a = self.compare(en, en.replace('Serializable', '可序列化'))
        self.assertFalse(any(f['category'] == 'definite' for f in a.findings))


if __name__ == '__main__':
    unittest.main()
