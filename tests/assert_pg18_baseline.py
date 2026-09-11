#!/usr/bin/env python3
"""Integration assertions for the UNFIXED 738d5de PG18 baseline report only."""
import json
from pathlib import Path
import sys


def main(directory):
    root = Path(directory)
    findings = json.loads((root / 'findings.json').read_text())
    tables = json.loads((root / 'tables.json').read_text())
    coverage = json.loads((root / 'coverage.json').read_text())
    assert coverage['en_complete'] and coverage['zh_complete']
    assert coverage['exit_code'] == 1
    assert any(f['code'] == 'missing_id' and f['details']['id'] == 'functions-sqljson-misc' for f in findings)
    table = next(t for t in tables if t['en']['id'] == 'functions-aggregate-table')
    assert table['en_shape']['row_groups']['tbody'] == 27
    assert table['zh_shape']['row_groups']['tbody'] == 20
    expected = {'any_value', 'json_agg_strict', 'jsonb_agg_strict', 'json_arrayagg',
                'json_objectagg', 'json_object_agg_strict', 'jsonb_object_agg_strict',
                'json_object_agg_unique', 'jsonb_object_agg_unique',
                'json_object_agg_unique_strict', 'jsonb_object_agg_unique_strict'}
    assert set(table['function_delta']['missing']) == expected
    facts = [f for f in findings if f['code'] == 'boolean_fact' and
             f['details']['table_id'] == 'functions-aggregate-table']
    assert len(facts) == 3
    assert sum('array_agg' in f['details']['row_en']['context'] for f in facts) == 2
    assert sum('string_agg' in f['details']['row_en']['context'] for f in facts) == 1
    print('PG18 known cases verified: missing SQL/JSON table; 7 rows / 11 function names; 3 Yes/No mismatches.')


if __name__ == '__main__':
    main(sys.argv[1])
