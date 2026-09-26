#!/usr/bin/env python3
"""Regression tests for bin/fix_cjk_spacing.py (source-level CJK despace)."""

import importlib.util
import sys
import unittest
from pathlib import Path


def _load(name):
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).resolve().parent / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fix = _load('fix_cjk_spacing')


def apply(s):
    new, deletions, anomalies, stats = fix.fix_text(s)
    assert not anomalies, f'unexpected anomalies: {anomalies}'
    return new


class SourceDespaceTests(unittest.TestCase):

    def test_basic_wrap_join_after_punctuation(self):
        src = '<para>\n    本章解释如何控制 PostgreSQL 的可靠性，\n    并介绍预写式日志的相关细节。\n</para>\n'
        out = apply(src)
        self.assertEqual(out, '<para>\n    本章解释如何控制 PostgreSQL 的可靠性，并介绍预写式日志的相关细节。\n</para>\n')

    def test_han_han_wrap_without_punctuation(self):
        src = '<para>多态结\n果类型</para>\n'
        self.assertEqual(apply(src), '<para>多态结果类型</para>\n')

    def test_literal_space_between_han(self):
        src = '<para>事务。 第二次执行</para>\n'
        self.assertEqual(apply(src), '<para>事务。第二次执行</para>\n')

    def test_pangu_han_latin_boundaries_kept(self):
        src = '<para>\n    使用 <productname>PostgreSQL</productname> 数据库。\n</para>\n'
        self.assertEqual(apply(src), src)

    def test_em_dash_and_ellipsis_kept(self):
        src = '<para>模块 — 描述</para>\n<para>继续… 内容</para>\n'
        self.assertEqual(apply(src), src)

    def test_entity_edges_kept(self):
        src = '<para>模块 &mdash; 描述</para>\n'
        self.assertEqual(apply(src), src)

    def test_quote_next_to_latin_kept(self):
        src = "<para>word “term” word</para>\n"
        self.assertEqual(apply(src), src)

    def test_quote_next_to_han_dropped(self):
        src = '<para>称为“发布者”。 后续</para>\n'
        self.assertEqual(apply(src), '<para>称为“发布者”。后续</para>\n')

    def test_inline_element_crossing(self):
        src = ('<para>定义发布的节点称为\n'
               '    <firstterm>发布者</firstterm>。发布是一组变更。</para>\n')
        out = apply(src)
        self.assertEqual(out, '<para>定义发布的节点称为<firstterm>发布者</firstterm>。发布是一组变更。</para>\n')

    def test_ws_only_run_between_inline_elements(self):
        src = '<para><firstterm>发布</firstterm>\n   <firstterm>订阅</firstterm>。</para>\n'
        self.assertEqual(apply(src), '<para><firstterm>发布</firstterm><firstterm>订阅</firstterm>。</para>\n')

    def test_run_after_inline_close_uses_its_last_char(self):
        src = '<para>类型<replaceable>名</replaceable>\n   说明</para>\n'
        self.assertEqual(apply(src), '<para>类型<replaceable>名</replaceable>说明</para>\n')
        # Latin replaceable keeps the space (pangu).
        src = '<para>类型<replaceable>name</replaceable>\n   说明</para>\n'
        self.assertEqual(apply(src), src)

    def test_xref_renders_han_gentext(self):
        src = '<para>参见 <xref linkend="wal"/>。</para>\n'
        # Left of the run is 见 (han), xref renders han -> space dropped.
        self.assertEqual(apply(src), '<para>参见<xref linkend="wal"/>。</para>\n')
        src = '<para>see <xref linkend="wal"/> for details.</para>\n'
        # Latin next to gentext keeps its space.
        self.assertEqual(apply(src), src)

    def test_verbatim_blocks_untouched(self):
        src = ('<para>说明。</para>\n<programlisting>\n字 符\n</programlisting>\n'
               '<screen>字 。 字</screen>\n<synopsis>字 符</synopsis>\n')
        self.assertEqual(apply(src), src)

    def test_literal_inline_atomic(self):
        src = '<para>字 <literal>foo</literal> 字</para>\n'
        self.assertEqual(apply(src), src)
        src = '<para>字。 <literal>foo</literal></para>\n'
        # STRICT '。' drops the space even next to latin literal.
        self.assertEqual(apply(src), '<para>字。<literal>foo</literal></para>\n')
        src = '<para>字 <literal>字</literal> 字</para>\n'
        # literal content is han on both edges -> both spaces go.
        self.assertEqual(apply(src), '<para>字<literal>字</literal>字</para>\n')

    def test_block_boundaries_stop_resolution(self):
        src = '<para>\n    句首。\n</para>\n<para>\n    下一段。</para>\n'
        self.assertEqual(apply(src), src)

    def test_comment_transparent(self):
        src = '<para>字。<!-- 注释 -->\n字</para>\n'
        self.assertEqual(apply(src), '<para>字。<!-- 注释 -->字</para>\n')

    def test_indexterm_transparent(self):
        # Inline neighbours look through the indexterm; boundary whitespace
        # (across the element edges) is dropped, and inner han-han spaces
        # are cleaned too (renders into the index).
        src = '<para>字。<indexterm><primary>事 务</primary></indexterm>\n字</para>\n'
        self.assertEqual(apply(src), '<para>字。<indexterm><primary>事务</primary></indexterm>字</para>\n')

    def test_index_term_edge_whitespace_stripped(self):
        src = '<indexterm>\n  <primary>\n   <varname>pg_trgm.sim</varname> 配置参数\n  </primary>\n</indexterm>\n'
        self.assertEqual(apply(src),
                         '<indexterm>\n  <primary><varname>pg_trgm.sim</varname> 配置参数</primary>\n</indexterm>\n')

    def test_indexterm_inner_text_cleaned(self):
        # indexterm renders into the back-of-book index: its own wrapped
        # text must be cleaned even though inline neighbours look through.
        src = '<para>字。<indexterm><primary>配置参数\n      ，归档</primary></indexterm>字</para>\n'
        self.assertEqual(apply(src), '<para>字。<indexterm><primary>配置参数，归档</primary></indexterm>字</para>\n')

    def test_table_cell_internal_wrap(self):
        src = '<entry>主机名。\n      说明字</entry>\n'
        self.assertEqual(apply(src), '<entry>主机名。说明字</entry>\n')

    def test_sgml_shorttag(self):
        src = '<para>字。\n<literal>中</>\n字</para>\n'
        self.assertEqual(apply(src), '<para>字。<literal>中</>字</para>\n')

    def test_sgml_uppercase_tags(self):
        src = '<Para>字。\n  字</Para>\n'
        self.assertEqual(apply(src), '<Para>字。字</Para>\n')

    def test_marked_section_content_processed(self):
        src = '<![%standalone-include;[\n<para>字。\n  字</para>\n]]>\n'
        self.assertEqual(apply(src), '<![%standalone-include;[\n<para>字。字</para>\n]]>\n')

    def test_doctype_with_internal_subset_untouched(self):
        src = '<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook V4.2//EN" [\n<!ENTITY c "成本">\n]>\n<book>字。 字</book>\n'
        out = apply(src)
        self.assertIn('<!ENTITY c "成本">', out)
        self.assertIn('<book>字。字</book>', out)

    def test_attributes_untouched(self):
        src = '<xref linkend="字 符" endterm="a。 b">\n<para>字。 字</para>\n'
        out = apply(src)
        self.assertIn('linkend="字 符"', out)
        self.assertIn('endterm="a。 b"', out)
        self.assertIn('<para>字。字</para>', out)

    def test_only_whitespace_removed_invariant(self):
        src = ('<para>多态结\n果类型。</para>\n<programlisting>字 符\n</programlisting>\n'
               '<para>混排 <literal>foo</literal> 文本。</para>\n')
        _, deletions, _, _ = fix.fix_text(src)
        new = apply(src)
        self.assertEqual(''.join(c for c in src if not c.isspace()),
                         ''.join(c for c in new if not c.isspace()))

    def test_idempotent(self):
        src = ('<para>多态结\n果类型。</para>\n<para>称为\n<firstterm>发布者</firstterm>。\n</para>\n')
        once = apply(src)
        self.assertEqual(apply(once), once)

    def test_nested_inline_wraps(self):
        src = '<para>使用 <command>initdb</command> 初始化。\n  之后运行。</para>\n'
        self.assertEqual(apply(src), '<para>使用 <command>initdb</command> 初始化。之后运行。</para>\n')

    def test_inline_child_leading_ws_against_parent(self):
        # Whitespace just inside an inline child's open tag renders between
        # the parent's preceding char and the child's first char.
        src = '<para>文档由<ulink url="x">\n   官方站点</ulink>提供了信息。</para>\n'
        self.assertEqual(apply(src),
                         '<para>文档由<ulink url="x">官方站点</ulink>提供了信息。</para>\n')

    def test_marked_section_boundary_wrap(self):
        src = ('<para>测试会失败。<![%flattext-install-include[文件包含]]>'
               '<![%flattext-install-ignore[<xref linkend="r">包含]]>\n    关于解释测试结果。</para>\n')
        self.assertEqual(apply(src),
                         '<para>测试会失败。<![%flattext-install-include[文件包含]]>'
                         '<![%flattext-install-ignore[<xref linkend="r">包含]]>关于解释测试结果。</para>\n')

    def test_footnote_is_block_boundary(self):
        src = '<para>句。<footnote><para>注。</para></footnote>\n后句</para>\n'
        # Footnote renders out-of-line; space after it is legitimate.
        self.assertEqual(apply(src), src)


if __name__ == '__main__':
    unittest.main()
