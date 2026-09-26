#!/usr/bin/env python3
"""Build a file-level and content-level diff workspace between two English doc trees.

Usage:
  diff_en_docs.py FROM TO [options]

  FROM / TO       versions under en/ (e.g. 16.14 16.15), or explicit paths
  --out DIR       output directory (default: en/diff/<FROM>-vs-<TO>)
  --context N     unified diff context lines (default 3)

Output layout (mirrors the historical en/diff/ convention):
  README.md            overview: totals, per-status counts, provenance
  SOURCE.json          both sides' manifest digests + generator invocation
  files-added.txt      paths present only in TO
  files-removed.txt    paths present only in FROM
  files-renamed.tsv    old-path <TAB> new-path (identical content)
  files-changed.txt    paths with different content in both
  stats.tsv           status <TAB> path <TAB> +lines <TAB> -lines ('binary' if not text)
  full.diff           one combined unified diff, headers a/<FROM>/<path> b/<TO>/<path>

The script only writes into --out; it never touches the source trees.
"""
import argparse
import datetime
import difflib
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def resolve_side(arg):
    for candidate in (Path(arg), ROOT / 'en' / arg):
        if candidate.is_dir():
            return candidate.resolve()
    sys.exit(f'cannot resolve version tree: {arg} (looked for en/{arg})')


def inventory(tree):
    result = {}
    for p in sorted(tree.rglob('*')):
        rel = p.relative_to(tree).as_posix()
        if p.is_symlink():
            result[rel] = ('symlink', os.readlink(p).encode())
        elif p.is_file():
            result[rel] = ('file', p.read_bytes())
        # empty directories are not tracked (SGML trees do not rely on them)
    return result


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def is_text(data):
    return b'\x00' not in data


def split_lines(data):
    # surrogateescape keeps arbitrary bytes intact through diff and back
    return data.decode('utf-8', 'surrogateescape').splitlines(keepends=True)


def unified(a_bytes, b_bytes, label_a, label_b, context):
    diff = difflib.unified_diff(
        split_lines(a_bytes), split_lines(b_bytes),
        fromfile=label_a, tofile=label_b, n=context, lineterm='\n')
    text = ''.join(diff)
    plus = minus = 0
    for line in text.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            plus += 1
        elif line.startswith('-') and not line.startswith('---'):
            minus += 1
    return text.encode('utf-8', 'surrogateescape'), plus, minus


def side_provenance(version, tree):
    files = {}
    nbytes = nsgml = 0
    for p in sorted(tree.rglob('*')):
        if p.is_symlink() or not p.is_file():
            continue
        rel = p.relative_to(tree).as_posix()
        files[rel] = sha256(p.read_bytes())
        nbytes += p.stat().st_size
        nsgml += p.suffix == '.sgml'
    manifest = hashlib.sha256(
        '\n'.join(f'{k} {v}' for k, v in sorted(files.items())).encode()).hexdigest()
    archive_sha = None
    sources = ROOT / 'en/SOURCES.json'
    if sources.is_file():
        try:
            for e in json.loads(sources.read_text()).get('entries', []):
                if e.get('version') == version:
                    archive_sha = e.get('archive_sha256')
                    break
        except json.JSONDecodeError:
            pass
    return {'version': version, 'doc_dir': str(tree.relative_to(ROOT)),
            'files': len(files), 'sgml_files': nsgml, 'bytes': nbytes,
            'manifest_sha256': manifest, 'archive_sha256': archive_sha}


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('from_version')
    parser.add_argument('to_version')
    parser.add_argument('--out')
    parser.add_argument('--context', type=int, default=3)
    args = parser.parse_args()

    tree_a = resolve_side(args.from_version)
    tree_b = resolve_side(args.to_version)
    name_a = args.from_version if not args.from_version.startswith(('/', '.')) \
        else tree_a.name
    name_b = args.to_version if not args.to_version.startswith(('/', '.')) \
        else tree_b.name
    out = Path(args.out).resolve() if args.out \
        else ROOT / 'en/diff' / f'{name_a}-vs-{name_b}'
    if out.exists() and any(out.iterdir()):
        sys.exit(f'{out} already exists and is not empty; remove it or pass --out')
    out.mkdir(parents=True)

    inv_a, inv_b = inventory(tree_a), inventory(tree_b)
    common = sorted(set(inv_a) & set(inv_b))
    removed = sorted(set(inv_a) - set(inv_b))
    added = sorted(set(inv_b) - set(inv_a))

    # rename detection: identical content hash, prefer same basename
    renames = []
    by_hash = {}
    for path in added:
        by_hash.setdefault(inv_b[path][1], []).append(path)
    remaining_removed = []
    for old in removed:
        kind, data = inv_a[old]
        candidates = by_hash.get(data, [])
        match = next((c for c in candidates if Path(c).name == Path(old).name), None) \
            or (candidates[0] if candidates else None)
        if match:
            renames.append((old, match))
            candidates.remove(match)
            if not candidates:
                by_hash.pop(data, None)
        else:
            remaining_removed.append(old)
    removed = [p for p in remaining_removed if p]
    renamed_new = {new for _, new in renames}
    added = [p for p in added if p not in renamed_new]

    changed = [p for p in common if inv_a[p] != inv_b[p]]
    unchanged = len(common) - len(changed)

    plus_total = minus_total = 0
    stats_rows = []
    diff_chunks = []

    def emit(status, path, a_bytes, b_bytes):
        nonlocal plus_total, minus_total
        la = f'a/{name_a}/{path}'
        lb = f'b/{name_b}/{path}'
        if not (is_text(a_bytes) and is_text(b_bytes)):
            stats_rows.append((status, path, 'binary', 'binary'))
            return
        chunk, plus, minus = unified(a_bytes, b_bytes, la, lb, args.context)
        diff_chunks.append(chunk)
        plus_total += plus
        minus_total += minus
        stats_rows.append((status, path, str(plus), str(minus)))

    for old, new in renames:
        stats_rows.append(('renamed', new, '0', '0'))
    for path in added:
        emit('added', path, b'', inv_b[path][1])
    for path in removed:
        emit('removed', path, inv_a[path][1], b'')
    for path in changed:
        emit('changed', path, inv_a[path][1], inv_b[path][1])

    (out / 'files-added.txt').write_text('\n'.join(added) + ('\n' if added else ''))
    (out / 'files-removed.txt').write_text('\n'.join(removed) + ('\n' if removed else ''))
    (out / 'files-changed.txt').write_text('\n'.join(changed) + ('\n' if changed else ''))
    (out / 'files-renamed.tsv').write_text(
        '\n'.join(f'{o}\t{n}' for o, n in renames) + ('\n' if renames else ''))
    with open(out / 'stats.tsv', 'w') as f:
        f.write('status\tpath\tplus_lines\tminus_lines\n')
        for row in stats_rows:
            f.write('\t'.join(row) + '\n')
    with open(out / 'full.diff', 'wb') as f:
        for chunk in diff_chunks:
            f.write(chunk)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    prov_a = side_provenance(name_a, tree_a)
    prov_b = side_provenance(name_b, tree_b)
    (out / 'SOURCE.json').write_text(json.dumps({
        'generated_at_utc': now,
        'generated_by': f'bin/diff_en_docs.py {name_a} {name_b} --context {args.context}',
        'from': prov_a, 'to': prov_b,
    }, ensure_ascii=False, indent=1) + '\n')

    (out / 'README.md').write_text(f'''# {name_a} vs {name_b} 英文文档差异

- 生成时间（UTC）：{now}
- 生成命令：`bin/diff_en_docs.py {name_a} {name_b} --context {args.context}`

## 概览

| 指标 | 数量 |
| --- | ---: |
| FROM 侧文件 | {prov_a['files']}（{name_a}） |
| TO 侧文件 | {prov_b['files']}（{name_b}） |
| 未变化 | {unchanged} |
| 内容修改 | {len(changed)} |
| 新增 | {len(added)} |
| 删除 | {len(removed)} |
| 更名（内容相同） | {len(renames)} |
| 内容行变化 | +{plus_total} / -{minus_total}（不含更名） |

## 文件级

- 新增清单：`files-added.txt`；删除清单：`files-removed.txt`
- 更名对照：`files-renamed.tsv`（old<TAB>new，内容未变）
- 修改清单：`files-changed.txt`；逐文件 ± 行数：`stats.tsv`（非文本文件标记 `binary`）

## 内容级

`full.diff` 为统一格式完整差异，路径标注 `a/{name_a}/<相对路径>` 与 `b/{name_b}/<相对路径>`。

## 来源校验

| 侧 | 目录 | 文件数 | 字节数 | 清单 SHA256 | 归档 SHA256 |
| --- | --- | ---: | ---: | --- | --- |
| FROM | `{prov_a['doc_dir']}` | {prov_a['files']} | {prov_a['bytes']} | `{prov_a['manifest_sha256']}` | `{prov_a['archive_sha256']}` |
| TO | `{prov_b['doc_dir']}` | {prov_b['files']} | {prov_b['bytes']} | `{prov_b['manifest_sha256']}` | `{prov_b['archive_sha256']}` |

逐文件 SHA256 与生成参数见 `SOURCE.json`；两侧归档校验和取自 `en/SOURCES.json`（未登记则为空）。
''')

    print(f'{name_a} vs {name_b}: unchanged={unchanged} changed={len(changed)} '
          f'added={len(added)} removed={len(removed)} renamed={len(renames)} '
          f'lines=+{plus_total}/-{minus_total}')
    print(f'output: {out}')


if __name__ == '__main__':
    main()
