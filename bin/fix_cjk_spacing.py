#!/usr/bin/env python3
"""Surgically remove spurious whitespace between full-width chars in DocBook
sources (SGML and XML flavours alike), so every downstream render — HTML,
PDF, text extraction — is clean by construction.

Hard-wrapped prose collapses each interior newline+indent into a single
U+0020 at render time; when the effective characters across the wrap are
both full-width the space is spurious (「多态结 果类型」「。 但是」).
The rule set lives in bin/cjk_spacing.py and is shared verbatim with the
print post-processor (bin/prepare_chinese_pdf.py), which stays in place as
a belt-and-suspenders pass.

This tool never re-serializes: it tokenizes the raw file, resolves the
effective rendered neighbours of each interior whitespace run (across
inline elements; <xref> renders Chinese gentext; verbatim islands such as
<literal>/<programlisting> are atomic and never edited), and deletes the
run by byte offset when — and only when — drop_space() says its collapsed
space must not render.  Everything else stays byte-identical.

Semantics of the edits:
* verbatim elements (programlisting, screen, literal, synopsis, ...) are
  never touched; their real edge characters are used for classification;
* block boundaries (paragraph, list item, table cell, ...) stop neighbour
  resolution, so leading/trailing paragraph whitespace is preserved;
* transparent constructs (comments, PIs, indexterm, anchor, remark) render
  nothing and are looked through;
* em dash / ellipsis keep their spaces (zh title convention), Han<->Latin
  boundaries keep theirs (盘古之白).

Usage:
    fix_cjk_spacing.py [--write | --check] [-v] PATH [PATH...]

Default is a dry run reporting what would change.  --check exits 1 when
any removal remains (lint gate).  Idempotent by construction.
"""

from pathlib import Path
import argparse
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cjk_spacing import STRICT_RE, WS_RUN, drop_space, eff  # noqa: E402

HAN_SENTINEL = '\u4e00'  # <xref> renders 「第 X 节」-style gentext

# Verbatim content: never edited.  Block ones also stop neighbour
# resolution; the inline ones render in place and lend their real edge
# characters to the surrounding classification.
VERBATIM_BLOCK = frozenset((
    'programlisting', 'screen', 'synopsis', 'literallayout', 'address',
    'cmdsynopsis', 'funcsynopsis', 'classsynopsis', 'fieldsynopsis',
    'methodsynopsis', 'constructorsynopsis', 'destructorsynopsis',
))
VERBATIM_INLINE = frozenset((
    'literal', 'prompt', 'userinput', 'computeroutput', 'sgmltag',
))
# Rendered content is Chinese gentext even though the source element is empty.
GENTEXT = frozenset(('xref',))
# Renders nothing; neighbour resolution looks straight through.
TRANSPARENT = frozenset(('indexterm', 'anchor', 'remark', 'beginpage'))
# Index terms render into the back-of-book index joined by generated
# full-width separators, so whitespace at the very start/end of their
# content is junk next to the separator.
INDEX_TEXT = frozenset(('primary', 'secondary', 'tertiary', 'see', 'seealso'))
# SGML EMPTY elements whose open tag is the whole element.
EMPTY_ELEMENTS = frozenset((
    'xref', 'anchor', 'graphic', 'inlinegraphic', 'imagedata', 'videodata',
    'audiodata', 'textdata', 'colspec', 'spanspec', 'co', 'coref', 'area',
    'sbr',
))
# Inline elements whose subtrees render in place; resolution uses their
# edge characters, and they contribute edges to their parent.  Anything
# not classified here is treated as a block boundary (stops resolution).
INLINE = frozenset((
    'emphasis', 'phrase', 'quote', 'foreignphrase', 'wordasword',
    'citetitle', 'citation', 'firstterm', 'glossterm', 'trademark',
    'abbreviation', 'acronym', 'productname', 'personname', 'filename',
    'command', 'replaceable', 'parameter', 'option', 'optional', 'argument',
    'systemitem', 'classname', 'methodname', 'varname', 'function', 'type',
    'constant', 'envar', 'email', 'ulink', 'link', 'subscript',
    'superscript', 'keycap', 'keycode', 'keycombo', 'keysym', 'mousebutton',
    'guibutton', 'guilabel', 'guimenu', 'guimenuitem', 'guisubmenu',
    'guiicon', 'shortcut', 'accel', 'symbol', 'token', 'markup', 'medialabel',
    'database', 'hardware', 'interface', 'interfacename', 'returnvalue',
    'structfield', 'structname', 'void', 'lineannotation', 'errortext',
    'errortype',
))

_NAME_RE = re.compile(r'[A-Za-z_][A-Za-z0-9_.:-]*')


class ParseError(Exception):
    pass


class Node:
    """One element (or the document root): children plus resolved edges."""

    __slots__ = ('name', 'children', 'first', 'last', 'kind')

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind        # 'inline' | 'gentext' | 'transparent' | 'block'
        self.children = []      # Node or (tag, start, end) tuples
        self.first = self.last = None  # effective rendered chars


def _classify(name):
    if name in GENTEXT:
        return 'gentext'
    if name in TRANSPARENT:
        return 'transparent'
    if name in VERBATIM_INLINE or name in INLINE:
        return 'inline'
    return 'block'  # includes VERBATIM_BLOCK and anything unknown


def _scan_tag(s, i):
    """Parse one markup construct starting at s[i] == '<'.

    Returns (kind, name, j); j is just past the construct.  kind is one of
    'open', 'empty-open', 'close', 'shortclose', 'comment', 'pi', 'decl',
    'cdata', 'msection'.
    """
    n = len(s)
    if s.startswith('<!--', i):
        j = s.find('-->', i + 4)
        if j < 0:
            raise ParseError('unterminated comment')
        return 'comment', None, j + 3
    if s.startswith('<![CDATA[', i):
        j = s.find(']]>', i + 9)
        if j < 0:
            raise ParseError('unterminated CDATA')
        return 'cdata', None, j + 3
    if s.startswith('<![', i):
        depth, k = 0, i
        while k < n:
            if s.startswith('<![', k):
                depth += 1
                k = s.find('[', k) + 1
            elif s.startswith(']]>', k):
                depth -= 1
                k += 3
                if depth == 0:
                    return 'msection', None, k
            else:
                k += 1
        raise ParseError('unterminated marked section')
    if s.startswith('<?', i):
        j = s.find('?>', i)
        if j < 0:
            j = s.find('>', i)
        if j < 0:
            raise ParseError('unterminated processing instruction')
        return 'pi', None, j + (2 if s[j:j + 2] == '?>' else 1)
    if s.startswith('<!', i):
        # DOCTYPE and friends: respect comments, quotes and the internal
        # [ ] subset.
        k, quote, bracket = i + 2, '', 0
        while k < n:
            if s.startswith('<!--', k):
                k = s.find('-->', k + 4)
                if k < 0:
                    raise ParseError('unterminated comment in declaration')
                k += 3
                continue
            c = s[k]
            if quote:
                if c == quote:
                    quote = ''
            elif c in '"\'':
                quote = c
            elif c == '[':
                bracket += 1
            elif c == ']':
                bracket -= 1
            elif c == '>' and bracket <= 0:
                return 'decl', None, k + 1
            k += 1
        raise ParseError('unterminated declaration')
    if s.startswith('</', i):
        if s.startswith('</>', i):
            return 'shortclose', None, i + 3
        m = _NAME_RE.match(s, i + 2)
        if not m:
            raise ParseError(f'bad close tag at offset {i}')
        j = s.find('>', m.end())
        if j < 0:
            raise ParseError('unterminated close tag')
        return 'close', m.group(0).lower(), j + 1
    m = _NAME_RE.match(s, i + 1)
    if not m:
        raise ParseError(f'bad markup at offset {i}')
    name = m.group(0).lower()
    k, quote = m.end(), ''
    while k < n:
        c = s[k]
        if quote:
            if c == quote:
                quote = ''
        elif c in '"\'':
            quote = c
        elif c == '>':
            return ('empty-open' if s[k - 1] == '/' else 'open'), name, k + 1
        k += 1
    raise ParseError('unterminated tag')


def _parse_range(s, lo, hi, root):
    """Tokenize s[lo:hi] into root's children; tolerant of SGML omissions."""
    anomalies = []
    stack = [root]
    open_names = [root.name]
    text_start = lo
    i = lo

    def flush_text(end):
        nonlocal text_start
        if end > text_start:
            stack[-1].children.append(('text', text_start, end))

    while i < hi:
        if s[i] == '<':
            nxt = i + 1
            if nxt < hi and s[nxt] not in '!/?' and not _NAME_RE.match(s, nxt):
                i += 1  # bare '<' in prose (SGML-era leniency): plain text
                continue
        elif s[i] != '<':
            j = s.find('<', i)
            if j < 0 or j >= hi:
                flush_text(hi)
                break
            i = j
            continue
        flush_text(i)
        kind, name, j = _scan_tag(s, i)
        if j > hi:
            anomalies.append((i, 'construct crosses range end'))
            break
        if kind in ('comment', 'pi', 'decl'):
            pass  # renders nothing; invisible to neighbour resolution
        elif kind == 'cdata':
            stack[-1].children.append(('verbatim-text', i, j))
        elif kind == 'msection':
            node = Node('#msection', 'wrap')
            stack[-1].children.append(node)
            # Content starts after the keyword/condition bracket, i.e. the
            # first '[' past the '<![' opener.
            anomalies.extend(_parse_range(s, s.find('[', i + 3) + 1, j - 3, node))
        elif kind == 'open':
            node = Node(name, _classify(name))
            stack[-1].children.append(node)
            if name not in EMPTY_ELEMENTS:
                stack.append(node)
                open_names.append(name)
        elif kind == 'empty-open':
            stack[-1].children.append(Node(name, _classify(name)))
        else:  # close / shortclose
            if kind == 'shortclose':
                if len(stack) > 1:
                    stack.pop()
                    open_names.pop()
                else:
                    anomalies.append((i, 'short close with empty stack'))
            elif name not in open_names:
                anomalies.append((i, f'stray close </{name}>'))
            else:
                while open_names[-1] != name:
                    anomalies.append((i, f'implicitly closed <{open_names[-1]}>'))
                    stack.pop()
                    open_names.pop()
                stack.pop()
                open_names.pop()
        i = text_start = j
    else:
        flush_text(hi)

    while len(stack) > 1:
        anomalies.append((hi, f'unclosed <{open_names[-1]}>'))
        stack.pop()
        open_names.pop()
    return anomalies


def _last_char(seg):
    for k in range(len(seg) - 1, -1, -1):
        if not seg[k].isspace():
            return seg[k]
    return None


def _first_char(seg):
    for ch in seg:
        if not ch.isspace():
            return ch
    return None


def _resolve_edges(node, s):
    """Post-order: effective first/last rendered char of every subtree."""
    if node.kind == 'gentext':
        node.first = node.last = HAN_SENTINEL
        return
    first = last = None
    for child in node.children:
        if isinstance(child, Node):
            _resolve_edges(child, s)
            if child.kind in ('transparent', 'block'):
                continue  # invisible / renders as its own block
            if child.first is not None and first is None:
                first = child.first
            if child.last is not None:
                last = child.last
        else:
            _, lo, hi = child
            f, l = _first_char(s[lo:hi]), _last_char(s[lo:hi])
            if f is not None and first is None:
                first = f
            if l is not None:
                last = l
    node.first, node.last = first, last


def _boundary_left(items, idx, s):
    """Effective rendered char immediately left of items[idx] (an element)."""
    k = idx - 1
    while k >= 0:
        item = items[k]
        if isinstance(item, Node):
            if item.kind == 'transparent':
                k -= 1
                continue
            if item.kind == 'block':
                return None
            if item.last is None:
                k -= 1
                continue
            return item.last
        c = _last_char(s[item[1]:item[2]])
        if c is not None:
            return c
        k -= 1
    return None


def _boundary_right(items, idx, s):
    """Effective rendered char immediately right of items[idx] (an element)."""
    k = idx + 1
    while k < len(items):
        item = items[k]
        if isinstance(item, Node):
            if item.kind == 'transparent':
                k += 1
                continue
            if item.kind == 'block':
                return None
            if item.first is None:
                k += 1
                continue
            return item.first
        c = _first_char(s[item[1]:item[2]])
        if c is not None:
            return c
        k += 1
    return None


def _resolve_left(items, idx, pos, s):
    """Effective rendered char immediately left of items[idx][:pos]."""
    _, lo, _ = items[idx]
    c = _last_char(s[lo:pos])
    if c is not None:
        return c
    return _boundary_left(items, idx, s)


def _resolve_right(items, idx, pos, s):
    """Effective rendered char immediately right of items[idx][pos:]."""
    _, _, hi = items[idx]
    c = _first_char(s[pos:hi])
    if c is not None:
        return c
    return _boundary_right(items, idx, s)


def _child_edge_runs(item, s):
    """Proper-prefix/suffix whitespace runs at the rendered edges of an
    inline child's own content: whitespace between the child's open tag and
    its first char (or last char and close tag) renders against the parent's
    neighbours across those tags."""
    lead = trail = None
    for it in item.children:
        if isinstance(it, Node):
            if it.kind == 'transparent':
                continue
            break  # content begins with a rendered element
        m = WS_RUN.match(s, it[1], it[2])
        if m and m.end() < it[2]:
            lead = m
        break
    for it in reversed(item.children):
        if isinstance(it, Node):
            if it.kind == 'transparent':
                continue
            break
        for m in WS_RUN.finditer(s, it[1], it[2]):
            if m.end() == it[2] and m.start() > it[1]:
                trail = m
        break
    return lead, trail


def _collect(node, s, deletions, stats):
    if node.name in VERBATIM_BLOCK or node.name in VERBATIM_INLINE \
            or node.kind == 'gentext':
        return
    # TRANSPARENT elements render out of line (e.g. indexterm renders into
    # the back-of-book index), so their inner text still gets cleaned; only
    # their inline neighbours look through them.
    for idx, item in enumerate(node.children):
        if isinstance(item, Node):
            _collect(item, s, deletions, stats)
            if (item.kind in ('inline', 'wrap')
                    and item.name not in VERBATIM_INLINE):
                # Whitespace just inside an inline child's tags renders
                # between the parent's neighbours and the child's edges.
                lead, trail = _child_edge_runs(item, s)
                if lead is not None:
                    lctx = _boundary_left(node.children, idx, s)
                    if lctx is not None and item.first is not None \
                            and drop_space(lctx, item.first):
                        deletions.append((lead.start(), lead.end()))
                        stats['fw-fw'] += 1
                if trail is not None:
                    rctx = _boundary_right(node.children, idx, s)
                    if rctx is not None and item.last is not None \
                            and drop_space(item.last, rctx):
                        deletions.append((trail.start(), trail.end()))
                        stats['fw-fw'] += 1
            continue
        if item[0] == 'verbatim-text':
            continue
        lo, hi = item[1], item[2]
        for m in WS_RUN.finditer(s, lo, hi):
            left = _resolve_left(node.children, idx, m.start(), s)
            if left is None:
                continue
            right = _resolve_right(node.children, idx, m.end(), s)
            if right is None:
                continue
            if drop_space(left, right):
                deletions.append((m.start(), m.end()))
                stats['strict-punct' if (STRICT_RE.match(left) or STRICT_RE.match(right))
                     else 'fw-fw'] += 1
    if node.name in INDEX_TEXT:
        _strip_index_edge_ws(node, s, deletions, stats)


def _strip_index_edge_ws(node, s, deletions, stats):
    """Delete whitespace runs touching the start/end of an index term's
    content: the index joins entries with generated separators, so edge
    whitespace only produces a spurious gap before them."""
    def first_text():
        for item in node.children:
            if isinstance(item, Node):
                if item.kind == 'transparent':
                    continue
                return None  # content begins with an element
            return item
        return None

    def last_text():
        for item in reversed(node.children):
            if isinstance(item, Node):
                if item.kind == 'transparent':
                    continue
                return None
            return item
        return None

    item = first_text()
    if item:
        lo, hi = item[1], item[2]
        m = WS_RUN.match(s, lo, hi)
        if m:
            deletions.append((m.start(), m.end()))
            stats['fw-fw'] += 1
    item = last_text()
    if item:
        lo, hi = item[1], item[2]
        for m in WS_RUN.finditer(s, lo, hi):
            if m.end() == hi:
                deletions.append((m.start(), m.end()))
                stats['fw-fw'] += 1


def fix_text(s):
    """Return (new_text, deletions, anomalies, stats)."""
    root = Node('#document', 'block')
    anomalies = _parse_range(s, 0, len(s), root)
    _resolve_edges(root, s)
    deletions = []
    stats = {'fw-fw': 0, 'strict-punct': 0}
    _collect(root, s, deletions, stats)
    if not deletions:
        return s, deletions, anomalies, stats
    deletions.sort()
    out, cut = [], 0
    for start, end in deletions:
        if start < cut:
            continue
        out.append(s[cut:start])
        cut = end
    out.append(s[cut:])
    new = ''.join(out)
    # Invariant: non-whitespace content is byte-identical, only ws removed.
    assert ''.join(c for c in s if not c.isspace()) == \
           ''.join(c for c in new if not c.isspace()), 'content invariant'
    return new, deletions, anomalies, stats


def iter_files(paths):
    for p in map(Path, paths):
        if p.is_dir():
            for f in sorted(p.rglob('*')):
                if f.suffix not in ('.sgml', '.xml'):
                    continue
                if 'html' in f.parts or f.name.startswith('stylesheet'):
                    continue
                yield f
        elif p.suffix in ('.sgml', '.xml') and not p.name.startswith('stylesheet'):
            yield p


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument('paths', nargs='+')
    cli.add_argument('--write', action='store_true', help='apply fixes in place')
    cli.add_argument('--check', action='store_true',
                     help='exit 1 when any removal remains (lint gate)')
    cli.add_argument('-v', '--verbose', action='store_true')
    args = cli.parse_args(argv)

    total_files = total_removals = anomalies_total = skipped = 0
    for f in iter_files(args.paths):
        try:
            s = f.read_text(encoding='utf-8')
        except UnicodeDecodeError as exc:
            print(f'{f}: SKIP (not utf-8: {exc})')
            skipped += 1
            continue
        try:
            new, deletions, anomalies, stats = fix_text(s)
        except ParseError as exc:
            print(f'{f}: SKIP (parse error: {exc})')
            skipped += 1
            continue
        anomalies_total += len(anomalies)
        if deletions:
            total_files += 1
            total_removals += len(deletions)
            extra = ''
            if args.verbose:
                line = s.count('\n', 0, deletions[0][0]) + 1
                extra = f'  first@L{line}'
            print(f'{f}: {len(deletions)} removals '
                  f'(fw-fw {stats["fw-fw"]}, punct {stats["strict-punct"]}){extra}')
            if args.write:
                # Idempotency self-check before touching the file.
                assert not fix_text(new)[1], f'{f}: not idempotent'
                f.write_text(new, encoding='utf-8')
        if anomalies and args.verbose:
            for pos, msg in anomalies[:5]:
                print(f'  anomaly L{s.count(chr(10), 0, pos) + 1}: {msg}')
    print(f'TOTAL: {total_files} files, {total_removals} removals '
          f'{"written" if args.write else "pending"}, '
          f'{anomalies_total} parse anomalies, {skipped} skipped')
    if args.check and (total_removals or skipped):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
