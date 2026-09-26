"""A downstream filter must not turn a rejected SGML input into success."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from patch_legacy_xsl_pipeline import guard_sgml_pipelines, prepare_legacy_indexes, patch_pg7x, expand_sdata_fixups, prepare_native_xsl_index


@unittest.skipUnless(shutil.which('make'), 'make required')
class LegacyPipelineTests(unittest.TestCase):
    def test_generated_pg8_normalizer_is_english_only(self):
        repo = Path(__file__).resolve().parent.parent
        upstream_makefile = repo/'en/8.0.26/Makefile'
        if not upstream_makefile.exists():
            self.skipTest('fixed PostgreSQL 8.0.26 source required')
        for name, english in (
                ('standalone-en-8.0.26.fixture', True),
                ('standalone-pdf-en-8.0.26.fixture', True),
                ('standalone-zh-8.0.26.fixture', False),
                ('standalone-pdf-zh-8.0.26.fixture', False),
                ('unidentified-directory', False)):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                build = Path(tmp)/name
                root = build/'doc/src/sgml'
                root.mkdir(parents=True)
                (build/'src').mkdir()
                (build/'src/Makefile.global').write_text(
                    'srcdir = .\ntop_srcdir = ../../..\nVERSION = 8.0.26\n'
                    f'PERL = perl\nPYTHON = {sys.executable}\n')
                shutil.copy2(upstream_makefile, root/'Makefile')
                (root/'filelist.sgml').write_text('<!-- fixture -->\n')
                (root/'postgres.sgml').write_text(
                    '<book><title>Fixture</title>\n &bookindex;\n</book>')
                patched = subprocess.run(
                    [sys.executable, str(repo/'bin/patch_legacy_xsl_pipeline.py'), str(root)],
                    capture_output=True, text=True)
                self.assertEqual(patched.returncode, 0, patched.stderr)
                generated = (root/'Makefile').read_text()
                self.assertEqual('normalize_cals_tables.py' in generated, english)
                failed = subprocess.run(
                    ['make', '-C', str(root), 'GENERATED_SGML=', 'OSX=false', 'postgres.xml'],
                    capture_output=True, text=True)
                self.assertIn('false -D.', failed.stdout)
                self.assertNotEqual(failed.returncode, 0)
                # Use the real generated recipe on a converter fixture whose
                # ragged CALS declaration changes only in an English build.
                (root/'postgres.xml').unlink(missing_ok=True)
                converter = build/'fixture-osx'
                converter.write_text(
                    '#!/bin/sh\ncat <<\'XML\'\n<?xml version="1.0"?>\n'
                    '<book><title>Fixture</title><table><title>Grid</title>'
                    '<tgroup cols="2"><tbody><row><entry>A</entry>'
                    '<entry>B</entry><entry>C</entry></row></tbody></tgroup>'
                    '</table></book>\nXML\n')
                converter.chmod(0o755)
                success = subprocess.run(
                    ['make', '-C', str(root), 'GENERATED_SGML=',
                     f'OSX={converter}', 'postgres.xml'], capture_output=True, text=True)
                self.assertEqual(success.returncode, 0, success.stderr)
                self.assertIn(f'cols="{3 if english else 2}"',
                              (root/'postgres.xml').read_text())

    def test_native_xsl_index_is_enabled_without_replacing_targets(self):
        for recipe in ('\t$(OSX) -D. -x lower $< >postgres.xmltmp\n',
                       '\t$(OSX) -D. -x lower -i include-xslt-index $< >postgres.xmltmp\n'):
            with self.subTest(recipe=recipe), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                target = 'xslthtml-stamp: stylesheet.xsl postgres.xml\n\t$(XSLTPROC) $^\n\ttouch $@\n'
                (root/'Makefile').write_text('postgres.xml: postgres.sgml\n' + recipe + target)
                (root/'filelist.sgml').write_text('<!ENTITY % include-index "IGNORE">\n')
                (root/'postgres.sgml').write_text('<book>\n<![%include-index;[&bookindex;]]>\n</book>')
                prepare_native_xsl_index(tmp)
                first = {p.name:p.read_bytes() for p in root.iterdir()}
                self.assertIn(target, (root/'Makefile').read_text())
                self.assertIn('-i include-xslt-index', (root/'Makefile').read_text())
                self.assertIn('<index id="bookindex"></index>', (root/'postgres.sgml').read_text())
                self.assertIn('<!ENTITY % include-xslt-index "IGNORE">', (root/'filelist.sgml').read_text())
                prepare_native_xsl_index(tmp)
                self.assertEqual(first, {p.name:p.read_bytes() for p in root.iterdir()})

    def test_native_xsl_does_not_enable_a_commented_out_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'postgres.sgml').write_text('<book><!--<![%include-index;[&bookindex;]]>--></book>')
            prepare_native_xsl_index(tmp)
            self.assertEqual(len(list(root.iterdir())), 1)

    def test_iso_entity_filter_preserves_literal_option_brackets(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'Makefile'
            command = r"s/\[(amp|quot|lt|gt) *\]/\&\1;/gi;"
            path.write_text(command)
            expand_sdata_fixups(tmp)
            once = path.read_text()
            expand_sdata_fixups(tmp)
            self.assertEqual(path.read_text(), once)
            result = subprocess.check_output(['perl','-p','-e',once],
                input='[percnt]s [dollar]HOME [forall] 0[ndash ]127 [Aacute] [aacute] [bull] f[ast] [num]', text=True)
            self.assertEqual(result, '&percnt;s &dollar;HOME &forall; 0&ndash;127 &Aacute; &aacute; &bull; f[ast] [num]')

    def test_generated_chinese_pg7_pipeline_rejects_converter_failure(self):
        for name in ('standalone-zh-7.3.21.fixture', 'standalone-pdf-zh-7.3.21.fixture',
                     'unidentified-directory'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)/name
                root.mkdir()
                (root/'Makefile').write_text('OSX = false\nhtml:\n\t@true\n')
                (root/'postgres.sgml').write_text(
                    '<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook V3.1//EN">\n'
                    '<book><title>Fixture</title></book>')
                self.assertTrue(patch_pg7x(str(root)))
                guard_sgml_pipelines(str(root))
                generated = (root/'Makefile').read_text()
                self.assertNotIn('|| true; } |', generated)
                if name.startswith('standalone'):
                    self.assertIn('PGDOC_VERSION ?= 7.3.21', generated)
                result = subprocess.run(['make','-s','-C',str(root),'postgres.xml'],
                                        capture_output=True)
                self.assertNotEqual(result.returncode, 0)

    def test_multibook_index_is_enabled_without_overwriting_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'setindex.sgml'
            prepare_legacy_indexes(tmp, '<book></book>')
            self.assertFalse(path.exists())
            prepare_legacy_indexes(tmp, '<set>&setindex;</set>')
            self.assertEqual(path.read_text(), '<setindex id="setindex"></setindex>\n')
            path.write_text('<setindex><title>Existing index</title></setindex>')
            prepare_legacy_indexes(tmp, '<set>&setindex;</set>')
            self.assertIn('Existing index', path.read_text())
            prepare_legacy_indexes(tmp, '<book>&bookindex;</book>')
            self.assertEqual((Path(tmp)/'bookindex.sgml').read_text(),
                             '<index id="bookindex"></index>\n')

    def test_converter_failure_is_not_masked_by_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'Makefile'
            path.write_text('OSX = false\nall:\n\t$(OSX) input.sgml | cat > postgres.xml\n')
            before = subprocess.run(['make','-s','-C',tmp], capture_output=True)
            self.assertEqual(before.returncode, 0)
            guard_sgml_pipelines(tmp)
            once = path.read_bytes()
            guard_sgml_pipelines(tmp)
            self.assertEqual(once, path.read_bytes())
            after = subprocess.run(['make','-s','-C',tmp], capture_output=True)
            self.assertNotEqual(after.returncode, 0)


if __name__ == '__main__':
    unittest.main()
