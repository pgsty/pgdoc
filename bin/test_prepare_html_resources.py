import tempfile
import unittest
import hashlib
import json
from pathlib import Path

from prepare_html_resources import BUNDLE, CSS_REFERENCES, OFFICIAL_CSS, adapt_legacy_css, localize_official_styles, prepare_resources
from urllib.parse import urlsplit, unquote


class HTMLResourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.sgml = Path(self.temp.name) / 'doc/src/sgml'
        self.output = self.sgml / 'html'
        self.output.mkdir(parents=True)

    def write(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_copies_real_graphics_and_nested_css_resources(self):
        self.write(self.output / 'index.html', '<link rel="stylesheet" href="stylesheet.css"><img src="clientserver.gif">')
        self.write(self.sgml / 'stylesheet.css', '@import "styles/theme.css";')
        self.write(self.sgml / 'styles/theme.css', 'body { background: url(../paper.png) }')
        self.write(self.sgml / 'paper.png', 'paper image bytes')
        self.write(self.sgml.parent / 'graphics/clientserver.gif', 'legacy image bytes')
        copied, checked, design_links = prepare_resources(self.sgml)
        self.assertEqual(checked, 4)
        self.assertEqual(len(copied), 4)
        self.assertEqual((self.output / 'clientserver.gif').read_text(), 'legacy image bytes')
        self.assertEqual((self.output / 'paper.png').read_text(), 'paper image bytes')
        self.assertEqual(prepare_resources(self.sgml)[:2], ([], 4))

    def test_missing_stylesheet_is_an_error(self):
        self.write(self.output / 'index.html', '<link rel="stylesheet" href="missing.css">')
        with self.assertRaisesRegex(ValueError, 'missing local resource: missing.css'):
            prepare_resources(self.sgml)

    def test_empty_image_source_is_an_error(self):
        for markup in ('<img src="">', '<img alt="a diagram">', '<img src="   ">'):
            with self.subTest(markup=markup):
                self.write(self.output / 'index.html', markup)
                with self.assertRaisesRegex(ValueError, 'image has no nonempty src'):
                    prepare_resources(self.sgml)

    def test_missing_css_image_is_an_error(self):
        self.write(self.output / 'index.html', '<link rel="stylesheet" href="stylesheet.css">')
        self.write(self.sgml / 'stylesheet.css', 'body { background: url(missing.png) }')
        with self.assertRaisesRegex(ValueError, 'missing local resource: missing.png'):
            prepare_resources(self.sgml)

    def test_remote_resources_are_not_downloaded(self):
        self.write(self.output / 'index.html', '<link rel="stylesheet" href="https://example.test/style.css"><img src="//example.test/a.png"><img src="data:image/png;base64,AA==">')
        self.assertEqual(prepare_resources(self.sgml)[:2], ([], 0))

    def test_resource_cannot_escape_output(self):
        self.write(self.output / 'index.html', '<img src="../private.png">')
        with self.assertRaisesRegex(ValueError, 'resource escapes HTML output'):
            prepare_resources(self.sgml)

    def test_official_theme_is_local_and_source_css_is_preserved(self):
        self.write(self.output / 'index.html', '<link rel="stylesheet" href="stylesheet.css">')
        css = '@import url("' + OFFICIAL_CSS + '");\nbody { color: red; }\n'
        self.write(self.sgml / 'stylesheet.css', css)
        report = self.sgml / 'localization.json'
        prepare_resources(self.sgml, localization_report=report)
        changed = self.output / 'stylesheet.css'
        self.assertEqual(changed.read_text(), css.replace(OFFICIAL_CSS, '_static/pgweb/media/css/docs-complete.css'))
        self.assertEqual((self.sgml / 'stylesheet.css').read_text(), css)
        self.assertEqual(json.loads(report.read_text())[0]['before_sha256'], hashlib.sha256(css.encode()).hexdigest())
        self.assertEqual(localize_official_styles(self.output), [])

    def test_only_exact_stylesheet_url_is_rewritten(self):
        text = ('<link href="' + OFFICIAL_CSS + '"><a href="' + OFFICIAL_CSS + '">Source</a>'
                '<script>const u="' + OFFICIAL_CSS + '";</script>')
        self.write(self.output / 'nested/page.html', text)
        report = localize_official_styles(self.output)
        result = (self.output / 'nested/page.html').read_text()
        self.assertEqual(result, text.replace('<link href="' + OFFICIAL_CSS, '<link href="../_static/pgweb/media/css/docs-complete.css', 1))
        self.assertEqual(len(report), 1)

    def test_pinned_theme_has_complete_offline_resource_closure(self):
        manifest = json.loads((BUNDLE / 'manifest.json').read_text())
        for item in manifest['files']:
            source = BUNDLE / item['path']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), item['sha256'])
            if source.suffix != '.css':
                continue
            for match in CSS_REFERENCES.finditer(source.read_text()):
                ref = next(group for group in match.groups() if group is not None)
                parsed = urlsplit(ref)
                if parsed.scheme == 'data':
                    continue
                self.assertFalse(parsed.scheme or parsed.netloc or parsed.path.startswith('/'), ref)
                self.assertTrue((source.parent / unquote(parsed.path)).is_file(), ref)

    def test_legacy_css_only_changes_unmatched_selectors(self):
        css = ('/* BODY.BOOK .TITLE must remain a comment */\n'
               'BODY { background: white; margin: 1em; }\n'
               'BODY.BOOK H1.TITLE { color: #020167; text-align: center; }\n'
               '.PROGRAMLISTING, .SCREEN { margin-left: 4ex; }\n'
               '.KEEP { background: url("paper.png"); }\n')
        self.write(self.output / 'stylesheet.css', css)
        report = adapt_legacy_css(self.output, {('div', 'book'), ('h1', 'title'), ('pre', 'programlisting'), ('pre', 'screen'), ('p', 'KEEP')}, {'book'})
        expected = css.replace('BODY.BOOK H1.TITLE {', 'body > div.book H1.title {').replace('.PROGRAMLISTING, .SCREEN {', '.programlisting, .screen {')
        self.assertEqual((self.output / 'stylesheet.css').read_text(), expected)
        self.assertEqual(len(report[0]['selectors']), 2)
        self.assertEqual(adapt_legacy_css(self.output, {('div', 'book'), ('h1', 'title'), ('pre', 'programlisting'), ('pre', 'screen')}, {'book'}), [])

    def test_lowercase_body_prefix_maps_only_actual_root_container(self):
        self.write(self.output / 'index.html', '<body><div class="book"><h1 class="title">Title</h1></div></body>')
        self.write(self.output / 'stylesheet.css', 'BODY.book H1.title { text-align: center; }\nBODY.set H1.title { color: red; }')
        report = self.sgml / 'style.json'
        prepare_resources(self.sgml, style_report=report)
        self.assertEqual((self.output / 'stylesheet.css').read_text(), 'body > div.book H1.title { text-align: center; }\nBODY.set H1.title { color: red; }')
        self.assertEqual(len(json.loads(report.read_text())), 1)

    def test_existing_matching_body_or_uppercase_class_is_preserved(self):
        css = 'BODY.BOOK H1.TITLE { color: blue; }\n.PROGRAMLISTING { margin-left: 4ex; }'
        self.write(self.output / 'stylesheet.css', css)
        self.assertEqual(adapt_legacy_css(self.output, {('body', 'BOOK'), ('h1', 'TITLE'), ('pre', 'PROGRAMLISTING'), ('pre', 'programlisting')}, {'book'}), [])
        self.assertEqual((self.output / 'stylesheet.css').read_text(), css)

    def test_source_copy_localization_and_selector_edit_each_have_ledger(self):
        self.write(self.output / 'index.html', '<body><link rel="stylesheet" href="stylesheet.css"><div class="book"><h1 class="title">Title</h1></div></body>')
        css = '@import url("' + OFFICIAL_CSS + '");\nBODY.BOOK H1.TITLE { text-align: center; }'
        self.write(self.sgml / 'stylesheet.css', css)
        localization, styles = self.sgml / 'urls.json', self.sgml / 'styles.json'
        prepare_resources(self.sgml, localization_report=localization, style_report=styles)
        url_edit, style_edit = json.loads(localization.read_text()), json.loads(styles.read_text())
        self.assertEqual(len(url_edit), 1)
        self.assertEqual(len(style_edit), 1)
        self.assertEqual(url_edit[0]['after_sha256'], style_edit[0]['before_sha256'])
        self.assertEqual(style_edit[0]['after_sha256'], hashlib.sha256((self.output / 'stylesheet.css').read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
