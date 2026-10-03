import unittest

from prepare_chinese_html import normalize_html, normalize_html_prose


class ChineseHTMLSpacingTests(unittest.TestCase):
    @staticmethod
    def prepare(text):
        return normalize_html_prose(normalize_html(text)[0])

    def test_prose_technical_punctuation_is_not_rewritten(self):
        source = '<p>如果使用SSL压缩，则返回"on"，否则返回"off"。</p><p>#: 注释和#, 标志；分钟:秒。</p>'
        expected = source.replace('使用SSL压缩', '使用 SSL 压缩')
        result = self.prepare(source)
        self.assertEqual(result, expected)
        self.assertEqual(self.prepare(result), result)

    def test_complete_pipeline_preserves_entities_attributes_and_verbatim(self):
        source = ('<p title="x > 中A">字符 &lt;、&gt;和 &amp;；&#34;中文&#34;。'
                  '<code>"中 文", x&amp;y</code>继续。</p>'
                  '<svg><text>中A,字</text></svg><math><mi>中A</mi></math>'
                  '<script>if (a < b) { s = "中A,字"; }</script>'
                  '<pre>中A,字\n中 文</pre>')
        result = self.prepare(source)
        self.assertIn('title="x > 中A"', result)
        for entity in ('&lt;', '&gt;', '&amp;', '&#34;'):
            self.assertEqual(source.count(entity), result.count(entity))
        for island in ('<code>"中 文", x&amp;y</code>', '<svg><text>中A,字</text></svg>',
                       '<math><mi>中A</mi></math>', '<pre>中A,字\n中 文</pre>',
                       '<script>if (a < b) { s = "中A,字"; }</script>'):
            self.assertIn(island, result)
        self.assertEqual(self.prepare(result), result)

    def test_real_inline_text_boundaries_are_spaced_without_changing_markup(self):
        source = ('<p>使用<a href="pg.html"><em>PostgreSQL</em></a>数据库；'
                  '异步<acronym>I/O</acronym>适用。参数<code>xmlbinary</code>的设置。</p>'
                  '<p>中&#65;文；见<code>~/.pgpass</code>文件。</p>')
        expected = ('<p>使用 <a href="pg.html"><em>PostgreSQL</em></a> 数据库；'
                    '异步 <acronym>I/O</acronym> 适用。参数 <code>xmlbinary</code> 的设置。</p>'
                    '<p>中 &#65; 文；见 <code>~/.pgpass</code> 文件。</p>')
        result = self.prepare(source)
        self.assertEqual(result, expected)
        self.assertEqual(self.prepare(result), result)

    def test_prose_urls_and_partial_quotes_are_preserved(self):
        source = '<p>网址 https://example.org/中文A?x=中A&amp;y=中A；"中<a>文</a>"。</p>'
        result = self.prepare(source)
        self.assertIn('https://example.org/中文A?x=中A&amp;y=中A', result)
        self.assertIn('"中<a>文</a>"', result)
        self.assertEqual(self.prepare(result), result)

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
