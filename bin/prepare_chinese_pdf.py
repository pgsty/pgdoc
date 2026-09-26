#!/usr/bin/env python3
"""Print-only fixes for Chinese prose in generated XSL-FO.

Two problems are fixed by changing the generated print layout, never the
SGML, identifiers, links, or whitespace-preserving code examples:

1. FOP can otherwise treat an entire list of Latin identifiers separated by
   U+3001 as one word and paint it outside the page; insert invisible
   line-break opportunities after full-width separators, except where the
   break would put a closing punctuation mark at the start of the next
   line (kinsoku, e.g. between "）" and "。").
2. Hard-wrapped SGML sources collapse each newline into a U+0020, so a wrap
   between two full-width characters renders as a spurious space in the PDF
   (e.g. "多态结 果类型").  Drop exactly those spaces: a space is removed
   when both neighbours are full-width, or when either side is full-width
   punctuation.  Curly quotes only lose their space next to other
   full-width text, so Latin phrases keep theirs ('word “term”').  Em dash
   and ellipsis never trigger removal because zh titles space them
   deliberately ("模块 &mdash; 描述").  Han<->Latin boundaries keep their
   space, matching the corpus convention.
"""

from pathlib import Path
import argparse
import re
import xml.etree.ElementTree as ET


_HAN = '\u3400-\u9fff\uf900-\ufaff'
# Full-width punctuation that never takes an adjacent space in running text.
_STRICT = ('\u3001\u3002\u3008\u3009\u300a\u300b\u3010\u3011\u3014\u3015'
           '\u3017-\u301c\u301f\u3030\u3031\u303b-\u303f'
           '\uff01-\uff0f\uff1a-\uff1f\uff3b-\uff40\uff5b-\uff60'
           '\uffe0-\uffe5')
# Double/single quotation marks rendered by <quote>/l10n gentext.
_QUOTES = '\u201c\u201d\u2018\u2019\u301d\u301e'
# U+2014 (em dash) and U+2026 (ellipsis) are deliberately absent from both
# sets; see the module docstring.
_FW_RE = re.compile(f'[{_HAN}\u3001-\u303f\uff01-\uff60\uffe0-\uffe5{_QUOTES}]')
_STRICT_RE = re.compile(f'[{_STRICT}]')
_QUOTES_RE = re.compile(f'[{_QUOTES}]')
_WS_RUN = re.compile(r'[ \t\n\r]+')
_SKIP = ' \t\n\r\u200b'
# 行首禁则字符：break_prose 插入的 \u200b 不得把断行机会放在它们之前，
# 否则 FOP 会在「）。」之间断行，让下一行以句号开头。
_NO_LINE_START = ('\u3001\u3002\uff0c\uff1b\uff1a\uff1f\uff01\uff09'
                  '\u3008\u3009\u300a\u300b\u3010\u3011\u3014\u3015'
                  '\u3017-\u301f\u3003-\u3006\u201c\u201d\u2018\u2019'
                  '\u2026\u2014\uff5b\uff5d')
_NOSTART_RE = re.compile(f'[{_NO_LINE_START}]')
# 断行机会插入：字符类别 + 不与既有 \u200b 重复 + 不得把禁则字符推到行首
_BREAK_RE = re.compile(
    r'(?:[、，；。）_.]|(?<=[A-Za-z])-(?=[A-Za-z]))(?!\u200b)(?![%s])'
    % _NO_LINE_START)


def _drop_space(left, right):
    """True when the collapsed space between the two chars must not render."""
    if not left or not right:
        return False
    l_fw = bool(_FW_RE.match(left))
    r_fw = bool(_FW_RE.match(right))
    if _STRICT_RE.match(left) or _STRICT_RE.match(right):
        return True
    if l_fw and r_fw:
        return True
    return bool((_QUOTES_RE.match(left) and r_fw)
                or (_QUOTES_RE.match(right) and l_fw))


def _eff(s, reverse=False):
    if not s:
        return None
    it = reversed(s) if reverse else iter(s)
    for c in it:
        if c not in _SKIP:
            return c
    return None


class _Edge:
    """First/last rendered character of a subtree, plus strip targets."""
    __slots__ = ('first', 'last', 'first_ref', 'last_ref',
                 'first_prot', 'last_prot')

    def __init__(self):
        self.first = self.last = None
        self.first_ref = self.last_ref = None
        self.first_prot = self.last_prot = True


def _ref_text(ref):
    el, which, child = ref
    return el.text if which == 'text' else child.tail


def _ref_set(ref, value):
    el, which, child = ref
    if which == 'text':
        el.text = value
    else:
        child.tail = value


def _strip_ref_end(ref, leading):
    s = _ref_text(ref)
    if not s:
        return False
    # stylesheet-fo.xsl already inserts U+200B break sentinels during XSLT,
    # so a whitespace run at a chunk edge can be followed (trailing side) or
    # preceded (leading side) by sentinels.  Strip only the real whitespace
    # and keep the sentinels: they are invisible and a break opportunity at
    # the seam stays valid once the spurious space is gone.
    if leading:
        new = re.sub(r'^(\u200b*)[ \t\n\r]+', r'\1', s)
    else:
        new = re.sub(r'[ \t\n\r]+(\u200b*)$', r'\1', s)
    if new != s:
        _ref_set(ref, new)
        return True
    return False


def _annotate_into(edge, text, ref, protected):
    """Fold one text chunk into the edge; return its last char or None."""
    if text is None:
        return None
    f = _eff(text)
    if f is not None and edge.first is None:
        edge.first, edge.first_ref, edge.first_prot = f, ref, protected
    l = _eff(text, reverse=True)
    if l is not None:
        edge.last, edge.last_ref, edge.last_prot = l, ref, protected
        return l
    return None


def _process_chunks(el, child_edges, removed):
    """Drop spurious spaces between the direct text chunks of one element.

    Whitespace can sit at the trailing end of the left chunk, in whitespace-
    only chunks in between, and at the leading end of the right chunk; FOP
    collapses the whole run to a single rendered space, so all of it goes.
    Runs that reach into whitespace-preserving subtrees are never touched.
    """
    seq = [('text', (el, 'text', None))] if el.text is not None else []
    for child, ce in zip(el, child_edges):
        seq.append(('el', child, ce))
        if child.tail is not None:
            seq.append(('text', (el, 'tail', child)))

    for item in seq:
        if item[0] != 'text':
            continue
        ref = item[1]
        s = _ref_text(ref)
        if not s or not _WS_RUN.search(s):
            continue

        def repl(m, s=s):
            prev = _eff(s[:m.start()], reverse=True)
            nxt = _eff(s[m.end():])
            if prev and nxt and _drop_space(prev, nxt):
                removed[0] += 1
                return ''
            return m.group(0)

        new = _WS_RUN.sub(repl, s)
        if new != s:
            _ref_set(ref, new)

    left_char = None
    left_ref = None     # trailing-strip target of the previous content chunk
    middles = []        # whitespace-only text chunks since then

    def resolve(right_char, right_ref):
        nonlocal left_char, left_ref, middles
        if left_char is None or not _drop_space(left_char, right_char):
            middles = []
            return
        changed = False
        if left_ref is not None:
            changed |= _strip_ref_end(left_ref, leading=False)
        for mref in middles:
            if _ref_text(mref):
                _ref_set(mref, '')
                changed = True
        if right_ref is not None:
            changed |= _strip_ref_end(right_ref, leading=True)
        if changed:
            removed[0] += 1
        middles = []

    for item in seq:
        if item[0] == 'text':
            ref = item[1]
            first = _eff(_ref_text(ref) or '')
            if first is None:
                middles.append(ref)
                continue
            resolve(first, ref)
            left_char = _eff(_ref_text(ref), reverse=True)
            left_ref = ref
        else:
            _, child, ce = item
            if ce is None or ce.first is None:
                continue
            resolve(ce.first, None if ce.first_prot else ce.first_ref)
            left_char = ce.last
            left_ref = None if ce.last_prot else ce.last_ref


def _despace_pass(el, protected, removed):
    """Post-order single pass fixing chunks of every non-preserve element."""
    if not isinstance(el.tag, str):
        return None
    protected = (protected
                 or el.get('white-space-treatment') == 'preserve'
                 or el.tag.endswith('}instream-foreign-object'))
    child_edges = [_despace_pass(child, protected, removed) for child in el]
    if not protected:
        _process_chunks(el, child_edges, removed)
    edge = _Edge()
    _annotate_into(edge, el.text, (el, 'text', None), protected)
    for child, ce in zip(el, child_edges):
        if ce is not None and ce.first is not None and edge.first is None:
            edge.first, edge.first_ref, edge.first_prot = \
                ce.first, ce.first_ref, ce.first_prot
        tail_last = _annotate_into(edge, child.tail, (el, 'tail', child),
                                   protected)
        if ce is not None and ce.last is not None and tail_last is None:
            edge.last, edge.last_ref, edge.last_prot = \
                ce.last, ce.last_ref, ce.last_prot
    if edge.first is None and edge.last is None:
        return None
    return edge


def _kinsoku_pass(root):
    """移除会把断行机会放到行首禁则字符之前的 \u200b。

    break_prose 按字符类别插入 \u200b，看不见跨节点的下一个字符；
    「）。」之间的 \u200b 会让 FOP 把句号断到行首。文档序单遍扫描：
    \u200b 之后（含跨节点）紧跟禁则字符即删除该 \u200b。返回删除数量。
    """
    holders = []

    def walk(el, protected):
        if not isinstance(el.tag, str):
            return
        protected = (protected
                     or el.get('white-space-treatment') == 'preserve'
                     or el.tag.endswith('}instream-foreign-object'))
        holders.append((el, None, protected))
        for child in el:
            walk(child, protected)
            holders.append((el, child, protected))

    walk(root, False)

    def text_of(h):
        el, child, _ = h
        return el.text if child is None else child.tail

    def set_text(h, value):
        el, child, _ = h
        if child is None:
            el.text = value
        else:
            child.tail = value

    removed = 0
    for idx, h in enumerate(holders):
        if h[2]:
            continue
        t = text_of(h)
        if not t or '\u200b' not in t:
            continue

        def strip_bad(m):
            nxt = t[m.end():m.end() + 1]
            return '' if (nxt and _NOSTART_RE.match(nxt)) else m.group(0)

        new = re.sub(r'\u200b+', strip_bad, t)
        if new.endswith('\u200b'):
            nxt = None
            for h2 in holders[idx + 1:]:
                c = _eff(text_of(h2))
                if c is not None:
                    nxt = c
                    break
            if nxt is not None and _NOSTART_RE.match(nxt):
                new = new.rstrip('\u200b')
        if new != t:
            removed += t.count('\u200b') - new.count('\u200b')
            set_text(h, new)
    return removed


def prepare(path, cjk_family='Alibaba PuHuiTi 3.0'):
    path = Path(path)
    for _, (prefix, uri) in ET.iterparse(path, events=('start-ns',)):
        if not prefix.startswith('ns'):
            ET.register_namespace(prefix, uri)
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    tree = ET.parse(path, parser=parser)
    removed = [0]
    _despace_pass(tree.getroot(), False, removed)
    added = 0

    def break_prose(text):
        nonlocal added
        if not text:
            return text
        # Idempotent if the same FO is rendered more than once; same-node
        # kinsoku via the lookahead, cross-node by _kinsoku_pass below.
        broken = _BREAK_RE.sub(lambda m: m[0] + '\u200b', text)
        added += broken.count('\u200b') - text.count('\u200b')
        return broken

    def visit(node, preserve=False, in_cell=False, centered_cell=False):
        if not isinstance(node.tag, str):
            return
        preserve = (preserve or node.get('white-space-treatment') == 'preserve'
                    or node.tag.endswith('}instream-foreign-object'))
        in_cell = in_cell or node.tag.endswith('}table-cell')
        centered_cell = centered_cell or (node.tag.endswith('}table-cell') and node.get('text-align') == 'center')
        family = node.get('font-family', '')
        if (node.tag.endswith('}inline') and cjk_family in [x.strip() for x in family.split(',')]
                and family != cjk_family
                and re.search(r'[\u3400-\u9fff]', ''.join(node.itertext()))):
            # Use the CJK font's own metrics for translated inline parameters.
            node.set('font-family', cjk_family)
        if (in_cell and not preserve and node.tag.endswith('}inline') and not len(node)
                and re.fullmatch(r'[A-Za-z0-9]{20,}', (node.text or '').strip())):
            # Long type names such as anycompatiblemultirange must fit the
            # datatype column without introducing breaks inside the name.
            node.set('font-size', '8.5pt')
        if (preserve and node.tag.endswith('}block') and family
                and cjk_family in [x.strip() for x in family.split(',')]
                and family != cjk_family
                and re.search(r'[^\s\u200b]{70,}', ''.join(node.itertext()))):
            # Preserve verbatim separators and examples, including oid2name's
            # wide dashed table rule; only their print size changes.
            node.set('font-size', '8.5pt')
        if in_cell and not preserve and node.tag.endswith('}block') and not len(node):
            value = (node.text or '').strip().replace('\u200b', '')
            # Compact, otherwise unbreakable values in the equal-width columns
            # used by the datatype and replication comparison tables.
            if (re.fullmatch(r'[A-Za-z0-9_:+.\-]{9,}', value)
                    or re.search(r'\d{16,}', value)
                    or (centered_cell and re.search(r'[A-Za-z]{8,}', value))):
                node.set('font-size', '7.8pt' if centered_cell else '8.5pt')
        if not preserve:
            node.text = break_prose(node.text)
        for child in node:
            visit(child, preserve, in_cell, centered_cell)
            if not preserve:
                child.tail = break_prose(child.tail)
        if node.tag.endswith('}list-item-label'):
            for child in node:
                if child.tag.endswith('}block') and re.fullmatch(r'\d{2,}\.\u200b?', (child.text or '').strip()):
                    child.set('font-size', '8.9pt')

    visit(tree.getroot())
    removed[0] += _kinsoku_pass(tree.getroot())
    temporary = path.with_name(path.name + '.linebreaks.tmp')
    tree.write(temporary, encoding='utf-8', xml_declaration=True)
    temporary.replace(path)
    return added, removed[0]


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument('fo', type=Path)
    cli.add_argument('--cjk-family', default='Alibaba PuHuiTi 3.0')
    args = cli.parse_args()
    added, removed = prepare(args.fo, args.cjk_family)
    print(f'Chinese PDF: added {added} prose line-break opportunities, '
          f'removed {removed} spurious CJK spaces (incl. kinsoku).')
