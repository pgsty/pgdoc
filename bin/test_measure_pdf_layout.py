from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

from measure_pdf_layout import probe, apply, FO, KEEP


class MeasuredLayoutTests(unittest.TestCase):
    def calibrate(self, source_text, area_text):
        folder = tempfile.TemporaryDirectory();self.addCleanup(folder.cleanup)
        root=Path(folder.name);source=root/'source.fo';measured=root/'probe.fo';manifest=root/'map.json';areas=root/'areas.xml';report=root/'report.json'
        source.write_text(source_text);areas.write_text(area_text)
        probe(source,measured,manifest);apply(source,areas,manifest,report)
        second=root/'second.fo';probe(source,second,root/'second.json')
        self.assertEqual(measured.read_bytes(),second.read_bytes())
        self.assertEqual(''.join(ET.fromstring(source_text).itertext()),''.join(ET.parse(source).getroot().itertext()))
        return ET.parse(source).getroot()

    def test_nested_introduction_counts_across_probe_pages(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="para" orphans="2" widows="2">下标语法示例：<fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block>说明。</fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="para" bpd="40000"><lineArea bpd="40000"/></block></pageViewport><pageViewport simple-page-master-name="body-odd"><regionBody bpd="648000"/><block prod-id="para" bpd="550000"><block prod-id="code" bpd="540000"/><lineArea bpd="10000"/></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);code=next(n for n in tree.iter() if n.get('id')=='code')
        self.assertEqual(code.get(KEEP),'auto')  # 540pt fits alone, 580pt with its introduction does not.
        self.assertEqual(code.get('keep-with-previous.within-column'),'always')

    def test_standalone_introduction_crosses_empty_anchor(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" orphans="2" widows="2">例如：</fo:block><fo:block id="anchor" keep-with-next.within-column="always"><!-- Invisible comment --><?test invisible?></fo:block><fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="24000"/><block prod-id="code" bpd="80000"/></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);anchor=next(n for n in tree.iter() if n.get('id')=='anchor');code=next(n for n in tree.iter() if n.get('id')=='code')
        self.assertEqual(anchor.get('keep-with-previous.within-column'),'always')
        self.assertEqual(code.get(KEEP),'always')

    def test_break_controls_do_not_hide_standalone_introduction_or_empty_anchor(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" space-after.optimum="1em">例如：\u200b</fo:block><fo:block id="anchor">\u200b</fo:block><fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="24000"/><block prod-id="code" bpd="80000"/></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);nodes={n.get('id'):n for n in tree.iter() if n.get('id')}
        self.assertEqual(nodes['anchor'].get('keep-with-previous.within-column'),'always')
        self.assertEqual(nodes['intro'].text,'例如：\u200b')
        self.assertEqual(nodes['anchor'].text,'\u200b')

    def test_legacy_paragraphs_without_explicit_widows_keep_their_introductions(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" space-after.optimum="1em"><fo:inline>示例</fo:inline>如下：\u200b<fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block>规则如下：\u200b</fo:block><fo:block id="group" space-after.optimum="1em"><fo:block id="term" keep-with-next.within-column="always">第一条</fo:block><fo:block><fo:block id="first" space-after.optimum="1em">完整说明。</fo:block></fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="140000"><lineArea bpd="20000"/><block prod-id="code" bpd="100000"/><lineArea bpd="20000"/></block><block prod-id="group" bpd="600000"><block prod-id="term" bpd="24000"/><block><block prod-id="first" bpd="576000"/></block></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);nodes={n.get('id'):n for n in tree.iter() if n.get('id')}
        self.assertEqual(nodes['code'].get('keep-with-previous.within-column'),'always')
        self.assertEqual(nodes['code'].get(KEEP),'always')
        self.assertEqual(nodes['intro'].get(KEEP),'auto')
        self.assertEqual(nodes['group'].get('keep-with-previous.within-column'),'always')
        self.assertIsNone(nodes['group'].get(KEEP))  # A wrapper is not a prose paragraph.

    def test_compact_function_paragraph_counts_caption_toward_example_height(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="para" margin-left="4em" text-align="left">例如，要为统计对象 <fo:inline>myschema.mystatsobj</fo:inline> 设置一些值：<fo:block id="code" white-space-treatment="preserve">SELECT pg_restore_extended_stats(...);</fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="para" bpd="580000"><lineArea bpd="40000"/><block prod-id="code" bpd="540000"/></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);code=next(n for n in tree.iter() if n.get('id')=='code')
        self.assertEqual(code.get(KEEP),'auto')
        self.assertEqual(code.get('keep-with-previous.within-column'),'always')

    def test_introduction_height_includes_native_line_leading(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="para" orphans="2" widows="2">示例：<fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="para" bpd="580000"><lineArea bpd="20000" bpda="40000"/><block prod-id="code" bpd="540000"/></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);code=next(n for n in tree.iter() if n.get('id')=='code')
        self.assertEqual(code.get(KEEP),'auto')  # The line's 40pt advance, not its 20pt glyph box, must be included.

    def test_mixed_paragraph_uses_only_its_trailing_introduction(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" orphans="2" widows="2">先前示例。<fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block>规则如下：</fo:block><fo:block id="next" orphans="2" widows="2">第一条规则。</fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="640000"><lineArea bpd="20000"/><block prod-id="code" bpd="600000"/><lineArea bpd="20000"/></block><block prod-id="next" bpd="540000"/></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);following=next(n for n in tree.iter() if n.get('id')=='next')
        self.assertEqual(following.get(KEEP),'always')  # Its 540pt plus the final 20pt, not the complete 640pt paragraph.
        self.assertEqual(following.get('keep-with-previous.within-column'),'always')

    def test_previous_uncaptioned_code_is_not_counted_as_introduction(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="para" orphans="2" widows="2">前文。<fo:block id="earlier" white-space-treatment="preserve">SELECT 0;</fo:block>另一个示例：<fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="para" bpd="1080000"><lineArea bpd="20000"/><block prod-id="earlier" bpd="500000"/><lineArea bpd="20000"/><block prod-id="code" bpd="540000"/></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);code=next(n for n in tree.iter() if n.get('id')=='code')
        self.assertEqual(code.get(KEEP),'always')

    def test_definition_group_keeps_introduction_without_forcing_oversized_group(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" orphans="2" widows="2">可用权限如下：</fo:block><fo:block id="group" keep-together.within-column="always"><fo:block id="term" keep-with-next.within-column="always">SELECT</fo:block><fo:block><fo:block id="first" orphans="2" widows="2">完整说明。</fo:block></fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="30000"/><block prod-id="group" bpd="600000"><block prod-id="term" bpd="24000"/><block><block prod-id="first" bpd="576000"/></block></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);group=next(n for n in tree.iter() if n.get('id')=='group')
        self.assertEqual(group.get(KEEP),'auto')
        self.assertEqual(group.get('keep-with-previous.within-column'),'always')

    def test_mixed_intro_and_first_definition_do_not_form_an_oversized_keep_chain(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" orphans="2" widows="2">前文。<fo:block id="earlier" white-space-treatment="preserve">SELECT 0;</fo:block>可用命令如下：</fo:block><fo:block id="group"><fo:block id="term" keep-with-next.within-column="always">命令</fo:block><fo:block><fo:block id="first" orphans="2" widows="2">说明。<fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block></fo:block></fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="250000"><lineArea bpd="30000"/><block prod-id="earlier" bpd="200000"/><lineArea bpd="20000"/></block><block prod-id="group" bpd="420000"><block prod-id="term" bpd="20000"/><block><block prod-id="first" bpd="400000"><lineArea bpd="24000"/><block prod-id="code" bpd="376000"/></block></block></block></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);nodes={n.get('id'):n for n in tree.iter() if n.get('id')}
        self.assertEqual(nodes['intro'].get(KEEP),'auto')  # 250+20+400pt cannot be retained as one chain.
        self.assertEqual(nodes['first'].get(KEEP),'always')
        self.assertEqual(nodes['code'].get(KEEP),'always')
        self.assertEqual(nodes['group'].get('keep-with-previous.within-column'),'always')

    def test_table_introduction_and_header_count_toward_first_row(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" orphans="2" widows="2">输出如下：</fo:block><fo:table id="table"><fo:table-header><fo:table-row><fo:table-cell id="header"><fo:block>列</fo:block></fo:table-cell></fo:table-row></fo:table-header><fo:table-body><fo:table-row id="row"><fo:table-cell id="cell"><fo:block>内容</fo:block></fo:table-cell></fo:table-row></fo:table-body></fo:table></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="40000"/><block prod-id="header" bpd="20000"/><block prod-id="cell" bpd="530000"/></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);row=next(n for n in tree.iter() if n.get('id')=='row');table=next(n for n in tree.iter() if n.get('id')=='table')
        self.assertEqual(row.get(KEEP),'auto')
        self.assertEqual(table.get('keep-with-previous.within-column'),'always')

    def test_list_label_and_introduction_count_toward_first_item(self):
        source='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="intro" orphans="2" widows="2">规则如下：</fo:block><fo:list-block id="list"><fo:list-item id="item"><fo:list-item-label id="label"><fo:block>1.</fo:block></fo:list-item-label><fo:list-item-body id="body"><fo:block>第一项。</fo:block></fo:list-item-body></fo:list-item></fo:list-block></fo:flow></fo:page-sequence></fo:root>'''
        areas='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="intro" bpd="30000"/><block prod-id="label" bpd="550000"/><block prod-id="body" bpd="10000"/></pageViewport></areaTree>'''
        tree=self.calibrate(source,areas);item=next(n for n in tree.iter() if n.get('id')=='item');listing=next(n for n in tree.iter() if n.get('id')=='list')
        self.assertEqual(item.get(KEEP),'auto')
        self.assertEqual(listing.get('keep-with-previous.within-column'),'always')

    def test_last_list_item_uses_body_measurement_without_wrapping_list_structure(self):
        source_text='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:list-block><fo:list-item><fo:list-item-label><fo:block>1.</fo:block></fo:list-item-label><fo:list-item-body><fo:block>前项</fo:block></fo:list-item-body></fo:list-item><fo:list-item><fo:list-item-label><fo:block>2.</fo:block></fo:list-item-label><fo:list-item-body id="last"><fo:block>末项</fo:block></fo:list-item-body></fo:list-item></fo:list-block></fo:flow></fo:page-sequence></fo:root>'''
        area_text='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="last" bpd="24000"/></pageViewport></areaTree>'''
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source.fo';measured=root/'probe.fo';manifest=root/'map.json';at=root/'areas.xml';report=root/'report.json'
            source.write_text(source_text);at.write_text(area_text)
            probe(source,measured,manifest);apply(source,at,manifest,report)
            items=list(ET.parse(source).iter(FO+'list-item'))
            self.assertIsNone(items[0].get(KEEP))
            self.assertEqual(items[1].get(KEEP),'always')
            self.assertEqual(items[1].get('keep-with-previous.within-column'),'always')
            second=root/'second.fo';probe(source,second,root/'second.json')
            self.assertEqual(measured.read_bytes(),second.read_bytes())

    def test_synopsis_heading_counts_toward_code_keep_decision(self):
        source_text='''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block role="pgdoc-reference-synopsis" id="synopsis"><fo:block>大纲</fo:block><fo:block id="code" white-space-treatment="preserve">CREATE AGGREGATE ...</fo:block></fo:block></fo:flow></fo:page-sequence></fo:root>'''
        area_text='''<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/><block prod-id="synopsis" bpd="600000"><block prod-id="code" bpd="540000"/></block></pageViewport></areaTree>'''
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source.fo';measured=root/'probe.fo';manifest=root/'map.json';at=root/'areas.xml';report=root/'report.json'
            source.write_text(source_text);at.write_text(area_text)
            probe(source,measured,manifest);apply(source,at,manifest,report)
            code=next(n for n in ET.parse(source).iter() if n.get('id')=='code')
            self.assertEqual(code.get(KEEP),'auto')
            self.assertEqual(code.text,'CREATE AGGREGATE ...')
            second=root/'second.fo';probe(source,second,root/'second.json')
            self.assertEqual(measured.read_bytes(),second.read_bytes())

    def test_native_heights_protect_short_units_and_allow_oversized_rows(self):
        original = '''<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format">
          <fo:page-sequence><fo:static-content flow-name="xsl-region-before"><fo:table><fo:table-body><fo:table-row><fo:table-cell id="header"><fo:block>header</fo:block></fo:table-cell></fo:table-row></fo:table-body></fo:table></fo:static-content>
          <fo:flow flow-name="xsl-region-body"><fo:block id="code" white-space-treatment="preserve">SELECT 1;\nSELECT 2;</fo:block>
          <fo:block id="para" orphans="2" widows="2">短段落。</fo:block>
          <fo:block id="ending" role="pgdoc-compact-ending">另见：SELECT。</fo:block>
          <fo:block id="foot" role="pgdoc-table-footnote">完整脚注。</fo:block>
          <fo:table><fo:table-body>
            <fo:table-row><fo:table-cell id="short"><fo:block>short</fo:block></fo:table-cell></fo:table-row>
            <fo:table-row><fo:table-cell id="tall"><fo:block>very long</fo:block></fo:table-cell></fo:table-row>
          </fo:table-body></fo:table>
        </fo:flow></fo:page-sequence></fo:root>'''
        areas = '''<areaTree><pageSequence>
          <pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/>
            <block prod-id="code" bpd="24000"/><block prod-id="para" bpd="24000"/><block prod-id="ending" bpd="48000"/><block prod-id="foot" bpd="12000"/>
            <block prod-id="short" bpd="70000"/><block prod-id="tall" bpd="600000"/>
          </pageViewport>
          <pageViewport simple-page-master-name="body-odd"><regionBody bpd="648000"/>
            <block prod-id="tall" bpd="200000"/>
          </pageViewport>
        </pageSequence></areaTree>'''
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp);source=root/'source.fo';measured=root/'probe.fo';manifest=root/'map.json';at=root/'areas.xml';report=root/'report.json'
            source.write_text(original);at.write_text(areas)
            probe(source,measured,manifest)
            self.assertEqual(source.read_text(),original)
            result=apply(source,at,manifest,report)
            before=ET.fromstring(original);after=ET.parse(source).getroot()
            self.assertEqual(''.join(before.itertext()),''.join(after.itertext()))
            self.assertEqual([n.get('id') for n in before.iter()],[n.get('id') for n in after.iter()])
            body=after.find('.//'+FO+'flow')
            self.assertEqual(body.find(FO+'block').get(KEEP),'always')
            self.assertIsNone(after.find('.//'+FO+'static-content').find('.//'+FO+'table-row').get(KEEP))
            rows=list(body.iter(FO+'table-row'))
            self.assertEqual([n.get(KEEP) for n in rows],['always','auto'])
            self.assertIsNone(next(n for n in body if n.get('id')=='para').get(KEEP))
            ending=next(n for n in body if n.get('id')=='ending')
            self.assertEqual(ending.get('keep-with-previous.within-column'),'always')
            self.assertEqual(next(n for n in body if n.get('id')=='foot').get(KEEP),'always')
            self.assertEqual(result['intact_unit_limit_pt'],568)
            second=root/'second.fo';second_map=root/'second.json'
            probe(source,second,second_map)
            self.assertEqual(measured.read_bytes(),second.read_bytes())

    def test_stale_or_missing_measurements_fail_instead_of_appearing_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'source.fo';measured=root/'probe.fo';manifest=root/'map.json';at=root/'areas.xml';report=root/'report.json'
            original='<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format"><fo:page-sequence><fo:flow flow-name="xsl-region-body"><fo:block id="code" white-space-treatment="preserve">SELECT 1;</fo:block></fo:flow></fo:page-sequence></fo:root>'
            source.write_text(original);probe(source,measured,manifest)
            at.write_text('<areaTree><pageViewport simple-page-master-name="body-first"><regionBody bpd="648000"/></pageViewport></areaTree>')
            with self.assertRaisesRegex(ValueError,'required code/cell'):
                apply(source,at,manifest,report)
            source.write_text(original.replace('SELECT 1','SELECT 2'))
            with self.assertRaisesRegex(ValueError,'FO changed'):
                apply(source,at,manifest,report)
