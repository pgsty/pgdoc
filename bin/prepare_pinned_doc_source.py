#!/usr/bin/env python3
"""Verify and copy a fixed PostgreSQL checkout into an empty docs workspace."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def git(source, *args):
    return subprocess.check_output(['git', '-C', str(source), *args])


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
    patterns = {
        'configure.ac': r'AC_INIT\(\[PostgreSQL\],\s*\[([^]]+)\]',
        'configure': r"^PACKAGE_VERSION='([^']+)'",
        'meson.build': r"^\s*version:\s*'([^']+)'",
    }
    versions = {}
    for name, pattern in patterns.items():
        match = re.search(pattern, (source / name).read_text(), re.M)
        if not match:
            raise ValueError(f'cannot read PostgreSQL version from {name}')
        versions[name] = match[1]
    if len(set(versions.values())) != 1:
        raise ValueError(f'conflicting version declarations: {versions}')
    version = versions['configure.ac']
    if requested.isdigit():
        matches = re.match(r'^\d+', version)[0] == requested
    else:
        matches = version == requested
    if not matches:
        raise ValueError(f'pinned source version mismatch: requested {requested}, got {version}')
    if any(destination.iterdir()):
        raise ValueError('pinned destination must be empty')
    files = []
    # Copy exactly the verified tracked source, including executable modes.
    # Untracked build products and .git never become source inputs.
    names = git(source, 'ls-files', '-z').decode().split('\0')
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
    if git(source, 'rev-parse', 'HEAD').decode().strip() != commit or git(source, 'status', '--porcelain', '--untracked-files=no').strip():
        raise ValueError('pinned source changed while copying')
    provenance = {'source_dir': str(source), 'commit': commit,
                  'version': version, 'version_declarations': versions, 'files': files}
    (destination / '.pgdoc-source.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'Pinned PostgreSQL source: {source}\n  commit: {commit}\n  version: {version}\n  verified files: {len(files)}\n  manifest: {destination / ".pgdoc-source.json"}')


if __name__ == '__main__':
    try:
        prepare(*sys.argv[1:])
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        sys.exit(f'Pinned source error: {error}')
