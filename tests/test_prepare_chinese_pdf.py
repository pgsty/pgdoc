"""Regression checks for print-only layout changes and protected source text."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location(
    'prepare_chinese_pdf', Path(__file__).resolve().parents[1] / 'bin/prepare_chinese_pdf.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ChinesePdfTests(unittest.TestCase):
    def test_layout_preserves_code_links_and_existing_breaks(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block id="pg_stat_activity">函数<fo:inline>array_agg</fo:inline>、
            <fo:basic-link internal-destination="pg_stat_activity">pg_stat_activity</fo:basic-link>，
            http:/\u200b/example<branch xmlns="urn:example"/>InvalidBackendId（-1）。arg6
            <fo:block white-space-treatment="preserve">SELECT 'a、b_c.d';</fo:block>、正文
          </fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            self.assertGreater(module.prepare(path), 0)
            before, after = ET.fromstring(source), ET.parse(path).getroot()
            self.assertEqual([(n.tag,n.attrib) for n in before.iter()],
                             [(n.tag,n.attrib) for n in after.iter()])
            self.assertEqual(''.join(before.itertext()).replace('\u200b',''),
                             ''.join(after.itertext()).replace('\u200b',''))
            self.assertIn('http:/\u200b/example', ''.join(after.itertext()))
            self.assertIn('InvalidBackendId（-1）\u200b。\u200barg6', ''.join(after.itertext()))
            code = next(n for n in after.iter() if n.get('white-space-treatment') == 'preserve')
            self.assertEqual(code.text, "SELECT 'a、b_c.d';")
            self.assertEqual(module.prepare(path), 0)

    def test_cjk_metrics_do_not_change_latin_or_symbol_fonts(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:inline font-family="Mono,Test CJK">见说明</fo:inline>
          <fo:inline font-family="Mono,Test CJK">array_agg</fo:inline>
          <fo:inline font-family="Symbol,ZapfDingbats">→</fo:inline>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'Test CJK')
            self.assertEqual([n.get('font-family') for n in ET.parse(path).getroot()],
                             ['Test CJK','Mono,Test CJK','Symbol,ZapfDingbats'])

    def test_long_type_names_and_verbatim_rules_keep_their_text(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:table-cell><fo:block><fo:inline>anycompatiblemultirange</fo:inline></fo:block></fo:table-cell>
          <fo:block font-family="Mono,Test CJK" white-space-treatment="preserve">''' + '-' * 74 + '''
    155173    accounts</fo:block></fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'Test CJK')
            result = ET.parse(path).getroot()
            self.assertEqual(''.join(ET.fromstring(source).itertext()), ''.join(result.itertext()))
            resized = [n for n in result.iter() if n.get('font-size') == '8.5pt']
            self.assertEqual(len(resized), 2)
            self.assertEqual(module.prepare(path, 'Test CJK'), 0)


if __name__ == '__main__':
    unittest.main()
