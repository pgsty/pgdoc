#!/usr/bin/env python3
"""Compare complete DocBook XML books, retaining external-entity locations.

Exit 0: checked structure/identifiers agree (NOT semantic acceptance).
Exit 1: definite alignment differences. Exit 2: incomplete/invalid inputs.
Exit 3: no definite difference, but unresolved structural matching ambiguity.
Only Python's standard library and xmlcatalog (for external DTDs) are needed.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlparse
from xml.parsers import expat


SKIP_DIRS = {'html', '.git', '.cache', '.build', '__pycache__'}
LEVELS = {'book', 'part', 'chapter', 'appendix', 'preface', 'section',
          'reference', 'refentry', 'refnamediv', 'refsynopsisdiv', 'simplesect',
          'partintro', 'bibliography', 'glossary', 'index', 'set', 'varlistentry'}
TITLES = {'title', 'titleabbrev', 'refentrytitle', 'refname', 'refdescriptor'}
CONTAINERS = {'table', 'informaltable', 'figure', 'informalfigure', 'example',
              'informalexample', 'equation', 'procedure', 'sidebar'}
BLOCKS = {'para', 'simpara', 'itemizedlist', 'orderedlist', 'variablelist',
          'listitem', 'varlistentry', 'programlisting', 'screen', 'synopsis'}
STABLE = {'function', 'type', 'parameter', 'structfield', 'structname', 'varname', 'command',
          'literal', 'option', 'symbol', 'token'}
FACTS = {'yes': True, 'no': False, '是': True, '否': False}
REFATTRS = {'linkend', 'linkends', 'endterm', 'otherterm', 'zone', 'arearefs', 'startref'}
# A small, explicit reference-page vocabulary. These are matching hints within
# an already paired parent, never semantic acceptance or ID exemptions.
HEADING_GROUPS = [
    ('Description', '描述'), ('See Also', '另见', '参见', '又见'),
    ('Examples', 'Example', '示例', '例子'), ('Compatibility', '兼容性'),
    ('Parameters', 'Arguments', '参数'), ('Notes', '注解', '注意', '注释'),
    ('Return Value', '返回值'), ('Options', '选项'), ('Environment', '环境'),
    ('Outputs', '输出'), ('Diagnostics', '诊断'), ('Exit Status', '退出状态'),
    ('Usage', '用法', '使用'), ('Files', '文件'), ('How It Works', '工作原理'),
    ('Author', '作者')]
HEADING_KEYS = {label.casefold(): group[0] for group in HEADING_GROUPS for label in group}


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_manifest(root):
    root = Path(root).resolve()
    files = [{'path': str(p.relative_to(root)), 'sha256': file_hash(p)}
             for p in sorted(root.rglob('*')) if p.is_file()
             and not any(x in SKIP_DIRS for x in p.relative_to(root).parts)]
    return {'root': str(root), 'tree_sha256': hashlib.sha256(''.join(
        f"{r['sha256']}  {r['path']}\n" for r in files).encode()).hexdigest(), 'files': files}


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def norm(text):
    return ' '.join(text.replace('\u200b', '').split())


def local(tag):
    return tag.rsplit('}', 1)[-1].split(':')[-1]


@dataclass(eq=False)
class Node:
    tag: str
    attrs: dict
    file: str
    line: int
    parent: Node | None
    order: int
    index: int
    children: list = field(default_factory=list)
    parts: list = field(default_factory=list)
    end_line: int = 0

    @property
    def ids(self):
        return list(dict.fromkeys(self.attrs[k] for k in ('id', 'xml:id') if k in self.attrs))

    @property
    def ident(self):
        return self.ids[0] if self.ids else ''

    def text(self):
        return ''.join(x.text() if isinstance(x, Node) else x for x in self.parts)

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def xpath(self):
        part = f'{self.tag}[{self.index}]'
        return (self.parent.xpath() if self.parent else '') + '/' + part

    def ancestry(self):
        nodes = []
        n = self.parent
        while n:
            nodes.append(n)
            n = n.parent
        return list(reversed(nodes))


def landmark(n):
    return (bool(n.ids) or n.tag in LEVELS | TITLES | CONTAINERS | {'anchor'}
            or bool(re.fullmatch(r'(?:sect|refsect)\d+', n.tag))
            or any(c.tag in TITLES for c in n.children))


def title(n):
    if n.tag in TITLES:
        return norm(n.text())
    return ' / '.join(norm(c.text()) for c in n.children if c.tag in TITLES)


def evidence(n):
    if n is None:
        return None
    return {'file': n.file, 'line': n.line, 'end_line': n.end_line,
            'xpath': n.xpath(), 'tag': n.tag, 'id': n.ident,
            'parent_path': n.parent.xpath() if n.parent else '/',
            'ancestors': [f'{a.tag}#{a.ident}' if a.ident else a.tag for a in n.ancestry()],
            'depth': len(n.ancestry()), 'order': n.order, 'title': title(n),
            'context': norm(n.text())[:350]}


class Book:
    def __init__(self, root, generated=None, auxiliary=None, catalogs=()):
        self.root = Path(root).resolve()
        self.generated = Path(generated).resolve() if generated else None
        self.auxiliary = Path(auxiliary).resolve() if auxiliary else None
        self.catalogs = list(catalogs) or [p for p in (
            '/etc/xml/catalog', '/opt/homebrew/etc/xml/catalog', '/usr/local/etc/xml/catalog')
            if Path(p).exists()]
        self.nodes, self.stack, self.edges, self.declarations = [], [], [], []
        self.dependencies, self.errors, self.events = {}, [], Counter()
        self.complete = False
        self.tree = None
        self.cache = {}
        self.bytes_read = 0

    def label(self, path):
        for base, prefix in [(self.root, ''), (self.generated, '@generated/'),
                             (self.auxiliary, '@auxiliary/')]:
            if base and path.is_relative_to(base):
                return prefix + str(path.relative_to(base))
        return str(path)

    def resolve(self, system, public, base):
        url = urlparse(system or '')
        if url.scheme in ('http', 'https', 'urn'):
            key = (system, public)
            if key not in self.cache:
                found = None
                for catalog in self.catalogs:
                    for query in (public, system):
                        if not query:
                            continue
                        r = subprocess.run(['xmlcatalog', str(catalog), query], text=True,
                                           capture_output=True)
                        if r.returncode == 0 and r.stdout.strip().startswith('file:'):
                            found = Path(unquote(urlparse(r.stdout.strip()).path)).resolve()
                            break
                    if found:
                        break
                if not found:
                    raise ValueError(f'No local catalog resolution for {system} ({public}); network disabled')
                self.cache[key] = found
            return self.cache[key]
        if url.scheme not in ('', 'file'):
            raise ValueError(f'Unsupported external entity URI: {system}')
        path = Path(unquote(url.path))
        if not path.is_absolute():
            path = Path(base).parent / path
        path = path.resolve()
        if path.exists():
            return path
        # Only explicit generated/auxiliary directories can satisfy a missing
        # source file. Never use a second English source tree as a fallback.
        if path.is_relative_to(self.root):
            rel = path.relative_to(self.root)
            for fallback in (self.generated, self.auxiliary):
                if fallback and (fallback / rel).is_file():
                    return fallback / rel
        raise FileNotFoundError(f'Missing included entity: {path}')

    def parse(self, entry='postgres.sgml'):
        parser = expat.ParserCreate(namespace_separator='}')
        # PostgreSQL's tiny root includes a 20+ MB book. Expat's default
        # amplification ratio mistakes this legitimate include tree for an
        # entity bomb. Retain explicit byte/node limits as well as a ratio cap.
        if hasattr(parser, 'SetBillionLaughsAttackProtectionMaximumAmplification'):
            parser.SetBillionLaughsAttackProtectionMaximumAmplification(10000)
        try:
            self._parse(parser, (self.root / entry).resolve())
            if not self.nodes or self.stack:
                raise ValueError('No complete document element')
            self.tree = self.nodes[0]
            self.complete = True
        except (expat.ExpatError, OSError, ValueError) as exc:
            self.errors.append(str(exc))
        return self

    def _parse(self, parser, path):
        label = self.label(path)
        self.bytes_read += path.stat().st_size
        if self.bytes_read > 256 * 1024 * 1024:
            raise ValueError('Expanded external input exceeds 256 MiB limit')
        self.dependencies[str(path)] = {'file': label, 'path': str(path), 'sha256': file_hash(path)}
        parser.SetBase(str(path))
        parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_ALWAYS)
        def start(tag, attrs):
            if len(self.nodes) >= 2_000_000:
                raise ValueError('Document exceeds 2,000,000 node limit')
            if tag.startswith('http://www.w3.org/2001/XInclude}'):
                raise ValueError(f'Unsupported XInclude at {label}:{parser.CurrentLineNumber}')
            attrs = {k.replace('http://www.w3.org/XML/1998/namespace}', 'xml:')
                       .replace('http://www.w3.org/1999/xlink}', 'xlink:'): v for k, v in attrs.items()}
            parent = self.stack[-1] if self.stack else None
            tag = local(tag)
            index = 1 + sum(c.tag == tag for c in parent.children) if parent else 1
            n = Node(tag, attrs, label, parser.CurrentLineNumber, parent, len(self.nodes), index)
            if parent:
                parent.children.append(n)
                parent.parts.append(n)
            self.nodes.append(n)
            self.stack.append(n)
        def end(tag):
            self.stack.pop().end_line = parser.CurrentLineNumber
        def chars(data):
            if self.stack:
                self.stack[-1].parts.append(data)
        def external(context, base, system, public):
            edge = {'from': label, 'line': parser.CurrentLineNumber,
                    'system': system, 'public': public, 'context': sorted(context.split('\f')) if context else None,
                    'kind': 'content' if context else 'dtd_or_parameter'}
            self.edges.append(edge)
            resolved = self.resolve(system, public, base or str(path))
            edge['to'] = self.label(resolved)
            self._parse(parser.ExternalEntityParserCreate(context), resolved)
            return 1
        def entity(name, parameter, value, base, system, public, notation):
            self.declarations.append({'name': name, 'parameter': bool(parameter),
                'file': label, 'line': parser.CurrentLineNumber, 'system': system,
                'public': public, 'value': value, 'base': base, 'notation': notation})
        def skipped(name, parameter):
            raise ValueError(f'Skipped entity {name} at {label}:{parser.CurrentLineNumber}')
        parser.StartElementHandler, parser.EndElementHandler = start, end
        parser.CharacterDataHandler, parser.ExternalEntityRefHandler = chars, external
        parser.EntityDeclHandler, parser.SkippedEntityHandler = entity, skipped
        parser.CommentHandler = lambda value: self.events.update(['comments'])
        parser.StartCdataSectionHandler = lambda: self.events.update(['cdata'])
        # Attribute defaults from the DTD are parsed but do not become alleged
        # translation differences; only actual source attributes are retained.
        parser.specified_attributes = True
        try:
            with path.open('rb') as stream:
                parser.ParseFile(stream)
        except expat.ExpatError as exc:
            raise ValueError(f'{label}:{parser.ErrorLineNumber}:{parser.ErrorColumnNumber}: {exc}') from exc

    def inventory(self):
        source = source_manifest(self.root)
        active = {r['file'] for r in self.dependencies.values()}
        nodefiles = {n.file for n in self.nodes}
        for row in source['files']:
            rel = row['path']
            row['role'] = ('included_content' if rel in nodefiles else
                           'included_declarations' if rel in active else
                           'orphan_sgml' if rel.endswith('.sgml') else
                           'style_build_or_asset')
        return {'complete': self.complete, 'source': source,
                'nodes': len(self.nodes), 'events': dict(self.events),
                'dependencies': list(self.dependencies.values()),
                'include_edges': self.edges, 'entity_declarations': self.declarations,
                'errors': self.errors}


def counter_delta(a, b):
    return {'missing': dict(a - b), 'extra': dict(b - a)}


def protected(n, tags=STABLE):
    # Keep only ASCII tokens; translated placeholders/prose cannot be called
    # identifier defects. All raw signatures remain available for review.
    return [(x.tag, norm(x.text())) for x in n.walk() if x.tag in tags
            and re.fullmatch(r'[\x20-\x7e]+', norm(x.text()))]


def frontier(n):
    result = []
    for child in n.children:
        if landmark(child):
            result.append(child)
        else:
            result.extend(frontier(child))
    return result


def owned(n):
    """Nodes owned by one landmark, excluding nested landmarks' contents."""
    yield n
    for c in n.children:
        if not landmark(c):
            yield from owned(c)


def references(n):
    for attr, value in n.attrs.items():
        if attr in REFATTRS:
            for target in value.split():
                yield (n.tag, attr, target)
        elif attr in {'xlink:href', 'href'} and value.startswith('#'):
            yield (n.tag, attr, value[1:])


def table_grid(table):
    """Resolve CALS names/spans to column coordinates, including row spans."""
    result = {}
    for group in (x for x in table.walk() if x.tag == 'tgroup'):
        cols = int(group.attrs['cols'])
        names, spans, previous = {}, {}, 0
        for c in group.children:
            if c.tag == 'colspec':
                previous = int(c.attrs.get('colnum', previous + 1))
                if 'colname' in c.attrs:
                    names[c.attrs['colname']] = previous
            elif c.tag == 'spanspec':
                spans[c.attrs['spanname']] = (names[c.attrs['namest']], names[c.attrs['nameend']])
        for body in (c for c in group.children if c.tag in {'thead', 'tbody', 'tfoot'}):
            occupied = {}
            for ri, row in enumerate(c for c in body.children if c.tag == 'row'):
                cursor = 1
                for cell in (c for c in row.children if c.tag in {'entry', 'entrytbl'}):
                    while occupied.get(cursor, -1) >= ri:
                        cursor += 1
                    if 'spanname' in cell.attrs:
                        left, right = spans[cell.attrs['spanname']]
                    elif 'namest' in cell.attrs:
                        left = names[cell.attrs['namest']]
                        # DocBook's calculate.colspan defaults to one when
                        # nameend is absent; namest still locates the column.
                        right = names[cell.attrs['nameend']] if 'nameend' in cell.attrs else left
                    else:
                        left = names[cell.attrs['colname']] if 'colname' in cell.attrs else cursor
                        right = left
                    down = int(cell.attrs.get('morerows', 0))
                    if not 1 <= left <= right <= cols or down < 0:
                        raise ValueError(f'Invalid span at {cell.file}:{cell.line}')
                    if any(occupied.get(col, -1) >= ri for col in range(left, right + 1)):
                        raise ValueError(f'Overlapping cells at {cell.file}:{cell.line}')
                    for col in range(left, right + 1):
                        occupied[col] = ri + down
                    result[cell] = (left, right, down)
                    cursor = right + 1
    return result


def fingerprint(n, common_ids):
    heading = title(n)
    if heading.casefold() in HEADING_KEYS:
        return (n.tag, (), (('heading', HEADING_KEYS[heading.casefold()]),))
    ids = tuple(x.ident for x in n.walk() if x is not n and x.ident in common_ids)
    if n.tag == 'varlistentry':
        terms = [c for c in n.children if c.tag == 'term']
        tokens = tuple(t for term in terms for t in protected(term))
        if not tokens:
            tokens = tuple(('term', norm(t.text())) for t in terms
                           if re.fullmatch(r'[\x20-\x7e]+', norm(t.text())))
    else:
        tokens = tuple(protected(n, {'function', 'command', 'structfield', 'varname'}))
    return (n.tag, ids, tokens) if ids or tokens else None


class Alignment:
    def __init__(self, en, zh):
        self.en, self.zh = en, zh
        self.findings, self.pairs, self.reverse, self.methods = [], {}, {}, {}
        self.titles, self.tables = [], []

    def add(self, code, category, en=None, zh=None, **details):
        lower_priority = {'extra_id', 'source_file_move', 'sibling_order',
                          'table_row_order', 'internal_reference_targets'}
        self.findings.append({'number': len(self.findings) + 1, 'code': code,
            'category': category, 'priority': 'P1' if category == 'definite' and code not in lower_priority else 'P2',
            'en': evidence(en), 'zh': evidence(zh), 'details': details})

    def pair(self, a, b, method):
        if a in self.pairs or b in self.reverse:
            return False
        self.pairs[a], self.reverse[b], self.methods[a] = b, a, method
        return True

    def run(self):
        if not self.en.complete or not self.zh.complete:
            return self
        active_en = {n.file for n in self.en.nodes}
        active_zh = {n.file for n in self.zh.nodes}
        for name in sorted(active_en - active_zh):
            self.add('included_file_missing', 'definite',
                     next(n for n in self.en.nodes if n.file == name), self.zh.tree,
                     file=name, zh_is_book_context=True)
        for name in sorted(active_zh - active_en):
            self.add('included_file_extra', 'definite', self.en.tree,
                     next(n for n in self.zh.nodes if n.file == name),
                     file=name, en_is_book_context=True)
        maps = []
        for lang, book in [('en', self.en), ('zh', self.zh)]:
            ids = defaultdict(list)
            for n in book.nodes:
                for ident in n.ids:
                    ids[ident].append(n)
            maps.append(ids)
            for ident, nodes in ids.items():
                if len(nodes) > 1:
                    self.add('duplicate_id', 'definite', nodes[0] if lang == 'en' else None,
                             nodes[0] if lang == 'zh' else None,
                             id=ident, side=lang, occurrences=[evidence(n) for n in nodes])
            for n in book.nodes:
                for attr, value in n.attrs.items():
                    targets = value.split() if attr in REFATTRS else (
                        [value[1:]] if attr in {'xlink:href', 'href'} and value.startswith('#') else [])
                    for target in targets:
                        if target not in ids:
                            self.add('unresolved_reference', 'definite', n if lang == 'en' else None,
                                     n if lang == 'zh' else None, target=target, attribute=attr, side=lang)
        ei, zi = maps
        common_ids = ei.keys() & zi.keys()
        for ident in sorted(ei.keys() & zi.keys()):
            if len(ei[ident]) == len(zi[ident]) == 1:
                self.pair(ei[ident][0], zi[ident][0], 'unique_id')
        for ident in sorted(ei.keys() - zi.keys()):
            n = ei[ident][0]
            other = next((self.pairs[a] for a in reversed(n.ancestry()) if a in self.pairs), None)
            self.add('missing_id', 'definite', n, other, id=ident, zh_is_nearest_matched_ancestor=True)
        for ident in sorted(zi.keys() - ei.keys()):
            n = zi[ident][0]
            other = next((self.reverse[a] for a in reversed(n.ancestry()) if a in self.reverse), None)
            self.add('extra_id', 'definite', other, n, id=ident, en_is_nearest_matched_ancestor=True)
        self.pair(self.en.tree, self.zh.tree, 'document_root')
        # Use unique structural evidence, then singleton gaps bounded by
        # already paired neighbours. Repeated anonymous nodes remain ambiguous.
        queue = deque(self.pairs)
        seen = set()
        while queue:
            a = queue.popleft()
            if a in seen:
                continue
            seen.add(a)
            b = self.pairs[a]
            ac, bc = frontier(a), frontier(b)
            for tag in sorted(TITLES):
                aa = [x for x in ac if x.tag == tag and x not in self.pairs]
                bb = [x for x in bc if x.tag == tag and x not in self.reverse]
                if len(aa) == len(bb) == 1 and self.pair(aa[0], bb[0], 'unique_title_of_matched_parent'):
                    queue.append(aa[0])
            for node in ac:
                if node in self.pairs:
                    queue.append(node)
            for key in sorted({fingerprint(x, common_ids) for x in ac if x not in self.pairs} - {None}):
                aa = [x for x in ac if x not in self.pairs and fingerprint(x, common_ids) == key]
                bb = [x for x in bc if x not in self.reverse and fingerprint(x, common_ids) == key]
                if len(aa) == len(bb) == 1 and self.pair(aa[0], bb[0], 'unique_protected_context'):
                    queue.append(aa[0])
            def gaps(nodes, side):
                groups = defaultdict(list)
                for i, n in enumerate(nodes):
                    mapping = self.pairs if side == 'en' else self.reverse
                    if n in mapping:
                        continue
                    before = next((x if side == 'en' else self.reverse[x]
                                   for x in reversed(nodes[:i]) if x in mapping), None)
                    after = next((x if side == 'en' else self.reverse[x]
                                  for x in nodes[i+1:] if x in mapping), None)
                    groups[(n.tag, before, after)].append(n)
                return groups
            ag, bg = gaps(ac, 'en'), gaps(bc, 'zh')
            for key in sorted(ag.keys() | bg.keys(), key=lambda k: (k[0], k[1].order if k[1] else -1, k[2].order if k[2] else -1)):
                aa, bb = ag[key], bg[key]
                # A singleton title/anonymous container can acquire an ID in
                # the translation. Keep the missing/extra ID finding as well.
                if len(aa) == len(bb) == 1 and (not aa[0].ident or not bb[0].ident):
                    if self.pair(aa[0], bb[0], 'singleton_between_matched_neighbors'):
                        queue.append(aa[0])
                elif aa or bb:
                    category = 'ambiguous' if aa and bb else 'definite'
                    self.add('anonymous_alignment' if category == 'ambiguous' else 'unpaired_landmarks',
                             category, a, b, tag=key[0],
                             english=[evidence(n) for n in aa], chinese=[evidence(n) for n in bb])
        zh_identity = {x: x for x in self.reverse}
        for a, b in list(self.pairs.items()):
            if a.tag != b.tag:
                self.add('node_kind', 'definite', a, b)
            if a.ident and b.ident:
                if a.file != b.file:
                    self.add('source_file_move', 'definite', a, b)
                def parent_signature(n, mapping):
                    result = []
                    for p in reversed(n.ancestry()):
                        if p in mapping:
                            result.append(('paired', mapping[p].order))
                            break
                        result.append((p.tag, p.ident))
                    return result
                # Compare both signatures in Chinese node identity space.
                if parent_signature(a, self.pairs) != parent_signature(b, zh_identity):
                    self.add('parent_or_level', 'definite', a, b)
            ac, bc = frontier(a), frontier(b)
            order_en = [self.pairs[x] for x in ac if x in self.pairs and self.pairs[x] in bc]
            order_zh = [x for x in bc if x in order_en]
            if order_en != order_zh:
                self.add('sibling_order', 'definite', a, b,
                         english_order=[evidence(n) for n in ac if n in self.pairs],
                         chinese_order=[evidence(n) for n in order_zh])
            if a.tag in TITLES:
                self.check_title(a, b)
            # link and xref have different rendering but the same linkend
            # identity contract. Keep raw tags in the reference inventories.
            ra = Counter((attr, target) for n in owned(a) for _, attr, target in references(n))
            rb = Counter((attr, target) for n in owned(b) for _, attr, target in references(n))
            if ra != rb:
                self.add('internal_reference_targets', 'definite', a, b,
                         missing=list((ra - rb).elements()), extra=list((rb - ra).elements()))
            if a.tag in {'table', 'informaltable'} and b.tag in {'table', 'informaltable'}:
                self.check_table(a, b)
            if a.tag in LEVELS | CONTAINERS or re.fullmatch(r'(?:sect|refsect)\d+', a.tag):
                def blocks(n):
                    counts = Counter()
                    def visit(x):
                        for c in x.children:
                            if c.tag in BLOCKS:
                                counts[c.tag] += 1
                            if c not in frontier_set:
                                visit(c)
                    frontier_set = set(frontier(n))
                    visit(n)
                    return counts
                ea, zb = blocks(a), blocks(b)
                if ea != zb:
                    self.add('content_structure_signal', 'review', a, b, en_counts=dict(ea), zh_counts=dict(zb))
        # Initial ID-set findings precede anonymous matching. Enrich them with
        # the actual counterpart when matching subsequently establishes one.
        # Missing ID never means missing prose if a counterpart was located.
        for f in self.findings:
            if f['code'] == 'missing_id':
                node = ei[f['details']['id']][0]
                if node in self.pairs:
                    f['zh'] = evidence(self.pairs[node])
                    f['details']['zh_is_nearest_matched_ancestor'] = False
                    f['details']['counterpart_method'] = self.methods[node]
            elif f['code'] == 'extra_id':
                node = zi[f['details']['id']][0]
                if node in self.reverse:
                    other = self.reverse[node]
                    f['en'] = evidence(other)
                    f['details']['en_is_nearest_matched_ancestor'] = False
                    f['details']['counterpart_method'] = self.methods[other]
        return self

    def check_title(self, a, b):
        row = {'en': evidence(a), 'zh': evidence(b), 'method': self.methods[a],
               'semantic_status': 'not_automatically_verified'}
        self.titles.append(row)
        ta, tb = norm(a.text()), norm(b.text())
        pa, pb = Counter(protected(a)), Counter(protected(b))
        if pa != pb:
            self.add('title_identifier_candidate', 'review', a, b,
                     en_tokens=list(pa.elements()), zh_tokens=list(pb.elements()))
        elif ta == tb and len(ta.split()) >= 4 and not re.search('[\u3400-\u9fff]', tb):
            self.add('title_untranslated_candidate', 'review', a, b)

    def check_table(self, a, b):
        def rows(n):
            return [x for x in n.walk() if x.tag == 'row' and
                    next((p for p in reversed(x.ancestry()) if p.tag in {'table', 'informaltable'}), None) is n]
        def cells(n):
            return [x for x in n.children if x.tag in {'entry', 'entrytbl'}]
        def signatures(n):
            return [x for x in n.walk() if x.attrs.get('role') == 'func_signature']
        def names(n):
            sigs = signatures(n)
            scope = sigs
            if not scope and n.tag == 'row' and cells(n):
                first = cells(n)[0]
                first_para = next((c for c in first.children if c.tag == 'para'), first)
                # Catalog descriptions can mention functions in later paras;
                # these are references, not definitions of table functions.
                if not any(c.tag == 'structfield' for c in first_para.walk()):
                    fn = next((c for c in first_para.walk() if c.tag == 'function'), None)
                    if fn and norm(first_para.text()).startswith(norm(fn.text())):
                        scope = [first_para]
            return tuple(norm(x.text()) for scope_node in scope for x in scope_node.walk()
                         if x.tag == 'function')
        def identity(n):
            if n.parent.tag == 'thead':
                return None
            functions = names(n)
            if functions:
                return ('functions', functions)
            cs = cells(n)
            if cs:
                first = cs[0]
                primary = next((c for c in first.children if c.tag == 'para'), first)
                fields = [t for t in protected(primary, {'structfield', 'structname', 'varname'})]
                if fields:
                    return ('catalog_identifier', fields[0])
                toks = tuple(protected(primary))
                if toks:
                    return ('tokens', toks)
                text = norm(cs[0].text())
                if text.lower() in FACTS:
                    return None
                if re.fullmatch(r'[A-Za-z0-9_.$+*/():=<>? -]+', text):
                    return ('first_cell', text)
            return None
        ar, br = rows(a), rows(b)
        def shape(n, rr):
            return {'tgroups': [int(x.attrs['cols']) for x in n.walk() if x.tag == 'tgroup'],
                    'row_groups': dict(Counter(x.parent.tag for x in rr)),
                    'entry_counts': dict(Counter(len(cells(x)) for x in rr))}
        ash, bsh = shape(a, ar), shape(b, br)
        grids = []
        for side, node in [('en', a), ('zh', b)]:
            try:
                grids.append(table_grid(node))
            except (KeyError, ValueError) as exc:
                grids.append({})
                self.add('table_grid_invalid', 'definite', a, b, side=side, error=str(exc))
        fn_a = Counter(f for r in ar for f in names(r))
        fn_b = Counter(f for r in br for f in names(r))
        record = {'en': evidence(a), 'zh': evidence(b), 'en_shape': ash, 'zh_shape': bsh,
                  'en_functions': dict(fn_a), 'zh_functions': dict(fn_b),
                  'function_delta': counter_delta(fn_a, fn_b), 'paired_rows': [], 'ambiguous_rows': []}
        self.tables.append(record)
        if ash != bsh:
            self.add('table_shape', 'definite', a, b, en_shape=ash, zh_shape=bsh)
        if fn_a != fn_b:
            self.add('table_function_identifiers', 'definite', a, b, **counter_delta(fn_a, fn_b))
        ag, bg = defaultdict(list), defaultdict(list)
        for row in ar:
            ag[(row.parent.tag, identity(row))].append(row)
        for row in br:
            bg[(row.parent.tag, identity(row))].append(row)
        paired = []
        for key in sorted(ag.keys() | bg.keys(), key=lambda k: json.dumps(k)):
            aa, bb = ag[key], bg[key]
            if key[1] is not None and len(aa) == len(bb) == 1:
                paired.append((aa[0], bb[0], 'unique_row_identity'))
            elif key[1] is not None and (len(aa) > 1 or len(bb) > 1):
                # Overloads with the same name: match using argument/return
                # type tokens, independently of translated explanatory prose.
                def overload(n):
                    return tuple(t for s in signatures(n) for t in protected(s, {'type', 'parameter'}))
                used_a, used_b = set(), set()
                for subkey in sorted({overload(x) for x in aa} - {()}):
                    xs = [x for x in aa if overload(x) == subkey]
                    ys = [x for x in bb if overload(x) == subkey]
                    if len(xs) == len(ys) == 1:
                        paired.append((xs[0], ys[0], 'unique_overload_types_parameters'))
                        used_a.add(xs[0]); used_b.add(ys[0])
                aa, bb = [x for x in aa if x not in used_a], [x for x in bb if x not in used_b]
                if aa or bb:
                    record['ambiguous_rows'].append({'key': key, 'en': [evidence(n) for n in aa], 'zh': [evidence(n) for n in bb]})
            elif key[1] is None and len(aa) == len(bb) == 1:
                paired.append((aa[0], bb[0], 'single_anonymous_row_in_group'))
            elif aa or bb:
                record['ambiguous_rows'].append({'key': key, 'en': [evidence(n) for n in aa], 'zh': [evidence(n) for n in bb]})
                if key[1] is not None and not (aa and bb):
                    # Unmarked English words (e.g. "equal", "Items", or
                    # "Serializable") are translatable prose, not identifiers.
                    stable = key[1][0] in {'functions', 'catalog_identifier'}
                    self.add('table_row_identifier', 'definite' if stable else 'review', aa[0] if aa else a,
                             bb[0] if bb else b, key=key, en_rows=len(aa), zh_rows=len(bb))
        if record['ambiguous_rows']:
            self.add('table_rows_unpaired', 'ambiguous', a, b, groups=record['ambiguous_rows'])
        ordered = sorted(paired, key=lambda x: x[0].order)
        if [y.order for _, y, _ in ordered] != sorted(y.order for _, y, _ in ordered):
            self.add('table_row_order', 'definite', a, b,
                     pairs=[{'en': evidence(x), 'zh': evidence(y)} for x, y, _ in ordered])
        for x, y, method in paired:
            cx, cy = cells(x), cells(y)
            sx, sy = signatures(x), signatures(y)
            rx, ry = [norm(s.text()) for s in sx], [norm(s.text()) for s in sy]
            record['paired_rows'].append({'en': evidence(x), 'zh': evidence(y), 'method': method,
                                         'en_signatures': rx, 'zh_signatures': ry})
            px, py = Counter(t for s in sx for t in protected(s)), Counter(t for s in sy for t in protected(s))
            header = x.parent.tag == 'thead' and y.parent.tag == 'thead'
            if px != py and not header:
                # Exact ASCII token loss is definite only if both sides use
                # signature markup. Markup/prose/placeholder changes need review.
                self.add('signature_tokens', 'review', x, y,
                         en_tokens=list(px.elements()), zh_tokens=list(py.elements()),
                         en_signatures=rx, zh_signatures=ry)
            elif rx != ry and not header:
                self.add('signature_text_candidate', 'review', x, y, en_signatures=rx, zh_signatures=ry)
            if len(cx) == len(cy):
                for i, (u, v) in enumerate(zip(cx, cy)):
                    f, g = FACTS.get(norm(u.text()).lower()), FACTS.get(norm(v.text()).lower())
                    if f is not None and g is not None and f != g:
                        self.add('boolean_fact', 'definite', u, v, column=i+1,
                                 row_en=evidence(x), row_zh=evidence(y), table_id=a.ident)
                    if u in grids[0] and v in grids[1] and grids[0][u] != grids[1][v]:
                        self.add('cell_span', 'definite', u, v, column=i+1,
                                 en_grid=grids[0][u], zh_grid=grids[1][v])
            # Non-signature type/parameter differences are evidence for review,
            # including prose changes in min/max accepted types.
            tx, ty = Counter(protected(x, {'type', 'parameter'})), Counter(protected(y, {'type', 'parameter'}))
            if tx != ty:
                self.add('row_type_parameter_candidate', 'review', x, y,
                         en_tokens=list(tx.elements()), zh_tokens=list(ty.elements()))


def write_tsv(path, fields, rows):
    with Path(path).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list, tuple)) else v
                             for k, v in row.items() if k in fields})


def exit_status(en_complete, zh_complete, categories):
    if not (en_complete and zh_complete):
        return 2
    return 1 if categories.get('definite') else (3 if categories.get('ambiguous') else 0)


def report(alignment, out, manifest):
    a = alignment
    counts = []
    for side, book in [('en', a.en), ('zh', a.zh)]:
        c = Counter((n.file, n.tag, len(n.ancestry())) for n in book.nodes)
        counts.extend({'side': side, 'file': f, 'tag': t, 'depth': d, 'count': v}
                      for (f, t, d), v in sorted(c.items()))
        write_json(out / f'{side}-inventory.json', book.inventory())
        write_json(out / f'{side}-references.json', [dict(node=evidence(n), targets=list(references(n)))
                   for n in book.nodes if any(references(n))])
        with (out / f'{side}-nodes.jsonl').open('w') as stream:
            for n in book.nodes:
                # Every node, not just elements with IDs, has verifiable XPath.
                row = {'file': n.file, 'line': n.line, 'tag': n.tag, 'ids': n.ids,
                       'xpath': n.xpath(), 'order': n.order, 'attributes': n.attrs}
                if landmark(n):
                    row.update(evidence(n))
                stream.write(json.dumps(row, ensure_ascii=False) + '\n')
    write_tsv(out / 'counts.tsv', ['side', 'file', 'tag', 'depth', 'count'], counts)
    ec = {(r['file'], r['tag'], r['depth']): r['count'] for r in counts if r['side'] == 'en'}
    zc = {(r['file'], r['tag'], r['depth']): r['count'] for r in counts if r['side'] == 'zh'}
    write_tsv(out / 'counts-diff.tsv', ['file', 'tag', 'depth', 'en', 'zh', 'zh_minus_en'],
              [dict(file=f, tag=t, depth=d, en=ec.get((f,t,d), 0), zh=zc.get((f,t,d), 0),
                    zh_minus_en=zc.get((f,t,d), 0)-ec.get((f,t,d), 0))
               for f,t,d in sorted(ec.keys() | zc.keys()) if ec.get((f,t,d), 0) != zc.get((f,t,d), 0)])
    write_json(out / 'findings.json', a.findings)
    write_tsv(out / 'findings.tsv', ['number', 'priority', 'category', 'code', 'en', 'zh', 'details'], a.findings)
    write_json(out / 'title-pairs.json', a.titles)
    with (out / 'landmark-pairs.jsonl').open('w') as stream:
        for en, zh in sorted(a.pairs.items(), key=lambda pair: pair[0].order):
            stream.write(json.dumps({'en': evidence(en), 'zh': evidence(zh),
                                    'method': a.methods[en]}, ensure_ascii=False) + '\n')
    write_tsv(out / 'title-pairs.tsv', ['en', 'zh', 'method', 'semantic_status'], a.titles)
    write_json(out / 'tables.json', a.tables)
    categories = Counter(f['category'] for f in a.findings)
    coverage = {'en_complete': a.en.complete, 'zh_complete': a.zh.complete,
        'en_nodes': len(a.en.nodes), 'zh_nodes': len(a.zh.nodes),
        'en_landmarks': sum(landmark(n) for n in a.en.nodes),
        'zh_landmarks': sum(landmark(n) for n in a.zh.nodes),
        'paired_landmarks': len(a.pairs), 'paired_titles': len(a.titles),
        'paired_tables': len(a.tables),
        'paired_table_rows': sum(len(t['paired_rows']) for t in a.tables),
        'landmark_coverage_by_tag': {tag: {'en': sum(n.tag == tag for n in a.en.nodes if landmark(n)),
            'zh': sum(n.tag == tag for n in a.zh.nodes if landmark(n)),
            'paired': sum(n.tag == tag for n in a.pairs)}
            for tag in sorted({n.tag for n in a.en.nodes + a.zh.nodes if landmark(n)})},
        'categories': dict(categories), 'semantic_acceptance': False}
    exit_code = exit_status(a.en.complete, a.zh.complete, categories)
    coverage['exit_code'] = exit_code
    write_json(out / 'coverage.json', coverage)
    write_json(out / 'manifest.json', manifest)
    assets = []
    inputs = [{r['path']: r['sha256'] for r in manifest['inputs'][side]['files']}
              for side in ('en', 'zh')]
    for path in sorted(inputs[0].keys() | inputs[1].keys()):
        if not path.endswith('.sgml'):
            assets.append({'path': path, 'en_sha256': inputs[0].get(path),
                           'zh_sha256': inputs[1].get(path),
                           'status': 'same' if inputs[0].get(path) == inputs[1].get(path) else 'different_or_one_side',
                           'scope': 'style_build_or_asset_not_body'})
    write_tsv(out / 'assets.tsv', ['path', 'status', 'scope', 'en_sha256', 'zh_sha256'], assets)
    byfile = defaultdict(Counter)
    for f in a.findings:
        ev = f['en'] or f['zh']
        byfile[ev['file'] if ev else '?'][f['category']] += 1
        byfile[ev['file'] if ev else '?'][f['priority']] += 1
    ordered_files = sorted(byfile, key=lambda f: (-byfile[f]['P1'], -byfile[f]['definite'], -byfile[f]['review'], f))
    write_tsv(out / 'files.tsv', ['file', 'P1', 'P2', 'definite', 'ambiguous', 'review'],
              [dict(file=f, **{k: byfile[f][k] for k in ['P1', 'P2', 'definite', 'ambiguous', 'review']}) for f in ordered_files])
    lines = ['# DocBook 中英文全量对齐检查', '',
             f"版本：{manifest['version']}。退出码：{exit_code}。结构对齐不代表全文语义正确。", '',
             '解析错误：' + json.dumps({'en': a.en.errors, 'zh': a.zh.errors}, ensure_ascii=False), '',
             '```json', json.dumps(coverage, ensure_ascii=False, indent=2), '```', '',
             '固定输入、逐文件哈希、工具版本和调用参数见 [manifest.json](manifest.json)。',
             '整本书包含图、实体声明、孤立文件及解析错误见 en/zh-inventory.json；全部节点见 en/zh-nodes.jsonl。',
             '每个文件、标签和深度的计数见 [counts.tsv](counts.tsv)。全部标题并排证据见 [title-pairs.tsv](title-pairs.tsv)。',
             '所有表及行配对证据见 [tables.json](tables.json)。以下候选不应直接当作修复数量。', '',
             '## 文件优先级', '', '| 文件 | P1 | 确定结构/标识符差异 | 匹配歧义 | 语义复核信号 |', '|---|---:|---:|---:|---:|']
    for f in ordered_files:
        c = byfile[f]
        lines.append(f"| {f} | {c['P1']} | {c['definite']} | {c['ambiguous']} | {c['review']} |")
    lines += ['', '## 全部差异证据', '']
    for f in a.findings:
        lines += [f"### {f['number']:04d} · {f['category']} · {f['code']}", '']
        for side in ('en', 'zh'):
            ev = f[side]
            if ev:
                lines.append(f"- {side}: `{ev['file']}:{ev['line']}` · `{ev['xpath']}` · `{ev['id']}` · {ev['title']}")
        lines += ['', '```json', json.dumps(f['details'], ensure_ascii=False, indent=2), '```', '']
    lines += ['## 覆盖边界', '',
              '- 解析实际入口的 XML/DocBook 实体与包含链；注释不计为正文，CDATA 只计文本。未支持的 XInclude、缺输入、未解析实体会失败。',
              '- ID、出现次数、父级、标签层级、兄弟顺序、无 ID 结构节点、内部引用、表格形状和函数标识符分别检查。',
              '- 无 ID 多候选不会强制按序号配对；歧义及未配对节点保留在报告内。',
              '- 标题翻译无需字面相等；所有标题语义尚需人工复核。函数签名、类型、参数及内容结构差异是有证据的候选。',
              '- Yes/No 与是/否仅对完整单元格归一化；不解析任意自然语言断言。没有全文语义正确率。',
              '- 样式和构建资产单独盘点；不比较所有 XML 属性。不自动写入豁免，不自动改译文。', '']
    (out / 'REPORT.md').write_text('\n'.join(lines))
    return coverage


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--en', type=Path, required=True)
    p.add_argument('--zh', type=Path, required=True)
    p.add_argument('--version', required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--entry', default='postgres.sgml')
    p.add_argument('--prepared', type=Path, help='Directory made by prepare_doc_alignment.py')
    p.add_argument('--zh-aux', type=Path, help='Explicit additional inputs; every consumed file is hashed')
    p.add_argument('--catalog', action='append', default=[])
    p.add_argument('--native-sgml', action='store_true', help='Validate native SGML with OpenSP, then map converted XML to original locations')
    args = p.parse_args()
    out = args.out.resolve()
    for root in (args.en.resolve(), args.zh.resolve()):
        if out == root or out.is_relative_to(root):
            p.error('--out must be outside input trees')
    out.mkdir(parents=True, exist_ok=False)
    initial = {k: source_manifest(v) for k, v in [('en', args.en), ('zh', args.zh)]}
    prepared = None
    if args.prepared:
        prepared = json.loads((args.prepared / 'manifest.json').read_text())
        if prepared['version'] != args.version:
            raise ValueError('Prepared source version differs from --version')
        for side in ('en', 'zh'):
            item = prepared['languages'][side]
            if item['source']['tree_sha256'] != initial[side]['tree_sha256']:
                raise ValueError(f'{side} source changed since generation')
            if item['generated']['tree_sha256'] != source_manifest(args.prepared / side)['tree_sha256']:
                raise ValueError(f'{side} generated inputs changed since preparation')
    makefile = args.zh / 'Makefile'
    if makefile.exists():
        m = re.search(r'^PG_VERSION\s*\??=\s*(\S+)', makefile.read_text(), re.M)
        if m and m[1] != args.version:
            raise ValueError(f'Chinese Makefile PG_VERSION={m[1]}, requested {args.version}')
    en = Book(args.en, args.prepared / 'en' if args.prepared else None, catalogs=args.catalog)
    zh = Book(args.zh, args.prepared / 'zh' if args.prepared else None, args.zh_aux, args.catalog)
    if args.native_sgml:
        from doc_alignment_sgml import load_sgml_book
        en = load_sgml_book(en, out / 'native-en', args.entry)
        zh = load_sgml_book(zh, out / 'native-zh', args.entry)
    else:
        en, zh = en.parse(args.entry), zh.parse(args.entry)
    for side, book in [('en', en), ('zh', zh)]:
        if source_manifest(book.root)['tree_sha256'] != initial[side]['tree_sha256']:
            book.complete = False
            book.errors.append('Input changed during check')
        for dep in book.dependencies.values():
            if file_hash(dep['path']) != dep['sha256']:
                book.complete = False
                book.errors.append('Dependency changed during check: ' + dep['path'])
    root = Path(__file__).resolve().parents[1]
    def git(*cmd):
        r = subprocess.run(['git', '-C', str(root), *cmd], text=True, capture_output=True)
        return r.stdout.strip() if r.returncode == 0 else None
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'version': args.version,
        'argv': sys.argv, 'python': sys.version, 'expat': expat.EXPAT_VERSION,
        'script_sha256': file_hash(__file__), 'git_head': git('rev-parse', 'HEAD'),
        'git_status': git('status', '--short'), 'inputs': initial, 'preparation': prepared,
        'catalogs': en.catalogs, 'rules': source_manifest(root / 'tmp/ref')}
    coverage = report(Alignment(en, zh).run(), out, manifest)
    print(json.dumps({k: v for k,v in coverage.items() if k != 'landmark_coverage_by_tag'}, ensure_ascii=False))
    return coverage['exit_code']


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'Incomplete alignment check: {exc}', file=sys.stderr)
        sys.exit(2)
