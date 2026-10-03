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

# ---------------------------------------------------------------------------
# Build-time zh prose normalization (shared by PDF FO post-processing and the
# HTML build).  Applied only to rendered prose text -- never to verbatim
# code, monospace runs, URLs or identifiers inside markup.
# ---------------------------------------------------------------------------

_PANGU_L = re.compile(f'(?<=[{HAN_RANGE}])(?=[A-Za-z0-9])')
_PANGU_R = re.compile(f'(?<=[A-Za-z0-9])(?=[{HAN_RANGE}])')
# Symbol-leading literals (~/%, --options, /paths) take a space after Han;
# only ~/% close against Han from the left ("…%APPDATA%\u6307" -> "% \u6307"),
# '/'/'-' are skipped there so "B-\u6811" style terms stay intact.
_PANGU_SYM_L = re.compile(f'(?<=[{HAN_RANGE}])(?=[~][/A-Za-z0-9]|[%/][A-Za-z0-9]|--[A-Za-z]|[$][A-Za-z0-9{HAN_RANGE}])')
_PANGU_SYM_R = re.compile(r'(?<=[~%\*)\]=])(?=[㐀-鿿])')
# Lone operator tokens (=, :=) and __dunder__/star-leading literals next to Han.
_PANGU_OP_L = re.compile(r'(?<=[\u3400-\u9fff])(?==[^=]|::?=|__[A-Za-z_]|\*|-[A-Za-z])')
HAN_ONLY_RE = re.compile(f'[{HAN_RANGE}]')
# Product name directly followed by a version number (PostgreSQL14).  Words
# like utf8/sha256 are legitimately joined, so only well-known product names
# get the split.
_PROD_VER = re.compile(r'(PostgreSQL|Postgres)(?=[0-9])')
# , ; : ? !  adjacent to Han on either side.
_HALF_PUNCT = re.compile(
    f'(?<=[{HAN_RANGE}])[,;:?!]|[,;:?!](?=[{HAN_RANGE}])')
_FULL = {',': '\uff0c', ';': '\uff1b', ':': '\uff1a', '?': '\uff1f', '!': '\uff01'}
_COLON_R_HAN = re.compile(f':(?=[{HAN_RANGE}])')
_DOT_L_HAN = re.compile(f'(?<=[{HAN_RANGE}])\\.')
# Straight double quote with Han on either side, toggled open/close.
_DQ = re.compile(f'"(?=[{HAN_RANGE}])|(?<=[{HAN_RANGE}])"')


def _dquotes(text):
    # A quote pair can span inline elements. Never guess the orientation of
    # a lone quote in a text node; source <quote> markup handles those pairs.
    if len(list(_DQ.finditer(text))) % 2:
        return text
    state = ['closed']
    def repl(m):
        opening = state[0] == 'closed'
        state[0] = 'open' if opening else 'closed'
        return '\u201c' if opening else '\u201d'
    return _DQ.sub(repl, text)


URL_RE = re.compile(r'(?:[A-Za-z][A-Za-z0-9+.-]*://|mailto:)[^\s<>"，。；：？！、（）《》]+')


def _normalize_plain(text, punctuation=True):
    """Normalize one prose text node; idempotent.

    * pan-gu: exactly one U+0020 at every Han<->Latin/digit boundary;
    * halfwidth , ; : ? ! -> fullwidth when adjacent to Han.  A colon is
      additionally kept when its left neighbour is an ASCII digit/alnum
      ("10:30", "psql:5432" survive); an ASCII dot is only converted when
      its LEFT neighbour is Han (trailing period on a Chinese sentence),
      so "v18.6" and "第 2.1 节" keep their dots;
    * straight double quotes touching Han alternate into \u201c \u201d pairs.
    """
    if not text:
        return text
    out = _PANGU_L.sub(' ', text)
    out = _PANGU_R.sub(' ', out)
    out = _PANGU_SYM_L.sub(' ', out)
    out = _PANGU_SYM_R.sub(' ', out)
    out = _PANGU_OP_L.sub(' ', out)
    out = _PROD_VER.sub(r'\1 ', out)
    if not punctuation:
        return out
    out = _HALF_PUNCT.sub(lambda m: _FULL[m.group(0)], out)
    # "literal, 则" -- half punct + space + Han (the space is the pan-gu
    # insert at the element boundary); convert and drop the stray space.
    out = re.sub(r'([,;:?!]) (?=[\u3400-\u9fff])',
                 lambda m: _FULL[m.group(1)], out)
    if ':' in out:
        out = _COLON_R_HAN.sub(
            lambda m: m.group(0)
            if (out[max(0, m.start() - 1)].isascii() and out[max(0, m.start() - 1)].isalnum())
            else '\uff1a', out)
    out = _DOT_L_HAN.sub('\u3002', out)
    if ('?' in out or '!' in out) and HAN_ONLY_RE.search(out):
        # A trailing ASCII ?/! after Latin/digit inside a Han-bearing node is
        # a Chinese sentence tail ("什么是PostgreSQL?" / "何时使用JIT?") —
        # fullwidth it.  Nodes without Han keep ASCII punctuation untouched.
        out = re.sub(r'(?<=[A-Za-z0-9])[?!]',
                     lambda m: '\uff1f' if m.group(0) == '?' else '\uff01',
                     out)
    out = _dquotes(out)
    out = WS_RUN.sub(lambda m: '' if m.start() and m.end() < len(out)
                     and drop_space(out[m.start() - 1], out[m.end()]) else m[0], out)
    return out


def normalize_prose(text, *, punctuation=True):
    """Normalize prose while preserving URLs; optionally change only spaces."""
    if not text:
        return text
    pieces, cursor = [], 0
    for match in URL_RE.finditer(text):
        pieces.extend((_normalize_plain(text[cursor:match.start()], punctuation), match[0]))
        cursor = match.end()
    pieces.append(_normalize_plain(text[cursor:], punctuation))
    return ''.join(pieces)
