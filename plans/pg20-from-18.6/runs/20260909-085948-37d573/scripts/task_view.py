#!/usr/bin/env python3
"""Show a prepared task or unit; this command never translates or edits files."""
import argparse
import csv
import json
from pathlib import Path
csv.field_size_limit(32*1024*1024)
plan=Path(__file__).resolve().parents[1]
cfg=json.loads((plan/'RUN.json').read_text())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('task_id',nargs='?')
parser.add_argument('--unit')
args=parser.parse_args()
if not args.task_id and not args.unit:parser.error('provide a task ID or --unit UNIT_ID')
task=None
if args.task_id:
    task=next((x for x in csv.DictReader((plan/'TASKS.tsv').open(),delimiter='\t') if x['task_id']==args.task_id),None)
    if task is None:parser.error('unknown task ID')
    for field in ['dependencies','target_files','actions','hunk_ids','unit_ids']:
        task[field]=json.loads(task[field])
needed={args.unit} if args.unit else set(task['unit_ids'])
found=[]
for name in ['translation-units.jsonl','generated-translation-units.jsonl']:
    for line in (Path(cfg['report'])/name).open():
        unit=json.loads(line)
        if unit['unit_id'] in needed:found.append(unit)
if {x['unit_id'] for x in found}!=needed:parser.error('unit reference is missing')
print(json.dumps({'task':task,'units':found},ensure_ascii=False,indent=2))
