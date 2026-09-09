"""Assemble the approved, unchanged terminology inputs for this handoff."""
from pathlib import Path
import csv
import hashlib
import json
import shutil

PACK = Path(__file__).resolve().parents[1]
ROOT = PACK.parents[1]
SOURCE = ROOT / 'outputs/01a08005-ffff-72b1-84e0-109c680e9bc8/v2'
REFS = PACK / 'refs'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.reader(stream, delimiter='\t'))


def main():
    if REFS.exists():
        raise SystemExit('refs already exists; do not overwrite the frozen handoff inputs')
    original = ROOT / 'tmp/ref/glossary.tsv'
    assert digest(original) == 'ff69734367df13cf3650a12c945743643f6723e7032e93a3d35ecc4de4cd81db'
    mappings = {
        'glossary.original.tsv': original,
        'glossary.tsv': SOURCE / 'glossary.final.tsv',
        'glossary.rules.tsv': SOURCE / 'glossary.rules.tsv',
        'changes.tsv': SOURCE / 'glossary-changes.final.tsv',
        'aliases.tsv': SOURCE / 'glossary-aliases.tsv',
        'preserve.tsv': SOURCE / 'terms-to-preserve.tsv',
        'net-changes.md': SOURCE / '最终术语修订汇总.md',
        'exclude.tsv': ROOT / 'tmp/ref/exclude.tsv',
        'style.md': ROOT / 'tmp/ref/style.md',
    }
    REFS.mkdir(parents=True)
    sources = []
    for name, source in mappings.items():
        target = REFS / name
        shutil.copyfile(source, target)
        assert digest(source) == digest(target)
        if name == 'net-changes.md':
            text = target.read_text(encoding='utf-8')
            for old, new in [('glossary.final.tsv', 'glossary.tsv'), ('glossary-aliases.tsv', 'aliases.tsv'), ('glossary-changes.final.tsv', 'changes.tsv')]:
                text = text.replace('](' + old + ')', '](' + new + ')')
            text = text.replace('](讨论记录.md)', '](../../../outputs/01a08005-ffff-72b1-84e0-109c680e9bc8/v2/讨论记录.md)')
            text = text.replace('](../../../tmp/ref/glossary.tsv)', '](glossary.original.tsv)')
            target.write_text(text, encoding='utf-8')
        sources.append({'file': name, 'source': str(source.relative_to(ROOT)), 'source_sha256': digest(source), 'sha256': digest(target), 'bytes': target.stat().st_size, 'link_relocations_only': name == 'net-changes.md'})
    before, after = rows(REFS / 'glossary.original.tsv')[1:], rows(REFS / 'glossary.tsv')[1:]
    assert len(before) == len(after) == 631
    assert len({r[0] for r in after}) == 631
    actual = [(i, *a, *b) for i, (a, b) in enumerate(zip(before, after), 1) if a != b]
    changes = rows(REFS / 'changes.tsv')[1:]
    assert actual == [(int(r[0]), *r[1:5]) for r in changes]
    rules = rows(REFS / 'glossary.rules.tsv')[1:]
    assert len(rules) == 631
    assert [(int(r[0]), r[1]) for r in rules] == [(i, r[0]) for i, r in enumerate(after, 1)]
    manifest = {
        'prepared_on': '2026-09-08',
        'full_terms': 631, 'net_changes': 68,
        'english_only': 5, 'chinese_only': 59, 'both': 4,
        'review': 'Claude Code Fable 5.1 / xhigh; 3 rounds; final approved mapping copied byte-for-byte',
        'files': sources,
    }
    (REFS / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Prepared frozen references: 631 terms, 631 rules, 68 net changes; source files unchanged.')


if __name__ == '__main__':
    main()
