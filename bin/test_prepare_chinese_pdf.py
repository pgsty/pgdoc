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
            added, removed = module.prepare(path)
            self.assertGreater(added, 0)
            self.assertGreater(removed, 0)
            before, after = ET.fromstring(source), ET.parse(path).getroot()
            self.assertEqual([(n.tag, n.attrib) for n in before.iter()],
                             [(n.tag, n.attrib) for n in after.iter()])
            # Spurious wrap spaces around 、/， are gone, the legal gap before
            # the preserve block stays, and code text is untouched.
            block = next(n for n in after.iter() if n.get('id') == 'pg_stat_activity')
            self.assertEqual(
                ''.join(block.itertext()).replace('\u200b', ''),
                "函数array_agg、pg_stat_activity，http://example"
                "InvalidBackendId（-1）。arg6\n            "
                "SELECT 'a、b_c.d';、正文\n          ")
            self.assertIn('http:/\u200b/example', ''.join(after.itertext()))
            self.assertIn('InvalidBackendId（-1）。\u200barg6', ''.join(after.itertext()))
            # 行首禁则：）。 之间不得留下断行机会
            self.assertNotIn('）\u200b。', ''.join(after.itertext()))
            code = next(n for n in after.iter() if n.get('white-space-treatment') == 'preserve')
            self.assertEqual(code.text, "SELECT 'a、b_c.d';")
            stable = ET.fromstring(ET.tostring(after))
            module.prepare(path)
            self.assertEqual(''.join(stable.itertext()),
                             ''.join(ET.parse(path).getroot().itertext()))

    def test_spurious_cjk_spaces_dropped_and_legal_spaces_kept(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>在大多数情况下，解析器可以从同一家族中其他多态类型的参数推导出多态结
            果类型的实际数据类型。一个例外是，
            <fo:inline>anyarray</fo:inline>，见
            <fo:basic-link>第 38.2 节</fo:basic-link>。 word “term” word
            模块 — 描述
            <fo:inline font-family="Mono">pg_stat_activity</fo:inline> 视图
            字 <fo:inline white-space-treatment="preserve">  保留  </fo:inline> 尾
          </fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            added, removed = module.prepare(path)
            self.assertGreater(added, 0)
            self.assertGreater(removed, 0)
            result = ET.parse(path).getroot()
            block = next(n for n in result.iter() if n.tag.endswith('}block'))
            self.assertEqual(
                ''.join(block.itertext()).replace('\u200b', ''),
                '在大多数情况下，解析器可以从同一家族中其他多态类型的参数推导出多态'
                '结果类型的实际数据类型。一个例外是，'
                'anyarray，见'
                '第 38.2 节。word “term” word'
                '\n            模块 — 描述\n            '
                'pg_stat_activity 视图字  保留  尾'
                '\n          ')
            preserved = next(n for n in result.iter()
                             if n.get('white-space-treatment') == 'preserve')
            self.assertEqual(preserved.text, '  保留  ')
            joined = ''.join(block.itertext())
            # 节点末尾 \u200b + 下一节点以禁则字符开头：跨节点也要移除
            self.assertNotRegex(joined, '\u200b[。，、；：？！）》”’…—]')
            stable = ET.fromstring(ET.tostring(result))
            module.prepare(path)
            self.assertEqual(''.join(stable.itertext()),
                             ''.join(ET.parse(path).getroot().itertext()))

    def test_kinsoku_break_opportunities_never_precede_closing_punct(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>完成（某些情况）。</fo:block>
          <fo:block>列表如下：</fo:block>
          <fo:block>详见<xref/>）。</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)
            joined = ''.join(ET.parse(path).getroot().itertext())
            for bad in ('）\u200b。', '）\u200b）', '：\u200b。'):
                self.assertNotIn(bad, joined)
            self.assertIn('）。\u200b', joined)
            stable = joined
            module.prepare(path)
            self.assertEqual(stable,
                             ''.join(ET.parse(path).getroot().itertext()))

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
                             ['Test CJK', 'Mono,Test CJK', 'Symbol,ZapfDingbats'])

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
            stable = ET.fromstring(ET.tostring(result))
            module.prepare(path, 'Test CJK')
            self.assertEqual(''.join(stable.itertext()),
                             ''.join(ET.parse(path).getroot().itertext()))


if __name__ == '__main__':
    unittest.main()
