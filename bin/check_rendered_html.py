#!/usr/bin/env python3
"""Independently check generated XHTML, links and visible Chinese text.

Inline tags do not become artificial spaces. Code, SVG, MathML and URLs
remain protected. Spacing findings are candidates; broken XML/links/resources
and changed protected content are errors. No normalizer code is imported.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

BLOCKS = frozenset(('p', 'td', 'th', 'li', 'dt', 'dd', 'h1', 'h2', 'h3', 'h4',
                   'h5', 'h6', 'div', 'br', 'pre', 'table', 'ul', 'ol', 'dl'))
PROTECTED = frozenset(('code', 'pre', 'kbd', 'samp', 'tt', 'var', 'script',
                      'style', 'textarea', 'svg', 'math', 'listing', 'xmp'))
IGNORED = frozenset(('head', 'script', 'style', 'textarea', 'svg', 'math', 'pre'))
ADJACENT = re.compile(r'[\u3400-\u9fff\uf900-\ufaff][A-Za-z0-9]|[A-Za-z0-9][\u3400-\u9fff\uf900-\ufaff]')
URL = re.compile(r'(?:[A-Za-z][A-Za-z0-9+.-]*://|mailto:)[^\s<>"，。；：？！、（）《》]+')
CSS_REF = re.compile(r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s)]+))\s*\)|@import\s+["\']([^"\']+)["\']')


def tag(node):
    return node.tag.rsplit('}', 1)[-1] if isinstance(node.tag, str) else ''


def visible_text(root):
    chars, locked = [], []

    def add(text, protect):
        chars.extend(text or '')
        locked.extend([protect] * len(text or ''))

    def walk(node, protect=False):
        name = tag(node)
        if name in IGNORED:
            add('\n', True)
            return
        if name in BLOCKS:
            add('\n', True)
        protect = protect or name in PROTECTED
        add(node.text, protect)
        for child in node:
            walk(child, protect)
            add(child.tail, protect)
        if name in BLOCKS:
            add('\n', True)

    walk(root)
    text = ''.join(chars)
    for match in URL.finditer(text):
        locked[match.start():match.end()] = [True] * len(match[0])
    return text, locked


def protected_text(root):
    """Compare each outermost protected island including its nested markup."""
    islands = []

    def walk(node):
        if tag(node) in PROTECTED:
            # Tail belongs to surrounding prose, not this island.
            islands.append((tag(node), ''.join(node.itertext()),
                            tuple((tag(n), tuple(sorted(n.attrib.items()))) for n in node.iter())))
        else:
            for child in node:
                walk(child)
    walk(root)
    return islands


def check(directory, before_dir=None):
    directory = Path(directory).resolve()
    ids, links, findings = {}, [], []
    stats = Counter()

    def local_target(page, ref):
        uri = urlsplit(ref)
        if uri.scheme or uri.netloc or not uri.path:
            return None
        return (page.parent / unquote(uri.path)).resolve()

    def finding(name, kind, **data):
        findings.append({'file': name, 'type': kind, **data})
        stats[kind] += 1

    for page in sorted(directory.rglob('*.html')):
        name = page.relative_to(directory).as_posix()
        stats['pages'] += 1
        raw = page.read_text(encoding='utf-8')
        try:
            doc = ET.fromstring(raw)
        except ET.ParseError as exc:
            finding(name, 'xml_error', text=str(exc))
            continue
        values = [n.get('id') for n in doc.iter() if n.get('id')]
        ids[page] = set(values) | {n.get('name') for n in doc.iter() if tag(n) == 'a' and n.get('name')}
        for ident, count in Counter(values).items():
            if count > 1:
                finding(name, 'duplicate_id', id=ident, count=count)
        for node in doc.iter():
            href = node.get('href')
            if tag(node) == 'a' and href:
                links.append((page, href))
            refs = [node.get('src')]
            if tag(node) == 'object':
                refs.append(node.get('data'))
            if tag(node) == 'link' and 'stylesheet' in node.get('rel', '').split():
                refs.append(href)
            for ref in filter(None, refs):
                target = local_target(page, ref)
                if target:
                    stats['resource_references'] += 1
                    if not target.is_file():
                        finding(name, 'missing_resource', ref=ref)
        text, locked = visible_text(doc)
        for match in ADJACENT.finditer(text):
            if all(locked[match.start():match.end()]):
                continue
            finding(name, 'spacing_candidate', code_boundary=any(locked[match.start():match.end()]),
                    text=re.sub(r'\s+', ' ', text[max(0, match.start()-45):match.end()+45]))
        if '\ufffd' in text:
            finding(name, 'replacement_character', count=text.count('\ufffd'))
        if before_dir is not None:
            before = Path(before_dir) / name
            if not before.is_file():
                finding(name, 'missing_before_page')
            else:
                try:
                    old = ET.fromstring(before.read_text(encoding='utf-8'))
                    if protected_text(old) != protected_text(doc):
                        finding(name, 'protected_content_changed')
                    # Text edits must not rewrite any attribute, including URLs.
                    if [(tag(n), n.attrib) for n in old.iter()] != [(tag(n), n.attrib) for n in doc.iter()]:
                        finding(name, 'markup_changed')
                except ET.ParseError as exc:
                    finding(name, 'before_xml_error', text=str(exc))
    for page, href in links:
        uri = urlsplit(href)
        if uri.scheme or uri.netloc:
            continue
        stats['internal_links'] += 1
        target = (page.parent / unquote(uri.path)).resolve() if uri.path else page
        name = page.relative_to(directory).as_posix()
        if not target.is_file():
            finding(name, 'missing_link_file', href=href)
        elif uri.fragment and unquote(uri.fragment) not in ids.get(target, set()):
            finding(name, 'missing_fragment', href=href)
    for css in sorted(directory.rglob('*.css')):
        stats['css_files'] += 1
        raw = re.sub(r'/\*.*?\*/', '', css.read_text(encoding='utf-8'), flags=re.S)
        for match in CSS_REF.finditer(raw):
            ref = next(x for x in match.groups() if x is not None)
            target = local_target(css, ref)
            if target and not target.is_file():
                finding(css.relative_to(directory).as_posix(), 'missing_css_resource', ref=ref)
    stats['errors'] = sum(value for key, value in stats.items() if key in {
        'xml_error', 'duplicate_id', 'missing_resource', 'missing_link_file', 'missing_fragment',
        'missing_css_resource', 'replacement_character', 'missing_before_page',
        'protected_content_changed', 'markup_changed', 'before_xml_error'})
    return {'directory': str(directory), 'stats': dict(stats), 'findings': findings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--before-dir', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.directory, args.before_dir)
    if args.report:
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result['stats'], ensure_ascii=False))
    return int(bool(result['stats']['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
