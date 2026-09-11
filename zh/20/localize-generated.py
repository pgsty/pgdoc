#!/usr/bin/env python3
"""Apply reviewed Chinese translations after regenerating the pinned PG20 input.

Keep upstream generators and inputs intact. Each input/output is hash-bound;
the map is the maintained translation source, including the complete wait-event
tables. Generated SGML stays in the isolated build workspace.
"""
import hashlib
import json
from pathlib import Path
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    target = Path(sys.argv[1])
    mapping = json.loads(Path(__file__).with_name('generated-translations.json').read_text())
    outputs = []
    for name, record in mapping.items():
        path = target / name
        data = path.read_bytes()
        if digest(data) != record['input_sha256']:
            raise ValueError(f'{name}: regenerated PG20 input hash mismatch')
        text = data.decode()
        for edit in record['edits']:
            if text.count(edit['english']) != 1:
                raise ValueError(f'{name}: generated translation boundary mismatch')
            text = text.replace(edit['english'], edit['chinese'])
        if digest(text.encode()) != record['output_sha256']:
            raise ValueError(f'{name}: localized output hash mismatch')
        outputs.append((path, text))
    # The inherited project entity is an empty, generated bookinfo placeholder.
    notes = target / 'pgdoccn-notes.sgml'
    if not notes.exists():
        notes.write_text('<!-- pgdoccn notes placeholder -->\n')
    for path, text in outputs:
        path.write_text(text)
        print(f'Localized generated PG20 table: {path.name} {digest(text.encode())}')


if __name__ == '__main__':
    main()
