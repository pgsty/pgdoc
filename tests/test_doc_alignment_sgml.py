"""Native SGML must distinguish parsing and staging, including empty includes."""
import os
from pathlib import Path
import sys
import tempfile
import unittest

BIN = Path(__file__).resolve().parents[1] / 'bin'
sys.path.insert(0, str(BIN))
from check_doc_alignment import Book
from doc_alignment_sgml import consumed_entities, load_sgml_book


class NativeConsumptionTests(unittest.TestCase):
    def test_unused_general_entity_after_prolog_comment_is_not_consumed(self):
        staging = Path('/tmp/native-source')
        sources = {x: staging / x for x in ['postgres.sgml', 'unused.sgml', 'empty.sgml', 'defs.sgml']}
        declarations = [
            {'name': 'unused', 'target': 'unused.sgml', 'parameter': False},
            {'name': 'empty', 'target': 'empty.sgml', 'parameter': False},
            {'name': 'defs', 'target': 'defs.sgml', 'parameter': True},
        ]
        records = ['L1 postgres.sgml', '_prolog comment', 'f<OSFILE>defs.sgml', 'Tdefs',
                   'f<OSFILE>unused.sgml', 'Tunused', 'f<OSFILE>empty.sgml', 'Tempty',
                   '(BOOK', 'f<OSFILE>empty.sgml', 'Tempty', ')BOOK', 'C']
        used, witnesses = consumed_entities(records, staging, sources, declarations, 'postgres.sgml')
        self.assertEqual(used, {'postgres.sgml', 'defs.sgml', 'empty.sgml'})
        self.assertEqual({w['name'] for w in witnesses}, {'defs', 'empty'})

    def test_ambiguous_parameter_general_namespace_does_not_invent_coverage(self):
        staging = Path('/tmp/native-source')
        declarations = [{'name': 'x', 'target': 'x.sgml', 'parameter': parameter} for parameter in (True, False)]
        with self.assertRaisesRegex(ValueError, 'Ambiguous native entity'):
            consumed_entities(['f<OSFILE>x.sgml', 'Tx', '(BOOK'], staging,
                              {'postgres.sgml': staging/'postgres.sgml', 'x.sgml': staging/'x.sgml'},
                              declarations, 'postgres.sgml')


@unittest.skipUnless(os.environ.get('NSGMLS') and os.environ.get('OSX'), 'Set NSGMLS and OSX for native integration')
class NativeIntegrationTests(unittest.TestCase):
    def parse(self, files):
        temporary = tempfile.TemporaryDirectory(prefix='native-alignment-')
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / 'source'
        root.mkdir()
        for name, text in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        return load_sgml_book(Book(root), Path(temporary.name) / 'audit')

    def test_nested_shorttags_locations_and_unused_entities(self):
        book = self.parse({
            'postgres.sgml': '<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook V4.2//EN" [\n'
                             '<!ENTITY % dead SYSTEM "absent-defs.sgml">\n'
                             '<!ENTITY % active SYSTEM "defs.sgml">%active;\n'
                             '<!ENTITY unused SYSTEM "orphan.sgml">\n'
                             '<!ENTITY missing SYSTEM "absent.sgml">\n'
                             ']><book id="b"><title>Book</title>&ch;&empty;</book>',
            'defs.sgml': '<!ENTITY ch SYSTEM "sub/ch.sgml"><!ENTITY sec SYSTEM "sub/sec.sgml"><!ENTITY empty SYSTEM "empty.sgml">',
            'sub/ch.sgml': '<chapter id="c">\n<title>Chapter</title>\n&sec;</chapter>',
            'sub/sec.sgml': '<sect1 id="s"><title>Section</title>\n<para>Text <literal>code</>.</para></sect1>',
            'empty.sgml': '<!-- consumed comment only -->',
            'orphan.sgml': '<!-- staged but not consumed -->',
        })
        self.assertTrue(book.complete, book.errors)
        self.assertEqual({d['file'] for d in book.dependencies.values()},
                         {'postgres.sgml', 'defs.sgml', 'sub/ch.sgml', 'sub/sec.sgml', 'empty.sgml'})
        self.assertEqual({e['to'] for e in book.edges}, {'defs.sgml', 'sub/ch.sgml', 'sub/sec.sgml', 'empty.sgml'})
        self.assertEqual(next(n for n in book.nodes if n.tag == 'literal').file, 'sub/sec.sgml')
        self.assertEqual(next(n for n in book.nodes if n.tag == 'literal').line, 2)
        self.assertEqual(next(r['role'] for r in book.inventory()['source']['files'] if r['path']=='orphan.sgml'), 'orphan_sgml')

    def test_missing_used_entity_and_malformed_native_sgml_fail(self):
        for body in ('&missing;', '<sect1><title>Wrong nesting</title></chapter>'):
            book = self.parse({'postgres.sgml': '<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook V4.2//EN" '
                               '[<!ENTITY missing SYSTEM "absent.sgml">]><book><title>Book</title>' + body + '</book>'})
            self.assertFalse(book.complete)
            self.assertTrue(book.errors)


if __name__ == '__main__':
    unittest.main()
