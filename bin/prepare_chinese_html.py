#!/usr/bin/env python3
"""Remove generated CJK spacing from HTML without reserializing its markup.

Source SGML is normalized separately.  XSL-generated index labels and copied
cross-reference titles can introduce additional whitespace.  This pass uses
an isolated instance of the source fixer's byte-preserving deletion engine,
with HTML element classifications.  Code, raw-text blocks, SVG and MathML
remain untouched.  Only ASCII whitespace may be removed.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import sys


def load_html_engine():
    spec = importlib.util.spec_from_file_location(
        '_pgdoc_html_spacing', Path(__file__).with_name('fix_cjk_spacing.py'))
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    engine.VERBATIM_BLOCK = frozenset(('pre', 'script', 'style', 'textarea', 'svg', 'math'))
    engine.VERBATIM_INLINE = frozenset(('code', 'kbd', 'samp', 'var'))
    engine.INLINE = frozenset((
        'a', 'span', 'em', 'strong', 'b', 'i', 'u', 's', 'del', 'ins',
        'mark', 'small', 'sub', 'sup', 'cite', 'abbr', 'acronym', 'time',
        'ruby', 'rt', 'rp', 'font', 'label', 'q', 'bdi', 'bdo',
    ))
    engine.EMPTY_ELEMENTS = frozenset((
        'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
        'link', 'meta', 'param', 'source', 'track', 'wbr',
    ))
    engine.GENTEXT = frozenset()
    engine.TRANSPARENT = frozenset()
    engine.INDEX_TEXT = frozenset()
    return engine


ENGINE = load_html_engine()
RAW_TEXT = re.compile(r'<(script|style|textarea)\b', re.IGNORECASE)


def mask_raw_text(text):
    """Keep offsets while hiding raw JS/CSS '<' from the SGML tokenizer."""
    if not RAW_TEXT.search(text):
        return text
    parts, copied, position = [], 0, 0
    while (start := text.find('<', position)) >= 0:
        kind, name, end = ENGINE._scan_tag(text, start)
        position = end
        if kind != 'open' or name not in ('script', 'style', 'textarea'):
            continue
        closing = re.search(r'</' + name + r'\s*>', text[end:], re.IGNORECASE)
        if closing is None:
            raise ValueError(f'unclosed raw-text element at offset {start}')
        content_end = end + closing.start()
        parts.extend((text[copied:end], 'X' * (content_end - end)))
        copied = content_end
        position = end + closing.end()
    parts.append(text[copied:])
    return ''.join(parts)


def normalize_html(text):
    try:
        masked = mask_raw_text(text)
        _, deletions, anomalies, _ = ENGINE.fix_text(masked)
        root = ENGINE.Node('#document', 'block')
        anomalies.extend(ENGINE._parse_range(masked, 0, len(masked), root))
        deletions.extend(nested_inline_deletions(root, text))
    except ENGINE.ParseError as exc:
        raise ValueError(str(exc)) from exc
    if anomalies:
        raise ValueError(f'HTML tokenizer anomalies: {anomalies[:5]}')
    merged = []
    for start, end in sorted(deletions):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    pieces, cursor, accepted = [], 0, []
    for start, end in merged:
        removed = text[start:end]
        if not removed or re.search(r'[^ \t\r\n]', removed):
            raise ValueError(f'non-whitespace deletion at offset {start}')
        pieces.append(text[cursor:start])
        cursor = end
        accepted.append((start, end))
    pieces.append(text[cursor:])
    return ''.join(pieces), accepted


def nested_inline_deletions(root, text):
    """Resolve text runs across nested inline edges, retaining source offsets.

    The SGML engine's immediate-child edge rules cannot see whitespace-only
    text next to another nested inline element. HTML has no generated text at
    this stage, so each block's visible inline run can be checked directly.
    Protected text supplies boundary characters but is never edited.
    """
    segments, deletions = [], []

    def flush():
        if not segments:
            return
        visible, positions, protected = [], [], []
        for start, end, locked in segments:
            visible.append(text[start:end])
            positions.extend(range(start, end))
            protected.extend([locked] * (end - start))
        run = ''.join(visible)
        for match in re.finditer(r'[ \t\r\n]+', run):
            start, end = match.span()
            if not start or end == len(run) or any(protected[start:end]):
                continue
            if not ENGINE.drop_space(run[start - 1], run[end]):
                continue
            first = previous = positions[start]
            for offset in positions[start + 1:end]:
                if offset != previous + 1:
                    deletions.append((first, previous + 1))
                    first = offset
                previous = offset
            deletions.append((first, previous + 1))
        segments.clear()

    def walk(node, locked=False):
        if node.name in ENGINE.VERBATIM_BLOCK:
            flush()
            return
        block = node.kind == 'block'
        if block:
            flush()
        locked = locked or node.name in ENGINE.VERBATIM_INLINE
        for child in node.children:
            if isinstance(child, ENGINE.Node):
                walk(child, locked)
            else:
                kind, start, end = child
                segments.append((start, end, locked or kind == 'verbatim-text'))
        if block:
            flush()

    walk(root)
    flush()
    return deletions


def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def prepare_directory(directory, before_dir=None):
    directory = Path(directory)
    if before_dir is not None:
        before_dir = Path(before_dir)
        if before_dir.exists():
            raise ValueError(f'before directory already exists: {before_dir}')
    rows = []
    for page in sorted(directory.rglob('*.html')):
        with page.open(encoding='utf-8', newline='') as stream:
            original = stream.read()
        normalized, deletions = normalize_html(original)
        relative = page.relative_to(directory)
        if before_dir is not None:
            saved = before_dir / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(page, saved)
        rows.append({
            'file': relative.as_posix(), 'before_sha256': sha256(original),
            'after_sha256': sha256(normalized), 'deletions': deletions,
            'removed_characters': sum(end - start for start, end in deletions),
        })
        if deletions:
            with page.open('w', encoding='utf-8', newline='') as stream:
                stream.write(normalized)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--before-dir', type=Path)
    args = parser.parse_args()
    try:
        rows = prepare_directory(args.directory, args.before_dir)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'Chinese HTML spacing failed: {exc}', file=sys.stderr)
        return 1
    if args.report:
        args.report.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    changed = sum(bool(row['deletions']) for row in rows)
    removed = sum(row['removed_characters'] for row in rows)
    print(f'Chinese HTML spacing: {len(rows)} pages checked; {changed} changed; {removed} whitespace characters removed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
