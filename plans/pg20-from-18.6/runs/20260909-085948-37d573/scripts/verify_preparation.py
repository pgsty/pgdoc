#!/usr/bin/env python3
"""Check frozen preparation evidence. Does not reset the translation target.

--check-draft asserts zh/20 is still the original PG18 inherited draft.
Omit it during formal translation/resume, when recorded target edits are expected.
--reconstruct applies the complete raw diff only to a new isolated audit copy.
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter,defaultdict
from pathlib import Path

csv.field_size_limit(32*1024*1024)
PLAN=Path(__file__).resolve().parents[1]
CFG=json.loads((PLAN/'RUN.json').read_text())
ROOT,STATE,REPORT=(Path(CFG[k]) for k in ('root','state','report'))
INITIAL=json.loads((STATE/'initial-state.json').read_text())


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def tree(p,skip_build=False):
    return {str(x.relative_to(p)):sha(x) for x in sorted(p.rglob('*')) if x.is_file() and (not skip_build or x.relative_to(p).parts[0] not in {'html','man1','man3','man7'})}


def tsv(p):return list(csv.DictReader(p.open(),delimiter='\t'))


def jsonl(p):return [json.loads(x) for x in p.open()]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-draft',action='store_true')
    parser.add_argument('--reconstruct',action='store_true')
    parser.add_argument('--write-report',action='store_true')
    args=parser.parse_args()
    results={};failures=[]
    def check(name,condition,detail=None):
        results[name]={'pass':bool(condition)}
        if detail is not None:results[name]['detail']=detail
        if not condition:failures.append(name)
    for name,record in INITIAL['inputs'].items():
        expected={k:v['sha256'] for k,v in record['files'].items()}
        check('frozen:'+name,tree(Path(record['frozen_path']))==expected)
        skip=name.startswith('zh/')
        check('live-reference:'+name,tree(Path(record['live_path']),skip)==expected)
    for name,records in INITIAL['legacy_source_hashes'].items():
        check('legacy-preserved:'+name,tree(ROOT/name,True)=={k:v['sha256'] for k,v in records.items()})
    for name,h in INITIAL['context_files'].items():
        # During formal translation the two build scripts can change by task.
        if name.startswith('bin/') and not args.check_draft:continue
        check('context-preserved:'+name,sha(ROOT/name)==h)
    target=json.loads((STATE/'target-source.json').read_text());src=Path(target['source_root'])
    head=subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD'],text=True).strip()
    check('pinned-source-commit',head==target['commit_sha'])
    tracked=json.loads((STATE/'upstream-pg20-files.json').read_text())
    drift=[p for p,h in tracked.items() if not (src/p).is_file() or sha(src/p)!=h]
    check('pinned-source-bytes',not drift,drift)
    check('source-20devel-declarations',all('20devel' in (src/name).read_text() for name in ['configure.ac','configure','meson.build']))
    check('en20-exact-import',tree(ROOT/'en/20')==tree(src/'doc/src/sgml'))
    if args.check_draft:
        expected={k:v['sha256'] for k,v in INITIAL['inheritance']['tree'].items()}
        check('zh20-inherited-draft',tree(ROOT/'zh/20')==expected)
    inv=tsv(REPORT/'inventory.tsv');stat=json.loads((REPORT/'statistics.json').read_text())
    counts=Counter(x['action'] for x in inv)
    check('inventory-old-equation',stat['old_files']==sum(counts[k] for k in ['unchanged','modified','deleted','type_changed']))
    check('inventory-new-equation',stat['new_files']==sum(counts[k] for k in ['unchanged','modified','added','type_changed']))
    check('inventory-union',len(inv)==len({x['path'] for x in inv})==stat['union_files'])
    oldtree,newtree=tree(STATE/'inputs/en/18.6'),tree(ROOT/'en/20')
    check('inventory-exact-hashes',all(x['old_sha256']==oldtree.get(x['path'],'') and x['new_sha256']==newtree.get(x['path'],'') for x in inv))
    hunks=tsv(REPORT/'hunks.tsv');units=jsonl(REPORT/'translation-units.jsonl')
    hu={h['hunk_id']:h for h in hunks};um={u['unit_id']:u for u in units}
    check('unique-hunk-unit-ids',len(hu)==len(hunks) and len(um)==len(units))
    check('hunk-count',len(hunks)==stat['raw_hunks'])
    inverse=defaultdict(set)
    for u in units:
        for h in u['hunk_ids']:inverse[h].add(u['unit_id'])
    check('bidirectional-hunk-unit-coverage',set(inverse)==set(hu) and all(inverse[h]==set(json.loads(row['unit_ids'])) for h,row in hu.items()))
    uncovered=[]
    for h,row in hu.items():
        for side,label in [('old','old_english'),('new','new_english')]:
            ranges=[]
            for uid in inverse[h]:
                ref=um[uid].get(label) or {}
                path=ref.get('path','')
                if path.endswith('/'+row['file']):ranges.append((ref['start_line'],ref['end_line']))
            for lo,hi in json.loads(row[f'{side}_changed_ranges']):
                if not any(a<=lo and b>=hi for a,b in ranges):uncovered.append([h,side,lo,hi])
    check('every-raw-changed-line-covered',not uncovered,uncovered[:20])
    bad_refs=[];cache={}
    for u in units:
        for field in ['old_english','new_english','pg18_chinese','historical_english','historical_chinese']:
            ref=u.get(field)
            if not ref or 'text' not in ref:continue
            path=ref['path']
            if path not in cache:cache[path]=Path(path).read_text()
            text=cache[path][ref['char_start']:ref['char_end']]
            if text!=ref['text'] or hashlib.sha256(text.encode()).hexdigest()!=ref['sha256']:bad_refs.append([u['unit_id'],field])
    check('exact-English-Chinese-span-references',not bad_refs,bad_refs[:20])
    tasks=tsv(PLAN/'TASKS.tsv');tm={t['task_id']:t for t in tasks}
    gu=jsonl(REPORT/'generated-translation-units.jsonl');gh=tsv(REPORT/'generated-hunks.tsv')
    all_units=set(um)|{u['unit_id'] for u in gu};ownership=Counter(uid for t in tasks for uid in json.loads(t['unit_ids']))
    check('task-unit-ownership-exactly-once',set(ownership)==all_units and all(v==1 for v in ownership.values()))
    check('all-generated-hunks-owned', {h for u in gu for h in u['hunk_ids']}=={h['hunk_id'] for h in gh})
    unknown=[(t['task_id'],d) for t in tasks for d in json.loads(t['dependencies']) if d not in tm]
    check('task-dependencies-exist',not unknown,unknown)
    seen,active=set(),set()
    def visit(t):
        if t in active:raise ValueError('task dependency cycle '+t)
        if t in seen:return
        active.add(t)
        for dep in json.loads(tm[t]['dependencies']):visit(dep)
        active.remove(t);seen.add(t)
    try:
        for tid in tm:visit(tid)
        check('task-dependency-DAG',True)
    except (KeyError,ValueError) as exc:check('task-dependency-DAG',False,str(exc))
    covered_files={path.removeprefix('zh/20/') for t in tasks for path in json.loads(t['target_files']) if path.startswith('zh/20/')}
    check('all-inventory-paths-have-tasks',{x['path'] for x in inv}<=covered_files,sorted({x['path'] for x in inv}-covered_files))
    # Reconstruct raw authored trees, an independent check of completeness.
    if args.reconstruct:
        out=Path(tempfile.mkdtemp(prefix='audit-reconstruction-',dir=STATE))
        shutil.copytree(STATE/'inputs/en/18.6',out,dirs_exist_ok=True)
        # BSD patch otherwise retains empty files even for /dev/null deletions.
        # The pinned target contains no authored empty files.
        proc=subprocess.run(['patch','-E','-p2','-t','-i',str(REPORT/'full.diff')],cwd=out,capture_output=True,text=True)
        (STATE/'raw-diff-reconstruction.log').write_text(proc.stdout+proc.stderr)
        check('full-diff-reconstructs-target',proc.returncode==0 and tree(out)==tree(ROOT/'en/20'),{'exit_code':proc.returncode,'reconstruction':str(out),'log':str(STATE/'raw-diff-reconstruction.log')})
    check('no-translation-claimed',all(u['status']=='prepared_not_applied' for u in units+gu))
    check('formal-materials-have-no-unfilled-source-placeholders',all(not re.search(r'待填 SHA|自行补文件列表|<FILE>|<SHA>|TODO_SHA', (PLAN/n).read_text()) for n in ['TRANSLATE-PG20.md','PLAN.md','BUILD-ADAPTATION.md']))
    result={'status':'PASS' if not failures else 'FAIL','checks':results,'failed_checks':failures,'counts':{'raw_files':len(inv),'raw_hunks':len(hunks),'raw_units':len(units),'generated_hunks':len(gh),'tasks':len(tasks)},'draft_checked':args.check_draft,'body_translation_performed':False,'html_pdf_builds_performed':False,'scope':'preparation completeness and provenance, not formal translation acceptance'}
    if args.write_report:(REPORT/'preparation-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'failed_checks':failures,'counts':result['counts'],'checks':len(results)},ensure_ascii=False,indent=2))
    if failures:raise SystemExit(1)


if __name__=='__main__':main()
