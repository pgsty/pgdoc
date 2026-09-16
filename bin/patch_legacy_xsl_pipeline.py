#!/usr/bin/env python3
"""Backport the XSL pipeline onto PG <= 9.1 doc makefiles in a build work tree.

PG 9.2+ doc/src/sgml/Makefile ships an xslthtml-stamp target, and PG 9.4+
postgres.sgml/filelist.sgml carry the include-xslt-index marked section, so
the jade-free XSL pipeline (osx -> postgres.xml -> xsltproc) renders chunked
HTML / XSL-FO with a stylesheet-generated index.  PG 9.1 and older only have
the pre-stamp xslthtml target, no marked section, and a narrower SDATA entity
fixup list, while this toolchain does not ship DSSSL jade at all.

Patches applied in place (all guarded; idempotent):

  filelist.sgml   declare %include-xslt-index (9.4 form)
  postgres.sgml   add the include-xslt-index marked section (9.4 form)
  Makefile        osx step: -i include-xslt-index
                  postgres.xml entity fixup: 9.4 entity list, /gi
                  html: html-stamp -> html: xslthtml-stamp
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
OSX_OLD = "\t$(OSX) -D. -x lower $<"
OSX_NEW = "\t$(OSX) -D. -x lower -i include-xslt-index $<"
XSLTHTML_BLOCK = """
# -- begin pgdoc backport: XSL HTML pipeline for PG <= 9.1 (patch_legacy_xsl_pipeline.py) --
xslthtml: xslthtml-stamp

xslthtml-stamp: stylesheet.xsl postgres.xml
\t$(XSLTPROC) $(XSLTPROCFLAGS) $(XSLTPROC_HTML_FLAGS) $^
\tcp $(srcdir)/stylesheet.css html/
\ttouch $@
# -- end pgdoc backport --
"""


def main():
    sgml_dir = sys.argv[1]
    makefile = f"{sgml_dir}/Makefile"
    with open(makefile, encoding="utf-8") as f:
        mf = f.read()

    if "xslthtml-stamp:" in mf:
        return  # PG >= 9.2 already ships the XSL pipeline
    if "postgres.xml:" not in mf:
        return  # nothing to backport onto

    # filelist.sgml: declare the marked-section keyword (9.4 form)
    fl_path = f"{sgml_dir}/filelist.sgml"
    with open(fl_path, encoding="utf-8") as f:
        fl = f.read()
    if "include-xslt-index" not in fl:
        anchor = '<!ENTITY % include-index "IGNORE">'
        decl = (anchor + "\n\n<!--\n Create empty index element for processing by XSLT stylesheet.\n"
                " -->\n<!ENTITY % include-xslt-index \"IGNORE\">\n")
        if anchor in fl:
            fl = fl.replace(anchor, decl, 1)
        else:
            fl += "\n" + decl
        with open(fl_path, "w", encoding="utf-8") as f:
            f.write(fl)

    # postgres.sgml: emit the empty <index> under the marked section (9.4 form)
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
        else:
            print("patch_legacy_xsl_pipeline: WARNING: include-index anchor not found in postgres.sgml",
                  file=sys.stderr)

    # Makefile: flip the section on in the SGML->XML step
    assert OSX_OLD in mf, "osx recipe line not found"
    mf = mf.replace(OSX_OLD, OSX_NEW, 1)
    # Makefile: widen the SDATA entity fixup (accented names, bullets) to 9.4's
    if PERL_91 in mf:
        mf = mf.replace(PERL_91, PERL_94, 1)
    else:
        print("patch_legacy_xsl_pipeline: WARNING: entity fixup line not replaced",
              file=sys.stderr)
    # Makefile: route html through the XSL pipeline and add the stamp target
    assert "\nhtml: html-stamp\n" in mf, "html target line not found"
    mf = mf.replace("\nhtml: html-stamp\n", "\nhtml: xslthtml-stamp\n", 1)
    mf += XSLTHTML_BLOCK
    with open(makefile, "w", encoding="utf-8") as f:
        f.write(mf)
    print("patch_legacy_xsl_pipeline: backported XSL pipeline onto PG <= 9.1 doc makefile")


if __name__ == "__main__":
    main()
