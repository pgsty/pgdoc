#!/usr/bin/env python3
"""Download official English PDFs; freeze legacy builds and pin devel builds."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
LEGACY = ('6.3.2', '6.4.2', '6.5.3', '7.0.3', '7.1.3', '7.2.8', '7.3.21', '7.4.30')


def policy(version):
    for release in LEGACY:
        if version in (release, release.rsplit('.', 1)[0]):
            return release, 'legacy-once', release.rsplit('.', 1)[0]
    if re.fullmatch(r'(?:[89]\.\d)(?:\.\d+)?', version):
        major = '.'.join(version.split('.')[:2])
        if major in [f'8.{n}' for n in range(5)] + [f'9.{n}' for n in range(7)]:
            return version, 'official', major
    match = re.fullmatch(r'(\d+)(devel|\.\d+|beta\d+|rc\d+)?', version)
    if match and int(match[1]) >= 10:
        return version, 'devel' if match[2] == 'devel' else 'official', match[1]
    raise ValueError(f'Unsupported PostgreSQL version: {version}')


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_pdf(path, paper):
    with path.open('rb') as stream:
        if stream.read(5) != b'%PDF-':
            raise ValueError(f'Not a PDF: {path}')
    info = subprocess.check_output(['pdfinfo', str(path)], text=True,
                                   env={**os.environ, 'LC_ALL': 'C'})
    fields = dict(line.split(':', 1) for line in info.splitlines() if ':' in line)
    pages = int(fields.get('Pages', '0').strip())
    size = re.match(r'\s*([\d.]+) x ([\d.]+) pts', fields.get('Page size', ''))
    expected = (595.276, 841.89) if paper == 'A4' else (612, 792)
    # Official early pdfTeX A4 books use 593.051 x 838.744 pt. Allow the
    # historical rounding while still distinguishing A4 from US Letter.
    if pages < 1 or not size or any(abs(float(size[i + 1]) - value) > 4
                                  for i, value in enumerate(expected)):
        raise ValueError(f'Invalid page count or {paper} page size: {path}')
    title = fields.get('Title', '').strip()
    pattern = r'PostgreSQL\s+(\d+(?:\.\d+){0,2}(?:beta\d+|rc\d+|devel)?)\b'
    version = re.search(pattern, title, re.I)
    version_source = 'metadata'
    if not version:
        cover = subprocess.check_output(['pdftotext', '-f', '1', '-l', '1', str(path), '-'], text=True)
        version = re.search(pattern, cover, re.I)
        version_source = 'cover' if version else None
    return {'pages': pages, 'page_size': fields['Page size'].strip(),
            'title': title, 'pdf_version': version[1] if version else None,
            'version_source': version_source,
            'bytes': path.stat().st_size, 'sha256': sha256(path)}


def source_entry(root, version):
    entries = json.loads((root / 'en/SOURCES.json').read_text())['entries']
    source = next((entry for entry in entries if entry['version'] == version), None)
    if not source:
        raise ValueError(f'No fixed source for {version} in en/SOURCES.json')
    if not re.fullmatch(r'[0-9a-f]{64}', source.get('archive_sha256', '')):
        raise ValueError(f'No fixed archive SHA-256 for {version}')
    if not (root / source['archive']).is_file() or not (root / source['doc_dir'] / 'postgres.sgml').is_file():
        raise ValueError(f'Missing fixed archive or English source for {version}')
    return source


def check_version(record, version, major, mode):
    actual = record['pdf_version']
    if mode == 'legacy-once':
        # Earliest manuals omit a version in PDF metadata; later titles must agree.
        valid = actual is None or actual in (version, major)
    elif mode == 'devel':
        valid = actual == version
    else:
        valid = actual and policy(actual)[2] == major and (version == major or actual == version)
    if not valid:
        raise ValueError(f'PDF is {actual!r}, requested {version}; use its actual version or major {major}')


def build(root, source, version, paper, output):
    env = os.environ.copy()
    for key in ('PGDOC_SOURCE_DIR', 'PGDOC_SOURCE_COMMIT',
                'PGDOC_SOURCE_ARCHIVE', 'PGDOC_SOURCE_SHA256'):
        env.pop(key, None)
    env.update(PGDOC_SOURCE_ARCHIVE=str(root / source['archive']),
               PGDOC_SOURCE_SHA256=source['archive_sha256'])
    subprocess.run([str(root / 'bin/build_standalone_pdfsrc.sh'),
                    str(root / source['doc_dir']), 'en', version,
                    str(output), paper], env=env, check=True)


def download(url, output):
    with urlopen(url, timeout=60) as response, output.open('wb') as stream:
        shutil.copyfileobj(response, stream)
        return {'url': url, 'final_url': response.geturl(),
                'last_modified': response.headers.get('Last-Modified')}


def write_receipt(path, receipt):
    with tempfile.NamedTemporaryFile(mode='w', dir=path.parent,
                                     prefix=path.name, suffix='.tmp', delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def preserve_previous(output):
    if not output.exists():
        return
    backup = output.parent / 'history' / output.stem / sha256(output)
    backup.mkdir(parents=True, exist_ok=True)
    for path in (output, output.with_suffix('.source.json'), output.with_suffix('.fop.log')):
        if path.exists():
            target = backup / path.name
            if not target.exists():
                shutil.copy2(path, target)


def prepare(version, paper, output_root, *, root=ROOT, refresh=False, dry_run=False):
    version, mode, major = policy(version)
    output = output_root.resolve() / 'en' / f'postgresql-{version}-en-{paper}.pdf'
    receipt_path = output.with_suffix('.source.json')
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
    url = f'https://www.postgresql.org/files/documentation/pdf/{major}/postgresql-{major}-{paper}.pdf'
    if receipt and mode == 'legacy-once':
        if receipt.get('mode') != mode or receipt.get('version') != version or receipt.get('paper') != paper:
            raise ValueError(f'Unexpected frozen PDF receipt: {receipt_path}')
        if not output.is_file() or sha256(output) != receipt['sha256']:
            raise ValueError(f'Frozen PDF missing or changed; restore the recorded file, do not rebuild: {output}')
        print(f'Frozen, unchanged: {output}')
        return output
    if mode == 'official' and receipt and not refresh:
        if (receipt.get('mode') == mode and receipt.get('url') == url
                and receipt.get('version') == version and receipt.get('paper') == paper):
            if not output.is_file() or sha256(output) != receipt['sha256']:
                raise ValueError(f'Downloaded PDF missing or changed; use --refresh to fetch the official original: {output}')
            print(f'Official PDF cached: {output}')
            return output
    existing_legacy = mode == 'legacy-once' and output.exists()
    source = source_entry(root, version) if mode != 'official' and not existing_legacy else None
    if dry_run:
        action = 'freeze existing' if existing_legacy else ('download' if mode == 'official' else 'build')
        print(f'{version} {paper}: {action} ({mode}) -> {output}')
        if mode == 'official':
            print(f'  {url}')
        elif source:
            print(f"  {source['archive']} sha256={source['archive_sha256']}")
        return output
    output.parent.mkdir(parents=True, exist_ok=True)
    record = {'version': version, 'major': major, 'language': 'en', 'paper': paper,
              'mode': mode, 'recorded_at': datetime.now(timezone.utc).isoformat()}
    if existing_legacy:
        record.update(inspect_pdf(output, paper), origin='existing-local')
        check_version(record, version, major, mode)
        write_receipt(receipt_path, record)
        print(f'Frozen existing PDF (bytes unchanged): {output}')
        return output
    with tempfile.TemporaryDirectory(prefix='.prepare-', dir=output.parent) as work:
        candidate = Path(work) / output.name
        if mode == 'official':
            record.update(download(url, candidate))
        else:
            record['source'] = {key: source[key] for key in ('archive', 'archive_sha256', 'doc_dir')}
            build(root, source, version, paper, candidate)
        record.update(inspect_pdf(candidate, paper))
        check_version(record, version, major, mode)
        preserve_previous(output)
        candidate.replace(output)
        fop_log = candidate.with_suffix('.fop.log')
        if fop_log.exists():
            fop_log.replace(output.with_suffix('.fop.log'))
        elif output.with_suffix('.fop.log').exists():
            output.with_suffix('.fop.log').unlink()
        write_receipt(receipt_path, record)
    print(f'Prepared {mode}: {output}')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--paper', choices=('A4', 'US'), default='A4')
    parser.add_argument('--output-root', type=Path, default=ROOT / 'tmp/pdf')
    parser.add_argument('--refresh', action='store_true', help='Refresh an official download; never rebuild a frozen legacy PDF')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        prepare(args.version, args.paper, args.output_root, refresh=args.refresh, dry_run=args.dry_run)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
