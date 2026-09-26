import unittest

from prepare_chinese_html import normalize_html


class ChineseHTMLSpacingTests(unittest.TestCase):
    def test_generated_index_and_cross_reference_titles(self):
        source = '<dt>类型 (见 <a href="#types">数据类型</a>)</dt><p>见 <a href="config.html"> 规划器代价常量\n </a>，继续。</p>'
        expected = '<dt>类型 (见<a href="#types">数据类型</a>)</dt><p>见<a href="config.html">规划器代价常量</a>，继续。</p>'
        result, deletions = normalize_html(source)
        self.assertEqual(result, expected)
        self.assertTrue(deletions)
        self.assertEqual(normalize_html(result), (result, []))

    def test_code_attributes_and_latin_spaces_are_unchanged(self):
        source = '<p data-note="中 文 > &amp;">使用 <code title="中 文">中 文  x + y</code> 数据库。 <span>继续</span>。</p><pre><code>中 文\n中 。 文</code></pre><p>Latin words <em>stay spaced</em> here.</p>'
        expected = source.replace('使用 <code', '使用<code').replace('数据库。 <span>', '数据库。<span>')
        self.assertEqual(normalize_html(source)[0], expected)

    def test_raw_script_style_and_math_are_protected(self):
        source = '<script>if (a < b) { s = "中 文"; }</script><style>.x:before { content: "中 文 <" }</style><svg><text>中 文 。 文</text></svg><math><mi>中 文</mi></math><p>中 文</p>'
        self.assertEqual(normalize_html(source)[0], source.replace('<p>中 文</p>', '<p>中文</p>'))

    def test_raw_text_detection_respects_comments_and_attributes(self):
        source = '<!-- <script> is documented here --><p title="<script>">中 文</p><script data-note="a > b">x = "中 文 <";</script>'
        self.assertEqual(normalize_html(source)[0], source.replace('>中 文</p>', '>中文</p>'))

    def test_block_and_void_boundaries_stay_separate(self):
        source = '<p>中</p>\n<p>文<br/> 文<img src="a.png"/> 字</p><p>使用 <span>PostgreSQL</span> 数据库。</p>'
        self.assertEqual(normalize_html(source), (source, []))

    def test_comments_and_inline_formatting_are_preserved(self):
        source = '<p>中 <!-- 注 释 --> <strong>文</strong> <span title="属 性">中</span> 文。</p>'
        expected = '<p>中<!-- 注 释 --><strong>文</strong><span title="属 性">中</span>文。</p>'
        self.assertEqual(normalize_html(source)[0], expected)

    def test_malformed_input_fails_instead_of_guessing(self):
        with self.assertRaises(ValueError):
            normalize_html('<p>中 <span>文</p>')

    def test_nested_inline_edges_and_protected_spaces(self):
        source = '<p>）<a href="a"> <span>DocBook</span></a></p><p><a><span>pg_dump</span>\n </a>。</p><p>中<a> <em> <span>文</span> </em> </a>字</p><p>中<a><code> 文 </code></a>。</p>'
        expected = '<p>）<a href="a"><span>DocBook</span></a></p><p><a><span>pg_dump</span></a>。</p><p>中<a><em><span>文</span></em></a>字</p><p>中<a><code> 文 </code></a>。</p>'
        self.assertEqual(normalize_html(source)[0], expected)
        self.assertEqual(normalize_html(expected), (expected, []))


if __name__ == '__main__':
    unittest.main()
