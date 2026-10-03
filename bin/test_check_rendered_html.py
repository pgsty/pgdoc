import tempfile
from pathlib import Path
import unittest
from check_rendered_html import check


class RenderedHTMLTests(unittest.TestCase):
    def test_inline_tags_do_not_hide_missing_spaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'index.html'
            p.write_text('<html><body><p>使用<a><em>PostgreSQL</em></a>数据库；参数<code>xmlbinary</code>的设置。</p><pre>中A</pre></body></html>')
            result = check(tmp)
            self.assertEqual(result['stats']['spacing_candidate'], 4)
            self.assertEqual(result['stats']['errors'], 0)

    def test_entities_links_and_code_preservation_are_independent_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); before = root / 'before'; after = root / 'after'
            before.mkdir(); after.mkdir()
            source = '<html><body><p id="ok">字符 &gt; 和 &amp;。</p><pre>SELECT  1;</pre><a href="#ok">跳转</a></body></html>'
            (before / 'index.html').write_text(source)
            (after / 'index.html').write_text(source)
            self.assertEqual(check(after, before)['stats']['errors'], 0)
            (after / 'index.html').write_text(source.replace('SELECT  1;', 'SELECT 2;').replace('#ok', '#missing'))
            result = check(after, before)
            self.assertEqual(result['stats']['protected_content_changed'], 1)
            self.assertEqual(result['stats']['missing_fragment'], 1)
            self.assertEqual(result['stats']['markup_changed'], 1)
            (after / 'index.html').write_text(source.replace('&gt;', '&gt；'))
            self.assertEqual(check(after)['stats']['xml_error'], 1)
