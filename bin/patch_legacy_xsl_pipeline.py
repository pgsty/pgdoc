#!/usr/bin/env python3
"""Adapt historical XSL pipelines in an isolated documentation build tree.

PG 9.2+ doc/src/sgml/Makefile ships an xslthtml-stamp target, and PG 9.4+
postgres.sgml/filelist.sgml carry the include-xslt-index marked section, so
the jade-free XSL pipeline (osx -> postgres.xml -> xsltproc) renders chunked
HTML / XSL-FO with a stylesheet-generated index.  PG 9.1 and older only have
the pre-stamp xslthtml target, no marked section, and a narrower SDATA entity
fixup list, while this toolchain does not ship DSSSL jade at all.

Patches applied in place (all guarded; idempotent):

  filelist.sgml   declare %include-xslt-index (9.4 form); PG <= 8.4 lacks
                  %include-index too, so the fallback declares both
  postgres.sgml   add the include-xslt-index marked section (9.4 form);
                  PG <= 8.4 references &bookindex; bare, so wrap that
  Makefile        osx step: -i include-xslt-index
                  postgres.xml entity fixup: 9.4 entity list, /gi
                  html: html-stamp -> html: xslthtml-stamp
                  html: html-output (+HTML.index retry recipe,
                    PG <= 8.4) -> html: xslthtml-stamp
                  postgres.xml prerequisites: PG <= 8.4 depend on
                  $(GENERATED_SGML) (pulls in the jade-only
                    bookindex.sgml chain) -> $(ALMOSTALLSGML) (9.x form)
                  append 9.4-recipe xslthtml-stamp target

PG 6.x doc makefiles (jade/DSSSL-only: no html: target, no postgres.xml rule,
uppercase-era sources relying on omitted end tags) get a self-contained
appended block instead: osx (with an OMITTAG YES DocBook V3.0 declaration,
see tmp/pg6x/deps) -> postgres.xml -> xsltproc chunked HTML.

Usage: patch_legacy_xsl_pipeline.py <doc/src/sgml dir>
Existing native XSL targets are preserved. Their missing index activation
and historical SDATA filters are still repaired when needed.
"""
import os
import re
import sys

PERL_91 = (r"""	$(PERL) -p -e 's/\[(amp|copy|egrave|gt|lt|mdash|nbsp|ouml|pi|quot|uuml) *\]/\&\1;/g;' \
""")
PERL_94 = (r"""	$(PERL) -p -e 's/\[(aacute|acirc|aelig|agrave|amp|aring|atilde|auml|bull|copy|eacute|egrave|gt|iacute|lt|mdash|nbsp|ntilde|oacute|ocirc|oslash|ouml|pi|quot|scaron|uuml) *\]/\&\1;/gi;' \
""")
# PG <= 8.4 pipes osx straight into perl with the continuation indented by
# tab+2spaces instead of the 9.x temp-file form (tab only).
PERL_84 = (r"""	  $(PERL) -p -e 's/\[(amp|copy|egrave|gt|lt|mdash|nbsp|ouml|pi|quot|uuml) *\]/\&\1;/g;' \
""")
PERL_94_PIPE = (r"""	  $(PERL) -p -e 's/\[(aacute|acirc|aelig|agrave|amp|aring|atilde|auml|bull|copy|eacute|egrave|gt|iacute|lt|mdash|nbsp|ntilde|oacute|ocirc|oslash|ouml|pi|quot|scaron|uuml) *\]/\&\1;/gi;' \
""")
OSX_OLD = "\t$(OSX) -D. -x lower $<"
OSX_NEW = "\t$(OSX) -D. -x lower -i include-xslt-index $<"
# PG <= 8.3 pipes osx into sed (entity fixup + DOCTYPE append) instead of
# 8.4's perl.  Normalize that recipe to the 8.4 form first so the anchors
# below (OSX_OLD / PERL_84 / PGXML_OLD) all apply unchanged.
SED_RECIPE_83 = (
    "\npostgres.xml: postgres.sgml $(GENERATED_SGML)\n"
    "\t$(OSX) -x lower $< | \\\n"
    "\t  sed -e 's/\\[\\(amp\\|copy\\|egrave\\|gt\\|lt\\|mdash\\|nbsp\\|ouml\\|pi\\|quot\\|uuml\\) *\\]/\\&\\1;/g' \\\n"
    "\t      -e '1a\\' -e '<!DOCTYPE book PUBLIC \"-//OASIS//DTD DocBook XML V4.2//EN\" \"http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd\">' \\\n"
    "\t  >$@\n"
)
# PG 8.0/8.1 use the same osx|sed recipe but order the entity alternation
# lt-first; keep both spellings so the normalization applies to them too.
SED_RECIPE_80 = (
    "\npostgres.xml: postgres.sgml $(GENERATED_SGML)\n"
    "\t$(OSX) -x lower $< | \\\n"
    "\t  sed -e 's/\\[\\(lt\\|gt\\|amp\\|nbsp\\|copy\\|quot\\|ouml\\|uuml\\|egrave\\) *\\]/\\&\\1;/g' \\\n"
    "\t      -e '1a\\' -e '<!DOCTYPE book PUBLIC \"-//OASIS//DTD DocBook XML V4.2//EN\" \"http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd\">' \\\n"
    "\t  >$@\n"
)
PERL_RECIPE_84 = (
    "\npostgres.xml: postgres.sgml $(GENERATED_SGML)\n"
    "\t$(OSX) -D. -x lower $< | \\\n"
    "\t  $(PERL) -p -e 's/\\[(amp|copy|egrave|gt|lt|mdash|nbsp|ouml|pi|quot|uuml) *\\]/\\&\\1;/g;' \\\n"
    "\t             -e '$$_ .= qq{<!DOCTYPE book PUBLIC \"-//OASIS//DTD DocBook XML V4.2//EN\" \"http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd\">\\n} if $$. == 1;' \\\n"
    "\t  >$@\n"
)
# PG <= 8.4 assigns OSX/XSLTPROC unconditionally, so the tool paths exported
# by the zh Makefile (deps/bin) cannot reach the recipes.  9.x wraps them in
# ifndef; do the same here.
OSX_DEF_8X = "OSX = osx # (may be called sx or sgml2xml on some systems)\n"
OSX_DEF_8X_WRAPPED = ("ifndef OSX\n"
                      "OSX = osx # (may be called sx or sgml2xml on some systems)\n"
                      "endif\n")
# PG <= 8.4 routes html through the DSSSL html-output target and re-runs
# itself until HTML.index settles; both must go when html flips to XSL.
HTML_84 = ("\nhtml: html-output\n"
           "# Re-run this target until HTML.index does not change\n"
           "\t@cmp -s HTML.index.start HTML.index || $(MAKE) $@\n")
# PG <= 8.2 routes html straight through jade with no index re-run loop.
HTML_82 = ("\nhtml: postgres.sgml $(ALLSGML) stylesheet.dsl\n"
           "\t@rm -f *.html\n"
           "\t$(JADE) $(JADEFLAGS) $(SPFLAGS) $(SGMLINCLUDE) $(CATALOG)"
           " -d stylesheet.dsl -i output-html -t sgml $<\n")
HTML_NEW = "\nhtml: xslthtml-stamp\n"
# PG <= 8.4 builds postgres.xml from $(GENERATED_SGML), which contains
# bookindex.sgml -- only producible via the jade HTML.index chain.  9.x uses
# ALMOSTALLSGML (same list minus bookindex.sgml) for exactly this reason.
PGXML_OLD = "\npostgres.xml: postgres.sgml $(GENERATED_SGML)\n"
PGXML_NEW = "\npostgres.xml: postgres.sgml $(ALMOSTALLSGML)\n"
ALLSGML_8X = "\nALLSGML := $(wildcard $(srcdir)/*.sgml $(srcdir)/ref/*.sgml) $(GENERATED_SGML)\n"
ALMOST_DEF = "\nALMOSTALLSGML := $(filter-out %bookindex.sgml,$(ALLSGML))\n"
XSLTHTML_BLOCK = """
# -- begin pgdoc backport: XSL HTML pipeline for PG <= 9.1 (patch_legacy_xsl_pipeline.py) --
xslthtml: xslthtml-stamp

xslthtml-stamp: stylesheet.xsl postgres.xml
	$(XSLTPROC) $(XSLTPROCFLAGS) $(XSLTPROC_HTML_FLAGS) $^
	cp $(srcdir)/stylesheet.css html/
	touch $@
# -- end pgdoc backport --
"""

# PG <= 8.1 ships stylesheet-fo.xsl but no make rules for it (the XSL-FO
# targets only appear in later upstream Makefiles, and the backported 8.2/8.3
# trees lose them as well).  Append the 9.4-form FO chain so
# build_standalone_pdfsrc.sh's `make postgres-{A4,US}.fo` resolves.  Only
# added when stylesheet-fo.xsl is present and no fo rule exists yet.
XSLFO_BLOCK = """
# -- begin pgdoc backport: XSL-FO targets for PG <= 9.1 (patch_legacy_xsl_pipeline.py) --
%-A4.fo.tmp: stylesheet-fo.xsl %.xml
	$(XSLTPROC) $(XSLTPROCFLAGS) --stringparam paper.type A4 -o $@ $^

%-US.fo.tmp: stylesheet-fo.xsl %.xml
	$(XSLTPROC) $(XSLTPROCFLAGS) --stringparam paper.type USletter -o $@ $^

XMLLINT ?= xmllint

# reformat FO output so that locations of errors are easier to find
%.fo: %.fo.tmp
	$(XMLLINT) --format --output $@ $^

.SECONDARY: postgres-A4.fo postgres-US.fo
# -- end pgdoc backport --
"""

FILELIST_FALLBACK = (
    "\n<!--\n"
    " Local hack (pgdoc): marked-section keywords for the XSL pipeline's\n"
    " stylesheet-generated index.  Upstream added these in PG 9.x; see the\n"
    " release.sgml of 9.0 for the original form.\n"
    " -->\n"
    '<!ENTITY % include-index "IGNORE">\n'
    '<!ENTITY % include-xslt-index "IGNORE">\n'
)

# SDATA fixup names for the PG 6.x recipe: the 9.4 list (PERL_94) plus the
# ISO names actually emitted when converting the 6.3-6.5 English trees
# (math/set operators absent from modern docs: and cap cup exist ge isin
# le mid minus prod setmn sigma sube tdot times) plus plausible additions
# for zh reuse sources (divide infin plusmn sup); all verified ISO names.
SDATA_6X = (
    "aacute acirc aelig agrave amp and aring atilde auml bull cap copy cup "
    "divide eacute egrave exist ge gt iacute infin isin le lt mdash mid "
    "minus nbsp ntilde oacute ocirc oslash ouml pi plusmn prod quot scaron "
    "percnt setmn sigma sube sup tdot times uuml"
)

# PG 6.x block appended to the (static, jade-era) doc makefile.  Tool vars
# use ?= so the deps environment wins; the SGML declaration is passed as an
# explicit osx argument because 6.x sources rely on omitted end tags, which
# the stock DocBook V3.0 declaration (OMITTAG NO) rejects.  -Dref covers the
# 6.4 reference.sgml -> allfiles.sgml system id (jade's old -D ref DBOPTS).
XSLTHTML_BLOCK_6X_TEMPLATE = """
# -- begin pgdoc backport: XSL HTML pipeline for PG 6.x (patch_legacy_xsl_pipeline.py) --
OSX ?= osx
PYTHON ?= python3
PERL ?= perl
XSLTPROC ?= xsltproc
XSLTPROCFLAGS ?= --nonet
XSLTPROC_HTML_FLAGS ?= --path .
PGDOC_VERSION ?= {version}
override XSLTPROCFLAGS += --stringparam pg.version '$(PGDOC_VERSION)'
PGDOC_SGML_DECL := {sgml_decl}
PGDOC_ALLSGML := $(wildcard *.sgml ref/*.sgml)

postgres.xml: postgres.sgml $(PGDOC_ALLSGML)
\t$(OSX) -D. -Dref -x lower $(PGDOC_SGML_DECL) $< | \\
\t  $(PERL) -p -e 's/\\[({sdata}) *\\]/\\&\\1;/g;' \\
\t             -e '$$_ .= qq{{<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN" "http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd">\\n}} if $$. == 1;' \\
\t  | $(PYTHON) {normalizer} \
\t  >$@

html: xslthtml-stamp

xslthtml: xslthtml-stamp

xslthtml-stamp: stylesheet.xsl postgres.xml
\t$(XSLTPROC) $(XSLTPROCFLAGS) $(XSLTPROC_HTML_FLAGS) $^
\t-cp stylesheet.css html/
\ttouch $@
# -- end pgdoc backport --
"""


def patch_pg6x(sgml_dir):
    """Append the synthesized XSL pipeline onto a PG 6.x jade-era makefile.

    6.x is identified by the Davenport DocBook V3.0 doctype in postgres.sgml;
    7.x jade-era makefiles (V3.1, same no-html/no-postgres.xml shape) are left
    alone for the 7x program's own pipeline work.
    """
    makefile = f"{sgml_dir}/Makefile"
    with open(makefile, encoding="utf-8") as f:
        mf = f.read()
    if "xslthtml-stamp:" in mf or "postgres.xml:" in mf or "\nhtml:" in mf:
        return False
    try:
        with open(f"{sgml_dir}/postgres.sgml", encoding="utf-8", errors="replace") as f:
            pg = f.read()
    except OSError:
        return False
    if "-//Davenport//DTD DocBook V3.0//EN" not in pg:
        return False
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sgml_decl = f"{repo_root}/deps/sgml/docbook-omittag.dcl"
    if not os.path.exists(sgml_decl):
        print("patch_legacy_xsl_pipeline: WARNING:"
              f" {sgml_decl} missing; osx will fall back to OMITTAG NO",
              file=sys.stderr)
        sgml_decl = ""
    # The build work tree name embeds the version (build_standalone_docsrc.sh
    # mktemp pattern "standalone-<lang>-<version>.XXXXXX"); empty fallback is
    # harmless (pg.version only drives the footer/devel switches).
    m = re.search(r"standalone-(?:pdf-)?(en|zh)-(\d+\.\d+(?:\.\d+)?)\.[A-Za-z0-9]+",
                  os.path.abspath(sgml_dir))
    version = m.group(2) if m else ""
    sdata = "|".join(SDATA_6X.split())
    block = XSLTHTML_BLOCK_6X_TEMPLATE.format(
        version=version, sgml_decl=sgml_decl, sdata=sdata,
        normalizer=os.path.join(repo_root, "bin", "normalize_cals_tables.py"))
    # 原始上游 6.x 归档同样保留 jade 时代的宽松标记（ENDTERM 里裸 "["、
    # 正文里裸 "<email>" 等）；osx 报错但输出仍可被后续管线消费，这里把
    # osx 的退出码降级，错误保留在构建日志，坏 XML 由 xsltproc 硬拦。
    block = block.replace(
        "$(OSX) -D. -Dref -x lower $(PGDOC_SGML_DECL) $< |",
        "{ $(OSX) -D. -Dref -x lower $(PGDOC_SGML_DECL) $< || true; } |")
    mf += block
    # 2026-09-25: the synthesized html chain alone leaves `make postgres-A4.fo`
    # without a rule; append the shared FO block when the zh overlay carries
    # stylesheet-fo.xsl (it always does).
    if "%-A4.fo.tmp:" not in mf and os.path.exists(f"{sgml_dir}/stylesheet-fo.xsl"):
        mf += XSLFO_BLOCK
    with open(makefile, "w", encoding="utf-8") as f:
        f.write(mf)
    print("patch_legacy_xsl_pipeline: synthesized XSL pipeline onto PG 6.x"
          f" doc makefile (pgdoc version '{version}')")
    return True


def patch_pg7x(sgml_dir):
    """Synthesize the XSL pipeline onto a PG 7.x jade-era makefile.

    Same shape as 6.x (no postgres.xml rule) but the makefile usually already
    owns an `html:` target and may include src/Makefile.global
    (7.1 – 7.4 run top-level configure; 7.0's include is conditional).
    Rename the jade html target so the appended XSL rules win, then reuse the
    6.x block (DocBook V3.1 doctype, osx + SDATA fixup) plus the FO chain.
    """
    makefile = f"{sgml_dir}/Makefile"
    with open(makefile, encoding="utf-8") as f:
        mf = f.read()
    if "xslthtml-stamp:" in mf or "postgres.xml:" in mf:
        return False
    try:
        with open(f"{sgml_dir}/postgres.sgml", encoding="utf-8",
                  errors="replace") as f:
            pg = f.read()
    except OSError:
        return False
    if "-//oasis//dtd docbook v3.1//en" not in pg.lower():
        return False
    prepare_legacy_indexes(sgml_dir, pg)
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    m = re.search(r"standalone-(?:pdf-)?(en|zh)-(\d+\.\d+(?:\.\d+)?)\.[A-Za-z0-9]+",
                  os.path.abspath(sgml_dir))
    version = m.group(2) if m else ""
    sdata = "|".join(SDATA_6X.split())
    # jade 的 html 目标改名保留，避免 GNU make 的 overriding 警告与歧义。
    mf = re.sub(r"(?m)^html:", "jade-html:", mf)
    block = XSLTHTML_BLOCK_6X_TEMPLATE.format(
        version=version, sgml_decl="", sdata=sdata,
        normalizer=os.path.join(repo_root, "bin", "normalize_cals_tables.py"))
    # The separate legacy-EN compatibility path accepts historical upstream
    # SGML diagnostics. Never apply that exception to maintained translations
    # or unidentified work directories: their converter must fail strictly.
    if m and m.group(1) == 'en':
        block = block.replace(
            "$(OSX) -D. -Dref -x lower $(PGDOC_SGML_DECL) $< |",
            "{ $(OSX) -D. -Dref -x lower $(PGDOC_SGML_DECL) $< || true; } |")
    mf += block
    # features 附录引用 &features-supported; 等生成文件；合成的 postgres.xml 用
    # 通配符依赖不会触发生成规则，这里显式补一道（Makefile 已有对应规则时）。
    if re.search(r"(?m)^features-supported\.sgml:", mf):
        mf += ("\n\n# -- begin pgdoc backport: generated feature tables (PG 7.x) --\n"
               "postgres.xml: | pgdoc-features\n\n"
               "pgdoc-features:\n"
               "\t$(MAKE) features-supported.sgml features-unsupported.sgml\n"
               "# -- end pgdoc backport --\n")
    # postgres.sgml 引用 &version;；通配符依赖不触发上游的 version.sgml 规则。
    # 7.0 的版本实体内联在 postgres.sgml 里（Makefile 无 version.sgml 规则），跳过。
    if re.search(r"(?m)^version\.sgml:", mf):
        mf += ("\n\n# -- begin pgdoc backport: generated version entity (PG 7.x) --\n"
               "postgres.xml: | pgdoc-version\n\n"
               "pgdoc-version:\n"
               "\t@test -f version.sgml || $(MAKE) version.sgml\n"
               "# -- end pgdoc backport --\n")
    if "%-A4.fo.tmp:" not in mf and os.path.exists(f"{sgml_dir}/stylesheet-fo.xsl"):
        mf += XSLFO_BLOCK
    with open(makefile, "w", encoding="utf-8") as f:
        f.write(mf)
    print("patch_legacy_xsl_pipeline: synthesized XSL pipeline onto PG 7.x"
          f" doc makefile (pgdoc version '{version}')")
    return True


def prepare_legacy_indexes(sgml_dir, postgres):
    """Let XSL generate the old book/set indexes formerly produced by jade."""
    for name, tag in (('setindex', 'setindex'), ('bookindex', 'index')):
        path = os.path.join(sgml_dir, name + '.sgml')
        if f'&{name};' in postgres and not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as stream:
                stream.write(f'<{tag} id="{name}"></{tag}>\n')
            print(f'patch_legacy_xsl_pipeline: enabled generated {name}')


def prepare_native_xsl_index(sgml_dir):
    """Enable the stylesheet index without replacing native XSL targets.

    PG 9.2/9.3 can have xslthtml-stamp while their overlaid SGML still only
    has the jade index branch. A native target is not proof of index support.
    """
    pg_path = os.path.join(sgml_dir, 'postgres.sgml')
    if not os.path.isfile(pg_path):
        return
    with open(pg_path, encoding='utf-8') as stream:
        postgres = stream.read()
    active = re.sub(r'<!--.*?-->', '', postgres, flags=re.S)
    anchor = '<![%include-index;[&bookindex;]]>'
    if anchor not in active:
        return
    makefile = os.path.join(sgml_dir, 'Makefile')
    with open(makefile, encoding='utf-8') as stream:
        mf = stream.read()
    if '$(OSX)' not in mf:
        return  # XML-native releases have no SGML marked-section switch.
    if OSX_OLD in mf:
        updated_mf = mf.replace(OSX_OLD, OSX_NEW, 1)
    elif '-i include-xslt-index' in mf:
        updated_mf = mf
    else:
        raise ValueError('native XSL index requires an identifiable osx recipe')

    fl_path = os.path.join(sgml_dir, 'filelist.sgml')
    with open(fl_path, encoding='utf-8') as stream:
        filelist = stream.read()
    updated_fl = filelist
    if 'include-xslt-index' not in re.sub(r'<!--.*?-->', '', filelist, flags=re.S):
        updated_fl += '\n<!-- XSL generates the index formerly built by jade. -->\n<!ENTITY % include-xslt-index "IGNORE">\n'
    updated_pg = postgres
    if 'include-xslt-index' not in active:
        updated_pg = postgres.replace(anchor, anchor + '\n<![%include-xslt-index;[<index id="bookindex"></index>]]>', 1)
    changed = False
    for path, before, after in ((fl_path, filelist, updated_fl),
                                (pg_path, postgres, updated_pg),
                                (makefile, mf, updated_mf)):
        if before != after:
            with open(path, 'w', encoding='utf-8') as stream:
                stream.write(after)
            changed = True
    if changed:
        print('patch_legacy_xsl_pipeline: enabled index in native XSL pipeline')


def main():
    sgml_dir = sys.argv[1]
    makefile = f"{sgml_dir}/Makefile"
    with open(makefile, encoding="utf-8") as f:
        mf = f.read()

    if ("xslthtml-stamp:" in mf or
            re.search(r"^html-stamp:.*\bstylesheet\.xsl\b", mf, re.M)):
        prepare_native_xsl_index(sgml_dir)
        return  # Preserve native targets; PG10 renamed its stamp to html-stamp.
    if "postgres.xml:" not in mf:
        # PG 6.x jade-era makefiles have neither an html: target nor a
        # postgres.xml rule; the 6.x branch synthesizes the whole pipeline.
        # PG 7.x jade-era makefiles (DocBook V3.1) get the same treatment via
        # patch_pg7x; each patcher declines doctypes it does not recognise.
        if not patch_pg6x(sgml_dir):
            patch_pg7x(sgml_dir)
        return
    # PG <= 8.2 ships stylesheet.xsl + a bare "XSLTPROC = xsltproc"
    # assignment (no ifndef wrapper, no xslthtml target at all).  Wrap the
    # assignment so the deps tools can override it, and note that the
    # XSLTHTML_BLOCK below synthesizes the xslthtml/stamp targets.
    if "\nxslthtml:" not in mf:
        if "XSLTPROC = xsltproc\n" in mf:
            mf = mf.replace("XSLTPROC = xsltproc\n",
                            "ifndef XSLTPROC\nXSLTPROC = xsltproc\nendif\n", 1)
        if "XSLTPROC_HTML_FLAGS" not in mf:
            mf = mf.replace("XSLTHTML_BLOCK_PLACEHOLDER", "", 1)  # no-op
            mf += ("\noverride XSLTPROCFLAGS += --stringparam"
                   " pg.version '$(VERSION)'\n"
                   "XSLTPROC_HTML_FLAGS = --path .\n")

    # filelist.sgml: declare the marked-section keywords (9.4 form).  PG <= 8.4
    # has no %include-index declaration at all, so the fallback adds both --
    # postgres.sgml's wrapped &bookindex; references %include-index.
    fl_path = f"{sgml_dir}/filelist.sgml"
    with open(fl_path, encoding="utf-8") as f:
        fl = f.read()
    if "include-xslt-index" not in fl:
        anchor = '<!ENTITY % include-index "IGNORE">'
        if anchor in fl:
            decl = (anchor + "\n\n<!--\n Create empty index element for processing by XSLT stylesheet.\n"
                    " -->\n<!ENTITY % include-xslt-index \"IGNORE\">\n")
            fl = fl.replace(anchor, decl, 1)
        else:
            fl += "\n" + FILELIST_FALLBACK
        with open(fl_path, "w", encoding="utf-8") as f:
            f.write(fl)

    # postgres.sgml: emit the empty <index> under the marked section (9.4
    # form).  PG <= 8.4 references &bookindex; bare, wrap it with both
    # sections so osx -i include-xslt-index selects the XSL path.
    pg_path = f"{sgml_dir}/postgres.sgml"
    with open(pg_path, encoding="utf-8") as f:
        pg = f.read()
    if "include-xslt-index" not in pg:
        anchor = "<![%include-index;[&bookindex;]]>"
        section = anchor + "\n<![%include-xslt-index;[<index id=\"bookindex\"></index>]]>"
        if anchor in pg:
            pg = pg.replace(anchor, section, 1)
            with open(pg_path, "w", encoding="utf-8") as f:
                f.write(pg)
        elif "\n &bookindex;\n" in pg:
            pg = pg.replace("\n &bookindex;\n",
                            "\n <![%include-index;[&bookindex;]]>\n"
                            "<![%include-xslt-index;[<index id=\"bookindex\"></index>]]>\n", 1)
            with open(pg_path, "w", encoding="utf-8") as f:
                f.write(pg)
        else:
            print("patch_legacy_xsl_pipeline: WARNING: bookindex anchor not found in postgres.sgml",
                  file=sys.stderr)

    # Makefile: normalize the PG <= 8.3 osx|sed recipe to the 8.4 perl form.
    # 8.2/8.3 order the sed entity alternation amp-first (SED_RECIPE_83);
    # 8.0/8.1 order it lt-first (SED_RECIPE_80).
    if SED_RECIPE_83 in mf:
        mf = mf.replace(SED_RECIPE_83, PERL_RECIPE_84, 1)
    elif SED_RECIPE_80 in mf:
        mf = mf.replace(SED_RECIPE_80, PERL_RECIPE_84, 1)
    # Makefile: flip the section on in the SGML->XML step
    assert OSX_OLD in mf, "osx recipe line not found"
    mf = mf.replace(OSX_OLD, OSX_NEW, 1)
    # Makefile: let the environment override the tool paths (9.x ifndef form)
    if OSX_DEF_8X in mf:
        mf = mf.replace(OSX_DEF_8X, OSX_DEF_8X_WRAPPED, 1)
    # Makefile: widen the SDATA entity fixup (accented names, bullets) to 9.4's
    if PERL_91 in mf:
        mf = mf.replace(PERL_91, PERL_94, 1)
    elif PERL_84 in mf:
        mf = mf.replace(PERL_84, PERL_94_PIPE, 1)
    else:
        print("patch_legacy_xsl_pipeline: WARNING: entity fixup line not replaced",
              file=sys.stderr)
    # Makefile: append the CALS normalizer to the postgres.xml pipeline --
    # raw upstream 8.x archives ship ragged tables (tgroup cols vs row
    # entries) that FOP rejects, exactly like the 6.x/7.x archives already
    # normalized.  The insertion point is after the perl DOCTYPE-append `-e`
    # line, i.e. right before the recipe's final `>$@`.
    # Chinese overlays have separately reviewed table layouts. Only extend
    # the raw-English pipeline here; keep Chinese and unidentified build
    # directories unchanged, including their existing 6.x/7.x handling.
    if re.search(r"(?:^|/)standalone-(?:pdf-)?en-\d+(?:\.\d+)*\.[A-Za-z0-9]+(?:/|$)",
                 os.path.normpath(sgml_dir)):
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        norm_stage = ("\t  | $(PYTHON) "
                      + os.path.join(repo_root, "bin", "normalize_cals_tables.py") + " \\\n")

        def _insert_normalizer(m):
            return m.group(1) + norm_stage + "\t  >$@\n"
        mf2 = re.sub(r"(\t +-e '\$\$_ \.= qq\{<!DOCTYPE book[^\n]*\\\n)\t +>\$@\n",
                     _insert_normalizer, mf, count=1)
        if mf2 == mf:
            print("patch_legacy_xsl_pipeline: WARNING: normalizer stage not inserted",
                  file=sys.stderr)
        mf = mf2
    # Makefile: drop the jade-only bookindex.sgml prerequisite (PG <= 8.4)
    if PGXML_OLD in mf:
        if "ALMOSTALLSGML" not in mf:
            if ALLSGML_8X in mf:
                mf = mf.replace(ALLSGML_8X, ALLSGML_8X + ALMOST_DEF, 1)
            else:
                print("patch_legacy_xsl_pipeline: WARNING: ALLSGML line not found,"
                      " ALMOSTALLSGML left undefined", file=sys.stderr)
        mf = mf.replace(PGXML_OLD, PGXML_NEW, 1)
    # Makefile: route html through the XSL pipeline and add the stamp target
    if "\nhtml: html-stamp\n" in mf:
        mf = mf.replace("\nhtml: html-stamp\n", HTML_NEW, 1)
    elif HTML_84 in mf:
        mf = mf.replace(HTML_84, HTML_NEW, 1)
    elif HTML_82 in mf:
        mf = mf.replace(HTML_82, HTML_NEW, 1)
    else:
        assert False, "html target line not found"
    mf += XSLTHTML_BLOCK
    if "%-A4.fo.tmp:" not in mf and os.path.exists(f"{sgml_dir}/stylesheet-fo.xsl"):
        mf += XSLFO_BLOCK
    with open(makefile, "w", encoding="utf-8") as f:
        f.write(mf)
    print("patch_legacy_xsl_pipeline: backported XSL pipeline onto PG <= 9.1 doc makefile")


def guard_sgml_pipelines(sgml_dir):
    """Do not let a successful perl/sed mask an osx SGML parse failure."""
    path = os.path.join(sgml_dir, 'Makefile')
    with open(path, encoding='utf-8') as stream:
        text = stream.read()
    guarded, count = re.subn(r'(?m)^(\t[ \t]*)(\$\(OSX\)[^\n]*\|[^\n]*)$',
                             r'\1set -o pipefail; \2', text)
    if count:
        guarded += '\n# SGML converter pipelines require failure propagation.\nSHELL := /bin/bash\n'
        with open(path, 'w', encoding='utf-8') as stream:
            stream.write(guarded)
        print(f'patch_legacy_xsl_pipeline: guarded {count} SGML converter pipeline(s)')


def expand_sdata_fixups(sgml_dir):
    """Bring historical osx filters up to the verified modern entity set."""
    path = os.path.join(sgml_dir, 'Makefile')
    with open(path, encoding='utf-8') as stream:
        text = stream.read()

    def expand(match):
        names = match[2].split('|')
        if not {'amp', 'quot'} <= set(names):
            return match[0]
        complete = ('aacute acirc aelig agrave amp aring atilde auml bull copy '
                    'eacute egrave gt iacute lt mdash nbsp ntilde oacute ocirc '
                    'oslash ouml pi quot scaron uuml dollar forall ndash percnt').split()
        names.extend(n for n in complete if n not in names)
        # Matching ignores case; the captured source spelling is retained so
        # [Aacute] becomes &Aacute; (uppercase accent), not &aacute;.
        return match[1] + '|'.join(names) + match[3] + 'i'

    updated = re.sub(r'(s/\\\[\()([A-Za-z|]+)(\) \*\\\]/\\&\\1;/g)(i?)', expand, text)
    if updated != text:
        with open(path, 'w', encoding='utf-8') as stream:
            stream.write(updated)
        print('patch_legacy_xsl_pipeline: completed ISO SDATA entity fixups')


if __name__ == "__main__":
    main()
    expand_sdata_fixups(sys.argv[1])
    guard_sgml_pipelines(sys.argv[1])
