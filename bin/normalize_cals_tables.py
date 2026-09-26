#!/usr/bin/env python3
"""Adapt legacy DocBook markup in osx-generated postgres.xml (stdin → stdout).

PG 6.x – 7.x sources carry 1998-era DocBook tables whose ``tgroup cols``
disagrees with the per-row ``<entry>`` counts (jade-era renderers tolerated
that; FOP rejects the resulting XSL-FO).  For every tgroup:

* if the widest row has more entries than ``cols``, raise ``cols``;
* if a row has fewer entries than ``cols`` (ragged trailing cells), pad with
  empty ``<entry></entry>``;
* tgroups using spans (``namest``/``nameend``/``morerows``/``spanname``) are
  left untouched and reported on stderr — spans need human judgement.

Every change is reported to stderr so build logs carry the audit trail.
Legacy bookbiblio entries use the modern biblioentry template; figure xrefs
whose endterm points to the entire figure use the normal numbered reference
instead of copying the image into the referring paragraph. Source SGML is
never modified.
"""
import re
import sys
from pathlib import Path

TG = re.compile(r'(<tgroup\b[^>]*cols=")(\d+)("[^>]*>)(.*?)(</tgroup>)', re.S)
ROW = re.compile(r'(<row\b[^>]*>)(.*?)(</row>)', re.S)
ENTRY = re.compile(r'<entry\b[^>]*>')


def normalize_legacy_markup(data, base_dir=None):
    base_dir = Path(base_dir) if base_dir is not None else Path.cwd()

    def resolve_image(match):
        tag = match.group(0)
        ref = re.search(r'\bfileref="([^"]+)"', tag)
        if not ref or '://' in ref[1]:
            return tag
        original = base_dir / ref[1]
        if original.exists() or original.suffix:
            return tag
        candidates = [original.with_suffix(ext) for ext in
                      ('.gif', '.png', '.jpg', '.jpeg', '.svg')
                      if original.with_suffix(ext).is_file()]
        if len(candidates) == 1:
            replacement = ref[1] + candidates[0].suffix
            print(f'normalize_cals_tables: resolved image {ref[1]} -> {replacement}',
                  file=sys.stderr)
            return tag[:ref.start(1)] + replacement + tag[ref.end(1):]
        return tag

    data = re.sub(r'<(?:graphic|imagedata)\b[^>]*>', resolve_image, data)
    figures = set(re.findall(r'<figure\b[^>]*\bid="([^"]+)"', data))

    def fix_xref(match):
        tag = match.group(0)
        link = re.search(r'\blinkend="([^"]+)"', tag)
        end = re.search(r'\s+endterm="([^"]+)"', tag)
        if link and end and link[1] == end[1] and link[1] in figures:
            print(f'normalize_cals_tables: use numbered figure xref {link[1]}',
                  file=sys.stderr)
            return tag[:end.start()] + tag[end.end():]
        return tag

    data = re.sub(r'<xref\b[^>]*>', fix_xref, data)
    data, count = re.subn(r'(<\/?)(bookbiblio)(?=[\s>])', r'\1biblioentry', data)
    if count:
        print(f'normalize_cals_tables: adapted {count // 2} bookbiblio entries',
              file=sys.stderr)
    return data


def fix_tgroup(m):
    head, cols_s, tail_head, body, tail = m.groups()
    cols = int(cols_s)
    if re.search(r'\b(namest|nameend|morerows|spanname)=', body):
        print('normalize_cals_tables: skip tgroup with spans'
              f' (cols={cols})', file=sys.stderr)
        return m.group(0)
    counts = []
    new_body = []
    for row in ROW.finditer(body):
        n = len(ENTRY.findall(row.group(2)))
        counts.append(n)
        new_body.append(row.group(0))
    if not counts:
        return m.group(0)
    widest = max(counts)
    if widest < cols:
        widest = cols
    changed = False
    if widest != cols:
        changed = True
    rebuilt = []
    for row, n in zip(ROW.finditer(body), counts):
        if n < widest:
            pad = '<entry></entry>' * (widest - n)
            rebuilt.append(row.group(1) + row.group(2) + pad + row.group(3))
            changed = True
        else:
            rebuilt.append(row.group(0))
    if not changed:
        return m.group(0)
    print(f'normalize_cals_tables: tgroup cols {cols} -> {widest},'
          f' row entry counts {sorted(set(counts))}', file=sys.stderr)
    return head + str(widest) + tail_head + body_replace(body, rebuilt) + tail


def body_replace(body, rebuilt_rows):
    out, pos = [], 0
    for row, new in zip(ROW.finditer(body), rebuilt_rows):
        out.append(body[pos:row.start()])
        out.append(new)
        pos = row.end()
    out.append(body[pos:])
    return ''.join(out)


def main():
    data = normalize_legacy_markup(sys.stdin.read())
    # 旧源的 <figure float="1"> 会让 docbook-xsl 生成 fo:float；FOP 不支持
    # float（渲染期 area-null NPE）。这个 jade 时代的排版暗示对 PDF 无意义，剥掉。
    data = re.sub(r'(<(?:figure|informalfigure|table|informaltable|equation)\b[^>]*?)\s+float="1"', r'\1', data)
    sys.stdout.write(TG.sub(fix_tgroup, data))


if __name__ == '__main__':
    main()
