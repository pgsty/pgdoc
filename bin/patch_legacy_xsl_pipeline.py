#!/usr/bin/env python3
"""Backport the XSL pipeline onto PG <= 9.1 doc makefiles in a build work tree.

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
No-op when the makefile already has xslthtml-stamp (PG >= 9.2) or lacks a
postgres.xml rule.
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
    "setmn sigma sube sup tdot times uuml"
)

# PG 6.x block appended to the (static, jade-era) doc makefile.  Tool vars
# use ?= so the deps environment wins; the SGML declaration is passed as an
# explicit osx argument because 6.x sources rely on omitted end tags, which
# the stock DocBook V3.0 declaration (OMITTAG NO) rejects.  -Dref covers the
# 6.4 reference.sgml -> allfiles.sgml system id (jade's old -D ref DBOPTS).
XSLTHTML_BLOCK_6X_TEMPLATE = """
# -- begin pgdoc backport: XSL HTML pipeline for PG 6.x (patch_legacy_xsl_pipeline.py) --
OSX ?= osx
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
    sgml_decl = f"{repo_root}/tmp/pg6x/deps/docbk30/docbook-omittag.dcl"
    if not os.path.exists(sgml_decl):
        print("patch_legacy_xsl_pipeline: WARNING:"
              f" {sgml_decl} missing; osx will fall back to OMITTAG NO",
              file=sys.stderr)
        sgml_decl = ""
    # The build work tree name embeds the version (build_standalone_docsrc.sh
    # mktemp pattern "standalone-<lang>-<version>.XXXXXX"); empty fallback is
    # harmless (pg.version only drives the footer/devel switches).
    m = re.search(r"standalone-(?:en|zh)-(\d+\.\d+(?:\.\d+)?)\.[A-Za-z0-9]+",
                  os.path.abspath(sgml_dir))
    version = m.group(1) if m else ""
    sdata = "|".join(SDATA_6X.split())
    mf += XSLTHTML_BLOCK_6X_TEMPLATE.format(
        version=version, sgml_decl=sgml_decl, sdata=sdata)
    with open(makefile, "w", encoding="utf-8") as f:
        f.write(mf)
    print("patch_legacy_xsl_pipeline: synthesized XSL pipeline onto PG 6.x"
          f" doc makefile (pgdoc version '{version}')")
    return True


def main():
    sgml_dir = sys.argv[1]
    makefile = f"{sgml_dir}/Makefile"
    with open(makefile, encoding="utf-8") as f:
        mf = f.read()

    if "xslthtml-stamp:" in mf:
        return  # PG >= 9.2 already ships the XSL pipeline
    if "postgres.xml:" not in mf:
        # PG 6.x jade-era makefiles have neither an html: target nor a
        # postgres.xml rule; the 6.x branch synthesizes the whole pipeline.
        patch_pg6x(sgml_dir)
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


if __name__ == "__main__":
    main()
