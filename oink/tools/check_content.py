#!/usr/bin/env python3
"""Automated QA for the converted Oink content.

Checks, per language and across languages:
  1. residue   — leftover DocBook markup or entity refs outside code fences
  2. links     — every internal markdown link resolves to an existing page,
                 and every #anchor exists on that page
  3. parity    — the EN and ZH page sets match; heading anchors match per page
Exit code 0 = clean; otherwise prints a summary and exits 1.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

OINK = Path(__file__).resolve().parents[1]
DOCS = OINK / "content" / "docs"

FENCE = re.compile(r"^(`{3,}|~~~)", re.M)
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
ANCHOR_DEF = re.compile(r'\{#([A-Za-z][\w.:-]*)\}')
SPAN_ID = re.compile(r'<span id="([^"]+)"></span>')
ATTR_ID = re.compile(r'\{[^}]*#([A-Za-z][\w.:-]*)')
HEADING = re.compile(r"^#{1,6}\s")
H_ANCHOR = re.compile(r"\{#([A-Za-z][\w.:-]*)\}\s*$", re.M)

RESIDUE_PATTERNS = [
    (re.compile(r"</?(sect\d|refsect\d?|para|simpara|programlisting|screen|"
                r"synopsis|variablelist|varlistentry|listitem|itemizedlist|"
                r"orderedlist|xref|linkend|indexterm|cmdsynopsis|refentry|"
                r"chapter|appendix|tgroup|tbody|thead|row|entry|title|note|"
                r"tip|warning|caution|important|figure|mediaobject|"
                r"imagedata|example|replaceable|literal|glossdef|glossterm)"
                r"[\s>/]"), "docbook-tag"),
    (re.compile(r"&(?!amp;|lt;|gt;|quot;|apos;|#\d+;|#x[0-9a-fA-F]+;)"
                r"[A-Za-z_][\w.-]*;"), "entity-ref"),
    (re.compile(r"\x02\d+\x03"), "block-placeholder"),
]


def strip_code(md: str) -> str:
    """Remove fenced code blocks and inline code spans."""
    out, in_fence, fence = [], False, None
    for line in md.split("\n"):
        m = re.match(r"^(\s*)(`{3,}|~~~)", line)
        if m:
            if not in_fence:
                in_fence, fence = True, m.group(2)[:3]
                continue
            if line.lstrip().startswith(fence):
                in_fence = False
                continue
        if not in_fence:
            out.append(line)
    text = "\n".join(out)
    return re.sub(r"`[^`]*`", "``", text)


def load_pages(suffix: str) -> dict[str, str]:
    pages = {}
    for p in DOCS.rglob("*.md"):
        name = p.name
        if suffix == "":
            if name.endswith(".zh.md"):
                continue
            rel = p.relative_to(DOCS).with_suffix("").as_posix()
        else:
            if not name.endswith(f"{suffix}.md"):
                continue
            rel = p.relative_to(DOCS).as_posix()[: -len(f"{suffix}.md")]
        pages["/" + rel] = p.read_text()
    return pages


def page_url(page: str) -> str:
    """'sql/functions/functions-admin' -> '/sql/functions/functions-admin/'"""
    return page + "/" if not page.endswith("/_index") else \
        page[: -len("_index")]


def main() -> int:
    problems: Counter = Counter()
    examples: dict[str, list] = {}

    def note(kind: str, msg: str):
        problems[kind] += 1
        examples.setdefault(kind, []).append(msg)

    en = load_pages("")
    zh = load_pages(".zh")
    print(f"pages: en={len(en)} zh={len(zh)}")

    # ---- residue -----------------------------------------------------
    for lang, pages in (("en", en), ("zh", zh)):
        for url, md in pages.items():
            prose = strip_code(md)
            for pat, name in RESIDUE_PATTERNS:
                m = pat.search(prose)
                if m:
                    note(f"residue:{name}:{lang}",
                         f"{url}: {m.group(0)[:40]!r}")

    # ---- anchors per page ---------------------------------------------
    anchors = {"en": {}, "zh": {}}
    headings = {"en": {}, "zh": {}}
    for lang, pages in (("en", en), ("zh", zh)):
        for url, md in pages.items():
            ids = set(ANCHOR_DEF.findall(md)) | set(SPAN_ID.findall(md)) \
                | set(ATTR_ID.findall(md))
            ids.discard("td-table--wide")
            ids = {i for i in ids if not i.startswith(".")}
            anchors[lang][url] = ids
            headings[lang][url] = set(H_ANCHOR.findall(md))

    # ---- links ---------------------------------------------------------
    for lang, pages in (("en", en), ("zh", zh)):
        other = anchors["zh"] if lang == "en" else anchors["en"]
        for url, md in pages.items():
            base = "/zh" if lang == "zh" else ""
            for target in LINK.findall(strip_code(md)):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                    continue
                if target.startswith("#"):
                    if target[1:] not in anchors[lang][url]:
                        note(f"link:anchor:{lang}",
                             f"{url}{target}")
                    continue
                path, _, frag = target.partition("#")
                if path.startswith("/zh/"):
                    path = path[len("/zh"):] or "/"
                if not path.startswith("/docs"):
                    note(f"link:prefix:{lang}", f"{url}: {target}")
                    continue
                rel = path[len("/docs"):] or "/"
                rel = rel[1:] if rel.startswith("/") else rel
                rel = rel.rstrip("/")
                if rel == "":
                    key = "/_index"
                elif "/" + rel + "/_index" in anchors[lang]:
                    key = "/" + rel + "/_index"
                else:
                    key = "/" + rel
                if key not in anchors[lang]:
                    note(f"link:page:{lang}", f"{url}: {target}")
                    continue
                if frag and frag not in anchors[lang][key]:
                    note(f"link:frag:{lang}", f"{url}: {target}")

    # ---- parity ---------------------------------------------------------
    en_urls, zh_urls = set(en), set(zh)
    for u in sorted(en_urls - zh_urls):
        note("parity:missing-zh", u)
    for u in sorted(zh_urls - en_urls):
        note("parity:missing-en", u)
    for u in sorted(en_urls & zh_urls):
        if headings["en"][u] != headings["zh"][u]:
            missing = headings["en"][u] - headings["zh"][u]
            extra = headings["zh"][u] - headings["en"][u]
            note("parity:anchors",
                 f"{u}: en-only={sorted(missing)[:3]} zh-only={sorted(extra)[:3]}")

    # ---- summary ---------------------------------------------------------
    if problems:
        print(f"FAIL: {sum(problems.values())} problem(s)")
        for kind, n in problems.most_common():
            print(f"  {kind}: {n}")
            for e in examples[kind][:6]:
                print(f"      {e}")
        return 1
    print("PASS: residue, links, bilingual parity all clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
