#!/usr/bin/env python3
"""Normalize legacy CALS tables in osx-generated postgres.xml (stdin → stdout).

PG 6.x – 7.x sources carry 1998-era DocBook tables whose ``tgroup cols``
disagrees with the per-row ``<entry>`` counts (jade-era renderers tolerated
that; FOP rejects the resulting XSL-FO).  For every tgroup:

* if the widest row has more entries than ``cols``, raise ``cols``;
* if a row has fewer entries than ``cols`` (ragged trailing cells), pad with
  empty ``<entry></entry>``;
* tgroups using spans (``namest``/``nameend``/``morerows``/``spanname``) are
  left untouched and reported on stderr — spans need human judgement.

Every change is reported to stderr so build logs carry the audit trail.
"""
import re
import sys

TG = re.compile(r'(<tgroup\b[^>]*cols=")(\d+)("[^>]*>)(.*?)(</tgroup>)', re.S)
ROW = re.compile(r'(<row\b[^>]*>)(.*?)(</row>)', re.S)
ENTRY = re.compile(r'<entry\b[^>]*>')


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
    data = sys.stdin.read()
    # 旧源的 <figure float="1"> 会让 docbook-xsl 生成 fo:float；FOP 不支持
    # float（渲染期 area-null NPE）。这个 jade 时代的排版暗示对 PDF 无意义，剥掉。
    data = re.sub(r'(<(?:figure|informalfigure|table|informaltable|equation)\b[^>]*?)\s+float="1"', r'\1', data)
    sys.stdout.write(TG.sub(fix_tgroup, data))


if __name__ == '__main__':
    main()
