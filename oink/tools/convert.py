#!/usr/bin/env python3
"""Convert the PostgreSQL 18 DocBook manual (en + zh) into an Oink/Hugo site.

Sources:  <repo>/en/18.6  and  <repo>/zh/18   (DocBook XML in .sgml files)
Output:   <repo>/oink/content/docs/**.md (+ .zh.md)  and  oink/static/images/

The book is assembled exactly like upstream does it (postgres.sgml +
filelist.sgml entities), parsed as one tree, then split into pages:

  * one page per chapter/appendix file, EXCEPT
  * reference part  -> one page per ref entry file (order kept)
  * contrib appendix-> one page per supplied-module sect1 file
  * chapters whose source file exceeds SPLIT_LINES -> section dir with one
    page per sect1 (mirrors the chunking of the official online manual)

DocBook ids become heading anchors ({#id}) and xref/linkend becomes a normal
Markdown link, so every cross-reference in the book keeps working.  The page
plan is derived from the ENGLISH tree and reused verbatim for Chinese (matched
by element id), which keeps both languages on identical URLs and anchors.
"""

from __future__ import annotations

import argparse
import html.entities
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

from lxml import etree

REPO = Path(__file__).resolve().parents[2]
OINK = REPO / "oink"
EN_DIR = REPO / "en" / "18.6"
ZH_DIR = REPO / "zh" / "18"
OUT_DIR = OINK / "content" / "docs"
IMG_SRC = EN_DIR / "images"
IMG_OUT = OINK / "static" / "images"

PG_VERSION = "18.6"
SPLIT_LINES = 2500
UPSTREAM = "https://www.postgresql.org/docs/18/"

XML_BUILTINS = {"amp", "lt", "gt", "quot", "apos"}
CUSTOM_ENTITIES = {"version": PG_VERSION, "majorversion": "18",
                   "zwsp": "", "nbsp": "\u00a0"}

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV"]

PART_ICONS = {
    "tutorial": "fa-solid fa-graduation-cap",
    "sql": "fa-solid fa-database",
    "admin": "fa-solid fa-server",
    "client-interfaces": "fa-solid fa-plug",
    "server-programming": "fa-solid fa-code",
    "reference": "fa-solid fa-terminal",
    "internals": "fa-solid fa-microchip",
    "appendixes": "fa-solid fa-paperclip",
}

sys.path.insert(0, str(REPO / "bin"))
try:
    from cjk_spacing import normalize_prose  # type: ignore
except Exception:                             # pragma: no cover
    def normalize_prose(t, *, punctuation=True):
        return t


# ==========================================================================
# book assembly
# ==========================================================================

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
ENTITY_RE = re.compile(r"&([a-zA-Z_][a-zA-Z0-9_.-]*);")
FILELINE_RE = re.compile(
    r'<!ENTITY\s+([a-zA-Z_][a-zA-Z0-9_.-]+)\s+SYSTEM\s+"([^"]+)">')


def load_filelist(srcdir: Path) -> dict[str, str]:
    """All SYSTEM entities: filelist.sgml, lists pulled in via %param;,
    and the book root's internal subset (reference.sgml)."""
    ents: dict[str, str] = {}
    main = (srcdir / "filelist.sgml").read_text()

    def scan(text: str, reldir: str):
        for m in FILELINE_RE.finditer(text):
            ents.setdefault(m.group(1),
                            (reldir + "/" if reldir else "") + m.group(2))

    scan(main, "")
    # e.g. <!ENTITY % allfiles SYSTEM "ref/allfiles.sgml"> %allfiles;
    for m in re.finditer(r'<!ENTITY\s+%\s+\w+\s+SYSTEM\s+"([^"]+)"', main):
        p = srcdir / m.group(1)
        if p.exists():
            scan(p.read_text(), p.parent.relative_to(srcdir).as_posix())
    # book-root internal subset
    book = (srcdir / "postgres.sgml").read_text()
    scan(book, "")
    for m in re.finditer(r'<!ENTITY\s+([a-zA-Z_][a-zA-Z0-9_.-]+)\s+"([^"]*)">', book):
        CUSTOM_ENTITIES.setdefault(m.group(1), m.group(2))
    return ents


def expand_book(srcdir: Path, skip: set[str] | None = None,
                fallback: Path | None = None) -> str:
    ents = load_filelist(srcdir)
    skip = skip or set()
    residue: set[str] = set()

    def expand(text: str, depth: int, stem: str) -> str:
        if depth > 12:
            raise RuntimeError("entity recursion too deep")
        def repl(m: re.Match) -> str:
            name = m.group(1)
            if name in XML_BUILTINS:
                return m.group(0)
            if name in CUSTOM_ENTITIES:
                return CUSTOM_ENTITIES[name]
            if name in ents:
                if name in skip:
                    return ""
                rel = ents[name]
                f = srcdir / rel
                marker = re.sub(r"\.[a-z]+$", "", rel)
                if not f.exists():
                    # build-time tables kept under tools/generated[-zh]
                    alt = (fallback / Path(rel).name) if fallback else None
                    if alt is None or not alt.exists():
                        return ""
                    f = alt
                    marker = Path(rel).stem
                raw = COMMENT_RE.sub("", f.read_text())
                inner = expand(raw, depth + 1, marker)
                return f"<!--FILE:{marker}-->\n{inner}\n<!--/FILE-->"
            if name + ";" in html.entities.html5:
                return html.entities.html5[name + ";"]
            residue.add(name)
            # e.g. C code "&binaryIntVal;" — keep it as literal text
            return f"&amp;{name};"
        return ENTITY_RE.sub(repl, text)

    out = expand(COMMENT_RE.sub("", (srcdir / "postgres.sgml").read_text()),
                 0, "postgres")
    if residue:
        print(f"  note: literal-kept pseudo entities: {sorted(residue)}")
    return out


def parse_book(xml_text: str):
    parser = etree.XMLParser(recover=True, huge_tree=True)
    root = etree.fromstring(xml_text.encode("utf-8"), parser)
    if root is None or root.tag != "book":
        raise SystemExit("book assembly failed to produce a <book> root")
    return root


def annotate_stems(el, stem: str = "postgres"):
    """Record the innermost enclosing <!--FILE:...--> for every element."""
    el.set("__stem", stem)
    stack = [stem]
    for node in el.iter():
        if node is el:
            continue
        if not isinstance(node.tag, str):
            txt = node.text or ""
            if txt.startswith("FILE:"):
                stack.append(txt[5:])
            elif txt == "/FILE" and len(stack) > 1:
                stack.pop()
            continue
        node.set("__stem", stack[-1])


# ==========================================================================
# generic tree helpers
# ==========================================================================

def tag(el):
    return etree.QName(el).localname if isinstance(el.tag, str) else ""


def kids(el, *names):
    return [c for c in el if isinstance(c.tag, str) and tag(c) in names]


def first_child(el, *names):
    for c in el:
        if isinstance(c.tag, str) and tag(c) in names:
            return c
    return None


def plain_text(el) -> str:
    if el is None:
        return ""
    return " ".join(" ".join(el.itertext()).split())


# ==========================================================================
# manifest
# ==========================================================================

@dataclass
class Page:
    kind: str                      # see build_manifest
    slug: str
    dir: str                       # parent dir under content/docs ('' = docs/)
    stem: str                      # source file stem
    weight: int
    num: str = ""                  # '8' or 'C'; '' = unnumbered
    roman: str = ""                # part roman numeral (part pages only)
    root_id: str = ""
    icon: str = ""
    el: object = None              # bound per language
    title: str = ""
    desc: str = ""
    search_keywords: list = field(default_factory=list)


class Manifest:
    def __init__(self):
        self.pages: list[Page] = []
        self.chapter_no = 0
        self.appendix_no = 0
        self.part_no = 0

    def add(self, page: Page) -> Page:
        self.pages.append(page)
        return page


def chapter_source_lines(srcdir: Path, stem: str) -> int:
    """Own file lines plus lines of SYSTEM entities it directly includes
    (release notes, generated tables)."""
    p = srcdir / f"{stem}.sgml"
    if not p.exists():
        return 0
    text = p.read_text()
    n = text.count("\n")
    ents = load_filelist(srcdir)
    for name in set(re.findall(r"&([a-zA-Z_][a-zA-Z0-9_.-]*);", text)):
        rel = ents.get(name)
        if rel and (srcdir / rel).exists():
            n += (srcdir / rel).read_text().count("\n")
    return n


def build_manifest(book, srcdir: Path) -> Manifest:
    man = Manifest()

    for info in kids(book, "bookinfo"):
        for legal in kids(info, "legalnotice"):
            man.add(Page("legal", "legal", "", "legal", 3,
                         root_id="legalnotice", el=legal))

    for child in book:
        if not isinstance(child.tag, str):
            continue
        t = tag(child)
        stem = child.get("__stem", "")
        if t == "preface":
            man.add(Page("preface", "preface", "", stem, 5,
                         root_id=child.get("id", "preface"), el=child))
        elif t == "part":
            pid = child.get("id", stem)
            man.part_no += 1
            roman = ROMAN[man.part_no]
            w = man.part_no * 10
            man.add(Page("part", pid, pid, "postgres", w, roman=roman,
                         root_id=pid, icon=PART_ICONS.get(pid, ""), el=child))
            plan_part(man, child, srcdir, w)
        elif t == "bibliography":
            man.add(Page("biblio", child.get("id", "bibliography"), "", stem,
                         95, root_id=child.get("id", "bibliography"), el=child))
    return man


def plan_part(man: Manifest, part, srcdir: Path, part_weight: int):
    pid = part.get("id", "")
    w = 10
    for child in part:
        if not isinstance(child.tag, str):
            continue
        t = tag(child)
        stem = child.get("__stem", "")
        cid = child.get("id", stem)
        if t == "chapter" or t == "appendix":
            if t == "chapter":
                man.chapter_no += 1
                num = str(man.chapter_no)
            else:
                man.appendix_no += 1
                num = chr(ord("A") + man.appendix_no - 1)
            if cid == "contrib":
                man.add(Page("contrib", "contrib", "appendixes/contrib", stem,
                             w, num=num, root_id="contrib", el=child))
                mw = 10
                for sect in kids(child, "sect1"):
                    man.add(Page("module", sect.get("id", f"contrib-{mw}"),
                                 "appendixes/contrib", sect.get("__stem", stem),
                                 mw, num=num,
                                 root_id=sect.get("id", ""), el=sect))
                    mw += 10
            elif t == "appendix":
                man.add(Page("appendix", cid, "appendixes", stem, w, num=num,
                             root_id=cid, el=child))
            else:
                lines = chapter_source_lines(srcdir, stem)
                sects = kids(child, "sect1")
                if lines > SPLIT_LINES and sects:
                    man.add(Page("chapterindex", cid, f"{pid}/{cid}", stem, w,
                                 num=num, root_id=cid, el=child))
                    for i, sect in enumerate(sects, 1):
                        sid = sect.get("id", f"{cid}-s{i}")
                        man.add(Page("sect", sid, f"{pid}/{cid}", stem, i,
                                     num=num, root_id=sid, el=sect))
                else:
                    man.add(Page("chapter", cid, pid, stem, w, num=num,
                                 root_id=cid, el=child))
        elif t == "reference":                 # reference-part group
            for refentry in kids(child, "refentry"):
                man.add(Page("ref", refentry.get("id",
                            refentry.get("__stem", "")), "reference",
                             refentry.get("__stem", ""), 0,
                             root_id=refentry.get("id", ""), el=refentry))
        w += 10

    for i, p in enumerate([p for p in man.pages if p.kind == "ref"], 1):
        p.weight = i


# ==========================================================================
# targets (id -> page/anchor/label), per language
# ==========================================================================

@dataclass
class Target:
    page: Page
    anchor: str
    label: str
    heading: bool


def make_label(lang: str, kind: str, num: str, title: str) -> str:
    if lang == "en":
        head = {"part": f"Part {num}", "chapter": f"Chapter {num}",
                "section": f"Section {num}", "appendix": f"Appendix {num}",
                "table": f"Table {num}", "figure": f"Figure {num}",
                "example": f"Example {num}"}.get(kind)
        return f"{head}: {title}" if head and title else (head or title)
    head = {"part": f"第 {num} 部分", "chapter": f"第 {num} 章",
            "section": f"第 {num} 节", "appendix": f"附录 {num}",
            "table": f"表 {num}", "figure": f"图 {num}",
            "example": f"例 {num}"}.get(kind)
    return f"{head} {title}" if head and title else (head or title)


def sectnum_of(el, page: Page) -> str:
    """Chapter-scoped dotted number like 8.5.2; '' when unnumbered."""
    chain = []
    node = el
    while node is not None and node is not page.el:
        t = tag(node)
        if t.startswith("sect") and t[-1].isdigit():
            parent = node.getparent()
            sibs = [s for s in parent if isinstance(s.tag, str) and tag(s) == t]
            chain.append(sibs.index(node) + 1)
        node = node.getparent()
    chain.reverse()
    if not chain:
        return page.num
    if not page.num:
        return ""
    return f"{page.num}." + ".".join(map(str, chain))


def collect_targets(man: Manifest, lang: str) -> dict[str, Target]:
    targets: dict[str, Target] = {}
    # the book root (linkend="postgres") points at the docs section root
    targets["postgres"] = Target(
        None, "",
        "PostgreSQL 18.6 Documentation" if lang == "en"
        else "PostgreSQL 18.6 文档", True)

    def title_of(el):
        t = first_child(el, "title", "refentrytitle", "glossterm")
        return plain_text(t) if t is not None else plain_text(el)[:60]

    for page in man.pages:
        root = page.el
        if root is None:
            continue
        counters = {"table": 0, "figure": 0, "example": 0}
        # children that are pages of their own must not be claimed here
        stop = {"part": ("chapter", "appendix", "reference"),
                "chapterindex": ("sect1",),
                "contrib": ("sect1",)}.get(page.kind, ())

        # page-root label
        rid = root.get("id", "")
        if page.kind == "part":
            lbl = make_label(lang, "part", page.roman, title_of(root))
        elif page.kind in ("chapter", "chapterindex", "module"):
            lbl = make_label(lang, "chapter", page.num, title_of(root))
        elif page.kind in ("appendix", "contrib"):
            lbl = make_label(lang, "appendix", page.num, title_of(root))
        elif page.kind == "preface":
            lbl = title_of(root)
        elif page.kind == "legal":
            lbl = title_of(root)
        elif page.kind == "biblio":
            lbl = title_of(root)
        else:                                    # sect / ref pages
            lbl = title_of(root)
        if rid:
            targets[rid] = Target(page, "", lbl, True)

        def walk(el):
            for c in el:
                if not isinstance(c.tag, str):
                    continue
                t = tag(c)
                cid = c.get("id", "")
                if t in stop:
                    if t == "reference" and page.kind == "part":
                        # reference groups render as headings on the index
                        if cid:
                            targets[cid] = Target(page, cid, title_of(c), True)
                    continue
                if t in ("sect1", "sect2", "sect3", "sect4", "sect5",
                         "refsect1", "refsect2", "refsect3", "glossdiv",
                         "reference"):
                    if t.startswith("refsect"):
                        num = ""
                    elif t == "reference":
                        num = ""
                    elif t == "glossdiv":
                        num = ""
                    else:
                        num = sectnum_of(c, page)
                    if cid:
                        lbl = make_label(lang, "section", num, title_of(c)) \
                            if num else title_of(c)
                        targets[cid] = Target(page, cid, lbl, True)
                    walk(c)
                elif t == "refentry":
                    if cid:
                        targets[cid] = Target(page, "", title_of(c), True)
                    walk(c)
                elif t in ("table", "informaltable"):
                    counters["table"] += 1
                    if cid:
                        num = (f"{page.num}.{counters['table']}"
                               if page.num else "")
                        title = title_of(c)
                        targets[cid] = Target(
                            page, cid,
                            make_label(lang, "table", num, title)
                            if title or num else "", False)
                    walk(c)
                elif t == "figure":
                    counters["figure"] += 1
                    if cid:
                        num = (f"{page.num}.{counters['figure']}"
                               if page.num else "")
                        targets[cid] = Target(
                            page, cid,
                            make_label(lang, "figure", num, title_of(c)), False)
                    walk(c)
                elif t == "example":
                    counters["example"] += 1
                    if cid:
                        num = (f"{page.num}.{counters['example']}"
                               if page.num else "")
                        targets[cid] = Target(
                            page, cid,
                            make_label(lang, "example", num, title_of(c)), False)
                    walk(c)
                elif t == "varlistentry":
                    if cid:
                        lbl = " / ".join(plain_text(x) for x in kids(c, "term"))
                        targets[cid] = Target(page, cid, lbl, False)
                    walk(c)
                elif t in ("glossentry", "formalpara", "anchor", "para",
                           "synopsis", "steps", "procedure", "listitem",
                           "refpurpose", "index", "legalnotice"):
                    if cid and cid not in targets:
                        targets[cid] = Target(page, cid, title_of(c), False)
                    walk(c)
                else:
                    if cid and cid not in targets:
                        targets[cid] = Target(page, cid, title_of(c), False)
                    walk(c)

        walk(root)
    return targets


# ==========================================================================
# renderer
# ==========================================================================

PH_RE = re.compile("\x02(\\d+)\x03")

# block elements DocBook allows inside <para>; rendered in place
BLOCK_IN_INLINE = {
    "programlisting", "screen", "synopsis", "literallayout", "cmdsynopsis",
    "itemizedlist", "orderedlist", "variablelist", "simplelist", "procedure",
    "note", "tip", "important", "warning", "caution", "table", "informaltable",
    "figure", "example", "mediaobject", "blockquote", "sidebar", "qandaset",
}

CALLOUT = {"note": "NOTE", "tip": "TIP", "important": "IMPORTANT",
           "warning": "WARNING", "caution": "CAUTION"}

CODE_INLINE_TAGS = {
    "literal", "command", "option", "parameter", "varname", "filename",
    "function", "type", "classname", "structname", "structfield", "symbol",
    "methodname", "modifier", "envar", "returnvalue", "constant", "sgmltag",
    "token", "errortext", "errcode", "database", "replaceable",
}

SQL_KEYWORDS = {
    "SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "ALTER", "DROP", "WITH",
    "GRANT", "REVOKE", "BEGIN", "COMMIT", "ROLLBACK", "SET", "SHOW", "COPY",
    "VACUUM", "ANALYZE", "ANALYSE", "REINDEX", "COMMENT", "DECLARE",
    "PREPARE", "EXECUTE", "EXPLAIN", "CALL", "DO", "LISTEN", "NOTIFY",
    "UNLISTEN", "LOCK", "MERGE", "REFRESH", "REASSIGN", "SECURITY",
    "DISCARD", "CHECKPOINT", "CLUSTER", "END", "ABORT", "CLOSE", "FETCH",
    "MOVE", "IMPORT", "SAVEPOINT", "RELEASE", "TRUNCATE", "VALUES", "TABLE",
    "ALTERDEFAULT", "RESET",
}


class Renderer:
    def __init__(self, lang: str, targets: dict, page: Page):
        self.lang = lang
        self.targets = targets
        self.page = page
        self.prefix = "" if lang == "en" else "/zh"
        self.warn: list[str] = []
        self.counters = {"table": 0, "figure": 0}

    # -- urls ---------------------------------------------------------------
    def page_path(self, page: Page) -> str:
        d = page.dir + "/" if page.dir else ""
        if page.kind in ("part", "chapterindex", "contrib"):
            return f"{self.prefix}/docs/{d}"
        return f"{self.prefix}/docs/{d}{page.slug}/"

    def url_for(self, cid: str) -> str:
        t = self.targets.get(cid)
        if t is None:
            return ""
        if t.page is None:                     # the book root
            return f"{self.prefix}/docs/"
        if not t.anchor:
            if t.page is self.page:
                return self.page_path(self.page)
            return self.page_path(t.page)
        if t.page is self.page:
            return f"#{t.anchor}"
        return self.page_path(t.page) + f"#{t.anchor}"

    # -- blocks --------------------------------------------------------------
    def blocks(self, el, level=2, skip=()) -> str:
        out = []
        for c in el:
            if not isinstance(c.tag, str):
                continue
            if skip and tag(c) in skip:
                continue
            md = self.block(c, level)
            if md and md.strip():
                out.append(md.strip("\n"))
        return "\n\n".join(out)

    def block(self, c, level=2) -> str:
        t = tag(c)
        h = getattr(self, "tag_" + t, None)
        md = h(c, level) if h else self._default_block(c, level)
        if md is None:
            return ""
        md = md.strip("\n")
        cid = c.get("id", "")
        if cid and t not in ANCHORED_BY_HANDLER:
            md = f'<span id="{cid}"></span>\n\n' + md
        return md

    def _default_block(self, c, level):
        t = tag(c)
        if t in ("title", "refmeta", "refnamediv", "indexterm", "titleabbrev",
                 "bookinfo", "refentryinfo", "docinfo"):
            return ""
        kids_blocks = [x for x in c if isinstance(x.tag, str)]
        if kids_blocks and any(tag(x) not in
                               ("indexterm",) for x in kids_blocks):
            return self.blocks(c, level)
        return self.para_like(c) if (c.text or kids_blocks) else ""

    # headings
    def heading(self, el, level, title=None, skip=()):
        t = title if title is not None \
            else self.inline_text(first_child(el, "title"))
        body = self.blocks(el, level + 1, skip=skip)
        if not t:
            return body
        cid = el.get("id", "")
        anchor = f" {{#{cid}}}" if cid else ""
        return f"{'#' * min(level, 6)} {t}{anchor}\n\n{body}".rstrip()

    def tag_sect1(self, c, l): return self.heading(c, l)
    def tag_sect2(self, c, l): return self.heading(c, l)
    def tag_sect3(self, c, l): return self.heading(c, l)
    def tag_sect4(self, c, l): return self.heading(c, l)
    def tag_sect5(self, c, l): return self.heading(c, l)
    def tag_refsect1(self, c, l): return self.heading(c, l)
    def tag_refsect2(self, c, l): return self.heading(c, l)
    def tag_refsect3(self, c, l): return self.heading(c, l)
    def tag_glossdiv(self, c, l): return self.heading(c, l)
    def tag_bibliodiv(self, c, l): return self.heading(c, l)
    def tag_reference(self, c, l):
        return self.heading(c, l, skip=("refentry",))

    def tag_refsynopsisdiv(self, c, l):
        title = self.inline_text(first_child(c, "title")) \
            or ("Synopsis" if self.lang == "en" else "概要")
        cid = c.get("id", "")
        anchor = f" {{#{cid}}}" if cid else ""
        return f"## {title}{anchor}\n\n{self.blocks(c, l + 1)}".rstrip()

    def tag_bridgehead(self, c, l):
        return f"**{self.inline_text(c)}**"

    # paragraphs
    def tag_para(self, c, l): return self.para_like(c)
    def tag_simpara(self, c, l): return self.para_like(c)

    def para_like(self, c) -> str:
        saved = getattr(self, "_q", None)
        self._q = []
        try:
            txt = self.inline(c)
            q = self._q
        finally:
            self._q = saved
        return self._assemble(txt, q)

    def _assemble(self, txt: str, queue: list) -> str:
        han = self.lang == "zh"

        def polish(s: str) -> str:
            s = s.strip()
            if han and s and re.search(r"[\u3400-\u9fff]", s):
                s = zh_polish(s)
            return s

        if not queue or not PH_RE.search(txt):
            return polish(txt)
        segs = []
        pos = 0
        for m in PH_RE.finditer(txt):
            pre = polish(txt[pos:m.start()])
            if pre:
                segs.append(pre)
            segs.append(queue[int(m.group(1))].strip("\n"))
            pos = m.end()
        post = polish(txt[pos:])
        if post:
            segs.append(post)
        return "\n\n".join(segs)

    def tag_formalpara(self, c, l):
        title = self.inline_text(first_child(c, "title"))
        body = self.blocks(c, l)
        return f"**{title}.**\n\n{body}" if title else body

    # lists
    def tag_itemizedlist(self, c, l):
        out = []
        for li in kids(c, "listitem"):
            out.append(indent_block(self.block(li, l), "- "))
        return "\n\n".join(out) if len(out) > 1 else "".join(out)

    def tag_orderedlist(self, c, l):
        out = []
        for i, li in enumerate(kids(c, "listitem"), 1):
            out.append(indent_block(self.block(li, l), f"{i}. "))
        return "\n\n".join(out) if len(out) > 1 else "".join(out)

    def tag_substeps(self, c, l):
        out = []
        for i, step in enumerate(kids(c, "step"), 1):
            out.append(indent_block(self.block(step, l), f"{i}. "))
        return "\n".join(out)

    def tag_procedure(self, c, l):
        title = self.inline_text(first_child(c, "title"))
        items = []
        for i, step in enumerate(kids(c, "step"), 1):
            items.append(indent_block(self.block(step, l), f"{i}. "))
        body = "\n".join(items) + "\n{.steps}"
        return f"**{title}**\n\n{body}" if title else body

    def tag_simplelist(self, c, l):
        members = [self.inline_text(m) for m in kids(c, "member")]
        if c.get("type") == "inline":
            return ", ".join(members)
        return "\n".join("- " + m for m in members if m)

    def tag_variablelist(self, c, l):
        entries = kids(c, "varlistentry")
        names = [self._term_names(e) for e in entries]
        has_empty = any(not n for n in names)
        flat = [x for n in names for x in n]
        has_dupes = len(flat) != len(set(flat))
        if has_empty or has_dupes:
            return self._varlist_plain(c, l)
        if len(entries) < 2 or not all(self._varlist_simple(e) for e in entries):
            return self._varlist_rich(c, l, names)
        rows = [f"| {self.L('term')} | {self.L('desc')} |", "| --- | --- |"]
        for e, n in zip(entries, names):
            term = " / ".join(self.inline_text(t) for t in kids(e, "term"))
            item = first_child(e, "listitem")
            para = first_child(item, "para", "simpara") if item is not None else None
            desc = self.inline_flat(para)
            anchors = self._entry_anchors(e)
            if anchors:
                desc = anchors + desc
            rows.append(f"| {cell(term)} | {cell(desc)} |")
        return "\n".join(rows) + "\n{.fields}"

    def _entry_anchors(self, e) -> str:
        ids = [e.get("id", "")] + [t.get("id", "")
                                   for t in kids(e, "term")]
        return "".join(f'<span id="{i}"></span>' for i in ids if i)

    def _term_names(self, e) -> list[str]:
        out = []
        for t in kids(e, "term"):
            parts = []

            def rec(x):
                if x is not t and isinstance(x.tag, str) and tag(x) == "indexterm":
                    return
                if x.text:
                    parts.append(x.text)
                for ch in x:
                    if isinstance(ch.tag, str):
                        rec(ch)
                    if ch.tail:
                        parts.append(ch.tail)

            rec(t)
            s = " ".join(" ".join(parts).split())
            if s:
                out.append(s)
        return out

    def _varlist_plain(self, c, l):
        out = []
        for e in kids(c, "varlistentry"):
            terms = " / ".join(self.inline_text(t) for t in kids(e, "term"))
            anchors = self._entry_anchors(e)
            body = ""
            for li in kids(e, "listitem"):
                body += self.blocks(li, l) + "\n"
            if anchors:
                body = anchors + "\n\n" + body
            if terms:
                out.append(f"**{terms}**\n\n{body.strip()}")
            else:
                out.append(body.strip())
        return "\n\n".join(out)

    def L(self, key):
        return ("Term" if key == "term" else "Description") if self.lang == "en" \
            else ("术语" if key == "term" else "描述")

    def _varlist_simple(self, e) -> bool:
        items = kids(e, "listitem")
        if len(items) != 1:
            return False
        blocks = [x for x in items[0] if isinstance(x.tag, str)]
        if len(blocks) != 1 or tag(blocks[0]) not in ("para", "simpara"):
            return False
        if any(isinstance(x.tag, str) and tag(x) in BLOCK_IN_INLINE
               for x in blocks[0].iterdescendants()):
            return False
        txt = self.inline(blocks[0])
        if len(txt) > 400 or "\n" in txt:
            return False
        for t in kids(e, "term"):
            if len(self.inline(t)) > 80:
                return False
        return True

    def _varlist_rich(self, c, l, names=None):
        out = ["{{< fields >}}"]
        entries = kids(c, "varlistentry")
        for i, e in enumerate(entries):
            nm = " / ".join(names[i]) if names is not None and i < len(names) \
                else " / ".join(self._term_names(e))
            body = ""
            for li in kids(e, "listitem"):
                body += self.blocks(li, l) + "\n"
            anchors = self._entry_anchors(e)
            if anchors:
                body = anchors + "\n\n" + body
            out.append('{{< field name="%s" >}}' % esc_attr(nm))
            out.append(body.strip())
            out.append("{{< /field >}}")
        out.append("{{< /fields >}}")
        return "\n".join(out)

    # admonitions
    def tag_note(self, c, l): return self.callout(c, l)
    def tag_tip(self, c, l): return self.callout(c, l)
    def tag_important(self, c, l): return self.callout(c, l)
    def tag_warning(self, c, l): return self.callout(c, l)
    def tag_caution(self, c, l): return self.callout(c, l)

    def callout(self, c, l):
        kind = CALLOUT[tag(c)]
        title = self.inline_text(first_child(c, "title"))
        marker = f"[!{kind}]" + (f" {title}" if title else "")
        body = self.blocks(c, l).strip()
        if not body:
            return ""
        quoted = "\n".join("> " + ln if ln else ">" for ln in body.split("\n"))
        return f"> {marker}\n{quoted}"

    # code
    def tag_programlisting(self, c, l):
        text = code_text(c)
        return fence(text, classify(text))

    def tag_screen(self, c, l):
        text = code_text(c)
        lang = "console" if re.search(r"^\s*[$%#=]|=> ", text, re.M) else ""
        return fence(text, lang)

    def tag_synopsis(self, c, l):
        text = code_text(c)
        return fence(text, classify(text) or "sql")

    def tag_literallayout(self, c, l):
        return fence(code_text(c), "")

    def tag_cmdsynopsis(self, c, l):
        lines = []
        for part in c:
            if not isinstance(part.tag, str):
                continue
            t = tag(part)
            txt = plain_text(part)
            rep = "..." if part.get("rep") == "repeat" else ""
            if t == "command":
                lines.append(txt)
            elif t == "arg":
                wrap = ("[%s]%s" if part.get("choice") not in ("plain", "req")
                        else "%s%s")
                lines.append("    " + (wrap % (txt, rep)))
            elif t == "group":
                sep = part.get("sep") or "|"
                opts = [plain_text(a) for a in kids(part, "arg")]
                joined = f" {sep} ".join(opts)
                lines.append(f"    [{joined}]{rep}")
            else:
                lines.append("    " + txt)
        return fence("\n".join(lines), "")

    # tables
    def tag_table(self, c, l): return self.table(c, formal=True)
    def tag_informaltable(self, c, l): return self.table(c, formal=False)

    def table(self, c, formal):
        if has_spans(c):
            return self.html_table(c)
        header: list[str] = []
        rows: list[list[str]] = []
        tgroup = first_child(c, "tgroup") or c
        thead = first_child(tgroup, "thead")
        if thead is not None:
            for tr in kids(thead, "row"):
                header = [cell(self.entry_text(e)) for e in kids(tr, "entry")]
        for tbody in kids(tgroup, "tbody"):
            for tr in kids(tbody, "row"):
                rows.append([cell(self.entry_text(e))
                             for e in kids(tr, "entry")])
        if not rows and not header:
            return ""
        ncols = max([len(header)] + [len(r) for r in rows]) if rows else len(header)
        if not header:
            header = [""] * ncols
        header += [""] * (ncols - len(header))
        rows = [r + [""] * (ncols - len(r)) for r in rows]
        out = ["| " + " | ".join(header) + " |",
               "| " + " | ".join("---" for _ in header) + " |"]
        out += ["| " + " | ".join(r) + " |" for r in rows]
        attrs = [".td-table--wide"]
        cid = c.get("id", "")
        if cid:
            attrs.append(f"#{cid}")
        if formal:
            title = self.inline_text(first_child(c, "title"))
            if title:
                self.counters["table"] += 1
                if self.page.num:
                    attrs.append('num="%s.%d"' % (self.page.num,
                                                  self.counters["table"]))
                attrs.append('caption="%s"' % esc_attr(title))
        return "\n".join(out) + "\n{" + " ".join(attrs) + "}"

    def entry_text(self, entry) -> str:
        parts = []
        for c in entry:
            if not isinstance(c.tag, str):
                continue
            t = tag(c)
            if t == "para":
                saved = getattr(self, "_q", None)
                self._q = []
                try:
                    txt = self.inline(c)
                    q = self._q
                finally:
                    self._q = saved
                if q and PH_RE.search(txt):
                    cell_parts = []
                    pos = 0
                    for m in PH_RE.finditer(txt):
                        pre = txt[pos:m.start()].strip()
                        if pre:
                            cell_parts.append(pre)
                        blk = q[int(m.group(1))]
                        cell_parts.append(
                            PH_RE.sub("", blk).strip().replace("\n", "<br>"))
                        pos = m.end()
                    post = txt[pos:].strip()
                    if post:
                        cell_parts.append(post)
                    parts.append("<br>".join(p for p in cell_parts if p))
                else:
                    parts.append(txt.strip())
            elif t in ("itemizedlist", "orderedlist", "variablelist",
                       "programlisting", "screen", "synopsis"):
                parts.append(self.block(c, 3).replace("\n", "<br>"))
            else:
                parts.append(self.inline(c).strip())
        txt = "<br>".join(p for p in parts if p)
        cid = entry.get("id", "")
        if cid:
            txt = f'<span id="{cid}"></span>{txt}'
        return txt

    def html_table(self, c):
        rows_html = []
        for tr in c.iter("row"):
            cells = []
            for e in kids(tr, "entry", "entrytbl"):
                if tag(e) == "entrytbl":
                    cells.append(f"<td>{self.html_table(e)}</td>")
                    continue
                text = self.entry_text(e).replace("|", "\\|")
                span = ""
                if e.get("namest"):
                    span += ' colspan="2"'
                if e.get("morerows"):
                    span += f' rowspan="{int(e.get("morerows")) + 1}"'
                cells.append(f"<td{span}>{text}</td>")
            if cells:
                rows_html.append("<tr>" + "".join(cells) + "</tr>")
        title = first_child(c, "title")
        cap = ""
        if title is not None:
            cap = f"<caption>{esc_html(plain_text(title))}</caption>"
        table = f'<table class="table td-raw">{cap}{"".join(rows_html)}</table>'
        cid = c.get("id", "")
        if cid:
            table = f'<span id="{cid}"></span>\n\n' + table
        return table

    # figures / examples
    def tag_figure(self, c, l):
        img = None
        for im in c.iter("imagedata"):
            if im.get("fileref"):
                img = im.get("fileref").replace("images/", "/images/")
                break
        title = self.inline_text(first_child(c, "title"))
        attrs = []
        cid = c.get("id", "")
        if cid:
            attrs.append(f"#{cid}")
        if title:
            self.counters["figure"] += 1
            if self.page.num:
                attrs.append('num="%s.%d"' % (self.page.num,
                                              self.counters["figure"]))
            attrs.append('caption="%s"' % esc_attr(title))
        parts = []
        if img:
            parts.append(f"![{esc_attr(title or 'figure')}]({img})")
            if attrs:
                parts.append("{" + " ".join(attrs) + "}")
        for child in c:
            if not isinstance(child.tag, str) or tag(child) in (
                    "title", "mediaobject", "caption"):
                continue
            parts.append(self.block(child, l))
        return "\n\n".join(parts)

    def tag_mediaobject(self, c, l):
        for im in c.iter("imagedata"):
            if im.get("fileref"):
                alt = plain_text(first_child(c, "textobject")) or "figure"
                return (f"![{esc_attr(alt)}]("
                        f"{im.get('fileref').replace('images/', '/images/')})")
        return ""

    def tag_example(self, c, l):
        title = self.inline_text(first_child(c, "title"))
        body = self.blocks(c, l)
        label = "Example" if self.lang == "en" else "例"
        return f"**{label} — {title}**\n\n{body}" if title else body

    def tag_blockquote(self, c, l):
        body = self.blocks(c, l).strip()
        return "\n".join("> " + ln if ln else ">" for ln in body.split("\n"))

    def tag_sidebar(self, c, l):
        title = self.inline_text(first_child(c, "title"))
        body = self.blocks(c, l)
        return f"**{title}**\n\n{body}" if title else body

    # glossary / bibliography / qandaset
    def tag_glossentry(self, c, l):
        cid = c.get("id", "")
        anchor = f" {{#{cid}}}" if cid else ""
        terms = " / ".join(self.inline_text(t) for t in kids(c, "glossterm"))
        out = [f"### {terms}{anchor}"]
        seealso = []
        for gd in kids(c, "glossdef"):
            for child in gd:
                if not isinstance(child.tag, str):
                    continue
                if tag(child) == "glossseealso":
                    seealso.append(self.inline_text(child))
                else:
                    md = self.block(child, l + 1)
                    if md:
                        out.append(md)
        if seealso:
            see = "See also" if self.lang == "en" else "参见"
            out.append(f"**{see}:** " + ", ".join(seealso))
        return "\n\n".join(out)

    def tag_glossdef(self, c, l):
        return self.blocks(c, l)

    def tag_bibliomixed(self, c, l):
        return "- " + self.inline(c).strip()

    def tag_bibliolist(self, c, l):
        return self.blocks(c, l)

    def tag_qandaset(self, c, l):
        out = []
        for entry in c.iter("qandaentry"):
            q = first_child(entry, "question")
            a = first_child(entry, "answer")
            if q is not None:
                out.append(f"**{self.inline_text(q)}**")
            if a is not None:
                out.append(self.blocks(a, l))
        return "\n\n".join(out)

    def tag_partintro(self, c, l):
        return self.blocks(c, l)

    # ------------------------------------------------------------------
    # inline
    # ------------------------------------------------------------------
    def inline_flat(self, el) -> str:
        """Inline render with local block queue, placeholders flattened."""
        saved = getattr(self, "_q", None)
        self._q = []
        try:
            txt = self.inline(el)
            q = self._q
        finally:
            self._q = saved
        if not q or not PH_RE.search(txt):
            return txt.strip()
        parts = []
        pos = 0
        for m in PH_RE.finditer(txt):
            pre = txt[pos:m.start()].strip()
            if pre:
                parts.append(pre)
            parts.append(PH_RE.sub("", q[int(m.group(1))]).strip()
                         .replace("\n", "<br>"))
            pos = m.end()
        post = txt[pos:].strip()
        if post:
            parts.append(post)
        return "<br>".join(x for x in parts if x)

    def inline_text(self, el) -> str:
        if el is None:
            return ""
        saved = getattr(self, "_q", None)
        self._q = []
        try:
            out = self.inline(el).strip()
        finally:
            self._q = saved
        return PH_RE.sub("", out)

    def inline(self, el) -> str:
        if el is None:
            return ""
        parts = [self.txt(el.text)]
        for c in el:
            if not isinstance(c.tag, str):
                parts.append(self.txt(c.tail or ""))
                continue
            t = tag(c)
            if t in BLOCK_IN_INLINE and getattr(self, "_q", None) is not None:
                md = self.block(c, 3)
                idx = len(self._q)
                self._q.append(md)
                parts.append(f"\x02{idx}\x03")
            else:
                h = getattr(self, "in_" + t, None)
                if h is not None:
                    parts.append(h(c))
                else:
                    parts.append(self.inline(c))
            parts.append(self.txt(c.tail or ""))
        return "".join(parts)

    def txt(self, s: str) -> str:
        if not s:
            return ""
        if not s.strip():
            return " "
        lead = " " if s[:1].isspace() else ""
        trail = " " if s[-1:].isspace() else ""
        body = " ".join(s.split())
        if self.lang == "zh" and re.search(r"[\u3400-\u9fff]", body):
            body = normalize_prose(body)
        return lead + esc_md(body) + trail

    def code_span(self, c) -> str:
        return md_code(plain_text(c))

    in_literal = code_span
    in_command = code_span
    in_option = code_span
    in_parameter = code_span
    in_varname = code_span
    in_filename = code_span
    in_function = code_span
    in_type = code_span
    in_classname = code_span
    in_structname = code_span
    in_structfield = code_span
    in_symbol = code_span
    in_methodname = code_span
    in_modifier = code_span
    in_envar = code_span
    in_returnvalue = code_span
    in_constant = code_span
    in_sgmltag = code_span
    in_token = code_span
    in_errortext = code_span
    in_errcode = code_span
    in_database = code_span

    def in_replaceable(self, c):
        # <literal><replaceable>x</replaceable></literal> arrives flattened by
        # plain_text(); a bare replaceable renders as italic text.
        return "*" + self.inline(c) + "*"

    def in_application(self, c):
        return "**" + self.inline(c) + "**"

    def in_emphasis(self, c):
        body = self.inline(c)
        return f"**{body}**" if c.get("role") == "bold" else f"*{body}*"

    def in_quote(self, c):
        return f"\u201c{self.inline(c)}\u201d"

    def _gloss_link(self, c, italic):
        body = self.inline(c)
        ref = c.get("linkend", "")
        if ref and ref in self.targets:
            body = f"[{body}]({self.url_for(ref)})"
        return f"*{body}*" if italic else body

    def in_firstterm(self, c): return self._gloss_link(c, True)
    def in_glossterm(self, c): return self._gloss_link(c, True)

    def in_citetitle(self, c): return "*" + self.inline(c) + "*"
    def in_acronym(self, c): return self.inline(c)
    def in_productname(self, c): return self.inline(c)
    def in_foreignphrase(self, c): return self.inline(c)
    def in_systemitem(self, c): return self.inline(c)
    def in_hardware(self, c): return self.inline(c)
    def in_guibutton(self, c): return "**" + self.inline(c) + "**"
    def in_guimenu(self, c): return self.inline(c)
    def in_guimenuitem(self, c): return self.inline(c)
    def in_guilabel(self, c): return "*" + self.inline(c) + "*"
    def in_keycap(self, c): return "**" + self.inline(c) + "**"
    def in_keycombo(self, c): return self.inline(c)
    def in_interfacename(self, c): return self.inline(c)

    def in_ulink(self, c):
        url = c.get("url", "")
        body = self.inline(c).strip() or url
        return f"[{body}]({url})"

    def in_email(self, c):
        addr = plain_text(c)
        return f"[{addr}](mailto:{addr})"

    def in_anchor(self, c):
        cid = c.get("id", "")
        return f'<span id="{cid}"></span>' if cid else ""

    def in_xref(self, c):
        ref = c.get("linkend", "")
        endterm = c.get("endterm", "")
        t = self.targets.get(ref)
        if t is None:
            self.warn.append(f"xref?{ref} on {self.page.slug}")
            return md_code(ref)
        label = t.label
        if endterm:
            et = self.targets.get(endterm)
            if et is not None:
                label = et.label
        url = self.url_for(ref)
        return f"[{label}]({url})"

    def in_link(self, c):
        ref = c.get("linkend", "")
        body = self.inline(c).strip()
        if not ref:
            return body
        if ref not in self.targets:
            self.warn.append(f"link?{ref} on {self.page.slug}")
            return body
        return f"[{body}]({self.url_for(ref)})"

    def in_optional(self, c):
        return "[" + self.inline(c) + "]"

    def in_lineannotation(self, c):
        return self.inline(c)

    def in_indexterm(self, c):
        cid = c.get("id", "")
        return f'<span id="{cid}"></span>' if cid else ""

    def in_phrase(self, c):
        return self.inline(c)


ANCHORED_BY_HANDLER = {
    "sect1", "sect2", "sect3", "sect4", "sect5", "refsect1", "refsect2",
    "refsect3", "glossdiv", "bibliodiv", "reference", "refsynopsisdiv",
    "glossentry", "table", "informaltable", "figure", "varlistentry",
    "formalpara",
}


# ==========================================================================
# text helpers
# ==========================================================================

def esc_md(s: str) -> str:
    if not s:
        return s
    out = []
    for ch in s:
        if ch in ("\\", "*", "[", "`"):
            out.append("\\" + ch)
        else:
            out.append(ch)
    return "".join(out)


def md_code(s: str) -> str:
    if not s:
        return ""
    s = " ".join(s.split()).replace("\u00a0", " ")
    if "`" in s:
        return f"`` {s} ``"
    return f"`{s}`"


def esc_attr(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def esc_html(s: str) -> str:
    return esc_attr(s)


def cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", "<br>").strip()


def classify(text: str) -> str:
    t = text.lstrip()
    first = t.split("\n", 1)[0].strip()
    head = first.split(None, 1)[0].upper().strip("(") if first else ""
    if head in SQL_KEYWORDS:
        return "sql"
    if re.match(r"^(#include|static |PGDLLEXPORT|extern |Datum|typedef|#define|"
                r"struct |#ifdef|Oid|bool|void|return)", t):
        return "c"
    if re.match(r"^(\$ |% |#!|/[\w.-]+/[\w./-]+ )", t):
        return "console"
    if t.startswith("<") and re.search(r"</\w+>", t):
        return "xml"
    return ""


def fence(text: str, lang: str) -> str:
    text = dedent_code(text)
    n = 3
    while "`" * n in text:
        n += 1
    f = "`" * n
    return f"{f}{lang}\n{text}\n{f}"


def dedent_code(text: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    cut = min(indents) if indents else 0
    return "\n".join(l[cut:] if l.strip() else "" for l in lines)


def code_text(el) -> str:
    parts: list[str] = []

    def rec(e):
        parts.append(e.text or "")
        for c in e:
            if isinstance(c.tag, str):
                rec(c)
            if c.tail:
                parts.append(c.tail)

    rec(el)
    return "".join(parts)


def indent_block(body: str, marker: str) -> str:
    lines = body.rstrip("\n").split("\n")
    # a blank first line comes from skipping the listitem "title"-less blocks
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        return ""
    pad = " " * len(marker)
    out = [marker + lines[0]]
    for ln in lines[1:]:
        out.append((pad + ln) if ln.strip() else "")
    return "\n".join(out)


def has_spans(table) -> bool:
    for e in table.iter():
        if isinstance(e.tag, str) and (e.get("namest") or e.get("nameend")
                                       or e.get("morerows")):
            return True
    return False


def zh_polish(md_text: str) -> str:
    """Fullwidth/pangu cleanup across inline-element boundaries, reusing the
    repo's shared rule core on every non-code, non-link chunk."""
    out = []
    i, n = 0, len(md_text)
    while i < n:
        ch = md_text[i]
        if ch == "`":                          # protect code spans / fences
            j = md_text.find("`", i + 1)
            j = n if j < 0 else j + 1
            out.append(md_text[i:j])
            i = j
            continue
        if ch == "[":
            j = md_text.find(")", i)
            j = n if j < 0 else j + 1
            out.append(md_text[i:j])
            i = j
            continue
        out.append(ch)
        i += 1
    return normalize_prose("".join(out))


# ==========================================================================
# page output
# ==========================================================================

def page_rel_path(page: Page, lang: str) -> Path:
    suffix = "" if lang == "en" else ".zh"
    d = OUT_DIR / page.dir if page.dir else OUT_DIR
    name = "_index" if page.kind in ("part", "chapterindex", "contrib") \
        else page.slug
    return d / f"{name}{suffix}.md"


def render_page(page: Page, lang: str, targets: dict) -> tuple[str, list]:
    r = Renderer(lang, targets, page)
    root = page.el
    body = r.blocks_skip_title(root)
    fm = ["---"]

    def kv(k, v):
        if v is None or v == "" or v == []:
            return
        fm.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")

    kv("title", page.title)
    kv("linkTitle", page.title if len(page.title) <= 30
       else page.title[:28] + "…")
    kv("description", page.desc)
    kv("weight", page.weight)
    kv("icon", page.icon)
    if page.root_id and page.kind != "legal":
        kv("upstream_link", UPSTREAM + page.root_id + ".html")
    else:
        kv("upstream_link", UPSTREAM)
    kv("upstream_name", f"PostgreSQL {PG_VERSION} Documentation")
    kv("upstream_copyright",
       "Copyright © 1996-2026, The PostgreSQL Global Development Group")
    kv("upstream_license", "PostgreSQL")
    kv("upstream_notice", "https://www.postgresql.org/about/licence/")
    if page.search_keywords:
        fm.append("search_keywords: "
                  + json.dumps(page.search_keywords, ensure_ascii=False))
    fm.append("---")
    md = "\n".join(fm) + "\n\n" + body.strip() + "\n"
    return md, r.warn


def _blocks_skip_title(self, el, level=2):
    out = []
    for c in el:
        if not isinstance(c.tag, str):
            continue
        t = tag(c)
        if t in ("title", "refmeta", "refnamediv", "indexterm", "titleabbrev",
                 "bookinfo", "refentryinfo", "docinfo", "prefaceinfo"):
            continue
        # index pages: children that became their own pages are not re-rendered
        if self.page.kind in ("chapterindex", "contrib") and t == "sect1":
            continue
        md = self.block(c, level)
        if md and md.strip():
            out.append(md.strip("\n"))
    return "\n\n".join(out)


Renderer.blocks_skip_title = _blocks_skip_title


def bind_language(man: Manifest, lang: str, tree,
                  en_by_stem: dict) -> tuple[list, list]:
    """Bind page elements to this language's tree (id first, stem fallback)."""
    by_id = {e.get("id"): e for e in tree.iter()
             if isinstance(e.tag, str) and e.get("id")}
    by_stem: dict[str, list] = {}
    for e in tree.iter():
        if isinstance(e.tag, str):
            by_stem.setdefault(e.get("__stem", ""), []).append(e)

    pages: list[Page] = []
    missing = []
    for p in man.pages:
        el = None
        if lang == "en":
            el = p.el
        else:
            if p.root_id and p.root_id in by_id:
                el = by_id[p.root_id]
            else:
                enl = en_by_stem.get(p.stem, [])
                zhl = by_stem.get(p.stem, [])
                try:
                    idx = enl.index(p.el)
                    el = zhl[idx] if idx < len(zhl) else None
                except ValueError:
                    el = None
        pl = Page(p.kind, p.slug, p.dir, p.stem, p.weight, p.num, p.roman,
                  p.root_id, p.icon, el=el)
        if el is None:
            missing.append(f"[{lang}] no element for {p.dir}/{p.slug}")
            continue
        pl.title = title_for(el, pl, lang)
        pl.desc = desc_for(el)
        pl.search_keywords = collect_keywords(el)
        pages.append(pl)
    return pages, missing


def title_for(el, page: Page, lang: str) -> str:
    t = first_child(el, "title", "refentrytitle", "glossterm")
    if t is not None and plain_text(t):
        return plain_text(t)
    if tag(el) == "refentry":
        rm = first_child(el, "refmeta")
        if rm is not None:
            rt = first_child(rm, "refentrytitle")
            if rt is not None:
                return plain_text(rt)
    if page.kind == "legal":
        return "Legal Notice" if lang == "en" else "法律声明"
    return page.root_id or page.slug


def desc_for(el) -> str:
    if tag(el) == "refentry":
        rn = first_child(el, "refnamediv")
        if rn is not None:
            rp = first_child(rn, "refpurpose")
            if rp is not None:
                return plain_text(rp)
    for c in el.iter("para", "simpara"):
        s = plain_text(c)
        if s:
            return (s[:190] + "…") if len(s) > 190 else s
    return ""


def collect_keywords(el) -> list:
    kws, seen = [], set()
    for it in el.iter("indexterm"):
        parts = []
        for lvl in ("primary", "secondary", "tertiary"):
            x = first_child(it, lvl)
            if x is not None:
                parts.append(plain_text(x))
        s = " ".join(p for p in parts if p)
        if s and s.lower() not in seen:
            seen.add(s.lower())
            kws.append(s)
    return kws[:40]


# ==========================================================================
# driver
# ==========================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="both", choices=["en", "zh", "both"])
    args = ap.parse_args()
    langs = ["en", "zh"] if args.lang == "both" else [args.lang]

    print("assembling EN book ...")
    gen_en = OINK / "tools" / "generated"
    gen_zh = OINK / "tools" / "generated-zh"
    en_tree = parse_book(expand_book(EN_DIR, fallback=gen_en))
    annotate_stems(en_tree)
    man = build_manifest(en_tree, EN_DIR)
    kinds = {}
    for p in man.pages:
        kinds[p.kind] = kinds.get(p.kind, 0) + 1
    print(f"  pages: {len(man.pages)}  {kinds}")

    for child in sorted(OUT_DIR.iterdir()) if OUT_DIR.exists() else []:
        if child.name.startswith("_index"):
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

    if IMG_SRC.is_dir():
        IMG_OUT.mkdir(parents=True, exist_ok=True)
        for f in IMG_SRC.glob("*.svg"):
            shutil.copy2(f, IMG_OUT / f.name)

    warnings: list[str] = []
    en_by_stem: dict[str, list] = {}
    for e in en_tree.iter():
        if isinstance(e.tag, str):
            en_by_stem.setdefault(e.get("__stem", ""), []).append(e)

    for lang in langs:
        if lang == "en":
            tree = en_tree
        else:
            print("assembling ZH book ...")
            tree = parse_book(expand_book(ZH_DIR, skip={"pgdoccn-notes"},
                                          fallback=gen_zh))
            annotate_stems(tree)
        pages, missing = bind_language(man, lang, tree, en_by_stem)
        warnings.extend(missing)
        targets = collect_targets(_wrap(pages), lang)
        for pl in pages:
            path = page_rel_path(pl, lang)
            path.parent.mkdir(parents=True, exist_ok=True)
            md, warns = render_page(pl, lang, targets)
            path.write_text(md)
            warnings.extend(f"[{lang}] {w}" for w in warns)
        print(f"  [{lang}] wrote {len(pages)} pages")

    if warnings:
        wf = OINK / "tools" / "convert-warnings.log"
        wf.write_text("\n".join(warnings) + "\n")
        print(f"{len(warnings)} warnings -> {wf}")
        for w in warnings[:25]:
            print("   ", w)
    else:
        print("clean: no warnings")


def _wrap(pages):
    m = Manifest.__new__(Manifest)
    m.pages = pages
    m.chapter_no = m.appendix_no = m.part_no = 0
    return m


if __name__ == "__main__":
    main()
