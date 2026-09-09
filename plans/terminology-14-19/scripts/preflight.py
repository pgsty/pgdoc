"""Read-only repository census and lexical discovery; NEVER edits documentation.

Counts include markup, comments and protected literals. They are search hints,
not a defect count, semantic alignment, or permission to replace a string.
"""
from pathlib import Path
from collections import Counter
from bisect import bisect_right
from datetime import datetime, timezone
import argparse
import csv
import hashlib
import json
import re
import subprocess

PACK = Path(__file__).resolve().parents[1]
GENERATED = {'version.sgml', 'pgdoccn-notes.sgml'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def tsv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter='\t'))


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True, check=True)
    return result.stdout.rstrip('\n')


def pattern(term, english=False):
    # Allow wrapping BETWEEN words. Do not rewrite input or infer synonyms.
    expr = r'\s+'.join(re.escape(p) for p in term.split())
    if english:
        expr = r'(?<![A-Za-z0-9_])' + expr + r'(?![A-Za-z0-9_])'
    return re.compile(expr, re.IGNORECASE if english else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=PACK.parents[1])
    parser.add_argument('--out', type=Path, required=True, help='A NEW output directory; existing directories are refused')
    args = parser.parse_args()
    root, out = args.repo.resolve(), args.out.resolve()
    if out.exists():
        raise SystemExit('Use a new --out directory; previous evidence must not be overwritten')
    manifest = load_json(PACK / 'refs/manifest.json')
    for item in manifest['files']:
        if sha(PACK / 'refs' / item['file']) != item['sha256']:
            raise SystemExit('Frozen reference changed: ' + item['file'])
    glossary = tsv(PACK / 'refs/glossary.tsv')
    rules = tsv(PACK / 'refs/glossary.rules.tsv')
    changes = tsv(PACK / 'refs/changes.tsv')
    assert len(glossary) == len(rules) == 631 and len(changes) == 68
    assert [r['English'] for r in glossary] == [r['English'] for r in rules]
    assert [int(r['原序号']) for r in rules] == list(range(1, 632))
    assert len({r['English'] for r in glossary}) == 631
    families = load_json(PACK / 'families.json')['families']
    ids = [term_id for family in families for term_id in family['term_ids']]
    assert len(ids) == len(set(ids)) == 68
    assert set(ids) == {int(r['原序号']) for r in changes}
    variants = load_json(PACK / 'search-variants.json')['terms']
    family_by_id = {term_id: f['id'] for f in families for term_id in f['term_ids']}
    specs = []
    for row in changes:
        term_id = int(row['原序号'])
        extra = variants.get(str(term_id), {})
        en = list(dict.fromkeys([row['原英文'], row['最终英文'], *extra.get('en', [])]))
        # Discovery is case-insensitive; avoid counting differently cased copies.
        en = list({v.casefold(): v for v in en}.values())
        old = [] if extra.get('skip_old_literal') else [row['原译']]
        specs.append({
            'id': term_id, 'row': row, 'extra': extra,
            'en': [(s, pattern(s, True)) for s in en],
            'old': [(s, pattern(s)) for s in old],
            'variant': [(s, pattern(s)) for s in extra.get('zh', []) if s != row['原译']],
            'new': pattern(row['最终中文']),
        })
    out.mkdir(parents=True)
    files, versions, matrix = [], [], []
    totals = Counter()
    with (out / 'candidate-hits.jsonl').open('w', encoding='utf-8') as hits_file:
        for major in range(14, 20):
            zh_dir = root / 'zh' / str(major)
            make_text = (zh_dir / 'Makefile').read_text(encoding='utf-8')
            match = re.search(r'^PG_VERSION\s*\??=\s*(\S+)', make_text, re.M)
            if not match:
                raise SystemExit(f'Cannot resolve PG_VERSION: {zh_dir}/Makefile')
            version = match.group(1)
            en_dir = root / 'en' / version
            if not (en_dir / 'postgres.sgml').is_file():
                raise SystemExit(f'Missing pinned English snapshot: {en_dir}')
            v = {'major': major, 'pg_version': version, 'zh_dir': str(zh_dir.relative_to(root)), 'en_dir': str(en_dir.relative_to(root)), 'makefile_sha256': sha(zh_dir / 'Makefile')}
            counters = {s['id']: {'en_source': 0, 'old_zh_literal': 0, 'extra_zh_variant': 0, 'new_zh_literal': 0} for s in specs}
            paths = {s['id']: {'en': set(), 'zh': set()} for s in specs}
            file_sets = {}
            for lang, directory in [('en', en_dir), ('zh', zh_dir)]:
                source_files = sorted(p for p in directory.rglob('*.sgml') if p.name not in GENERATED and not any(part in {'html', '.build', '.cache'} for part in p.relative_to(directory).parts))
                file_sets[lang] = {str(p.relative_to(directory)) for p in source_files}
                v[lang + '_sgml_files'] = len(source_files)
                for file in source_files:
                    data = file.read_bytes()
                    text = data.decode('utf-8')
                    lower = text.casefold()
                    rel = str(file.relative_to(root))
                    files.append({'major': major, 'lang': lang, 'path': rel, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
                    line_starts = [0] + [m.end() for m in re.finditer('\n', text)]
                    for spec in specs:
                        term_id = spec['id']
                        if lang == 'en':
                            forms = [('en_source', needle, regex) for needle, regex in spec['en']]
                            new_spans = []
                        else:
                            forms = [('old_zh_literal', needle, regex) for needle, regex in spec['old']]
                            forms += [('extra_zh_variant', needle, regex) for needle, regex in spec['variant']]
                            forms += [('new_zh_literal', spec['row']['最终中文'], spec['new'])]
                            new_spans = [(m.start(), m.end()) for m in spec['new'].finditer(text)]
                        # Merge overlapping discovery variants for a given role.
                        by_role = {}
                        for role, needle, regex in forms:
                            first_word = needle.split()[0]
                            if (first_word.casefold() if lang == 'en' else first_word) not in (lower if lang == 'en' else text):
                                continue
                            for m in regex.finditer(text):
                                if role == 'old_zh_literal' and spec['row']['原译'] != spec['row']['最终中文'] and any(a <= m.start() and m.end() <= b for a, b in new_spans):
                                    continue
                                by_role.setdefault(role, set()).add((m.start(), m.end()))
                        for role, spans in by_role.items():
                            # Overlapping singular/plural patterns are one candidate.
                            merged = []
                            for start, end in sorted(spans):
                                if merged and start < merged[-1][1]:
                                    merged[-1] = (merged[-1][0], max(merged[-1][1], end))
                                else:
                                    merged.append((start, end))
                            lines = sorted({bisect_right(line_starts, start) for start, _ in merged})
                            record = {'term_id': term_id, 'major': major, 'lang': lang, 'role': role, 'file': rel, 'matches': len(merged), 'lines': lines, 'samples': [text[max(0, a-65):min(len(text), b+100)].replace('\n', ' ') for a,b in merged[:3]], 'classification': 'LEXICAL_ONLY_UNREVIEWED'}
                            hits_file.write(json.dumps(record, ensure_ascii=False) + '\n')
                            counters[term_id][role] += len(merged)
                            paths[term_id][lang].add(rel)
                            totals[role] += len(merged)
            v['zh_only_sgml'] = sorted(file_sets['zh'] - file_sets['en'])
            v['en_only_sgml'] = sorted(file_sets['en'] - file_sets['zh'])
            versions.append(v)
            for spec in specs:
                term_id = spec['id']
                matrix.append({'term_id': term_id, 'family': family_by_id[term_id], 'major': major, 'english': spec['row']['最终英文'], 'old_chinese': spec['row']['原译'], 'final_chinese': spec['row']['最终中文'], **counters[term_id], 'en_files': sorted(paths[term_id]['en']), 'zh_files': sorted(paths[term_id]['zh']), 'status': 'PENDING_CONTEXT_REVIEW', 'old_literal_skipped': spec['extra'].get('skip_old_literal', False)})
    assert len(matrix) == 68 * 6
    config = {str(p.relative_to(root)): sha(p) for p in [root/'AGENTS.md', root/'Makefile', root/'tmp/ref/glossary.tsv', root/'tmp/ref/style.md', root/'tmp/ref/exclude.tsv'] if p.exists()}
    links = {str(p.relative_to(root)): str(p.readlink()) for p in [root/'en/current', root/'zh/current', root/'en/19'] if p.is_symlink()}
    summary = {'created_utc': datetime.now(timezone.utc).isoformat(), 'repo': str(root), 'git_head': git(root, 'rev-parse', 'HEAD'), 'git_branch': git(root, 'branch', '--show-current'), 'git_status': git(root, 'status', '--short'), 'versions': versions, 'source_files': len(files), 'scope_terms': 68, 'term_version_cells': len(matrix), 'lexical_totals': dict(totals), 'config_sha256': config, 'symlinks': links, 'limitations': ['Lexical matches include protected markup, code, comments and unrelated senses; they are not confirmed edits.', 'This scan is not a semantic alignment or a complete residual audit. Inline markup, entities, additional paraphrases and inflections can conceal terms.', 'No-hit cells remain PENDING_CONTEXT_REVIEW; absent is not inferred.', 'Old substrings wholly inside the same term’s final Chinese spelling are omitted; English-only changes retain both old/new Chinese presence counts.', 'Aliases and morphology hints are discovery aids only; reviewers must inspect refs/aliases.tsv and corresponding version English.']}
    write_json(out / 'inventory.json', summary)
    write_json(out / 'file-hashes.json', files)
    write_json(out / 'candidate-matrix.json', matrix)
    lines = ['# 开工前只读盘点', '', '以下为本地快照与字面候选，尚未校准正文。候选数量不能作为应修改数量。', '', '| 大版本 | 英文快照 | 中文目录 | 英文 SGML | 中文 SGML |', '|---|---|---|---:|---:|']
    for v in versions:
        lines.append(f'| {v["major"]} | {v["en_dir"]} | {v["zh_dir"]} | {v["en_sgml_files"]} | {v["zh_sgml_files"]} |')
    lines += ['', f'共 {len(files)} 个中英文 SGML 文件，68 个目标词条 × 6 个大版本 = 408 个待核实的词条/版本单元。实际执行还要把每个单元展开成逐处段落台账。', '', '## 各词族字面命中', '', '| 词族 | 词条数 | 原译字面命中 | 附加变体命中 | 英文检索命中 |', '|---|---:|---:|---:|---:|']
    for f in families:
        rows = [r for r in matrix if r['family'] == f['id']]
        lines.append(f'| {f["id"]} {f["name"]} | {len(f["term_ids"])} | {sum(r["old_zh_literal"] for r in rows)} | {sum(r["extra_zh_variant"] for r in rows)} | {sum(r["en_source"] for r in rows)} |')
    lines += ['', '## 路径差异', '']
    for v in versions:
        lines.append(f'- PG{v["major"]}：中文独有 {v["zh_only_sgml"]}；英文独有 {v["en_only_sgml"]}。不得仅凭同路径缺失认定概念不存在。')
    lines += ['', '限制：未解析 SGML 可翻译节点；保护区、同形异义、不同词条重叠、旧词已包含在新译中的情形须复核。主（master）不做单字旧译扫描，改从英文定位。零命中不等于不适用。', '', '顶层 Makefile 默认批量版本只有 14—18；正式验收须显式覆盖 19。en/current 当前指向 18.3，不能用作本次英文基准。', '']
    (out / 'summary.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps({'versions': len(versions), 'files': len(files), 'term_version_cells': len(matrix), 'lexical_totals': dict(totals), 'out': str(out)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
