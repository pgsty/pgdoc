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

Usage: patch_legacy_xsl_pipeline.py <doc/src/sgml dir>
No-op when the makefile already has xslthtml-stamp (PG >= 9.2) or lacks a
postgres.xml rule.
"""
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

FILELIST_FALLBACK = (
    "\n<!--\n"
    " Local hack (pgdoc): marked-section keywords for the XSL pipeline's\n"
    " stylesheet-generated index.  Upstream added these in PG 9.x; see the\n"
    " release.sgml of 9.0 for the original form.\n"
    " -->\n"
    '<!ENTITY % include-index "IGNORE">\n'
    '<!ENTITY % include-xslt-index "IGNORE">\n'
)


def main():
    sgml_dir = sys.argv[1]
    makefile = f"{sgml_dir}/Makefile"
    with open(makefile, encoding="utf-8") as f:
        mf = f.read()

    if "xslthtml-stamp:" in mf:
        return  # PG >= 9.2 already ships the XSL pipeline
    if "postgres.xml:" not in mf:
        return  # nothing to backport onto
    if "\nxslthtml:" not in mf:
        return  # PG >= 10 html pipeline is native XSL (html-stamp, no
                # xslthtml target); only <= 9.6-era makefiles need the backport

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
    else:
        assert False, "html target line not found"
    mf += XSLTHTML_BLOCK
    with open(makefile, "w", encoding="utf-8") as f:
        f.write(mf)
    print("patch_legacy_xsl_pipeline: backported XSL pipeline onto PG <= 9.1 doc makefile")


if __name__ == "__main__":
    main()
