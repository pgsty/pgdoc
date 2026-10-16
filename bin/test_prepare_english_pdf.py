"""Protect frozen books and verify routing without running whole-book builds."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import prepare_english_pdf as pdf


class EnglishPdfTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.root = Path(self.workspace.name)
        self.output_root = self.root / 'pdf'
        self.version = '18.6'
        self.payload = b'%PDF-1.4 official original'

    def output(self, version, paper='A4'):
        return self.output_root / 'en' / f'postgresql-{version}-en-{paper}.pdf'

    def seed(self, version, content=b'%PDF-1.4 existing book'):
        output = self.output(version)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(content)
        return output

    def source(self, version):
        source_dir = self.root / 'en' / version
        source_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / 'postgres.sgml').write_text('<book/>')
        archive = self.root / 'source.tar.gz'
        archive.write_bytes(b'fixed archive')
        source = {'version': version, 'archive': archive.name,
                  'archive_sha256': pdf.sha256(archive), 'doc_dir': f'en/{version}'}
        (self.root / 'en/SOURCES.json').write_text(json.dumps({'entries': [source]}))
        return source

    def inspect(self, path, paper):
        return {'sha256': pdf.sha256(path), 'bytes': path.stat().st_size,
                'pages': 10, 'pdf_version': self.version}

    def download(self, url, output):
        output.write_bytes(self.payload)
        return {'url': url, 'final_url': url}

    def prepare(self, version, **kwargs):
        return pdf.prepare(version, 'A4', self.output_root, root=self.root, **kwargs)

    def test_official_legacy_and_devel_are_distinct(self):
        self.assertEqual(pdf.policy('7.4'), ('7.4.30', 'legacy-once', '7.4'))
        for version in ('8.0.26', '9.6.24', '18', '18.6', '19beta4', '19rc1'):
            self.assertEqual(pdf.policy(version)[1], 'official')
        self.assertEqual(pdf.policy('20devel'), ('20devel', 'devel', '20'))
        for version in ('6.2', '7.4.29', '9.9', '../18', 'latest'):
            with self.assertRaises(ValueError):
                pdf.policy(version)

    @patch.object(pdf, 'download')
    @patch.object(pdf, 'build')
    def test_existing_legacy_is_frozen_without_touching_bytes(self, build, download):
        self.version = '7.4.30'
        output = self.seed('7.4.30')
        before = (output.read_bytes(), output.stat().st_mtime_ns)
        with patch.object(pdf, 'inspect_pdf', side_effect=self.inspect):
            self.prepare('7.4')
        receipt_path = output.with_suffix('.source.json')
        receipt_before = receipt_path.read_bytes()
        self.prepare('7.4.30', refresh=True)
        self.assertEqual(before, (output.read_bytes(), output.stat().st_mtime_ns))
        self.assertEqual(receipt_before, receipt_path.read_bytes())
        build.assert_not_called()
        download.assert_not_called()

    def test_missing_legacy_builds_once_and_cannot_be_silently_rebuilt(self):
        self.version = '7.4.30'
        self.source(self.version)
        def build(root, source, version, paper, output):
            output.write_bytes(b'%PDF-1.4 first build')
        with patch.object(pdf, 'build', side_effect=build) as builder, \
             patch.object(pdf, 'inspect_pdf', side_effect=self.inspect):
            output = self.prepare(self.version)
            self.prepare(self.version)
            self.assertEqual(builder.call_count, 1)
            output.write_bytes(b'%PDF-1.4 changed')
            with self.assertRaisesRegex(ValueError, 'Frozen PDF missing or changed'):
                self.prepare(self.version, refresh=True)
            output.unlink()
            with self.assertRaisesRegex(ValueError, 'restore the recorded file'):
                self.prepare(self.version)
            self.assertEqual(builder.call_count, 1)

    @patch.object(pdf, 'build')
    def test_official_download_is_exact_and_cache_does_not_build(self, build):
        with patch.object(pdf, 'download', side_effect=self.download) as downloader, \
             patch.object(pdf, 'inspect_pdf', side_effect=self.inspect):
            output = self.prepare('18.6')
            self.prepare('18.6')
        self.assertEqual(output.read_bytes(), self.payload)
        self.assertEqual(downloader.call_count, 1)
        receipt = json.loads(output.with_suffix('.source.json').read_text())
        self.assertEqual(receipt['mode'], 'official')
        self.assertEqual(receipt['sha256'], pdf.sha256(output))
        self.assertIn('/18/postgresql-18-A4.pdf', receipt['url'])
        build.assert_not_called()

    def test_refresh_preserves_old_artifact_and_receipt(self):
        with patch.object(pdf, 'download', side_effect=self.download), \
             patch.object(pdf, 'inspect_pdf', side_effect=self.inspect):
            output = self.prepare('18.6')
            original = output.read_bytes()
            old_hash = pdf.sha256(output)
            old_receipt = output.with_suffix('.source.json').read_bytes()
            self.payload = b'%PDF-1.4 newer official original'
            self.prepare('18.6', refresh=True)
        backup = output.parent / 'history' / output.stem / old_hash
        self.assertEqual((backup / output.name).read_bytes(), original)
        self.assertEqual((backup / output.with_suffix('.source.json').name).read_bytes(), old_receipt)
        self.assertEqual(output.read_bytes(), self.payload)

    def test_failed_download_and_version_mismatch_preserve_existing_file(self):
        output = self.seed('18.6')
        original = output.read_bytes()
        with patch.object(pdf, 'download', side_effect=OSError('network failure')), \
             patch.object(pdf, 'build') as builder:
            with self.assertRaisesRegex(OSError, 'network failure'):
                self.prepare('18.6')
            builder.assert_not_called()
        self.version = '18.7'
        with patch.object(pdf, 'download', side_effect=self.download), \
             patch.object(pdf, 'inspect_pdf', side_effect=self.inspect):
            with self.assertRaisesRegex(ValueError, 'requested 18.6'):
                self.prepare('18.6')
        self.assertEqual(output.read_bytes(), original)
        self.assertFalse(output.with_suffix('.source.json').exists())

    def test_wrong_version_is_not_frozen(self):
        output = self.seed('7.4.30')
        with patch.object(pdf, 'inspect_pdf', side_effect=self.inspect):
            with self.assertRaisesRegex(ValueError, 'requested 7.4.30'):
                self.prepare('7.4.30')
        self.assertFalse(output.with_suffix('.source.json').exists())

    def test_html_error_page_is_not_accepted_as_pdf(self):
        output = self.seed('18.6')
        original = output.read_bytes()
        self.payload = b'<html>upstream error</html>'
        with patch.object(pdf, 'download', side_effect=self.download):
            with self.assertRaisesRegex(ValueError, 'Not a PDF'):
                self.prepare('18.6')
        self.assertEqual(output.read_bytes(), original)

    def test_historical_official_pdf_uses_cover_version_and_original_paper_size(self):
        output = self.seed('8.0')
        info = 'Title:           \nPages: 1332\nPage size: 593.051 x 838.744 pts\n'
        with patch.object(pdf.subprocess, 'check_output', side_effect=[
                info, 'PostgreSQL 8.0.0 Documentation\n']):
            record = pdf.inspect_pdf(output, 'A4')
        self.assertEqual(record['pdf_version'], '8.0.0')
        self.assertEqual(record['version_source'], 'cover')
        self.assertEqual(record['page_size'], '593.051 x 838.744 pts')
        with patch.object(pdf.subprocess, 'check_output', return_value=info):
            with self.assertRaisesRegex(ValueError, 'US page size'):
                pdf.inspect_pdf(output, 'US')

    def test_devel_always_uses_registered_pin_and_keeps_previous_on_failure(self):
        source = self.source('20devel')
        output = self.seed('20devel')
        original = output.read_bytes()
        with patch.object(pdf, 'build', side_effect=subprocess.CalledProcessError(1, 'builder')) as builder:
            with self.assertRaises(subprocess.CalledProcessError):
                self.prepare('20devel')
        self.assertEqual(builder.call_args.args[1], source)
        self.assertEqual(output.read_bytes(), original)
        with patch.dict(os.environ, {'PGDOC_SOURCE_DIR': '/moving/master',
                                     'PGDOC_SOURCE_COMMIT': 'wrong',
                                     'PGDOC_SOURCE_SHA256': 'wrong'}), \
             patch.object(pdf.subprocess, 'run') as runner:
            pdf.build(self.root, source, '20devel', 'A4', output)
        command = runner.call_args.args[0]
        env = runner.call_args.kwargs['env']
        self.assertEqual(command[2:4], ['en', '20devel'])
        self.assertNotIn('PGDOC_SOURCE_DIR', env)
        self.assertNotIn('PGDOC_SOURCE_COMMIT', env)
        self.assertEqual(env['PGDOC_SOURCE_SHA256'], source['archive_sha256'])

    @patch.object(pdf, 'build')
    @patch.object(pdf, 'download')
    def test_dry_run_writes_nothing(self, download, build):
        self.prepare('18.6', dry_run=True)
        self.assertFalse(self.output_root.exists())
        download.assert_not_called()
        build.assert_not_called()

    def test_clean_preserves_english_files_and_frozen_receipts(self):
        output = self.seed('7.4.30')
        receipt = output.with_suffix('.source.json')
        receipt.write_text('{}')
        chinese = self.output_root / 'zh'
        chinese.mkdir()
        (chinese / 'generated.pdf').write_bytes(b'generated')
        subprocess.run(['make', '-f', str(pdf.ROOT / 'Makefile'), 'clean-pdf',
                        f'PDF_OUT_ROOT={self.output_root}'], check=True, capture_output=True)
        self.assertTrue(output.exists())
        self.assertTrue(receipt.exists())
        self.assertFalse(chinese.exists())


if __name__ == '__main__':
    unittest.main()
