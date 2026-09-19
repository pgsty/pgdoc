#!/usr/bin/env python3
"""Verify a fixed PostgreSQL checkout or release archive for a docs workspace."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile


def git(source, *args):
    return subprocess.check_output(['git', '-C', str(source), *args])


def version_declarations_pg6x(source, requested):
    # PG 6.x archives have no top-level Autoconf input; the version lives in
    # src/include/version.h(.in).  6.3.x omits PG_SUBVERSION (branch patch
    # level only in the archive name), so accept a prefix match there.
    vh = source / 'src/include/version.h.in'
    if not vh.is_file():
        vh = source / 'src/include/version.h'
    try:
        text = vh.read_text()
    except OSError:
        raise ValueError('pinned source has no configure.ac, configure.in'
                         ' or src/include/version.h(.in)')
    parts = {key: re.search(rf'^#define\s+{key}\s+"?(\d+)', text, re.M)
             for key in ('PG_RELEASE', 'PG_VERSION', 'PG_SUBVERSION')}
    if not (parts['PG_RELEASE'] and parts['PG_VERSION']):
        raise ValueError(f'cannot read PostgreSQL version from {vh.name}')
    version = f"{parts['PG_RELEASE'][1]}.{parts['PG_VERSION'][1]}"
    if parts['PG_SUBVERSION']:
        version += f".{parts['PG_SUBVERSION'][1]}"
    if requested != version and not requested.startswith(version + '.'):
        raise ValueError(f'pinned source version mismatch: requested {requested}, got {version}')
    return version, {vh.name: version}


def version_declarations(source, requested):
    # Older releases name the Autoconf input configure.in, rather than .ac.
    autoconf_inputs = [name for name in ('configure.ac', 'configure.in')
                       if (source / name).is_file()]
    if not autoconf_inputs:
        return version_declarations_pg6x(source, requested)
    patterns = {name: r'AC_INIT\(\[PostgreSQL\],\s*\[([^]]+)\]'
                for name in autoconf_inputs}
    patterns['configure'] = r"^PACKAGE_VERSION='([^']+)'"
    if (source / 'meson.build').exists():
        patterns['meson.build'] = r"^\s*version:\s*'([^']+)'"
    versions = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, (source / name).read_text(), re.M)
        if not match:
            raise ValueError(f'cannot read PostgreSQL version from {name}')
        versions[name] = match[1]
    if len(set(versions.values())) != 1:
        raise ValueError(f'conflicting version declarations: {versions}')
    version = versions['configure']
    if requested.isdigit():
        matches = re.match(r'^\d+', version)[0] == requested
    else:
        matches = version == requested
    if not matches:
        raise ValueError(f'pinned source version mismatch: requested {requested}, got {version}')
    return version, versions


def copy_files(source, destination, names):
    files = []
    for name in sorted(filter(None, names)):
        src, dst = source / name, destination / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink():
            target = os.readlink(src)
            dst.symlink_to(target)
            data = target.encode()
        else:
            data = src.read_bytes()
            shutil.copy2(src, dst)
            if dst.read_bytes() != data:
                raise ValueError(f'copy verification failed: {name}')
        files.append({'path': name, 'sha256': hashlib.sha256(data).hexdigest()})
    return files


def prepare(source, commit, requested, destination):
    source = Path(source).resolve()
    destination = Path(destination).resolve()
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('PGDOC_SOURCE_COMMIT must be a full 40-character commit')
    actual = git(source, 'rev-parse', 'HEAD').decode().strip()
    if actual != commit:
        raise ValueError(f'pinned commit mismatch: expected {commit}, got {actual}')
    if git(source, 'status', '--porcelain', '--untracked-files=no').strip():
        raise ValueError('pinned source has modified tracked content')
    version, versions = version_declarations(source, requested)
    if any(destination.iterdir()):
        raise ValueError('pinned destination must be empty')
    # Copy exactly the verified tracked source, including executable modes.
    # Untracked build products and .git never become source inputs.
    names = git(source, 'ls-files', '-z').decode().split('\0')
    files = copy_files(source, destination, names)
    if git(source, 'rev-parse', 'HEAD').decode().strip() != commit or git(source, 'status', '--porcelain', '--untracked-files=no').strip():
        raise ValueError('pinned source changed while copying')
    provenance = {'kind': 'git', 'source_dir': str(source), 'commit': commit,
                  'version': version, 'version_declarations': versions, 'files': files}
    (destination / '.pgdoc-source.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Pinned PostgreSQL source: {source}\n  commit: {commit}\n  version: {version}\n  verified files: {len(files)}\n  manifest: {destination / ".pgdoc-source.json"}')


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_archive(archive, expected_sha256, requested, destination):
    archive = Path(archive).resolve()
    destination = Path(destination).resolve()
    if not re.fullmatch(r'[0-9a-f]{64}', expected_sha256):
        raise ValueError('PGDOC_SOURCE_SHA256 must be a full 64-character SHA256')
    actual = file_sha256(archive)
    if actual != expected_sha256:
        raise ValueError(f'pinned archive SHA256 mismatch: expected {expected_sha256}, got {actual}')
    if any(destination.iterdir()):
        raise ValueError('pinned destination must be empty')
    with tempfile.TemporaryDirectory(prefix='pgdoc-archive-', dir=destination.parent) as temp:
        with tarfile.open(archive) as bundle:
            # Official release packages have one root. The data filter also
            # rejects paths or links that escape this isolated extraction.
            bundle.extractall(temp, filter='data')
        roots = list(Path(temp).iterdir())
        if len(roots) != 1 or not roots[0].is_dir():
            raise ValueError('pinned archive must contain one source directory')
        source = roots[0]
        version, versions = version_declarations(source, requested)
        # 6.3.x archives name the root with the patch level (postgresql-6.3.2)
        # while their version header only declares the branch (6.3).
        if source.name not in (f'postgresql-{version}', f'postgresql-{requested}'):
            raise ValueError(f'pinned archive root does not match source version: {source.name}')
        names = [str(path.relative_to(source)) for path in source.rglob('*')
                 if path.is_file() or path.is_symlink()]
        files = copy_files(source, destination, names)
    if file_sha256(archive) != expected_sha256:
        raise ValueError('pinned archive changed while copying')
    provenance = {'kind': 'release-archive', 'archive': str(archive),
                  'archive_sha256': expected_sha256, 'version': version,
                  'version_declarations': versions, 'files': files}
    (destination / '.pgdoc-source.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Pinned PostgreSQL archive: {archive}\n  SHA256: {expected_sha256}\n  version: {version}\n  verified files: {len(files)}\n  manifest: {destination / ".pgdoc-source.json"}')


if __name__ == '__main__':
    try:
        if len(sys.argv) == 6 and sys.argv[1] == '--archive':
            prepare_archive(*sys.argv[2:])
        elif len(sys.argv) == 5:
            prepare(*sys.argv[1:])
        else:
            raise ValueError('usage: prepare_pinned_doc_source.py <source-dir> <commit> <version> <destination> OR --archive <archive> <sha256> <version> <destination>')
    except (ValueError, OSError, subprocess.CalledProcessError, tarfile.TarError) as error:
        sys.exit(f'Pinned source error: {error}')
