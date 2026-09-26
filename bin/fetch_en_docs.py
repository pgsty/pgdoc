#!/usr/bin/env python3
"""Fetch a PostgreSQL release archive and extract its English doc source into en/.

Usage:
  fetch_en_docs.py VERSION [options]

  VERSION            release version, e.g. 16.15 / 18.6 / 19beta4
  --dest DIR         target directory (default: en/<VERSION>)
  --url URL          explicit archive URL (needed for snapshots and git exports)
  --archive PATH     use a local tarball instead of downloading
  --sha256 HASH      expected archive SHA256 (default: sidecar .sha256/.md5, else record-only)
  --force            allow overwriting a non-empty target directory
  --no-keep          delete the archive afterwards if this run downloaded it
  --register         add or update the SOURCES.json entry for this version
                     (only allowed with the default en/<VERSION> target)

Layout produced (matches en/SOURCES.json conventions):
  <dest>/            contents of <root>/doc/src/sgml/, copied verbatim
  <dest>/graphics/   contents of <root>/doc/src/graphics/ (6.3-7.3 only)
  <dest>/<name>.gif  every GIF from graphics/, copied to the doc root
                     where the SGML FileRef/fileref names resolve

The script never deletes existing trees; it only writes into --dest.
Archives are kept in .cache/upstream/ (the recovery base for en/ — do not prune).
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / '.cache/upstream'
SOURCE_BASE = 'https://ftp.postgresql.org/pub/source'


def digest(path, algo='sha256'):
    h = hashlib.new(algo)
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def http_ok(url):
    result = subprocess.run(['curl', '-sIL', '-o', '/dev/null',
                             '-w', '%{http_code}', '--max-time', '30', url],
                            capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip().startswith('200')


def resolve_archive(version, args):
    """Return (archive_path, url, index_url, expected, algo, downloaded_now)."""
    if args.archive:
        path = Path(args.archive).resolve()
        if not path.is_file():
            sys.exit(f'archive not found: {path}')
        return path, None, None, args.sha256, 'sha256' if args.sha256 else None, False

    if args.url:
        url, index_url = args.url, None
        archive = UPSTREAM / url.rsplit('/', 1)[-1]
    else:
        index_url = f'{SOURCE_BASE}/v{version}/'
        url = None
        for ext in ('.tar.bz2', '.tar.gz'):
            candidate = f'{index_url}postgresql-{version}{ext}'
            if http_ok(candidate):
                url = candidate
                archive = UPSTREAM / f'postgresql-{version}{ext}'
                break
        if url is None:
            sys.exit(f'no archive found under {index_url}; snapshots need --url '
                     'https://ftp.postgresql.org/pub/snapshot/dev/<name>.tar.bz2')

    expected, algo = args.sha256, ('sha256' if args.sha256 else None)
    if expected is None and url is not None:
        for suffix, hexlen, a in (('.sha256', 64, 'sha256'), ('.md5', 32, 'md5')):
            side = subprocess.run(['curl', '-sL', '--fail', '--max-time', '60',
                                   url + suffix], capture_output=True)
            # sidecars are either "<hash>  <file>" or BSD "MD5 (<file>) = <hash>"
            match = re.search(rb'\b[0-9a-fA-F]{%d}\b' % hexlen, side.stdout or b'') \
                if side.returncode == 0 else None
            if match:
                expected = match.group(0).decode().lower()
                algo = a
                print(f'published {a} checksum: {expected}')
                break
        if expected is None:
            print('WARNING: no published checksum found; recording local digest only')

    if archive.is_file():
        if expected and digest(archive, algo) != expected:
            print(f'cached archive {archive.name} fails checksum, re-downloading')
            archive.unlink()
        else:
            return archive, url, index_url, expected, algo, False

    archive.parent.mkdir(parents=True, exist_ok=True)
    tmp = archive.with_name(archive.name + '.part')
    result = subprocess.run(['curl', '-sS', '-fL', '--retry', '3', '--continue-at', '-',
                             '-o', str(tmp), url])
    if result.returncode != 0:
        tmp.unlink(missing_ok=True)
        sys.exit(f'download failed: {url}')
    if expected and digest(tmp, algo) != expected:
        tmp.unlink()
        sys.exit(f'{algo} mismatch after download: expected {expected}')
    os.replace(tmp, archive)
    return archive, url, index_url, expected, algo, True


def version_evidence(source, requested):
    """Consistent version declarations (adapted from prepare_pinned_doc_source.py)."""
    autoconf = [n for n in ('configure.ac', 'configure.in') if (source / n).is_file()]
    if not autoconf:
        vh = source / 'src/include/version.h.in'
        if not vh.is_file():
            vh = source / 'src/include/version.h'
        text = vh.read_text(errors='replace')
        parts = {k: re.search(rf'^#define\s+{k}\s+"?(\d+)', text, re.M)
                 for k in ('PG_RELEASE', 'PG_VERSION', 'PG_SUBVERSION')}
        if not (parts['PG_RELEASE'] and parts['PG_VERSION']):
            sys.exit('cannot read version from src/include/version.h(.in)')
        declared = f"{parts['PG_RELEASE'][1]}.{parts['PG_VERSION'][1]}"
        if parts['PG_SUBVERSION']:
            declared += f".{parts['PG_SUBVERSION'][1]}"
        if requested != declared and not requested.startswith(declared + '.'):
            sys.exit(f'version mismatch: archive says {declared}, requested {requested}')
        line = re.search(rf'^#define\s+PG_VERSION\s+\S+.*$', text, re.M)
        return declared, {'src/include/' + vh.name: [line.group(0)]}

    evidence = {}
    for name in autoconf:
        match = re.search(r'AC_INIT\(\[PostgreSQL\],\s*\[([^]]+)\]',
                          (source / name).read_text(errors='replace'))
        if not match:
            sys.exit(f'cannot read version from {name}')
        declared = match[1]
        evidence[name] = [match.group(0)]
    conf = re.search(r"^PACKAGE_VERSION='([^']+)'",
                     (source / 'configure').read_text(errors='replace'), re.M)
    if not conf or conf[1] != declared:
        sys.exit(f"configure declares {conf[1] if conf else '?'}, "
                 f"{autoconf[0]} declares {declared}")
    evidence.setdefault('configure', [f"PACKAGE_VERSION='{declared}'"])
    if (source / 'meson.build').is_file():
        meson = re.search(r"^\s*version:\s*'([^']+)'",
                          (source / 'meson.build').read_text(errors='replace'), re.M)
        if meson and meson[1] != declared:
            sys.exit(f'meson.build declares {meson[1]}, expected {declared}')
    if requested != declared and not requested.startswith(declared + '.'):
        sys.exit(f'version mismatch: archive says {declared}, requested {requested}')
    return declared, evidence


def read_evidence(archive, root_name, requested):
    with tempfile.TemporaryDirectory(prefix='pgdoc-evidence-') as td:
        with tarfile.open(archive) as bundle:
            names = bundle.getnames()
            wanted = [m for m in names if re.fullmatch(
                rf'{re.escape(root_name)}/(configure(\.ac|\.in)?|meson\.build'
                rf'|src/include/version\.h(\.in)?)', m)]
            bundle.extractall(td, members=wanted)
        return version_evidence(Path(td) / root_name, requested)


def copy_tree(src, dst):
    count = 0
    for p in sorted(src.rglob('*')):
        target = dst / p.relative_to(src)
        if p.is_symlink():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(os.readlink(p))
            count += 1
        elif p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            count += 1
    return count


def extract(archive, dest):
    with tempfile.TemporaryDirectory(prefix='pgdoc-fetch-') as td:
        with tarfile.open(archive) as bundle:
            try:
                bundle.extractall(td, filter='data')
            except TypeError:
                bundle.extractall(td)
        roots = [p for p in Path(td).iterdir() if p.is_dir()]
        if len(roots) != 1:
            sys.exit(f'archive must contain exactly one root directory: {archive.name}')
        source = roots[0]
        sgml = source / 'doc/src/sgml'
        if not sgml.is_dir():
            sys.exit(f'{archive.name} has no doc/src/sgml')
        dest.mkdir(parents=True, exist_ok=True)
        doc_files = copy_tree(sgml, dest)
        graphics = copy_tree(source / 'doc/src/graphics', dest / 'graphics') \
            if (source / 'doc/src/graphics').is_dir() else 0
        copies = 0
        if graphics:
            for gif in sorted((dest / 'graphics').iterdir()):
                if gif.is_file() and gif.suffix.lower() == '.gif':
                    shutil.copy2(gif, dest / gif.name)
                    copies += 1
        return source.name, doc_files, graphics, copies


def doc_only_bytes(dest, has_graphics):
    total = 0
    for p in dest.rglob('*'):
        if not p.is_file() or p.is_symlink():
            continue
        if has_graphics and (p.parent == dest and p.suffix.lower() == '.gif'
                             or dest / 'graphics' in p.parents):
            continue
        total += p.stat().st_size
    return total


def register(version, entry):
    path = ROOT / 'en/SOURCES.json'
    data = json.loads(path.read_text())
    entries = data.setdefault('entries', [])
    replaced = any(e.get('version') == version for e in entries)
    entries[:] = [entry if e.get('version') == version else e for e in entries] \
        if replaced else entries + [entry]
    data['last_incremental_update_utc'] = entry['checked_at_utc']
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')
    print(f'SOURCES.json: entry {version} {"updated" if replaced else "appended"}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('version')
    parser.add_argument('--dest')
    parser.add_argument('--url')
    parser.add_argument('--archive')
    parser.add_argument('--sha256')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--no-keep', action='store_true')
    parser.add_argument('--register', action='store_true')
    args = parser.parse_args()

    dest = Path(args.dest).resolve() if args.dest else ROOT / 'en' / args.version
    if dest.exists() and any(dest.iterdir()) and not args.force:
        sys.exit(f'{dest} already exists and is not empty (use --force to refresh)')
    if args.register and args.dest:
        sys.exit('--register requires the default en/<VERSION> target')

    archive, url, index_url, expected, algo, downloaded = \
        resolve_archive(args.version, args)
    actual_sha = digest(archive)

    root_name, doc_files, graphics, copies = extract(archive, dest)
    declared, evidence = read_evidence(archive, root_name, args.version)

    files = [p for p in dest.rglob('*') if p.is_file() or p.is_symlink()]
    nbytes = sum(p.stat().st_size for p in files if not p.is_symlink())
    nsgml = sum(1 for p in files if not p.is_symlink() and p.suffix == '.sgml')
    print(f'version {args.version} (declared {declared})')
    print(f'  archive: {archive}')
    print(f'  sha256:  {actual_sha}')
    print(f'  files:   {len(files)}  bytes: {nbytes}  sgml: {nsgml}  '
          f'graphics: {graphics}  gif copies: {copies}')

    if args.no_keep and downloaded:
        archive.unlink()
        print('  archive removed (--no-keep)')

    if args.register:
        checksum_url = None
        if url and algo in ('sha256', 'md5'):
            checksum_url = url + ('.sha256' if algo == 'sha256' else '.md5')
        entry = {
            'version': args.version, 'index_url': index_url, 'url': url,
            'filename': archive.name, 'size': archive.stat().st_size,
            'checksum_algorithm': algo if expected else None,
            'checksum': expected, 'checksum_url': checksum_url,
            'archive': str(archive.relative_to(ROOT)),
            'archive_sha256': actual_sha,
            'archive_bytes': archive.stat().st_size,
            'archive_root': root_name,
            'version_evidence': evidence,
            'doc_dir': str(dest.relative_to(ROOT)),
            'doc_source': 'doc/src/sgml',
            'doc_files': doc_files, 'doc_sgml_files': nsgml,
            'doc_bytes': doc_only_bytes(dest, graphics > 0),
            'docs_added': len(files), 'existing_doc_dir': False,
            'local_differences_preserved': [], 'local_extra_files_preserved': [],
            'graphics_files': graphics, 'graphic_copies_at_doc_root': copies,
            'documentation_files_verified': len(files),
            'documentation_bytes': nbytes,
            'documentation_missing_files': 0, 'documentation_mismatched_files': 0,
            'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        register(args.version, entry)


if __name__ == '__main__':
    main()
