<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xsl:stylesheet [
<!ENTITY % common.entities SYSTEM "http://docbook.sourceforge.net/release/xsl/current/common/entities.ent">
%common.entities;
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"
                xmlns:fo="http://www.w3.org/1999/XSL/Format">

<xsl:import href="http://docbook.sourceforge.net/release/xsl/current/fo/docbook.xsl"/>
<xsl:include href="stylesheet-common.xsl" />

<xsl:param name="fop1.extensions" select="1"></xsl:param>
<xsl:param name="tablecolumns.extension" select="0"></xsl:param>
<xsl:param name="toc.max.depth">3</xsl:param>
<xsl:param name="ulink.footnotes" select="1"></xsl:param>
<!-- Running titles use the center cell; leave enough width for long SQL
     command names without squeezing a second line against the rule. -->
<xsl:param name="header.column.widths">1 3 1</xsl:param>

<!-- The release notes have too many ulinks to look good as footnotes in print mode -->
<xsl:template match="sect1[starts-with(@id, 'release-')]//ulink[starts-with(@url, 'https://postgr.es/c/')]">
  <!-- Do nothing for ulink to avoid footnotes -->
</xsl:template>

<!--
Suppress the description of the commit link markers in print mode.
Use "node()" to keep the paragraph but remove all content;  prevents
an "Unresolved ID reference found" warning during PDF builds.
-->
<xsl:template match="appendix[@id='release']//para[@id='release-commit-links']//node()">
  <!-- Output an empty para -->
</xsl:template>

<xsl:param name="use.extensions" select="1"></xsl:param>
<xsl:param name="variablelist.as.blocks" select="1"></xsl:param>
<xsl:param name="orderedlist.label.width">1.5em</xsl:param>

<xsl:attribute-set name="monospace.verbatim.properties"
                   use-attribute-sets="verbatim.properties monospace.properties">
  <xsl:attribute name="wrap-option">wrap</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="nongraphical.admonition.properties">
  <xsl:attribute name="border-style">solid</xsl:attribute>
  <xsl:attribute name="border-width">1pt</xsl:attribute>
  <xsl:attribute name="border-color">black</xsl:attribute>
  <xsl:attribute name="padding-start">12pt</xsl:attribute>
  <xsl:attribute name="padding-end">12pt</xsl:attribute>
  <xsl:attribute name="padding-top">6pt</xsl:attribute>
  <xsl:attribute name="padding-bottom">6pt</xsl:attribute>
  <!-- Keep compact admonition boxes intact; verify page fit in the actual
       layout instead of assuming FOP will relax an oversized keep. -->
  <xsl:attribute name="keep-together.within-column">always</xsl:attribute>
</xsl:attribute-set>

<xsl:attribute-set name="admonition.title.properties">
  <xsl:attribute name="text-align">center</xsl:attribute>
</xsl:attribute-set>

<!-- Make all tables default to left alignment, for consistency with HTML -->
<xsl:attribute-set name="table.table.properties">
  <xsl:attribute name="text-align">left</xsl:attribute>
</xsl:attribute-set>

<!-- The longest parameter name is 220.27pt at 10pt, exceeding the A4
     index column's 219.637pt. Keep identifiers intact in a legible 9.5pt
     index, instead of inserting break characters inside their names. -->
<xsl:attribute-set name="index.entry.properties">
  <xsl:attribute name="font-size">9.5pt</xsl:attribute>
</xsl:attribute-set>

<!-- fix missing space after vertical simplelist
     https://github.com/docbook/xslt10-stylesheets/issues/31 -->
<xsl:attribute-set name="normal.para.spacing">
  <xsl:attribute name="space-after.optimum">1em</xsl:attribute>
  <xsl:attribute name="space-after.minimum">0.8em</xsl:attribute>
  <xsl:attribute name="space-after.maximum">1.2em</xsl:attribute>
  <!-- pgdoc zh: keep at least two lines of a paragraph on each side of a
       page break. -->
  <xsl:attribute name="orphans">2</xsl:attribute>
  <xsl:attribute name="widows">2</xsl:attribute>
</xsl:attribute-set>

<!-- A paragraph containing a block example should keep its lead-in with
     that example when they fit. A finite keep permits long examples to
     span pages and avoids an intro stranded below the body viewport. -->
<xsl:template match="para[programlisting or screen or synopsis]">
  <xsl:variable name="keep.together">
    <xsl:call-template name="pi.dbfo_keep-together"/>
  </xsl:variable>
  <fo:block xsl:use-attribute-sets="para.properties">
    <xsl:attribute name="keep-together.within-column">
      <xsl:choose>
        <xsl:when test="$keep.together != ''"><xsl:value-of select="$keep.together"/></xsl:when>
        <xsl:otherwise>10</xsl:otherwise>
      </xsl:choose>
    </xsl:attribute>
    <xsl:call-template name="anchor"/>
    <xsl:apply-templates/>
  </fo:block>
</xsl:template>

<!-- Keep a short final section with the preceding text.
     Its measured height determines the final keep during PDF preparation. -->
<xsl:template match="refsect1[not(following-sibling::refsect1)] |
                     refsect2[not(following-sibling::refsect2)] |
                     refsect3[not(following-sibling::refsect3)] |
                     sect1[not(following-sibling::sect1)] |
                     sect2[not(following-sibling::sect2)] |
                     sect3[not(following-sibling::sect3)] |
                     sect4[not(following-sibling::sect4)]">
  <fo:block role="pgdoc-compact-ending">
    <xsl:apply-imports/>
  </fo:block>
</xsl:template>

<!-- Keep the last two compact paragraphs with preceding content, including
     introductions before child sections and formal-example conclusions. -->
<xsl:template match="para[not(following-sibling::*[not(self::sect1 or self::sect2 or self::sect3 or self::sect4
                       or self::refsect1 or self::refsect2 or self::refsect3)])]
                     [parent::chapter or parent::appendix or parent::preface
                      or parent::example or starts-with(name(parent::*), 'sect')
                      or starts-with(name(parent::*), 'refsect')] |
                     para[count(following-sibling::*) = 1 and following-sibling::para]
                     [parent::chapter or parent::appendix or parent::preface
                      or parent::example or starts-with(name(parent::*), 'sect')
                      or starts-with(name(parent::*), 'refsect')]">
  <fo:block role="pgdoc-compact-ending-paragraph">
    <xsl:apply-imports/>
  </fo:block>
</xsl:template>

<!-- variablelist.as.blocks is enabled above, so this wrapper remains a legal
     block even for a definition list nested inside a paragraph. -->
<xsl:template match="variablelist[count(varlistentry) &lt;= 2 and not(following-sibling::*)]">
  <fo:block role="pgdoc-compact-ending">
    <xsl:apply-imports/>
  </fo:block>
</xsl:template>

<xsl:template match="note[not(following-sibling::*)] | tip[not(following-sibling::*)] |
                     important[not(following-sibling::*)] | caution[not(following-sibling::*)] |
                     warning[not(following-sibling::*)]">
  <fo:block role="pgdoc-compact-ending">
    <xsl:apply-imports/>
  </fo:block>
</xsl:template>

<!-- Measure the synopsis heading and spacing as well as its code block.
     A code block may fit on a bare page but strand the reference title. -->
<xsl:template match="refsynopsisdiv">
  <fo:block role="pgdoc-reference-synopsis">
    <xsl:apply-imports/>
  </fo:block>
</xsl:template>

<!-- The ECPG command overview is two lines long. Its first embedded command
     can follow the introduction; later commands retain their page breaks. -->
<xsl:template match="sect1[@id='ecpg-sql-commands']/refentry[not(preceding-sibling::refentry)]">
  <fo:block>
    <xsl:call-template name="anchor"/>
    <xsl:apply-templates/>
  </fo:block>
</xsl:template>

<xsl:attribute-set name="table.footnote.properties">
  <xsl:attribute name="role">pgdoc-table-footnote</xsl:attribute>
</xsl:attribute-set>

<!-- pgdoc zh: Chinese run-in headings already end with their own fullwidth
     punctuation (发布日期：/示例：), so suppress the ASCII period DocBook
     appends by default ("发布日期：.").  The title's padding-end still
     separates it from the following text. -->
<xsl:param name="runinhead.default.title.end.punct"/>
<xsl:param name="runinhead.title.end.punct">.!?：。？！；，、</xsl:param>

<!-- Change display of some elements -->

<xsl:template match="command">
  <xsl:call-template name="inline.monoseq"/>
</xsl:template>

<xsl:template match="confgroup" mode="bibliography.mode">
  <fo:inline>
    <xsl:apply-templates select="conftitle/text()" mode="bibliography.mode"/>
    <xsl:text>, </xsl:text>
    <xsl:apply-templates select="confdates/text()" mode="bibliography.mode"/>
    <xsl:value-of select="$biblioentry.item.separator"/>
  </fo:inline>
</xsl:template>

<xsl:template match="isbn" mode="bibliography.mode">
  <fo:inline>
    <xsl:text>ISBN </xsl:text>
    <xsl:apply-templates mode="bibliography.mode"/>
    <xsl:value-of select="$biblioentry.item.separator"/>
  </fo:inline>
</xsl:template>

<!-- Make every sect1 in contrib get a page break -->
<xsl:template match="id('contrib')/sect1">
  <fo:block break-after='page'/>
  <xsl:apply-imports/>
</xsl:template>

<!-- formatting for entries in tables of functions -->
<xsl:template match="entry[@role='func_table_entry']/para">
  <fo:block margin-left="4em" text-align="left">
    <xsl:if test="self::para[@role='func_signature']">
      <xsl:attribute name="text-indent">-3.5em</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates/>
  </fo:block>
</xsl:template>

<!-- formatting for entries in tables of catalog/view columns -->
<xsl:template match="entry[@role='catalog_table_entry']/para">
  <fo:block margin-left="4em" text-align="left">
    <xsl:if test="self::para[@role='column_definition']">
      <xsl:attribute name="text-indent">-3.5em</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates/>
  </fo:block>
</xsl:template>

<!-- overrides stylesheet-common.xsl -->
<!-- FOP needs us to be explicit about the font to use for right arrow -->
<xsl:template match="returnvalue">
  <fo:inline font-family="{$symbol.font.family}">&#x2192; </fo:inline>
  <xsl:call-template name="inline.monoseq"/>
</xsl:template>

<!-- FOP needs us to be explicit about use of symbol font in some cases -->
<xsl:template match="phrase[@role='symbol_font']">
  <fo:inline font-family="{$symbol.font.family}"><xsl:value-of select="."/></fo:inline>
</xsl:template>

<!-- bug fix from <https://sourceforge.net/p/docbook/bugs/1360/#831b> -->

<xsl:template match="varlistentry/term" mode="xref-to">
  <xsl:param name="verbose" select="1"/>
  <xsl:apply-templates mode="no.anchor.mode"/>
</xsl:template>

<!-- include refsects in PDF bookmarks
     (https://github.com/docbook/xslt10-stylesheets/issues/46) -->

<xsl:template match="refsect1|refsect2|refsect3"
              mode="bookmark">

  <xsl:variable name="id">
    <xsl:call-template name="object.id"/>
  </xsl:variable>
  <xsl:variable name="bookmark-label">
    <xsl:apply-templates select="." mode="object.title.markup"/>
  </xsl:variable>

  <fo:bookmark internal-destination="{$id}">
    <xsl:attribute name="starting-state">
      <xsl:value-of select="$bookmarks.state"/>
    </xsl:attribute>
    <fo:bookmark-title>
      <xsl:value-of select="normalize-space($bookmark-label)"/>
    </fo:bookmark-title>
    <xsl:apply-templates select="*" mode="bookmark"/>
  </fo:bookmark>
</xsl:template>

<!-- make generated ids reproducible
     (https://github.com/docbook/xslt10-stylesheets/issues/54) -->

<!-- from fo/autoidx.xsl -->

<xsl:key name="primaryonly"
         match="indexterm"
         use="normalize-space(primary)"/>

<xsl:template match="indexterm" mode="index-primary">
  <xsl:param name="scope" select="."/>
  <xsl:param name="role" select="''"/>
  <xsl:param name="type" select="''"/>

  <xsl:variable name="key" select="&primary;"/>
  <xsl:variable name="refs" select="key('primary', $key)[&scope;]"/>

  <xsl:variable name="term.separator">
    <xsl:call-template name="index.separator">
      <xsl:with-param name="key" select="'index.term.separator'"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="range.separator">
    <xsl:call-template name="index.separator">
      <xsl:with-param name="key" select="'index.range.separator'"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="number.separator">
    <xsl:call-template name="index.separator">
      <xsl:with-param name="key" select="'index.number.separator'"/>
    </xsl:call-template>
  </xsl:variable>

  <fo:block xmlns:rx="http://www.renderx.com/XSL/Extensions" xmlns:axf="http://www.antennahouse.com/names/XSL/Extensions">
    <xsl:if test="$autolink.index.see != 0">
      <xsl:attribute name="id">
        <!-- pgsql-docs: begin -->
        <xsl:text>ientry-</xsl:text>
        <xsl:call-template name="object.id"/>
        <!-- pgsql-docs: end -->
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="$axf.extensions != 0">
      <xsl:attribute name="axf:suppress-duplicate-page-number">true</xsl:attribute>
    </xsl:if>

    <xsl:for-each select="$refs/primary">
      <xsl:if test="@id or @xml:id">
        <fo:inline id="{(@id|@xml:id)[1]}"/>
      </xsl:if>
    </xsl:for-each>

    <xsl:value-of select="primary"/>

    <xsl:choose>
      <xsl:when test="$xep.extensions != 0">
        <xsl:if test="$refs[not(see) and not(secondary)]">
          <xsl:copy-of select="$term.separator"/>
          <xsl:variable name="primary" select="&primary;"/>
          <xsl:variable name="primary.significant" select="concat(&primary;, $significant.flag)"/>
          <rx:page-index list-separator="{$number.separator}"
                         range-separator="{$range.separator}">
            <xsl:if test="$refs[@significance='preferred'][not(see) and not(secondary)]">
              <rx:index-item xsl:use-attribute-sets="index.preferred.page.properties xep.index.item.properties"
                ref-key="{$primary.significant}"/>
            </xsl:if>
            <xsl:if test="$refs[not(@significance) or @significance!='preferred'][not(see) and not(secondary)]">
              <rx:index-item xsl:use-attribute-sets="xep.index.item.properties"
                ref-key="{$primary}"/>
            </xsl:if>
          </rx:page-index>
        </xsl:if>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="page-number-citations">
          <xsl:for-each select="$refs[not(see)
                                and not(secondary)]">
            <xsl:apply-templates select="." mode="reference">
              <xsl:with-param name="scope" select="$scope"/>
              <xsl:with-param name="role" select="$role"/>
              <xsl:with-param name="type" select="$type"/>
              <xsl:with-param name="position" select="position()"/>
            </xsl:apply-templates>
          </xsl:for-each>
        </xsl:variable>

        <xsl:copy-of select="$page-number-citations"/>
      </xsl:otherwise>
    </xsl:choose>

    <xsl:if test="$refs[not(secondary)]/*[self::see]">
      <xsl:apply-templates select="$refs[generate-id() = generate-id(key('see', concat(&primary;, &sep;, &sep;, &sep;, see))[&scope;][1])]"
                           mode="index-see">
         <xsl:with-param name="scope" select="$scope"/>
         <xsl:with-param name="role" select="$role"/>
         <xsl:with-param name="type" select="$type"/>
         <xsl:sort select="translate(see, &lowercase;, &uppercase;)"/>
      </xsl:apply-templates>
    </xsl:if>

  </fo:block>

  <xsl:if test="$refs/secondary or $refs[not(secondary)]/*[self::seealso]">
    <fo:block start-indent="1pc">
      <xsl:apply-templates select="$refs[generate-id() = generate-id(key('see-also', concat(&primary;, &sep;, &sep;, &sep;, seealso))[&scope;][1])]"
                           mode="index-seealso">
         <xsl:with-param name="scope" select="$scope"/>
         <xsl:with-param name="role" select="$role"/>
         <xsl:with-param name="type" select="$type"/>
         <xsl:sort select="translate(seealso, &lowercase;, &uppercase;)"/>
      </xsl:apply-templates>
      <xsl:apply-templates select="$refs[secondary and count(.|key('secondary', concat($key, &sep;, &secondary;))[&scope;][1]) = 1]"
                           mode="index-secondary">
       <xsl:with-param name="scope" select="$scope"/>
       <xsl:with-param name="role" select="$role"/>
       <xsl:with-param name="type" select="$type"/>
       <xsl:sort select="translate(&secondary;, &lowercase;, &uppercase;)"/>
      </xsl:apply-templates>
    </fo:block>
  </xsl:if>
</xsl:template>

<xsl:template match="indexterm" mode="index-see">
  <xsl:param name="scope" select="."/>
  <xsl:param name="role" select="''"/>
  <xsl:param name="type" select="''"/>

  <xsl:variable name="see" select="normalize-space(see)"/>

  <!-- can only link to primary, which should appear before comma
  in see "primary, secondary" entry -->
  <xsl:variable name="seeprimary">
    <xsl:choose>
      <xsl:when test="contains($see, ',')">
        <xsl:value-of select="substring-before($see, ',')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$see"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="seetarget" select="key('primaryonly', $seeprimary)[1]"/>

  <xsl:variable name="linkend">
    <xsl:if test="$seetarget">
      <!-- pgsql-docs: begin -->
      <xsl:text>ientry-</xsl:text>
      <xsl:call-template name="object.id">
        <xsl:with-param name="object" select="$seetarget"/>
      </xsl:call-template>
      <!-- pgsql-docs: end -->
    </xsl:if>
  </xsl:variable>

  <fo:inline xmlns:xlink='http://www.w3.org/1999/xlink'>
    <xsl:text> (</xsl:text>
    <xsl:call-template name="gentext">
      <xsl:with-param name="key" select="'see'"/>
    </xsl:call-template>
    <xsl:text> </xsl:text>
    <xsl:choose>
      <!-- manual links have precedence -->
      <xsl:when test="see/@linkend or see/@xlink:href">
        <xsl:call-template name="simple.xlink">
          <xsl:with-param name="node" select="see"/>
          <xsl:with-param name="content" select="$see"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:when test="$autolink.index.see = 0">
         <xsl:value-of select="$see"/>
      </xsl:when>
      <xsl:when test="$seetarget">
        <fo:basic-link internal-destination="{$linkend}"
                       xsl:use-attribute-sets="xref.properties">
          <xsl:value-of select="$see"/>
        </fo:basic-link>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$see"/>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:text>)</xsl:text>
  </fo:inline>
</xsl:template>

<xsl:template match="indexterm" mode="index-seealso">
   <xsl:param name="scope" select="."/>
  <xsl:param name="role" select="''"/>
  <xsl:param name="type" select="''"/>

  <xsl:for-each select="seealso">
    <xsl:sort select="translate(., &lowercase;, &uppercase;)"/>

    <xsl:variable name="seealso" select="normalize-space(.)"/>

    <!-- can only link to primary, which should appear before comma
    in seealso "primary, secondary" entry -->
    <xsl:variable name="seealsoprimary">
      <xsl:choose>
        <xsl:when test="contains($seealso, ',')">
          <xsl:value-of select="substring-before($seealso, ',')"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$seealso"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:variable>

    <xsl:variable name="seealsotarget" select="key('primaryonly', $seealsoprimary)[1]"/>

    <xsl:variable name="linkend">
      <xsl:if test="$seealsotarget">
        <!-- pgsql-docs: begin -->
        <xsl:text>ientry-</xsl:text>
        <xsl:call-template name="object.id">
          <xsl:with-param name="object" select="$seealsotarget"/>
        </xsl:call-template>
        <!-- pgsql-docs: end -->
      </xsl:if>
    </xsl:variable>

    <fo:block xmlns:xlink='http://www.w3.org/1999/xlink'>
      <xsl:text>(</xsl:text>
      <xsl:call-template name="gentext">
        <xsl:with-param name="key" select="'seealso'"/>
      </xsl:call-template>
      <xsl:text> </xsl:text>
      <xsl:choose>
        <!-- manual links have precedence -->
        <xsl:when test="@linkend or see/@xlink:href">
          <xsl:call-template name="simple.xlink">
            <xsl:with-param name="node" select="."/>
            <xsl:with-param name="content" select="$seealso"/>
          </xsl:call-template>
        </xsl:when>
        <xsl:when test="$autolink.index.see = 0">
          <xsl:value-of select="$seealso"/>
        </xsl:when>
        <xsl:when test="$seealsotarget">
          <fo:basic-link internal-destination="{$linkend}"
                         xsl:use-attribute-sets="xref.properties">
            <xsl:value-of select="$seealso"/>
          </fo:basic-link>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$seealso"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:text>)</xsl:text>
    </fo:block>

  </xsl:for-each>

</xsl:template>


</xsl:stylesheet>
