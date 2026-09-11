#!/usr/bin/env python3
"""Generate only upstream GENERATED_SGML in an isolated, pinned workspace."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from prepare_pinned_doc_source import prepare, prepare_archive
from check_doc_alignment import file_hash, source_manifest, write_json


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archive', type=Path)
    p.add_argument('--sha256')
    p.add_argument('--source-dir', type=Path)
    p.add_argument('--source-commit')
    p.add_argument('--version', required=True)
    p.add_argument('--en', type=Path, required=True)
    p.add_argument('--zh', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    if bool(a.archive) != bool(a.sha256) or bool(a.source_dir) != bool(a.source_commit):
        p.error('archive/sha256 and source-dir/source-commit must be supplied in pairs')
    if bool(a.archive) == bool(a.source_dir):
        p.error('select exactly one fixed release archive or Git source')
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    upstream = out / 'upstream'
    upstream.mkdir()
    if a.archive:
        prepare_archive(a.archive, a.sha256, a.version, upstream)
    else:
        prepare(a.source_dir, a.source_commit, a.version, upstream)
    pristine = upstream / 'doc/src/sgml'
    # The English comparison really must be against this release.  Do not fill
    # holes from the archive: report the standalone snapshot's coverage first.
    expected = {str(f.relative_to(pristine)): file_hash(f)
                for f in pristine.rglob('*.sgml')}
    actual = {str(f.relative_to(a.en)): file_hash(f)
              for f in a.en.rglob('*.sgml') if 'html' not in f.relative_to(a.en).parts}
    differences = {f: {'archive': expected.get(f), 'snapshot': digest}
                   for f, digest in actual.items() if expected.get(f) != digest}
    if differences:
        write_json(out / 'english-source-mismatch.json', differences)
        raise ValueError('English SGML differs from pinned archive; see english-source-mismatch.json')
    manifest = {'version': a.version,
                'source_provenance': json.loads((upstream / '.pgdoc-source.json').read_text()),
                'english_sgml_verified': len(actual),
                'archive_sgml_not_in_snapshot': sorted(expected.keys() - actual.keys()),
                'languages': {}}
    pristine_backup = out / 'pristine-sgml'
    with (out / 'configure.log').open('w') as log:
        subprocess.run(['./configure', '--without-icu', '--without-readline', '--without-zlib'],
                       cwd=upstream, stdout=log, stderr=subprocess.STDOUT, check=True)
    shutil.copytree(pristine, pristine_backup)
    make = shutil.which('gmake') or shutil.which('make')
    for lang, source in [('en', a.en.resolve()), ('zh', a.zh.resolve())]:
        # Restore the upstream build recipe before overlaying this language's
        # generator scripts and inputs. Never add upstream SGML to the parser.
        shutil.rmtree(pristine)
        shutil.copytree(pristine_backup, pristine)
        for row in source_manifest(source)['files']:
            rel = row['path']
            if rel in {'Makefile', '.gitignore'}:
                continue
            dest = pristine / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / rel, dest)
        extra = pristine / 'Makefile.alignment'
        extra.write_text('.PHONY: alignment-generated alignment-list\n'
                         'alignment-generated: $(GENERATED_SGML)\n'
                         'alignment-list:\n\t@echo $(GENERATED_SGML)\n')
        command = [make, '-s', '-C', str(pristine), '-f', 'Makefile', '-f', str(extra)]
        names = subprocess.check_output(command + ['alignment-list'], text=True).split()
        # Tarballs can carry generated files; force regeneration from this
        # language's exact generator inputs instead of relying on timestamps.
        for name in names:
            (pristine / name).unlink(missing_ok=True)
        with (out / f'{lang}-generate.log').open('w') as log:
            subprocess.run(command + ['alignment-generated'], stdout=log,
                           stderr=subprocess.STDOUT, check=True)
            localizer = source / 'localize-generated.py'
            if localizer.exists():
                subprocess.run([sys.executable, str(localizer), str(pristine)],
                               stdout=log, stderr=subprocess.STDOUT, check=True)
        target = out / lang
        target.mkdir()
        for name in names:
            shutil.copy2(pristine / name, target / name)
        manifest['languages'][lang] = {
            'source': source_manifest(source), 'generated': source_manifest(target),
            'command': command + ['alignment-generated']}
    write_json(out / 'manifest.json', manifest)
    print(json.dumps({'prepared': str(out), 'version': a.version,
                      'english_sgml_verified': len(actual)}))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        sys.exit(f'Preparation failed: {exc}')
