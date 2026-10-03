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
    def test_footnote_body_does_not_interfere_with_inline_spacing(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>一份<fo:basic-link external-destination="url(https://example.org)">语言接口列表
          </fo:basic-link><fo:footnote><fo:inline baseline-shift="super">1</fo:inline><fo:footnote-body><fo:block><fo:inline>1</fo:inline> https://example.org</fo:block></fo:footnote-body></fo:footnote>。继续阅读。</fo:block>
          <fo:block>See <fo:basic-link>drivers </fo:basic-link><fo:footnote><fo:inline>2</fo:inline><fo:footnote-body><fo:block>2 link</fo:block></fo:footnote-body></fo:footnote>for details.</fo:block>
          <fo:block white-space-treatment="preserve"><fo:basic-link>语言接口列表
          </fo:basic-link><fo:footnote><fo:inline>3</fo:inline><fo:footnote-body><fo:block>3 link</fo:block></fo:footnote-body></fo:footnote>。保留代码。</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)
            blocks = list(ET.parse(path).getroot())
            ns = {'fo': 'http://www.w3.org/1999/XSL/Format'}
            self.assertEqual(blocks[0].find('fo:basic-link', ns).text, '语言接口列表')
            body = blocks[0].find('.//fo:footnote-body', ns)
            self.assertEqual(''.join(body.itertext()), '1 https://example.org')
            self.assertEqual(''.join(blocks[1].itertext()), 'See drivers22 link for details.')
            self.assertEqual(blocks[2].find('fo:basic-link', ns).text,
                             '语言接口列表\n          ')
            stable = path.read_bytes()
            module.prepare(path)
            self.assertEqual(path.read_bytes(), stable)

    def test_footnote_anchor_attaches_to_reference_number(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>这种格式与 <fo:basic-link><fo:inline>RFC 5803 </fo:inline></fo:basic-link><fo:footnote><fo:inline baseline-shift="super">1</fo:inline><fo:footnote-body><fo:block>1 https://example.org/rfc5803</fo:block></fo:footnote-body></fo:footnote>中指定的格式相同。</fo:block>
          <fo:block white-space-treatment="preserve"><fo:basic-link>RFC 5803 </fo:basic-link><fo:footnote><fo:inline>1</fo:inline><fo:footnote-body><fo:block>1 original body</fo:block></fo:footnote-body></fo:footnote>中指定的格式相同。</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)
            blocks = list(ET.parse(path).getroot())
            ns = {'fo': 'http://www.w3.org/1999/XSL/Format'}
            self.assertEqual(''.join(blocks[0].find('fo:basic-link', ns).itertext()),
                             'RFC 5803')
            note = blocks[0].find('fo:footnote', ns)
            self.assertEqual(note.tail.replace('\u200b', ''), ' 中指定的格式相同。')
            self.assertEqual(''.join(note.find('fo:footnote-body', ns).itertext()).replace('\u200b', ''),
                             '1 https://example.org/rfc5803')
            self.assertEqual(blocks[1].find('fo:basic-link', ns).text, 'RFC 5803 ')
            self.assertEqual(blocks[1].find('fo:footnote', ns).tail,
                             '中指定的格式相同。')
            stable = path.read_bytes()
            module.prepare(path)
            self.assertEqual(path.read_bytes(), stable)

    def test_link_wrapper_padding_cannot_push_punctuation_to_next_line(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>调用 <fo:basic-link internal-destination="function"><fo:inline><fo:inline font-family="Courier New,Test CJK">PQconsumeInput</fo:inline>
          </fo:inline></fo:basic-link>，然后检查。</fo:block>
          <fo:block white-space-treatment="preserve"><fo:inline><fo:inline font-family="Courier New,Test CJK">code</fo:inline>
          </fo:inline>，保持代码空白。</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'Test CJK')
            tree = ET.parse(path)
            link = next(n for n in tree.iter() if n.tag.endswith('}basic-link'))
            self.assertEqual(''.join(link.itertext()), 'PQconsumeInput')
            code = [n for n in tree.iter() if n.tag.endswith('}block')][1]
            self.assertEqual(''.join(code.itertext()), 'code\n          ，保持代码空白。')
            stable = path.read_bytes()
            module.prepare(path, 'Test CJK')
            self.assertEqual(path.read_bytes(), stable)

    def test_reference_tail_spacing_settles_before_serialization(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>详见<fo:basic-link internal-destination="json"><fo:inline>表 9.47</fo:inline></fo:basic-link>。
          \u200b</fo:block><fo:block>下一段。</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)
            stable = path.read_bytes()
            module.prepare(path)
            self.assertEqual(path.read_bytes(), stable)
            self.assertEqual(''.join(ET.parse(path).getroot().itertext()).replace('\u200b','').split(),
                             ['详见表', '9.47。下一段。'])

    def test_nested_code_parameters_keep_tokens_without_binding_phrase(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block><fo:inline font-family="Courier New,Test CJK"><fo:inline font-family="Courier New,Test CJK" font-style="italic">name\u200b</fo:inline> <fo:inline font-family="Courier New,Test CJK" font-style="italic">datatype\u200b</fo:inline></fo:inline> 参数。</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'Test CJK')
            nodes = [n for n in ET.parse(path).iter() if n.tag.endswith('}inline')]
            self.assertIsNone(nodes[0].get('keep-together.within-line'))
            self.assertEqual([n.get('keep-together.within-line') for n in nodes[1:]], ['always', 'always'])
            self.assertEqual(''.join(nodes[0].itertext()), 'name\u200b datatype\u200b')
            stable = path.read_bytes()
            module.prepare(path, 'Test CJK')
            self.assertEqual(path.read_bytes(), stable)

    def test_synopsis_prose_island_with_whitespace_only_prefix(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block white-space-treatment="preserve" font-family="Courier New,Test CJK"><fo:inline> \n<fo:inline font-family="Courier New">name</fo:inline>与值相同</fo:inline></fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'Test CJK')
            block = next(n for n in ET.parse(path).iter() if n.tag.endswith('}block'))
            self.assertEqual(''.join(block.itertext()), ' \nname 与值相同')
            stable = path.read_bytes()
            module.prepare(path, 'Test CJK')
            self.assertEqual(path.read_bytes(), stable)

    def test_prose_technical_punctuation_is_not_rewritten(self):
        prose='如果使用SSL压缩，则返回"on"，否则返回"off"。#: 注释和#, 标志；分钟:秒。'
        source='<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:block>'+prose+'</fo:block></fo:root>'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.fo';path.write_text(source);module.prepare(path)
            result=''.join(ET.parse(path).getroot().itertext()).replace('\u200b','')
            self.assertEqual(result,prose.replace('使用SSL压缩','使用 SSL 压缩'))
            stable=path.read_bytes();module.prepare(path);self.assertEqual(stable,path.read_bytes())

    def test_nested_spacing_is_fixed_without_changing_optimum_or_header(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:static-content flow-name="xsl-region-before"><fo:block space-before.minimum="8pt" space-before.optimum="10pt" space-before.maximum="12pt">header</fo:block></fo:static-content><fo:flow flow-name="xsl-region-body"><fo:list-block><fo:list-item space-before.minimum="8pt" space-before.optimum="10pt" space-before.maximum="12pt"><fo:list-item-body><fo:block space-after.minimum="4pt" space-after.optimum="5pt" space-after.maximum="6pt">正文。</fo:block></fo:list-item-body></fo:list-item></fo:list-block></fo:flow></fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.fo';path.write_text(source);module.prepare(path)
            root=ET.parse(path).getroot();nodes=list(root.iter())
            header=next(n for n in nodes if n.text and n.text.strip()=='header')
            self.assertEqual(header.get('space-before.minimum'),'8pt')
            item=next(n for n in nodes if n.tag.endswith('}list-item'))
            self.assertEqual([item.get('space-before.'+x) for x in ['minimum','optimum','maximum']],['10pt']*3)
            para=next(n for n in nodes if n.text and n.text.startswith('正文'))
            self.assertEqual([para.get('space-after.'+x) for x in ['minimum','optimum','maximum']],['5pt']*3)
            stable=path.read_bytes();module.prepare(path);self.assertEqual(stable,path.read_bytes())

    def test_protected_symbol_literals_gain_only_an_external_gap(self):
        literals=['-Xstream', '--jobs', '/dev/null', '~/.pgpass', '%APPDATA%', '$PGDATA']
        source='<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">'+''.join(
            '<fo:block>使用<fo:inline font-family="Courier New">'+s+'</fo:inline>选项。</fo:block>' for s in literals)+'</fo:root>'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.fo';path.write_text(source);module.prepare(path)
            root=ET.parse(path).getroot()
            self.assertEqual([n.text.replace('\u200b','') for n in root.iter() if n.tag.endswith('}inline')],literals)
            for node,s in zip(root,literals):
                self.assertEqual(''.join(node.itertext()).replace('\u200b',''),'使用 '+s+' 选项。')
            stable=path.read_bytes();module.prepare(path);self.assertEqual(stable,path.read_bytes())

    def test_autosizing_uses_inherited_font_and_actual_flow_indents(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format" font-size="10pt">
          <fo:layout-master-set><fo:simple-page-master master-name="body-first" page-width="612pt" margin-left="72pt" margin-right="72pt"><fo:region-body/></fo:simple-page-master></fo:layout-master-set>
          <fo:flow start-indent="48pt" end-indent="12pt"><fo:block margin-left="4em"><fo:block font-family="Courier New" white-space-treatment="preserve">'''+('x'*70)+'''</fo:block></fo:block></fo:flow>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'test.fo';path.write_text(source);module.prepare(path)
            code=next(n for n in ET.parse(path).iter() if n.get('white-space-treatment')=='preserve')
            self.assertEqual(code.text,'x'*70)
            self.assertEqual(code.get('font-size'),'8.4pt')
            stable=path.read_bytes();module.prepare(path);self.assertEqual(stable,path.read_bytes())

    def test_full_prepare_preserves_synopsis_and_code_and_is_idempotent(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block white-space-treatment="preserve" font-family="Courier New,Test CJK">SQL
<fo:inline>其中 <fo:inline font-family="Courier New">X</fo:inline>与<fo:inline font-family="Courier New">Y</fo:inline>相同：</fo:inline>
<fo:inline>UNIQUE、PRIMARY KEY和EXCLUDE约束中的<fo:inline font-family="Courier New">index_parameters</fo:inline>为：</fo:inline></fo:block>
          <fo:block>短语<fo:inline font-family="Courier New,Test CJK">"加引号的文本"<fo:inline> 中 文  x,y </fo:inline></fo:inline>结束。</fo:block>
          <fo:table-row><fo:table-cell><fo:block><fo:inline font-family="Courier New" font-style="italic">pretty</fo:inline> <fo:inline font-family="Courier New">boolean</fo:inline></fo:block></fo:table-cell></fo:table-row>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'Test CJK')
            result = ET.parse(path).getroot()
            blocks = [n for n in result.iter() if n.tag.endswith('}block')]
            self.assertEqual(''.join(blocks[0].itertext()),
                             'SQL\n其中 X 与 Y 相同：\nUNIQUE、PRIMARY KEY 和 EXCLUDE 约束中的 index_parameters 为：')
            literal = next(n for n in result.iter() if n.text == '"加引号的文本"')
            self.assertEqual(''.join(literal.itertext()), '"加引号的文本" 中 文  x,y ')
            self.assertIn('Courier New', literal.get('font-family'))
            self.assertEqual(''.join(blocks[2].itertext()), 'pretty boolean')
            row = next(n for n in result.iter() if n.tag.endswith('}table-row'))
            self.assertEqual(row.get('keep-together.within-column'), '10')
            first = path.read_bytes()
            module.prepare(path, 'Test CJK')
            self.assertEqual(path.read_bytes(), first)

    def test_email_can_wrap_in_a_table_without_changing_address(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:table-cell><fo:block><fo:inline keep-together.within-line="always">&lt;pgman@candle.pha.pa.us&gt;</fo:inline></fo:block></fo:table-cell>
          <fo:block><fo:inline keep-together.within-line="always">&lt;a@example.org&gt;</fo:inline></fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)[0] if False else module.prepare(path)
            inline = [n for n in ET.parse(path).iter() if n.tag.endswith('}inline')]
            self.assertEqual(inline[0].get('keep-together.within-line'), 'auto')
            self.assertEqual(inline[0].text.replace('\u200b', ''), '<pgman@candle.pha.pa.us>')
            self.assertIn('@\u200b', inline[0].text)
            self.assertEqual(inline[1].get('keep-together.within-line'), 'always')
            self.assertNotIn('@\u200b', inline[1].text)

    def test_quoted_latin_terms_break_without_moving_closing_punctuation(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>在“origin”和“local”模式；“local”。</fo:block>
          <fo:block white-space-treatment="preserve">“origin”和“local”</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)[0] if False else module.prepare(path)
            blocks = [n for n in ET.parse(path).iter() if n.tag.endswith('}block')]
            self.assertIn('“origin”\u200b和“local”\u200b模式', blocks[0].text)
            self.assertIn('“local”。', blocks[0].text)
            self.assertEqual(blocks[1].text, '“origin”和“local”')

    def test_unsized_diagrams_fit_the_containing_block(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:layout-master-set><fo:simple-page-master master-name="body-first"
              page-height="11in" margin-top="0.5in" margin-bottom="0.5in">
            <fo:region-body margin-top="0.5in" margin-bottom="0.5in"/>
          </fo:simple-page-master></fo:layout-master-set>
          <fo:block><fo:external-graphic src="url(catalogs.gif)" width="auto"
            content-width="auto" height="auto" content-height="auto"/></fo:block>
          <fo:block><fo:external-graphic src="url(icon.png)" width="12pt"
            content-width="12pt"/></fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path)[0] if False else module.prepare(path)
            images = [n for n in ET.parse(path).iter() if n.tag.endswith('}external-graphic')]
            self.assertEqual(images[0].get('width'), '100%')
            self.assertEqual(images[0].get('content-width'), 'scale-down-to-fit')
            self.assertEqual(images[0].get('scaling'), 'uniform')
            self.assertEqual(images[0].get('max-height'), '600.000pt')
            self.assertEqual(images[0].get('src'), 'url(catalogs.gif)')
            self.assertEqual(images[1].get('width'), '12pt')
            self.assertEqual(images[1].get('content-width'), '12pt')
            self.assertIsNone(images[1].get('max-height'))

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
            added, removed, _kept, _tk = module.prepare(path)[0] if False else module.prepare(path)
            self.assertGreater(added, 0)
            self.assertGreater(removed, 0)
            before, after = ET.fromstring(source), ET.parse(path).getroot()
            # (attribute sets may grow: keeps/spacing stamps are layout-only)
            self.assertEqual([n.tag for n in before.iter()],
                             [n.tag for n in after.iter()])
            # Spurious wrap spaces around 、/， are gone, the legal gap before
            # the preserve block stays, and code text is untouched.
            block = next(n for n in after.iter() if n.get('id') == 'pg_stat_activity')
            self.assertEqual(
                ''.join(block.itertext()).replace('\u200b', ''),
                "函数 array_agg、pg_stat_activity，http://example"
                "InvalidBackendId（-1）。arg6\n            "
                "SELECT 'a、b_c.d';、正文\n          ")
            self.assertIn('http:/\u200b/example', ''.join(after.itertext()))
            self.assertIn('InvalidBackendId（-1）。\u200barg6', ''.join(after.itertext()))
            # 行首禁则：）。 之间不得留下断行机会
            self.assertNotIn('）\u200b。', ''.join(after.itertext()))
            code = next(n for n in after.iter() if n.get('white-space-treatment') == 'preserve')
            self.assertEqual(code.text, "SELECT 'a、b_c.d';")
            stable = ET.fromstring(ET.tostring(after))
            module.prepare(path)[0] if False else module.prepare(path)
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
            added, removed, _kept, _tk = module.prepare(path)[0] if False else module.prepare(path)
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
            module.prepare(path)[0] if False else module.prepare(path)
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
            module.prepare(path)[0] if False else module.prepare(path)
            joined = ''.join(ET.parse(path).getroot().itertext())
            for bad in ('）\u200b。', '）\u200b）', '：\u200b。'):
                self.assertNotIn(bad, joined)
            self.assertIn('）。\u200b', joined)
            stable = joined
            module.prepare(path)[0] if False else module.prepare(path)
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
                             ['Test CJK,Mono', 'Mono,Test CJK', 'Symbol,ZapfDingbats'])

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


    def test_identifiers_and_numbers_never_get_break_sentinels(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>先用<fo:inline font-family="Courier New,CJK">pg_dump</fo:inline>备份，详见第 32.15 节，版本 2.0.2 与 ssl_ca_file 以及路径 postgresql.auto.conf。</fo:block>
          <fo:block>下载 https://ftp.postgresql.org/pub/source/v18/ 之后再继续。异步 I/O 与备份/恢复也受影响。</fo:block>
          <fo:table-cell><fo:block>详见第 32.15 节的 pg_dump 说明</fo:block></fo:table-cell>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            added, _removed, _kept, _tk = module.prepare(path)[0] if False else module.prepare(path)
            self.assertGreater(added, 0)
            root = ET.parse(path).getroot()
            blocks = [n for n in root.iter() if n.tag.endswith('}block')]
            prose = ''.join(blocks[0].itertext())
            # Underscores, dots inside identifiers/numbers/versions stay atomic.
            for token in ('pg_dump', '32.15', '2.0.2', 'ssl_ca_file',
                          'postgresql.auto.conf'):
                self.assertIn(token, prose.replace('\u200b', ''))
                for i in range(1, len(token)):
                    self.assertNotIn(token[:i] + '\u200b' + token[i:], prose,
                                     f'sentinel inside {token!r}')
            # URL path slashes between alphanumerics remain breakable.
            self.assertIn('org/\u200bpub/\u200bsource/\u200bv18/',
                          ''.join(blocks[1].itertext()))
            # Short compounds such as I/O never break at the slash.
            joined_all = ''.join(ET.parse(path).getroot().itertext())
            self.assertNotIn('I/\u200bO', joined_all)
            self.assertNotIn('份/\u200b恢', joined_all)
            # Narrow table cells keep the permissive break class: FOP would
            # overflow an atomic identifier instead of wrapping it.
            self.assertRegex(''.join(blocks[2].itertext()),
                             r'32\.\u200b15 节的 pg_\u200bdump')

    def test_short_inline_code_keeps_together_but_long_runs_do_not(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:block>见<fo:inline font-family="Courier New,CJK">pg_dump</fo:inline>与
            <fo:inline font-family="Courier New,CJK">VACUUM (FULL, FREEZE, VERBOSE) ANALYZE</fo:inline>说明</fo:block>
          <fo:table-cell><fo:block><fo:inline font-family="Courier New,CJK">sha256crypt, sha512crypt</fo:inline></fo:block></fo:table-cell>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            _added, _removed, kept, _tk = module.prepare(path)[0] if False else module.prepare(path)
            inlines = [n for n in ET.parse(path).iter() if n.tag.endswith('}inline')]
            keeps = [n.get('keep-together.within-line') for n in inlines]
            self.assertEqual(keeps.count('always'), 1)
            self.assertEqual(kept, 1)
            # Narrow table cells must not get atomic keeps (FOP would overflow
            # the column instead of wrapping).
            self.assertIsNone(inlines[2].get('keep-together.within-line'))
            joined = ''.join(ET.parse(path).getroot().itertext()).replace('\u200b', '')
            self.assertIn('pg_dump', joined)
            self.assertIn('VACUUM (FULL, FREEZE, VERBOSE) ANALYZE', joined)

    def test_wide_programlisting_scales_to_body_width(self):
        source = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:layout-master-set><fo:simple-page-master master-name="body"
              page-width="6in" margin="1in">
            <fo:region-body/>
          </fo:simple-page-master></fo:layout-master-set>
          <fo:block font-family="Courier New,CJK" white-space-treatment="preserve">''' + '-' * 74 + '''
    155173    accounts</fo:block>
          <fo:block font-family="Courier New,CJK" white-space-treatment="preserve">short line</fo:block>
        </fo:root>'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.fo'
            path.write_text(source)
            module.prepare(path, 'CJK', 'Courier New')
            blocks = [n for n in ET.parse(path).iter()
                      if n.get('white-space-treatment') == 'preserve']
            # 288pt column / (74 × 0.62) ≈ 6.3pt -> clamped to the 7.3pt floor.
            self.assertEqual(blocks[0].get('font-size'), '7.3pt')
            self.assertIsNone(blocks[1].get('font-size'))


if __name__ == '__main__':
    unittest.main()
