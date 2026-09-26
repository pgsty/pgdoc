#!/usr/bin/env python3
"""Shared rule core for spurious-space handling between full-width chars.

Hard-wrapped DocBook sources collapse every interior newline (plus any
indentation) into a single U+0020 at render time, in HTML and in print
alike.  When the characters that end up adjacent across the wrap are both
full-width, that collapsed space is spurious (e.g. "多态结 果类型",
"。 但是").  This module holds the single source of truth for deciding
when a whitespace run must not render; it is used both by the print
pipeline (bin/prepare_chinese_pdf.py, on generated XSL-FO) and by the
source fixer (bin/fix_cjk_spacing.py, on the SGML/XML sources
themselves).

Rules, kept identical everywhere:

* A space is dropped when either neighbour is full-width punctuation
  (STRICT_PUNCT — it never takes an adjacent space), or when both
  neighbours are full-width (Han ideographs, CJK punctuation, fullwidth
  forms, or the curly quotation marks rendered by <quote>/l10n).
* Curly quotes only lose their space next to full-width text, so Latin
  phrases keep theirs ('word "term"').
* U+2014 (em dash) and U+2026 (ellipsis) are deliberately absent from
  both sets: zh titles space them on purpose ("模块 — 描述").
* Han<->Latin boundaries keep their space, matching the corpus
  convention (盘古之白).
"""

import re

HAN_RANGE = '\u3400-\u9fff\uf900-\ufaff'
# Full-width punctuation that never takes an adjacent space in running text.
STRICT_PUNCT = ('\u3001\u3002\u3008\u3009\u300a\u300b\u3010\u3011\u3014\u3015'
                '\u3017-\u301c\u301f\u3030\u3031\u303b-\u303f'
                '\uff01-\uff0f\uff1a-\uff1f\uff3b-\uff40\uff5b-\uff60'
                '\uffe0-\uffe5')
# Double/single quotation marks rendered by <quote>/l10n gentext.
QUOTE_MARKS = '\u201c\u201d\u2018\u2019\u301d\u301e'
# U+2014 (em dash) and U+2026 (ellipsis) are deliberately absent from both
# sets; see the module docstring.
FW_RE = re.compile(f'[{HAN_RANGE}\u3001-\u303f\uff01-\uff60\uffe0-\uffe5{QUOTE_MARKS}]')
STRICT_RE = re.compile(f'[{STRICT_PUNCT}]')
QUOTES_RE = re.compile(f'[{QUOTE_MARKS}]')
WS_RUN = re.compile(r'[ \t\n\r]+')
# Characters ignored when looking for the effective neighbour of a
# whitespace run (\u200b are the FO print sentinels; absent in sources).
SKIP = ' \t\n\r\u200b'


def drop_space(left, right):
    """True when the collapsed space between the two chars must not render."""
    if not left or not right:
        return False
    l_fw = bool(FW_RE.match(left))
    r_fw = bool(FW_RE.match(right))
    if STRICT_RE.match(left) or STRICT_RE.match(right):
        return True
    if l_fw and r_fw:
        return True
    return bool((QUOTES_RE.match(left) and r_fw)
                or (QUOTES_RE.match(right) and l_fw))


def eff(s, reverse=False):
    """First (or last) non-whitespace character of s, or None."""
    if not s:
        return None
    it = reversed(s) if reverse else iter(s)
    for c in it:
        if c not in SKIP:
            return c
    return None
