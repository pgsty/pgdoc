#!/usr/bin/env python3
"""Apply output-only fixes to the isolated DocBook FO stylesheet."""
from pathlib import Path
import sys


ANCHORS = '''
<!-- pgdoc: preserve legacy command-title destinations in rendered FO.
     DocBook's refnamediv converts the refentrytitle result to a string,
     dropping inline anchors. Attach the title ID to the visible heading. -->
<xsl:template match="refnamediv[not(preceding-sibling::refnamediv)]">
  <xsl:choose>
    <xsl:when test="../refmeta/refentrytitle/@id">
      <fo:block id="{../refmeta/refentrytitle/@id}">
        <xsl:apply-imports/>
      </fo:block>
    </xsl:when>
    <xsl:otherwise><xsl:apply-imports/></xsl:otherwise>
  </xsl:choose>
</xsl:template>
<!-- Like refsect1info, this is title-page metadata, not body markup. -->
<xsl:template match="refsynopsisdivinfo|docinfo"/>
<!-- Legacy bookbiblio annotations are real reader-facing text. DocBook's
     default bibliography mode hides abstract, so preserve these paragraphs. -->
<xsl:template match="biblioentry/abstract" mode="bibliography.mode">
  <fo:block><xsl:apply-templates/></fo:block>
</xsl:template>
<!-- Older books put citation IDs on title/titleabbrev, not biblioentry. -->
<xsl:template match="biblioentry/title[@id]|biblioentry/titleabbrev[@id]" mode="bibliography.mode">
  <fo:inline id="{@id}"><xsl:apply-imports/></fo:inline>
</xsl:template>
<xsl:template match="biblioentry/titleabbrev" mode="xref-to">
  <xsl:apply-templates/>
</xsl:template>
<!-- The 6.3 upstream cites DATE93 but supplies no such bibliography entry.
     Preserve its visible citation without inventing a destination or edition. -->
<xsl:template match="ulink[@url='refs.html#DATE93']">
  <xsl:choose>
    <xsl:when test="//*[@id='DATE93' or @id='date93']"><xsl:apply-imports/></xsl:when>
    <xsl:otherwise><xsl:apply-templates/></xsl:otherwise>
  </xsl:choose>
</xsl:template>
'''


def prepare(path):
    path = Path(path)
    text = path.read_text()
    # An empty break-after block can itself land on the next page when the
    # previous page is full, then cause a completely empty extra page.
    old = "  <fo:block break-after='page'/>\n  <xsl:apply-imports/>"
    new = "  <fo:block break-before='page'>\n    <xsl:apply-imports/>\n  </fo:block>"
    text = text.replace(old, new)
    if '<!-- pgdoc: preserve legacy command-title destinations' not in text:
        if '</xsl:stylesheet>' not in text:
            raise ValueError(f'Not an XSL stylesheet: {path}')
        text = text.replace('</xsl:stylesheet>', ANCHORS + '\n</xsl:stylesheet>')
    path.write_text(text)


if __name__ == '__main__':
    prepare(sys.argv[1])
