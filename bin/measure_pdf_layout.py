#!/usr/bin/env python3
"""Use FOP's actual block heights to keep units that fit on one body page.

Temporary probe IDs never enter the final FO. No text/font/link is changed.
The first layout permits code/rows to split for measurement; the final layout
keeps fitting examples and rows, and leaves oversized units breakable.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

FO = '{http://www.w3.org/1999/XSL/Format}'
KEEP = 'keep-together.within-column'
PREVIOUS = 'keep-with-previous.within-column'
PROSE_CONTROLS = str.maketrans('', '', '\u200b\u200c\u200d\ufeff')


def _prose_string(text):
    # Layout break controls have no visible width or punctuation. Ignore them
    # for prose recognition while preserving every character in the actual FO.
    return (text or '').translate(PROSE_CONTROLS)


def _prose_text(node):
    """Ignore comments, processing instructions and out-of-line footnotes."""
    if not isinstance(node.tag, str) or node.tag in (FO+'footnote', FO+'footnote-body'):
        return ''
    return _prose_string((node.text or '') + ''.join(_prose_text(c) + (c.tail or '') for c in node))


def _is_prose(node):
    if node.tag != FO+'block' or node.get('white-space-treatment') == 'preserve':
        return False
    if node.get('orphans') and node.get('widows'):
        return True
    # Older DocBook styles omit explicit widow/orphan properties on paragraphs.
    # Their normal paragraph spacing is still present. Compact function-table
    # paragraphs instead use a fixed left indent. Require direct inline prose
    # as well, so equally styled definition/list wrappers are excluded.
    compact_function_paragraph = node.get('margin-left') == '4em' and node.get('text-align') == 'left'
    if node.get('space-after.optimum') != '1em' and not compact_function_paragraph:
        return False
    text = (node.text or '') + ''.join(
        ('' if c.tag in (FO+'block', FO+'table', FO+'list-block') else _prose_text(c))
        + (c.tail or '') for c in node)
    return bool(_prose_string(text).strip())


def _trailing_prose(node):
    text = node.text or ''
    boundary = None
    for child in node:
        if child.tag in (FO+'block', FO+'table', FO+'list-block') and _prose_text(child).strip():
            text = child.tail or ''
            boundary = child
        else:
            text += _prose_text(child) + (child.tail or '')
    return _prose_string(text).strip(), boundary


def _starts_with_display(node):
    """Let a nested code/table/list own its introduction through plain wrappers."""
    if _prose_string(node.text).strip():
        return False
    for child in node:
        if _prose_text(child).strip():
            if child.tag in (FO+'table', FO+'list-block') or child.get('white-space-treatment') == 'preserve':
                return True
            return child.tag == FO+'block' and _starts_with_display(child)
        if _prose_string(child.tail).strip():
            return False
    return False


def _lead_ins(nodes, parents, body_nodes):
    """Find explicit prose introductions without changing the FO structure."""
    indices = {n: i for i, n in enumerate(nodes)}
    links = [];bindings = set()
    contexts = {}

    def context(parent, cursor):
        # Build sibling context once. Flat indexes can contain thousands of
        # blocks; rescanning every earlier sibling for each block is quadratic.
        if parent not in contexts:
            prefix = _prose_string(parent.text)
            last_block = None;anchors = [];rows = {}
            for child in parent:
                rows[child] = prefix, last_block, tuple(anchors)
                if child.tag in (FO+'block', FO+'table', FO+'list-block'):
                    if _prose_text(child).strip():
                        last_block = child;anchors = [];prefix = _prose_string(child.tail)
                    else:
                        anchors.append(child);prefix += _prose_string(child.tail)
                else:
                    prefix += _prose_text(child) + _prose_string(child.tail)
            contexts[parent] = rows
        return contexts[parent][cursor]

    def add(display, kind, binding, intro, intro_kind, boundary=None):
        key = indices[binding], indices[intro]
        if key in bindings:
            return
        bindings.add(key)
        link = {'display': indices[display], 'kind': kind, 'binding': indices[binding],
                'intro': indices[intro], 'intro_kind': intro_kind}
        if boundary is not None:
            link['tail_after'] = indices[boundary]
        links.append(link)
        return link

    for display in nodes:
        kind = ('code' if display.tag == FO+'block' and display.get('white-space-treatment') == 'preserve'
                else 'table' if display.tag == FO+'table'
                else 'list' if display.tag == FO+'list-block'
                else 'continuation' if display.tag == FO+'block' and _prose_text(display).strip()
                     and not _starts_with_display(display) else None)
        if kind is None or display not in body_nodes:
            continue
        cursor = display
        while cursor in parents:
            parent = parents[cursor]
            if parent.tag not in (FO+'block', FO+'flow') or parent.get('white-space-treatment') == 'preserve':
                break
            prefix, last_block, anchors = context(parent, cursor)
            if prefix.strip().endswith(('：', ':')) and _is_prose(parent):
                link = add(display, kind, cursor, parent, 'parent')
                if link is not None and last_block is not None:
                    link['prefix_after'] = indices[last_block]
                break
            if not prefix.strip() and last_block is not None:
                text, boundary = _trailing_prose(last_block)
                if _is_prose(last_block) and text.endswith(('：', ':')):
                    add(display, kind, anchors[0] if anchors else cursor, last_block,
                        'sibling-tail' if boundary is not None else 'sibling', boundary)
                break
            if prefix.strip() or last_block is not None or parent.tag == FO+'flow':
                break
            cursor = parent
    return links


def parse(path):
    for _, (prefix, uri) in ET.iterparse(path, events=('start-ns',)):
        if not prefix.startswith('ns'):
            ET.register_namespace(prefix, uri)
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    return ET.parse(path, parser=parser)


def probe(source, output, manifest):
    tree = parse(source)
    nodes = list(tree.iter())
    indices = {n: i for i, n in enumerate(nodes)}
    parents = {c: p for p in nodes for c in p}
    body_nodes = {n for flow in tree.iter(FO+'flow')
                  if flow.get('flow-name') == 'xsl-region-body' for n in flow.iter()}
    leads = _lead_ins(nodes, parents, body_nodes)
    lead_nodes = {link['intro'] for link in leads}
    display_nodes = {link['display'] for link in leads if link['kind'] != 'code'}
    tail_nodes = {link[name] for link in leads for name in ('tail_after', 'prefix_after') if name in link}
    first_list_parts = {}
    first_prose_nodes = set()
    for link in leads:
        display = nodes[link['display']]
        nodes[link['binding']].set(PREVIOUS, 'auto')
        if link['kind'] == 'table':
            body = display.find(FO+'table-body')
            header = display.find(FO+'table-header')
            link['first_row'] = indices[body.find(FO+'table-row')]
            link['header_rows'] = [indices[n] for n in header if n.tag == FO+'table-row'] if header is not None else []
        elif link['kind'] == 'list':
            item = display.find(FO+'list-item')
            link['first_item'] = indices[item]
            item.set(KEEP, '10')
            for part in item:
                if part.tag in (FO+'list-item-body', FO+'list-item-label'):
                    first_list_parts[indices[part]] = indices[item]
        elif link['kind'] == 'continuation':
            display.set(KEEP, 'auto')
            first = next((n for n in display.iter(FO+'block')
                          if _is_prose(n)
                          and n.get('keep-with-next.within-column') != 'always'
                          and _prose_text(n).strip()), None)
            if first is not None:
                link['first_prose'] = indices[first]
                first_prose_nodes.add(indices[first])
                first.set(KEEP, 'auto')
                code = next((n for n in first.iter(FO+'block')
                             if n.get('white-space-treatment') == 'preserve'), None)
                if code is not None:
                    link['first_code'] = indices[code]
    used_ids = {n.get('id') for n in nodes if n.get('id')}
    records = []
    for i, node in enumerate(nodes):
        if node not in body_nodes or not isinstance(node.tag, str):
            continue
        if node.tag == FO+'table-row':
            node.set(KEEP, '10')
        kind = None
        target = i
        if node.tag == FO+'table-cell' and parents[node].tag == FO+'table-row':
            kind, target = 'cell', indices[parents[node]]
        elif node.tag == FO+'list-item-body':
            item = parents[node]
            siblings = [n for n in parents[item] if n.tag == FO+'list-item']
            if len(siblings) > 1 and siblings[-1] is item:
                kind, target = 'ending-list-item', indices[item]
            elif i in first_list_parts:
                kind, target = 'lead-in-list-item', first_list_parts[i]
        elif i in first_list_parts:
            kind, target = 'lead-in-list-item', first_list_parts[i]
        elif node.tag == FO+'block':
            if node.get('role') == 'pgdoc-compact-ending':
                kind = 'ending-section'
            elif node.get('role') == 'pgdoc-compact-ending-paragraph':
                kind = 'ending-paragraph'
            elif node.get('role') == 'pgdoc-reference-synopsis':
                kind = 'synopsis'
            elif node.get('white-space-treatment') == 'preserve':
                kind = 'code'
                node.set(KEEP, '10')
            elif node.get('role') == 'pgdoc-table-footnote' or parents[node].tag == FO+'footnote-body':
                kind = 'footnote'
                node.set(KEEP, '10')
            elif _is_prose(node) and any(
                    c.tag == FO+'block' and c.get('white-space-treatment') == 'preserve'
                    for c in node):
                kind = 'example-paragraph'
        if kind is None and i in lead_nodes:
            kind = 'lead-in-prose'
        if kind is None and i in display_nodes:
            kind = 'lead-in-display'
        if kind is None and i in tail_nodes:
            kind = 'lead-in-tail-boundary'
        if kind is None and i in first_prose_nodes:
            kind = 'lead-in-first-prose'
        if kind is None:
            continue
        # Every attribute calibrated below must have a canonical probe value.
        # Otherwise a keep added by the first pass changes fragmentation and
        # measured height on the second pass, even though text is unchanged.
        if kind in ('ending-section', 'ending-paragraph', 'ending-list-item'):
            nodes[target].set(KEEP, 'auto')
            nodes[target].set('keep-with-previous.within-column', 'auto')
        elif kind == 'example-paragraph':
            node.set(KEEP, '10')
        elif kind == 'synopsis':
            node.set(KEEP, 'auto')
        key = node.get('id')
        if key is None:
            key = f'pgdoc-measure-{i}'
            if key in used_ids:
                raise ValueError(f'probe ID collision: {key}')
            node.set('id', key)
            used_ids.add(key)
        record = {'node': i, 'target': target, 'id': key, 'kind': kind}
        if kind == 'code':
            ancestor = parents.get(node)
            while ancestor is not None:
                if ancestor.get('role') == 'pgdoc-reference-synopsis':
                    record['synopsis'] = indices[ancestor]
                    break
                ancestor = parents.get(ancestor)
        records.append(record)
    data = {'sha256': hashlib.sha256(Path(source).read_bytes()).hexdigest(),
            'node_count': len(nodes), 'records': records, 'lead_ins': leads}
    # Calibration can add keeps in a different insertion order. A canonical
    # probe must be byte-identical before and after applying those keeps.
    for node in nodes:
        node.attrib = dict(sorted(node.attrib.items()))
    tree.write(output, encoding='utf-8', xml_declaration=True)
    Path(manifest).write_text(json.dumps(data, ensure_ascii=False) + '\n', encoding='utf-8')
    return len(records)


def apply(source, areas, manifest, report):
    data = json.loads(Path(manifest).read_text(encoding='utf-8'))
    if hashlib.sha256(Path(source).read_bytes()).hexdigest() != data['sha256']:
        raise ValueError('FO changed after measurement probe was created')
    keys = {r['id'] for r in data['records']}
    records_by_node = {r['node']: r for r in data['records']}
    parent_displays = defaultdict(dict)
    tail_boundaries = defaultdict(set)
    for link in data.get('lead_ins', []):
        if link['intro_kind'] == 'parent':
            parent_displays[records_by_node[link['intro']]['id']][records_by_node[link['display']]['id']] = link['display']
            if 'prefix_after' in link:
                parent_displays[records_by_node[link['intro']]['id']].setdefault(records_by_node[link['prefix_after']]['id'], None)
        elif link['intro_kind'] == 'sibling-tail':
            tail_boundaries[records_by_node[link['intro']]['id']].add(records_by_node[link['tail_after']]['id'])
        if 'first_prose' in link and link['first_prose'] != link['display']:
            parent_displays[records_by_node[link['display']]['id']][records_by_node[link['first_prose']]['id']] = link['first_prose']
    prefix_heights = defaultdict(float);pending = defaultdict(float);seen_displays = set()
    tail_heights = defaultdict(float)
    heights = defaultdict(float)
    body_height = None
    pages = 0
    for _, node in ET.iterparse(areas, events=('end',)):
        if node.tag != 'pageViewport':
            continue
        pages += 1
        if node.get('simple-page-master-name', '').startswith('body'):
            for body in node.iter('regionBody'):
                height = int(body.get('bpd', '0')) / 1000
                if height > 0:
                    body_height = min(body_height or height, height)
        for block in node.iter('block'):
            key = block.get('prod-id')
            if key in keys:
                heights[key] += int(block.get('bpd', '0')) / 1000
            if key in parent_displays:
                display_ids = parent_displays[key]
                def collect(area):
                    identity = area.get('prod-id')
                    if identity in display_ids:
                        if display_ids[identity] is not None and identity not in seen_displays:
                            prefix_heights[display_ids[identity]] = pending[key]
                            seen_displays.add(identity)
                        pending[key] = 0
                    elif any(n.get('prod-id') in display_ids for n in area.iter()):
                        for child in area:collect(child)
                    else:
                        pending[key] += int(area.get('bpda', area.get('bpd', '0'))) / 1000
                for child in block:collect(child)
            if key in tail_boundaries:
                boundaries = tail_boundaries[key]
                def collect_tail(area):
                    if area.get('prod-id') in boundaries:
                        tail_heights[key] = 0
                    elif any(n.get('prod-id') in boundaries for n in area.iter()):
                        for child in area:collect_tail(child)
                    else:
                        tail_heights[key] += int(area.get('bpda', area.get('bpd', '0'))) / 1000
                for child in block:collect_tail(child)
        node.clear()
    if body_height is None or body_height <= 80:
        raise ValueError('no usable body region in FOP area tree')
    missing = [r for r in data['records'] if r['id'] not in heights]
    if any(r['kind'] in ('code', 'cell', 'ending-section', 'ending-paragraph', 'ending-list-item', 'footnote', 'synopsis', 'lead-in-prose', 'lead-in-list-item', 'lead-in-first-prose') for r in missing):
        raise ValueError(f'FOP did not expose required code/cell/ending/footnote metrics: {missing[:3]}')
    tree = parse(source)
    nodes = list(tree.iter())
    if len(nodes) != data['node_count']:
        raise ValueError('FO structure changed after measurement')
    row_heights = defaultdict(float)
    list_heights = defaultdict(float)
    lead_heights = {link['display']: (prefix_heights[link['display']] if link['intro_kind']=='parent'
                                    else tail_heights[records_by_node[link['intro']]['id']] if link['intro_kind']=='sibling-tail'
                                    else heights[records_by_node[link['intro']]['id']])
                    for link in data.get('lead_ins', [])}
    if any(height <= 0 for height in lead_heights.values()):
        raise ValueError('FOP did not expose required prose introduction metrics')
    continuation_overheads = {}
    code_overheads = defaultdict(float)
    for link in data.get('lead_ins', []):
        if 'first_prose' in link:
            overhead = lead_heights[link['display']]
            if link['first_prose'] != link['display']:
                overhead += prefix_heights[link['first_prose']]
            continuation_overheads[link['display']] = overhead
            if 'first_code' in link:
                code_overheads[link['first_code']] += overhead
    synopsis_heights = {r['node']: heights[r['id']] for r in data['records'] if r['kind'] == 'synopsis'}
    synopsis_codes = defaultdict(float)
    for r in data['records']:
        if r['kind'] == 'code' and 'synopsis' in r:
            synopsis_codes[r['synopsis']] += heights[r['id']]
    changes = []

    def stamp(index, value, kind, height, attribute=KEEP):
        old = nodes[index].get(attribute)
        if old != value:
            nodes[index].set(attribute, value)
            changes.append({'node': index, 'kind': kind, 'height_pt': round(height, 3),
                            'attribute': attribute, 'before': old, 'after': value})

    limit = body_height - 80  # table headers, caption and paragraph spacing
    for r in data['records']:
        if r['id'] not in heights:
            continue
        height = heights[r['id']]
        if r['kind'] == 'cell':
            row_heights[r['target']] = max(row_heights[r['target']], height)
        elif r['kind'] in ('code', 'example-paragraph', 'footnote'):
            effective_height = height
            if r['kind'] == 'code':
                effective_height += lead_heights.get(r['node'], 0)
                effective_height += code_overheads[r['node']]
            if r['kind'] == 'code' and 'synopsis' in r:
                group = r['synopsis']
                effective_height += max(0, synopsis_heights[group] - synopsis_codes[group])
            stamp(r['target'], 'always' if effective_height <= limit else 'auto', r['kind'], effective_height)
        elif r['kind'] == 'lead-in-list-item':
            list_heights[r['target']] = max(list_heights[r['target']], height)
        elif r['kind'] in ('ending-section', 'ending-paragraph', 'ending-list-item'):
            compact_limit = 100
            if 0 < height <= compact_limit:
                stamp(r['target'], 'always', r['kind'], height)
                stamp(r['target'], 'always', r['kind'], height, 'keep-with-previous.within-column')
    for link in data.get('lead_ins', []):
        intro = lead_heights[link['display']]
        stamp(link['binding'], 'always', 'prose-introduction', intro, PREVIOUS)
        if link['kind'] == 'table':
            row_heights[link['first_row']] += intro + sum(row_heights[n] for n in link['header_rows'])
        elif link['kind'] == 'list':
            list_heights[link['first_item']] += intro
        elif link['kind'] == 'continuation':
            display = nodes[link['display']]
            height = heights[records_by_node[link['display']]['id']] + intro
            if _is_prose(display):
                stamp(link['display'], 'always' if height <= limit else 'auto', 'prose-continuation', height)
            elif display.get(KEEP) == 'always' and height > limit:
                stamp(link['display'], 'auto', 'block-continuation', height)
            if 'first_prose' in link:
                first = link['first_prose']
                first_height = heights[records_by_node[first]['id']]
                overhead = continuation_overheads[link['display']]
                if nodes[first].get(KEEP) == 'always' and first_height + overhead > limit:
                    stamp(first, 'auto', 'continuation-first-paragraph', first_height + overhead)
                intro_node = link['intro']
                chain_height = heights[records_by_node[intro_node]['id']] + first_height + overhead - intro
                if nodes[intro_node].get(KEEP) == 'always' and chain_height > limit:
                    stamp(intro_node, 'auto', 'introduction-keep-chain', chain_height)
    for index, height in row_heights.items():
        stamp(index, 'always' if height <= limit else 'auto', 'row', height)
    for index, height in list_heights.items():
        stamp(index, 'always' if height <= limit else 'auto', 'lead-in-list-item', height)
    temporary = Path(source).with_name(Path(source).name+'.measured.tmp')
    tree.write(temporary, encoding='utf-8', xml_declaration=True)
    temporary.replace(source)
    result = {'probe_pages': pages, 'body_height_pt': body_height,
              'intact_unit_limit_pt': limit, 'measured_nodes': len(heights),
              'missing_optional_nodes': len(missing), 'changes': changes,
              'prose_introductions': len(lead_heights),
              'final_sha256': hashlib.sha256(Path(source).read_bytes()).hexdigest()}
    Path(report).write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest='command', required=True)
    make = commands.add_parser('probe')
    make.add_argument('source', type=Path);make.add_argument('output', type=Path);make.add_argument('manifest', type=Path)
    finish = commands.add_parser('apply')
    finish.add_argument('source', type=Path);finish.add_argument('areas', type=Path);finish.add_argument('manifest', type=Path);finish.add_argument('report', type=Path)
    a = p.parse_args()
    if a.command == 'probe':
        print(f'Chinese PDF: probing {probe(a.source, a.output, a.manifest)} layout units.')
    else:
        result = apply(a.source, a.areas, a.manifest, a.report)
        print(f"Chinese PDF: measured {result['measured_nodes']} units; applied {len(result['changes'])} keeps within {result['intact_unit_limit_pt']:.1f}pt.")


if __name__ == '__main__':
    main()
