"""Legacy markup must produce references and bibliography, not copied figures."""
import contextlib
import io
import unittest
import tempfile
from pathlib import Path

from normalize_cals_tables import normalize_legacy_markup


class LegacyMarkupTests(unittest.TestCase):
    def test_extensionless_image_resolves_only_an_unambiguous_existing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'connections.gif').write_bytes(b'gif fixture')
            source = '<imagedata align="center" fileref="connections"/>'
            result = normalize_legacy_markup(source, root)
            self.assertEqual(result, source.replace('connections"', 'connections.gif"'))
            self.assertEqual(normalize_legacy_markup(result, root), result)
            (root/'connections.png').write_bytes(b'png fixture')
            self.assertEqual(normalize_legacy_markup(source, root), source)
            remote = '<imagedata fileref="https://example.org/connections"/>'
            self.assertEqual(normalize_legacy_markup(remote, root), remote)

    def test_figure_reference_keeps_destination_without_copying_contents(self):
        source = ('<figure id="diagram"><title id="caption">图示</title>'
                  '<graphic fileref="catalogs.gif"/></figure>'
                  '<xref endterm="diagram" linkend="diagram"/>'
                  '<xref linkend="diagram" endterm="caption"/>'
                  '<xref linkend="elsewhere" endterm="diagram"/>')
        with contextlib.redirect_stderr(io.StringIO()):
            result = normalize_legacy_markup(source)
        self.assertEqual(result, source.replace(
            '<xref endterm="diagram" linkend="diagram"/>',
            '<xref linkend="diagram"/>'))
        self.assertEqual(normalize_legacy_markup(result), result)

    def test_old_bibliography_preserves_metadata(self):
        source = ('<bookbiblio id="ref"><title>Original</title>'
                  '<authorgroup><author>A</author></authorgroup></bookbiblio>')
        with contextlib.redirect_stderr(io.StringIO()):
            result = normalize_legacy_markup(source)
        self.assertEqual(result, source.replace('bookbiblio', 'biblioentry'))


if __name__ == '__main__':
    unittest.main()
