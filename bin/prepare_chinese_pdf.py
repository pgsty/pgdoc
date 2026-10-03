#!/usr/bin/env python3
"""Print-only fixes for Chinese prose in generated XSL-FO.

Two problems are fixed by changing the generated print layout, never the
SGML, identifiers, links, or whitespace-preserving code examples:

1. FOP can otherwise treat an entire list of Latin identifiers separated by
   U+3001 as one word and paint it outside the page; insert invisible
   line-break opportunities after full-width separators, except where the
   break would put a closing punctuation mark at the start of the next
   line (kinsoku, e.g. between "）" and "。").  Sentinels are deliberately
   NOT inserted after "_", "." or between hyphenated letters: FOP breaks
   between CJK characters and at Han<->Latin boundaries natively (verified
   on FOP 2.11), while sentinels inside identifiers, section numbers and
   version strings split them across lines ("pg_\u200bdump", "32.\u200b15").
   A sentinel after "/" between alphanumerics keeps long URLs and paths
   breakable at component boundaries.
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
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cjk_spacing import (FW_RE as _FW_RE, QUOTES_RE as _QUOTES_RE,  # noqa: E402
                         STRICT_RE as _STRICT_RE, WS_RUN as _WS_RUN,
                         eff as _eff, drop_space as _drop_space,
                         normalize_prose as _normalize_prose)

# 行首禁则字符：break_prose 插入的 \u200b 不得把断行机会放在它们之前，
# 否则 FOP 会在「）。」之间断行，让下一行以句号开头。
_NO_LINE_START = ('\u3001\u3002\uff0c\uff1b\uff1a\uff1f\uff01\uff09'
                  '\u3008\u3009\u300a\u300b\u3010\u3011\u3014\u3015'
                  '\u3017-\u301f\u3003-\u3006\u201c\u201d\u2018\u2019'
                  '\u2026\u2014\uff5b\uff5d')
_NOSTART_RE = re.compile(f'[{_NO_LINE_START}]')
# 断行机会插入：字符类别 + 不与既有 \u200b 重复 + 不得把禁则字符推到行首。
# 注意：正文（_BREAK_RE）故意不含 "_"、"." 与字母间连字符——它们会把标识符/节号/
# 版本号拆到两行；FOP 本身可在汉字间与汉拉边界断行，无需在这些 token 内部制造断点。
# "/" 断点仅当两侧至少各有两个字母数字时插入（URL/长路径按组件边界断行），
# 以免把 I/O、A/B、客户端/服务器 之类的短复合词拆开。
_BREAK_RE = re.compile(
    r'(?:[、，；。）”’]|(?<=[A-Za-z0-9]{2})/(?=[A-Za-z0-9]{2}))(?!\u200b)(?![%s])'
    % _NO_LINE_START)
# 表格单元格内沿用旧宽松类别：窄列装不下原子标识符，FOP 会溢出而不是折行
# （自动表格布局还会连带把代码示例列挤窄）。单元格里按 _ 和 . 断行是既定取舍。
_BREAK_RE_CELL = re.compile(
    r'(?:[、，；。）”’_.]|(?<=[A-Za-z])-(?=[A-Za-z]))(?!\u200b)(?![%s])'
    % _NO_LINE_START)


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


def _strip_inline_padding(el, leading, mono_family):
    """Trim wrapper padding without entering an atomic/preserved code node."""
    if (el.tag not in ('{http://www.w3.org/1999/XSL/Format}inline',
                       '{http://www.w3.org/1999/XSL/Format}basic-link')
            or el.get('white-space-treatment') == 'preserve'
            or mono_family in [s.strip() for s in el.get('font-family', '').split(',')]):
        return False
    chunks = [('text', (el, 'text', None))]
    for child in el:
        chunks.append(('el', child))
        chunks.append(('text', (el, 'tail', child)))
    changed = False
    for kind, ref in chunks if leading else reversed(chunks):
        if kind == 'el':
            return _strip_inline_padding(ref, leading, mono_family) or changed
        text = _ref_text(ref)
        changed = _strip_ref_end(ref, leading) or changed
        if _eff(text or '') is not None:
            break
    return changed


def _process_chunks(el, child_edges, removed, inserted=None, mono_family='Courier New'):
    """Drop spurious spaces between the direct text chunks of one element.

    Whitespace can sit at the trailing end of the left chunk, in whitespace-
    only chunks in between, and at the leading end of the right chunk; FOP
    collapses the whole run to a single rendered space, so all of it goes.
    Runs that reach into whitespace-preserving subtrees are never touched.
    """
    # pan-gu helpers for cross-node boundaries (see resolve below)
    _HAN_ADJ_RE = re.compile(r'[\u3400-\u9fff\uf900-\ufaff]')
    _LATIN_RE = re.compile(r'[A-Za-z0-9]')
    if inserted is None:
        inserted = [0]
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
    left_subtree = None
    middles = []        # whitespace-only text chunks since then

    def resolve(right_char, right_ref, right_text=None, right_subtree=None):
        nonlocal left_char, left_ref, middles
        if left_char is None:
            middles = []
            return
        if _drop_space(left_char, right_char):
            changed = False
            if left_ref is not None:
                changed |= _strip_ref_end(left_ref, leading=False)
            if left_subtree is not None:
                changed |= _strip_inline_padding(left_subtree, False, mono_family)
            for mref in middles:
                if _ref_text(mref):
                    _ref_set(mref, '')
                    changed = True
            if right_ref is not None:
                changed |= _strip_ref_end(right_ref, leading=True)
            if right_subtree is not None:
                changed |= _strip_inline_padding(right_subtree, True, mono_family)
            if changed:
                removed[0] += 1
            middles = []
            return
        if middles:
            middles = []
            return
        # Direct cross-node Han<->Latin/digit adjacency (no whitespace run
        # in between): pan-gu normalization for element boundaries, e.g.
        # 见<fo:inline>pg_dump</fo:inline>命令 -> 见 pg_dump 命令.
        if not (_HAN_ADJ_RE.match(left_char) and _LATIN_RE.match(right_char)
                or _LATIN_RE.match(left_char) and _HAN_ADJ_RE.match(right_char)

                                or (left_char in "]\\*)\"'>%&" and _HAN_ADJ_RE.match(right_char))):
            # Han next to a symbol-leading literal chunk (/dev, %APPDATA%,
            # --jobs, ~/.pgpass): insert when the literal really continues
            # with a word character.
            if _HAN_ADJ_RE.match(left_char):
                rt = right_text if right_text is not None else (_ref_text(right_ref) if right_ref is not None else '')
                rt = rt or ''
                if re.match(r'(?:~?/|%|--?|\$)[A-Za-z0-9_.]', rt):
                    s = _ref_text(left_ref) if left_ref is not None else None
                    r = rt
                    if (s and not s[-1] in ' \t\n\r\u200b'
                            and not r[0] in ' \t\n\r\u200b'):
                        _ref_set(left_ref, s + ' ')
                        inserted[0] += 1
            return
        if left_ref is not None:
            # Left side editable: append here.  A trailing whitespace on the
            # left, or leading whitespace/sentinel on the right, means the
            # boundary is already separated -- keeps the pass idempotent.
            s = _ref_text(left_ref)
            r = right_text if right_text is not None else (_ref_text(right_ref) if right_ref is not None else None)
            if (s and not s[-1] in ' \t\n\r\u200b'
                    and not (r and r[0] in ' \t\n\r\u200b')):
                _ref_set(left_ref, s + ' ')
                inserted[0] += 1
            return
        if right_ref is not None:
            s = _ref_text(right_ref)
            if s and not s[0] in ' \t\n\r\u200b':
                _ref_set(right_ref, ' ' + s)
                inserted[0] += 1

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
            left_subtree = None
        else:
            _, child, ce = item
            if (child.tag == '{http://www.w3.org/1999/XSL/Format}footnote'
                    and left_char is not None):
                # A superscript belongs to the preceding word. Move ordinary
                # wrapper padding after it, then settle the prose seam there.
                changed = False
                if left_ref is not None:
                    changed |= _strip_ref_end(left_ref, leading=False)
                if left_subtree is not None:
                    changed |= _strip_inline_padding(left_subtree, False, mono_family)
                for ref in middles:
                    text = _ref_text(ref) or ''
                    new = _WS_RUN.sub('', text)
                    if new != text:
                        _ref_set(ref, new)
                        changed = True
                if changed:
                    tail = child.tail or ''
                    nxt = _eff(tail)
                    if (nxt is not None and not _NOSTART_RE.match(nxt)
                            and nxt not in '.,;:!?)]}' and not tail[:1].isspace()):
                        child.tail = ' ' + tail
                    removed[0] += 1
                left_ref = left_subtree = None
                middles = []
                continue
            if ce is None or ce.first is None:
                continue
            resolve(ce.first, None if ce.first_prot else ce.first_ref,
                    _ref_text(ce.first_ref) if ce.first_ref is not None else None,
                    child)
            left_char = ce.last
            left_ref = None if ce.last_prot else ce.last_ref
            left_subtree = child


def _despace_pass(el, protected, removed, inserted=None, mono_family='Courier New'):
    """Post-order single pass fixing chunks of every non-preserve element."""
    if not isinstance(el.tag, str):
        return None
    protected = (protected
                 or el.get('white-space-treatment') == 'preserve'
                 or mono_family in [x.strip() for x in el.get('font-family', '').split(',')]
                 or el.tag.endswith('}instream-foreign-object'))
    child_edges = [_despace_pass(child, protected, removed, inserted, mono_family) for child in el]
    if not protected:
        _process_chunks(el, child_edges, removed, inserted, mono_family)
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
    # A footnote body is rendered outside this line, and its superscript
    # mark is not a prose digit. Resolve spacing across the anchor using
    # the adjoining body text instead. The body itself was processed above.
    if el.tag == '{http://www.w3.org/1999/XSL/Format}footnote':
        return None
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

    # Resolve the next rendered character once. Slicing the remaining holder
    # list at every trailing sentinel makes a full manual quadratic in size.
    following = [None] * len(holders)
    next_char = None
    for idx in range(len(holders) - 1, -1, -1):
        following[idx] = next_char
        char = _eff(text_of(holders[idx]))
        if char is not None:
            next_char = char

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
            nxt = following[idx]
            if nxt is not None and _NOSTART_RE.match(nxt):
                new = new.rstrip('\u200b')
        if new != t:
            removed += t.count('\u200b') - new.count('\u200b')
            set_text(h, new)
    return removed


def _parse_points(value, size_pt=None):
    match = re.fullmatch(r'([0-9.]+)(pt|in|mm|cm|pc|em|%)', value or '')
    if not match:
        return None
    unit = match.group(2)
    if unit in ('em', '%'):
        return None if size_pt is None else float(match.group(1)) * size_pt / (100 if unit == '%' else 1)
    return float(match.group(1)) * {'pt': 1, 'in': 72, 'mm': 72/25.4,
                                    'cm': 72/2.54, 'pc': 12}[unit]


def _body_width_limit(root):
    """Narrowest text column across the body masters, in points (None if unknown)."""
    limits = []
    for master in root.iter('{http://www.w3.org/1999/XSL/Format}simple-page-master'):
        if not master.get('master-name', '').startswith('body'):
            continue
        body = master.find('{http://www.w3.org/1999/XSL/Format}region-body')
        if body is None:
            continue
        values = [_parse_points(master.get('page-width', 'auto'))]
        for node in (master, body):
            for side in ('left', 'right'):
                values.append(_parse_points(
                    node.get('margin-' + side, node.get('margin', '0pt'))))
        if all(v is not None for v in values):
            width = values[0] - sum(values[1:])
            if width > 0:
                limits.append(width)
    return min(limits) if limits else None


def _fixed_block_spacing_pass(root):
    """Use the chosen paragraph gap without stretching nested list gaps.

    FOP 2.11 can undercount adjustable gaps in nested lists, then paint the
    expanded content below the body viewport without an overflow diagnostic.
    Preserve each optimum; only remove its compression/stretch range.
    """
    for flow in root.iter('{http://www.w3.org/1999/XSL/Format}flow'):
        if flow.get('flow-name') != 'xsl-region-body':
            continue
        for node in flow.iter():
            for side in ('before', 'after'):
                base = 'space-' + side + '.'
                optimum = node.get(base + 'optimum')
                if optimum is not None:
                    for bound in ('minimum', 'maximum'):
                        if base + bound in node.attrib:
                            node.set(base + bound, optimum)


def _image_height_limit(root):
    """Reserve room for a figure caption inside the portrait body masters."""
    def points(value):
        match = re.fullmatch(r'([0-9.]+)(pt|in|mm|cm|pc)', value)
        if not match:
            return None
        return float(match[1]) * {'pt': 1, 'in': 72, 'mm': 72/25.4,
                                  'cm': 72/2.54, 'pc': 12}[match[2]]

    limits = []
    for master in root.iter('{http://www.w3.org/1999/XSL/Format}simple-page-master'):
        if not master.get('master-name', '').startswith('body'):
            continue
        body = master.find('{http://www.w3.org/1999/XSL/Format}region-body')
        if body is None:
            continue
        values = [points(master.get('page-height', 'auto'))]
        for node in (master, body):
            values.extend(points(node.get('margin-' + side, node.get('margin', '0pt')))
                          for side in ('top', 'bottom'))
        if all(v is not None for v in values):
            limit = values[0] - sum(values[1:]) - 48
            if limit > 0:
                limits.append(limit)
    return min(limits) if limits else None


def _title_keep_pass(root):
    """Propagate title-wrapper keeps up to the section container.

    DocBook titlepages emit wrapper blocks (keep-together=always, direct
    child with keep-with-next) nested two levels under the section's
    id-bearing container block.  FOP only honours keep-with-next between
    sibling blocks and does not bubble it across nesting, so a title could
    still strand at a page bottom.  Climb from each wrapper to every
    intermediate <fo:block> ancestor (stopping at the id-bearing section
    container, which also holds the body) and stamp keep-with-next there.
    """
    parent = {c: p for p in root.iter() for c in p}
    stamped = 0
    for node in root.iter():
        if not (isinstance(node.tag, str) and node.tag.endswith('}block')
                and node.get('keep-together.within-column') == 'always'
                and node.get('margin-left') == '0pt'
                and any(isinstance(child.tag, str)
                        and child.tag.endswith('}block')
                        and child.get('keep-with-next.within-column')
                        for child in node)):
            continue
        anc = parent.get(node)
        while (isinstance(getattr(anc, 'tag', None), str)
                and anc.tag.endswith('}block')
                and anc.get('keep-with-next.within-column') is None):
            # DocBook emits the section heading as a standalone id-bearing
            # <fo:block> whose only child is the title wrapper chain; the
            # body paragraphs are its SIBLINGS.  Binding that id block to
            # the next sibling is exactly title<->first-paragraph, so stamp
            # it too -- but only when it holds nothing else.
            only_title = (anc.get('id') is None
                          or len([c for c in anc
                                  if isinstance(getattr(c, 'tag', None), str)]) == 1)
            if anc.get('id') is not None and not only_title:
                break
            anc.set('keep-with-next.within-column', 'always')
            stamped += 1
            anc = parent.get(anc)
        # Bind the heading unit to the first real body block from BOTH
        # directions: FOP honours keep-with-next through empty id-anchor
        # blocks only when they are stamped too (zero height, always safe),
        # and a few shapes (synopsis-first sections, table-first sections)
        # additionally need keep-with-previous on the first content block.
        node = anc if isinstance(getattr(anc, 'tag', None), str) else None
        if node is None:
            continue
        holder = parent.get(node) if node.get('id') is None else node
        if holder is None:
            continue
        sibs = [c for c in holder
                if isinstance(getattr(c, 'tag', None), str)] if node.get('id') else list(holder)
        start = sibs.index(node) + 1 if node in sibs else 0
        idx = start
        while idx < len(sibs):
            sib = sibs[idx]
            if not (isinstance(getattr(sib, 'tag', None), str)
                    and sib.tag.endswith('}block')):
                break
            if (sib.get('id') is not None
                    and not [c for c in sib if isinstance(getattr(c, 'tag', None), str)]
                    and not (sib.text or '').strip()):
                # empty anchor: keep it chained and look further
                if sib.get('keep-with-next.within-column') is None:
                    sib.set('keep-with-next.within-column', 'always')
                    stamped += 1
                idx += 1
                continue
            if sib.get('keep-with-next.within-column') is not None:
                # heading-chain block (title wrapper levels): skip past it
                idx += 1
                continue
            if sib.get('break-before') == 'page':
                # The follower forces a page break of its own (DocBook
                # refentry pagebreak): the heading cannot be kept with it and
                # strands at the page bottom.  Drop the forced break so the
                # heading and the follower land on the next page together.
                del sib.attrib['break-before']
                stamped += 1
            if sib.get('keep-with-previous.within-column') is None:
                sib.set('keep-with-previous.within-column', 'always')
                stamped += 1
            # FOP drops the heading keep when the following block carries
            # space-before (verified: removing it makes the keep hold).  The
            # heading itself already provides the section gap, so dropping
            # the follower's top space is visually neutral.
            for attr in ('space-before.minimum', 'space-before.optimum',
                         'space-before.maximum'):
                if sib.get(attr) is not None:
                    del sib.attrib[attr]
                    stamped += 1
            break
    return stamped



def _prose_island(node):
    """Pan-gu the element boundaries of a Han prose island inside a verbatim
    synopsis (DocBook wraps zh lead-ins like "其中 X 可以是：" in a plain
    <fo:inline>).  Only inserts one space at Han<->Latin edges; never touches
    surrounding code text."""
    # This plain inline is an explanatory phrase in a verbatim synopsis.
    # Its text/tails are prose; nested font-marked literals remain protected.
    node.text = _normalize_prose(node.text, punctuation=False)
    for child in node:
        child.tail = _normalize_prose(child.tail, punctuation=False)
    chunks = []
    if node.text:
        chunks.append(('t', node.text, None))
    for child in node:
        chunks.append(('e', ''.join(child.itertext()), child))
        if child.tail:
            chunks.append(('t', child.tail, child))
    for i in range(len(chunks) - 1):
        kind, text, owner = chunks[i]
        if kind == 't':
            text = node.text if owner is None else owner.tail
        next_kind, next_chunk, next_owner = chunks[i + 1]
        if next_kind == 't':
            next_chunk = node.text if next_owner is None else next_owner.tail
        prev_text = text.rstrip() if text else ''
        nxt_text = next_chunk.lstrip()
        if not prev_text or not nxt_text:
            continue
        last, first = prev_text[-1], nxt_text[0]
        han_lat = (re.match(r'[\u3400-\u9fff]', last) and first.isascii() and first.isalnum())
        lat_han = (last.isascii() and last.isalnum() and re.match(r'[\u3400-\u9fff]', first))
        if not (han_lat or lat_han) or next_chunk[:1].isspace():
            continue
        if kind == 't':
            if not text[-1].isspace():
                chunks[i] = (kind, text + ' ', owner)
                if owner is None:
                    node.text = text + ' '
                else:
                    owner.tail = text + ' '
        else:
            gap = owner.tail or ''
            if not gap[:1].isspace():
                owner.tail = ' ' + gap



def prepare(path, cjk_family='Alibaba PuHuiTi 3.0', mono_family='Courier New'):
    path = Path(path)
    for _, (prefix, uri) in ET.iterparse(path, events=('start-ns',)):
        if not prefix.startswith('ns'):
            ET.register_namespace(prefix, uri)
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    tree = ET.parse(path, parser=parser)
    _fixed_block_spacing_pass(tree.getroot())
    removed = [0]
    inserted = [0]
    _despace_pass(tree.getroot(), False, removed, inserted, mono_family)
    image_height_limit = _image_height_limit(tree.getroot())
    body_width_limit = _body_width_limit(tree.getroot())
    added = 0
    kept = 0

    def break_prose(text, email=False, relaxed=False):
        nonlocal added
        if not text:
            return text
        # Idempotent if the same FO is rendered more than once; same-node
        # kinsoku via the lookahead, cross-node by _kinsoku_pass below.
        rx = _BREAK_RE_CELL if relaxed else _BREAK_RE
        broken = rx.sub(lambda m: m[0] + '\u200b', text)
        if email:
            broken = re.sub(r'@(?!\u200b)', '@\u200b', broken)
        added += broken.count('\u200b') - text.count('\u200b')
        return broken

    def visit(node, preserve=False, in_cell=False, centered_cell=False,
              email=False, indent=0.0, size_pt=9.0, mono_context=False,
              end_indent=0.0, list_distance=0.0):
        nonlocal kept
        if not isinstance(node.tag, str):
            return
        preserve = (preserve or node.get('white-space-treatment') == 'preserve'
                    or node.tag.endswith('}instream-foreign-object'))
        size = _parse_points(node.get('font-size'), size_pt)
        if size is not None:
            size_pt = size
        # Font size and indents inherit through flow/list containers as well
        # as blocks. start-indent is absolute; a margin is relative to the
        # parent's indent. Ignoring the flow's 4pc made examples size against
        # a column wider than the one FOP actually paints.
        start = _parse_points(node.get('start-indent'), size_pt)
        margin = _parse_points(node.get('margin-left'), size_pt)
        if start is not None:
            indent = start
        elif node.get('start-indent') == 'body-start()':
            indent += list_distance
        elif margin is not None:
            indent += margin
        end = _parse_points(node.get('end-indent'), size_pt)
        margin_end = _parse_points(node.get('margin-right'), size_pt)
        if end is not None:
            end_indent = end
        elif margin_end is not None:
            end_indent += margin_end
        distance = _parse_points(node.get('provisional-distance-between-starts'), size_pt)
        if distance is not None:
            list_distance = distance
        if (node.tag.endswith('}external-graphic')
                and node.get('width', 'auto') == 'auto'
                and node.get('content-width', 'auto') == 'auto'):
            # Legacy GIF diagrams have no physical size. Rendering their
            # intrinsic pixels as points clips wide figures (and tall catalog
            # diagrams) outside the page. FOP resolves 100% against the actual
            # containing block, including its indents; small images stay small.
            node.set('width', '100%')
            node.set('content-width', 'scale-down-to-fit')
            node.set('scaling', 'uniform')
            if (image_height_limit is not None
                    and node.get('height', 'auto') == 'auto'
                    and node.get('content-height', 'auto') == 'auto'
                    and node.get('max-height', 'none') == 'none'):
                node.set('max-height', f'{image_height_limit:.3f}pt')
        in_cell = in_cell or node.tag.endswith('}table-cell')
        if (in_cell and not preserve
                and node.get('keep-together.within-line') == 'always'
                and re.fullmatch(r'<[^<>\s]+@[^<>\s]+>',
                                 ''.join(node.itertext()).strip().replace('\u200b', ''))):
            # DocBook email markup otherwise overrides the break opportunities
            # at domain dots. Also permit a break after @ for narrow columns.
            node.set('keep-together.within-line', 'auto')
            email = True
        centered_cell = centered_cell or (node.tag.endswith('}table-cell') and node.get('text-align') == 'center')
        family = node.get('font-family', '')
        mono_node = (mono_family in [x.strip() for x in family.split(',')]
                     if family else mono_context)
        if (node.tag.endswith('}block') and node.get('id')
                and node.get('keep-with-next.within-column') is None
                and not (node.text or '').strip()
                and not [c for c in node if isinstance(getattr(c, 'tag', None), str)]):
            # Zero-height id-anchor blocks (comment-only) break every
            # keep-with-next chain that crosses them -- a section title
            # bound to "the next block" lands on the anchor and the page
            # still breaks right after it.  Anchors are invisible, so
            # keeping them with what follows is always safe.
            node.set('keep-with-next.within-column', 'always')
        if node.tag.endswith('}table-row') and node.get('keep-together.within-column') is None:
            # Prefer intact rows, but let FOP split a row taller than the
            # available page. An unconditional keep overflows JSON_QUERY.
            node.set('keep-together.within-column', '10')
        if (node.tag.endswith('}block')
                and node.get('keep-together.within-column') == 'always'
                and node.get('margin-left') == '0pt'
                and node.get('keep-with-next.within-column') is None):
            # Section-titlepage wrappers carry keep-together but not
            # keep-with-next, so FOP may still strand the title at a page
            # bottom.  Their signature is a direct child title block with
            # keep-with-next; propagate the keep to the wrapper itself.
            if any(isinstance(child.tag, str)
                   and child.tag.endswith('}block')
                   and child.get('keep-with-next.within-column')
                   for child in node):
                node.set('keep-with-next.within-column', 'always')
        if (node.tag.endswith('}inline') and cjk_family in [x.strip() for x in family.split(',')]
                and family != cjk_family
                and re.search(r'[\u3400-\u9fff]', ''.join(node.itertext()))):
            # Use the CJK font's own metrics for translated inline parameters.
            # Retain the other families, including the monospace marker:
            # font metrics must not erase the code/prose distinction.
            others = [x.strip() for x in family.split(',') if x.strip() != cjk_family]
            node.set('font-family', ','.join([cjk_family] + others))
        # Inline code runs glued to CJK without whitespace have no seam break
        # opportunities in FOP (verified: adjacent fo:inlines chain into one
        # unbreakable line), so a long chain needs last-resort sentinels
        # inside the identifier.  Short runs are safer kept atomic.
        long_inline = (not preserve and node.tag.endswith('}inline')
                       and mono_family in [x.strip() for x in family.split(',')]
                       and len(''.join(node.itertext()).replace('\u200b', '').strip()) > 22)
        if (not preserve and not in_cell and not long_inline
                and node.tag.endswith('}inline')
                and mono_family in [x.strip() for x in family.split(',')]
                and not (len(node) and any(re.search(r'\s', child.tail or '')
                                          for child in node))
                and node.get('keep-together.within-line') is None):
            # Keep short inline code atomic: identifiers, option names and
            # command fragments must never split across lines (FOP honors
            # keep-together.within-line on fo:inline). Longer runs keep their
            # inter-word spaces as break opportunities. Table cells are
            # excluded: narrow columns cannot fit atomic tokens, and FOP then
            # overflows the cell instead of wrapping (the per-cell font-size
            # heuristics below handle those columns). Nested parameters with
            # inter-word spaces keep their own tokens, but not the whole
            # phrase: FOP 2.11 crashes when a parent keep joins their trailing
            # XSL break sentinels across those spaces.
            text = ''.join(node.itertext()).replace('\u200b', '').strip()
            if 0 < len(text) <= 30:
                node.set('keep-together.within-line', 'always')
                kept += 1
        if (in_cell and not preserve and node.tag.endswith('}inline') and not len(node)
                and re.fullmatch(r'[A-Za-z0-9]{20,}', (node.text or '').strip())):
            # Long type names such as anycompatiblemultirange must fit the
            # datatype column without introducing breaks inside the name.
            node.set('font-size', '8.5pt')
        if (preserve and node.tag.endswith('}block')
                and node.get('keep-together.within-column') is None):
            # Conservative fallback; the build measures actual wrapped
            # height with FOP before deciding the final keep.
            node.set('keep-together.within-column',
                     'always' if ''.join(node.itertext()).count('\n') <= 8 else '10')
        mono_block = (preserve and node.tag.endswith('}block')
                      and mono_family in [x.strip() for x in family.split(',')])
        if ((in_cell or body_width_limit is None)
                and preserve and node.tag.endswith('}block')
                and family
                and cjk_family in [x.strip() for x in family.split(',')]
                and family != cjk_family
                and re.search(r'[^\s\u200b]{70,}', ''.join(node.itertext()))):
            # Preserve verbatim separators and examples, including oid2name's
            # wide dashed table rule; only their print size changes. Fallback
            # flat threshold for cells (column width unknown) and masterless FO.
            node.set('font-size', '8.5pt')
        if (mono_block and not in_cell and body_width_limit is not None):
            # Width-aware autosizing: Courier advances 0.6em per ASCII glyph
            # and the CJK fallback font 1em, so scale the whole block until
            # its longest source line fits the column it sits in. Replaces
            # the flat 70-char threshold for page-level programlistings and
            # only ever shrinks (never grows) with a 7.3pt readability floor.
            units = 0.0
            for line in ''.join(node.itertext()).split('\n'):
                u = sum(0.62 if ord(ch) < 128 else 1.05
                        for ch in line.replace('\u200b', ''))
                units = max(units, u)
            avail = body_width_limit - indent - end_indent
            if units > 0 and avail > 0:
                fit = avail / units
                if fit < size_pt - 0.05:
                    node.set('font-size', f'{max(7.3, fit // 0.1 * 0.1):.1f}pt')
        if in_cell and not preserve and node.tag.endswith('}block') and not len(node):
            value = (node.text or '').strip().replace('\u200b', '')
            # Compact, otherwise unbreakable values in the equal-width columns
            # used by the datatype and replication comparison tables.
            if (re.fullmatch(r'[A-Za-z0-9_:+.\-]{9,}', value)
                    or re.search(r'\d{16,}', value)
                    or (centered_cell and re.search(r'[A-Za-z]{8,}', value))):
                node.set('font-size', '7.8pt' if centered_cell else
                         '8.4pt' if re.search(r'\d{16,}', value) else '8.5pt')
        if (in_cell and not preserve and len(node)):
            # Signature rows: DocBook drops the source space between an
            # italic <parameter> and the following <type> at the FO inline
            # boundary ("pretty boolean" -> "prettyboolean").  Re-insert one
            # space when an italic mono inline is directly followed by a
            # non-italic mono inline across latin chars.
            kids = [c for c in node if isinstance(c.tag, str)]
            for a, b in zip(kids, kids[1:]):
                if (a.tag.endswith('}inline') and b.tag.endswith('}inline')
                        and a.get('font-style') == 'italic'
                        and b.get('font-style') is None
                        and mono_family in [x.strip() for x in (a.get('font-family') or '').split(',')]
                        and mono_family in [x.strip() for x in (b.get('font-family') or '').split(',')]
                        and not a.tail
                        and (a.text or '').strip()
                        and (b.text or '').strip()
                        and a.text.strip()[-1].isascii() and a.text.strip()[-1].isalnum()
                        and b.text.strip()[0].isascii() and b.text.strip()[0].isalnum()):
                    a.tail = ' '
        if (preserve and node.tag.endswith('}inline')
                and not node.get('font-family')
                and len(re.findall(r'[\u3400-\u9fff]',
                                   ''.join(node.itertext()) or '')) >= 1):
            _prose_island(node)
        if not preserve:
            text = node.text
            if text and not mono_node:
                text = _normalize_prose(text, punctuation=False)
            node.text = break_prose(text, email, in_cell or long_inline)
        for child in node:
            visit(child, preserve, in_cell, centered_cell, email, indent, size_pt,
                  mono_node, end_indent, list_distance)
            if not preserve:
                tail = child.tail
                if tail and not mono_node:
                    tail = _normalize_prose(tail, punctuation=False)
                child.tail = break_prose(tail, email, in_cell)
        if node.tag.endswith('}list-item-label'):
            for child in node:
                if child.tag.endswith('}block') and re.fullmatch(r'\d{2,}\.\u200b?', (child.text or '').strip()):
                    child.set('font-size', '8.9pt')

    visit(tree.getroot())
    # Inserted break sentinels can expose an edge space that was invisible
    # during the first spacing pass (PG13 JSON table cross-reference tails).
    # Resolve those rendered edges now, instead of changing them on rerun.
    _despace_pass(tree.getroot(), False, removed, inserted, mono_family)
    removed[0] += _kinsoku_pass(tree.getroot())
    title_keeps = _title_keep_pass(tree.getroot())
    temporary = path.with_name(path.name + '.linebreaks.tmp')
    tree.write(temporary, encoding='utf-8', xml_declaration=True)
    temporary.replace(path)
    return added, removed[0], kept, title_keeps


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    cli.add_argument('fo', type=Path)
    cli.add_argument('--cjk-family', default='Alibaba PuHuiTi 3.0')
    cli.add_argument('--mono-family', default='Courier New')
    args = cli.parse_args()
    added, removed, kept, title_keeps = prepare(args.fo, args.cjk_family, args.mono_family)
    print(f'Chinese PDF: added {added} prose line-break opportunities, '
          f'removed {removed} spurious CJK spaces (incl. kinsoku), '
          f'kept-together {kept} inline code runs, '
          f'{title_keeps} title keep stamps.')
