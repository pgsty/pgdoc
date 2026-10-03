#!/usr/bin/env python3
"""Copy and verify local resources referenced by generated HTML.

Old XSL HTML targets only write chunks; their image and CSS copy rules are
incomplete.  Resolve references against the generated output, then copy the
matching source file from doc/src/sgml or doc/src/graphics.  Missing resources
are build errors, including when an upstream make rule ignored its failed cp.
"""

import argparse
import hashlib
import json
import os
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit


class Resources(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = set()
        self.errors = []
        self.class_elements = set()
        self.body_containers = set()
        self.stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        self.class_elements.update((tag, name) for name in classes)
        if tag == 'div' and self.stack and self.stack[-1] == 'body':
            self.body_containers.update(classes)
        if tag == 'img' and not attrs.get('src', '').strip():
            self.errors.append('image has no nonempty src')
        if attrs.get('src'):
            self.references.add(attrs['src'])
        if tag == 'link' and 'stylesheet' in attrs.get('rel', '').lower().split():
            if attrs.get('href'):
                self.references.add(attrs['href'])
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack = self.stack[:len(self.stack) - 1 - self.stack[::-1].index(tag)]


CSS_REFERENCES = re.compile(
    r'''url\(\s*(?:'([^']*)'|"([^"]*)"|([^\s)]+))\s*\)|@import\s+['"]([^'"]+)['"]''',
    re.IGNORECASE,
)
OFFICIAL_CSS = 'https://www.postgresql.org/media/css/docs-complete.css'
BUNDLE = Path(__file__).resolve().parent.parent / 'deps/pgweb'
LINK_TAG = re.compile(r'<link\b[^>]*>', re.IGNORECASE)
HREF = re.compile(r'''\bhref\s*=\s*(['"])(.*?)\1''', re.IGNORECASE)
STYLESHEET_LINK = re.compile(
    r'<link\b[^>]*rel\s*=\s*["\']?stylesheet[^>]*>', re.IGNORECASE)
HEAD_END = re.compile(r'</head\s*>', re.IGNORECASE)


def inject_design_links(output):
    """Link the bundled official theme directly from every page's <head>.

    stylesheet.css pulls docs-complete.css through a nested @import chain.
    Desktop browsers handle it, but embedded WebKit views (IAB/Electron-era
    readers) stop applying the chain two levels deep, leaving the whole site
    on the 1998 fallback styling.  A direct <link> to the same local file is
    applied everywhere (verified by computed-style A/B), so emit it in every
    generated page after the last existing stylesheet link.
    """
    output = Path(output)
    destination = output / '_static/pgweb/media/css/docs-complete.css'
    if not destination.is_file():
        return []
    injected = []
    for page in sorted(output.rglob('*.html')):
        if '_static' in page.parts:
            continue
        text = page.read_text(encoding='utf-8')
        relative = Path(os.path.relpath(destination, page.parent)).as_posix()
        direct = ('<link rel="stylesheet" type="text/css" '
                  f'href="{relative}" />')
        links = list(STYLESHEET_LINK.finditer(text))
        if any(relative in m.group(0) for m in links):
            continue
        if links:
            anchor = links[-1].end()
        else:
            head = HEAD_END.search(text)
            if not head:
                continue
            anchor = head.start()
        page.write_text(text[:anchor] + direct + text[anchor:], encoding='utf-8')
        injected.append(page.relative_to(output).as_posix())
    return injected


def localize_official_styles(output, bundle=BUNDLE):
    """Pin the existing official theme without changing other URLs or CSS rules."""
    output, bundle = Path(output), Path(bundle)
    destination = output / '_static/pgweb'
    edits = []
    for path in sorted(output.rglob('*')):
        if path.suffix not in ('.html', '.css') or destination in path.parents:
            continue
        before = path.read_bytes()
        text = before.decode('utf-8')
        replacement = Path(os.path.relpath(destination / 'media/css/docs-complete.css', path.parent)).as_posix()
        if path.suffix == '.css':
            def css_reference(match):
                ref = next(group for group in match.groups() if group is not None)
                return match.group().replace(ref, replacement, 1) if ref == OFFICIAL_CSS else match.group()
            updated = CSS_REFERENCES.sub(css_reference, text)
        else:
            def link_reference(match):
                return HREF.sub(lambda attr: attr.group().replace(OFFICIAL_CSS, replacement, 1)
                                if attr.group(2) == OFFICIAL_CSS else attr.group(), match.group())
            updated = LINK_TAG.sub(link_reference, text)
        after = updated.encode('utf-8')
        if after != before:
            edits.append((path, before, after))
    if not edits:
        return []
    manifest = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8'))
    for item in manifest['files']:
        source = bundle / item['path']
        if hashlib.sha256(source.read_bytes()).hexdigest() != item['sha256']:
            raise ValueError(f'pinned official stylesheet resource hash mismatch: {source}')
    shutil.copytree(bundle, destination, dirs_exist_ok=True)
    report = []
    for path, before, after in edits:
        path.write_bytes(after)
        report.append({'file': path.relative_to(output).as_posix(),
                       'before_sha256': hashlib.sha256(before).hexdigest(),
                       'after_sha256': hashlib.sha256(after).hexdigest()})
    return report

def adapt_legacy_css(output, class_elements, body_containers):
    """Adapt only selectors absent from XSL HTML; preserve every declaration."""
    path = Path(output) / 'stylesheet.css'
    if not path.is_file():
        return []
    before = path.read_bytes()
    text = before.decode('utf-8')
    # Mask comments without moving offsets so comments and declarations never
    # become replacement candidates. Legacy DocBook sheets have flat rules.
    masked = re.sub(r'/\*.*?\*/', lambda m: ' ' * len(m.group()), text, flags=re.S)
    classes = {name for _, name in class_elements}
    edits, selectors = [], []
    for rule in re.finditer(r'([^{}]+)\{[^{}]*\}', masked):
        start, end = rule.span(1)
        selector = text[start:end]
        mask = masked[start:end]
        changes = []
        for match in re.finditer(r'\bbody\.(book|set)\b(?=\s)', mask, re.I):
            name = match.group(1)
            if ('body', name) not in class_elements and name.lower() in body_containers:
                changes.append((match.start(), match.end(), 'body > div.' + name.lower()))
        for match in re.finditer(r'\.([A-Z][A-Z0-9_-]*)\b', mask):
            name = match.group(1)
            if name not in classes and name.lower() in classes and not any(a <= match.start() < b for a, b, _ in changes):
                changes.append((match.start(), match.end(), '.' + name.lower()))
        if not changes:
            continue
        updated = selector
        for a, b, replacement in sorted(changes, reverse=True):
            updated = updated[:a] + replacement + updated[b:]
        edits.append((start, end, updated))
        selectors.append({'before': selector.strip(), 'after': updated.strip()})
    if not edits:
        return []
    updated = text
    for a, b, replacement in reversed(edits):
        updated = updated[:a] + replacement + updated[b:]
    after = updated.encode('utf-8')
    path.write_bytes(after)
    return [{'file': 'stylesheet.css', 'before_sha256': hashlib.sha256(before).hexdigest(),
             'after_sha256': hashlib.sha256(after).hexdigest(), 'selectors': selectors}]


def prepare_resources(sgml_dir, output_dir=None, localization_report=None, style_report=None, *, _adapt_styles=True):
    sgml_dir = Path(sgml_dir).resolve()
    output = Path(output_dir).resolve() if output_dir else sgml_dir / 'html'
    if not output.is_dir():
        raise ValueError(f'HTML output directory does not exist: {output}')
    localized = localize_official_styles(output)
    source_roots = (sgml_dir, sgml_dir.parent / 'graphics')
    pending, errors = [], []
    class_elements, body_containers = set(), set()
    for page in sorted(output.rglob('*.html')):
        parser = Resources()
        parser.feed(page.read_text(encoding='utf-8'))
        class_elements.update(parser.class_elements)
        body_containers.update(parser.body_containers)
        errors.extend(f'{page.relative_to(output)}: {error}' for error in parser.errors)
        pending.extend((page, ref) for ref in sorted(parser.references))

    copied, checked, css_seen = [], set(), set()
    while pending:
        referring, ref = pending.pop()
        parsed = urlsplit(ref)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = (referring.parent / unquote(parsed.path)).resolve()
        try:
            relative = target.relative_to(output)
        except ValueError:
            errors.append(f'{referring.relative_to(output)}: resource escapes HTML output: {ref}')
            continue
        checked.add(relative.as_posix())
        if not target.is_file():
            for source_root in source_roots:
                source = source_root / relative
                if source.is_file():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
                    copied.append(relative.as_posix())
                    break
            else:
                errors.append(f'{referring.relative_to(output)}: missing local resource: {ref}')
                continue
        if target.suffix.lower() == '.css' and target not in css_seen:
            css_seen.add(target)
            for match in CSS_REFERENCES.finditer(target.read_text(encoding='utf-8')):
                pending.append((target, next(group for group in match.groups() if group is not None)))

    if errors:
        raise ValueError('\n'.join(sorted(set(errors))))
    # Some old makefiles leave the stylesheet in the source directory.  It is
    # only available for localization after the ordinary resource-copy pass.
    newly_localized = localize_official_styles(output)
    localized.extend(newly_localized)
    if newly_localized:
        extra_copied, checked_count, _extra_links = prepare_resources(
            sgml_dir, output, _adapt_styles=False)
        copied.extend(extra_copied)
    else:
        checked_count = len(checked)
    adapted = adapt_legacy_css(output, class_elements, body_containers) if _adapt_styles else []
    design_links = inject_design_links(output)
    if style_report is not None:
        Path(style_report).write_text(json.dumps(adapted, indent=2) + '\n')
    if localization_report is not None:
        Path(localization_report).write_text(json.dumps(localized, indent=2) + '\n')
    return sorted(copied), checked_count, design_links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sgml_dir', type=Path)
    parser.add_argument('--output-dir', type=Path, help='prepare an already published output directory')
    parser.add_argument('--localization-report', type=Path, help='record before/after hashes of localized CSS references')
    parser.add_argument('--style-report', type=Path, help='record exact legacy CSS selector compatibility edits')
    args = parser.parse_args()
    try:
        copied, checked, design_links = prepare_resources(
            args.sgml_dir, args.output_dir, args.localization_report, args.style_report)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'HTML resource verification failed:\n{exc}', file=sys.stderr)
        return 1
    print(f'HTML resources: {checked} local files verified; {len(copied)} copied from source; '
          f'{len(design_links)} direct design links injected.')
    for relative in copied:
        print(f'  copied {relative}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
