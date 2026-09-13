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
<xsl:param name="orderedlist.label.width">2em</xsl:param>

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
</xsl:attribute-set>

<xsl:attribute-set name="admonition.title.properties">
  <xsl:attribute name="text-align">center</xsl:attribute>
</xsl:attribute-set>

<!-- Make all tables default to left alignment, for consistency with HTML -->
<xsl:attribute-set name="table.table.properties">
  <xsl:attribute name="text-align">left</xsl:attribute>
</xsl:attribute-set>

<!-- fix missing space after vertical simplelist
     https://github.com/docbook/xslt10-stylesheets/issues/31 -->
<xsl:attribute-set name="normal.para.spacing">
  <xsl:attribute name="space-after.optimum">1em</xsl:attribute>
  <xsl:attribute name="space-after.minimum">0.8em</xsl:attribute>
  <xsl:attribute name="space-after.maximum">1.2em</xsl:attribute>
</xsl:attribute-set>

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

    <xsl:call-template name="pg.inline.breaks"><xsl:with-param name="text" select="primary"/></xsl:call-template>

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


<!-- Preserve historical title/refname IDs at their printed locations.
     Repeated titles in contents, bookmarks and running headers stay anchor-free. -->
<xsl:template match="title[@id]" mode="title.markup">
  <xsl:param name="allow-anchors" select="0"/>
  <xsl:choose>
    <xsl:when test="$allow-anchors != 0">
      <fo:inline id="{@id}"/>
      <xsl:apply-templates/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:apply-templates mode="no.anchor.mode"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="refname[@id]">
  <fo:inline id="{@id}"/>
  <xsl:apply-imports/>
</xsl:template>

<!-- Permit display-only line breaks around inline code and at punctuation.
     The SGML, literal characters and preformatted code remain unchanged. -->
<xsl:template match="text()[ancestor::literal or ancestor::function or ancestor::type or ancestor::parameter or ancestor::replaceable or ancestor::varname or ancestor::structname or ancestor::structfield or ancestor::filename or ancestor::command or ancestor::computeroutput or ancestor::constant or ancestor::envar or ancestor::entry or ancestor::symbol or contains(., '、') or contains(., '，')][not(ancestor::programlisting or ancestor::screen or ancestor::synopsis or ancestor::literallayout or ancestor::*[@id='release-commit-links'])]" priority="2">
  <xsl:call-template name="pg.inline.breaks">
    <xsl:with-param name="text" select="."/>
  </xsl:call-template>
  <xsl:variable name="next" select="substring(normalize-space(following::text()[1]), 1, 1)"/>
  <xsl:if test="normalize-space(.) != '' and not($next != '' and contains('、，。；：）)]}', $next))"><xsl:text>&#x200B;</xsl:text></xsl:if>
</xsl:template>

<xsl:template name="pg.inline.breaks">
  <xsl:param name="text"/>
  <xsl:param name="run" select="0"/>
  <xsl:choose>
  <xsl:when test="string-length($text) &gt; 128">
    <xsl:call-template name="pg.inline.breaks"><xsl:with-param name="text" select="substring($text, 1, 128)"/></xsl:call-template>
    <xsl:call-template name="pg.inline.breaks"><xsl:with-param name="text" select="substring($text, 129)"/></xsl:call-template>
  </xsl:when>
  <xsl:when test="$text != ''">
    <xsl:variable name="char" select="substring($text, 1, 1)"/>
    <xsl:if test="contains('+-', $char) and string-length($text) &gt; 1 and contains('0123456789', substring($text, 2, 1))"><xsl:text>&#x200B;</xsl:text></xsl:if>
    <xsl:value-of select="$char"/>
    <xsl:variable name="letters" select="'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'"/>
    <xsl:variable name="nextchar" select="substring($text, 2, 1)"/>
    <xsl:variable name="boundary" select="contains('_.,/:;=[](){}|、，；&#xA0;', $char) or (contains('+-', $char) and not($nextchar != '' and contains('0123456789', $nextchar))) or (string-length($text) &gt; 1 and contains('abcdefghijklmnopqrstuvwxyz', $char) and contains('ABCDEFGHIJKLMNOPQRSTUVWXYZ', $nextchar)) or (ancestor::entry and $run &gt;= 5 and contains($letters, $char) and $nextchar != '' and contains($letters, $nextchar))"/>
    <xsl:if test="$boundary"><xsl:text>&#x200B;</xsl:text></xsl:if>
    <xsl:call-template name="pg.inline.breaks">
      <xsl:with-param name="text" select="substring($text, 2)"/>
      <xsl:with-param name="run" select="($run + 1) * number(contains($letters, $char) and not($boundary))"/>
    </xsl:call-template>
  </xsl:when>
  </xsl:choose>
</xsl:template>

<!-- Generated cross-reference labels in narrow cells need the same optional
     display breaks. Copy the original FO links and their destinations intact. -->
<xsl:template match="entry//xref" priority="5" xmlns:exsl="http://exslt.org/common" extension-element-prefixes="exsl">
  <xsl:variable name="generated"><xsl:apply-imports/></xsl:variable>
  <xsl:apply-templates select="exsl:node-set($generated)/node()" mode="pg.xref.breaks"/>
</xsl:template>
<xsl:template match="@*|node()" mode="pg.xref.breaks">
  <xsl:copy><xsl:apply-templates select="@*|node()" mode="pg.xref.breaks"/></xsl:copy>
</xsl:template>
<xsl:template match="text()" mode="pg.xref.breaks">
  <xsl:call-template name="pg.inline.breaks"><xsl:with-param name="text" select="."/></xsl:call-template>
</xsl:template>

<!-- The five-column function tables in PG10-12 cannot hold signatures and
     verbatim results on portrait paper. Keep each original cell intact and
     display each record as labelled rows, using its own column headings. -->
<xsl:template match="tgroup[@cols='5'][ancestor::chapter[@id='functions'] or parent::table[@id='pgbench-functions']][count(thead/row)=1][count(thead/row/entry)=5][not(.//entry[@namest or @nameend or @morerows or @spanname])]">
    <xsl:attribute name="table-layout">fixed</xsl:attribute>
    <xsl:attribute name="width">100%</xsl:attribute>
    <fo:table-column column-width="16%"/>
    <fo:table-column column-width="84%"/>
    <fo:table-body start-indent="0pt" end-indent="0pt">
      <xsl:for-each select="tbody/row">
        <xsl:variable name="row" select="."/>
        <xsl:for-each select="entry">
          <xsl:variable name="column" select="position()"/>
          <fo:table-row keep-together.within-column="always">
            <xsl:if test="$column = 1"><xsl:attribute name="keep-with-next.within-column">always</xsl:attribute></xsl:if>
            <fo:table-cell padding="3pt" border-bottom="0.25pt solid #cccccc">
              <fo:block font-weight="bold">
                <xsl:if test="$column = 1"><xsl:for-each select="$row"><xsl:call-template name="anchor"/></xsl:for-each></xsl:if>
                <xsl:value-of select="normalize-space(ancestor::tgroup[1]/thead/row/entry[$column])"/>
              </fo:block>
            </fo:table-cell>
            <fo:table-cell padding="3pt" border-bottom="0.25pt solid #cccccc">
              <fo:block><xsl:call-template name="anchor"/><xsl:apply-templates/></fo:block>
            </fo:table-cell>
          </fo:table-row>
        </xsl:for-each>
        <fo:table-row><fo:table-cell number-columns-spanned="2" padding="3pt"><fo:block/></fo:table-cell></fo:table-row>
      </xsl:for-each>
    </fo:table-body>
</xsl:template>

<!-- Keep long version strings, addresses, signatures and aligned query output
     within the print area. These optional break positions add no visible
     character; removing U+200B must reproduce the original preformatted text. -->
<xsl:template match="text()[ancestor::programlisting or ancestor::screen or ancestor::synopsis or ancestor::literallayout][not(ancestor::*[@id='release-commit-links'])]" priority="3">
  <xsl:call-template name="pg.inline.breaks"><xsl:with-param name="text" select="."/></xsl:call-template>
</xsl:template>

<!-- Dense numerical and comparison tables need slightly smaller print type. -->
<xsl:attribute-set name="table.table.properties">
  <xsl:attribute name="font-size">9pt</xsl:attribute>
</xsl:attribute-set>

<!-- Non-monospace literal layouts must also honor the break opportunities. -->
<xsl:attribute-set name="verbatim.properties">
  <xsl:attribute name="wrap-option">wrap</xsl:attribute>
</xsl:attribute-set>

<!-- Preserve full numerical bounds in narrow type-summary cells. -->
<xsl:template match="table[@id='datatype-numeric-table' or @id='datatype-money-table' or @id='datatype-datetime-table']//tbody/row/entry[position() &gt;= 4]/text()" priority="4">
  <fo:inline font-size="8pt"><xsl:call-template name="pg.inline.breaks"><xsl:with-param name="text" select="."/></xsl:call-template></fo:inline>
</xsl:template>

</xsl:stylesheet>
