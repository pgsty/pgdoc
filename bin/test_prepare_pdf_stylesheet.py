"""Render small XSL fixtures to verify heading anchors and page breaks."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET

from prepare_pdf_stylesheet import prepare


@unittest.skipUnless(shutil.which('xsltproc'), 'xsltproc required')
class PdfStylesheetTests(unittest.TestCase):
    def test_heading_destination_and_break_follow_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp/'base.xsl').write_text('''<xsl:stylesheet version="1.0"
              xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
              xmlns:fo="http://www.w3.org/1999/XSL/Format">
              <xsl:template match="/"><fo:root><xsl:apply-templates/></fo:root></xsl:template>
              <xsl:template match="refmeta"/>
              <xsl:template match="refnamediv|sect1"><fo:block><xsl:apply-templates/></fo:block></xsl:template>
              <xsl:template match="biblioentry"><fo:block><xsl:apply-templates mode="bibliography.mode"/></fo:block></xsl:template>
              <xsl:template match="abstract" mode="bibliography.mode"/>
              <xsl:template match="xref"><xsl:apply-templates select="//*[@id=current()/@linkend]" mode="xref-to"/></xsl:template>
              <xsl:template match="*" mode="xref-to">???</xsl:template>
              <xsl:template match="ulink"><fo:basic-link external-destination="{@url}"><xsl:apply-templates/></fo:basic-link></xsl:template>
            </xsl:stylesheet>''')
            path = tmp/'stylesheet.xsl'
            path.write_text('''<xsl:stylesheet version="1.0"
              xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
              xmlns:fo="http://www.w3.org/1999/XSL/Format">
              <xsl:import href="base.xsl"/>
              <xsl:template match="sect1">
  <fo:block break-after='page'/>
  <xsl:apply-imports/>
              </xsl:template>
            </xsl:stylesheet>''')
            source = tmp/'source.xml'
            source.write_text('''<book><refentry><refmeta><refentrytitle id="command-title">Command</refentrytitle></refmeta>
              <refnamediv>Heading</refnamediv><refnamediv>Second name</refnamediv></refentry>
              <sect1>Extension text</sect1>
              <biblioentry><abstract><para>Encore planner/Report.ps</para></abstract></biblioentry>
              <biblioentry><title id="full">Original title</title><titleabbrev id="short">Author 1987</titleabbrev></biblioentry>
              <xref linkend="short"/>
              <ulink url="refs.html#DATE93">[DATE93]</ulink>
              <refsynopsisdivinfo>metadata-only</refsynopsisdivinfo></book>''')
            prepare(path)
            once = path.read_bytes()
            prepare(path)
            self.assertEqual(once, path.read_bytes())
            root = ET.fromstring(subprocess.check_output(['xsltproc', '--nonet', str(path), str(source)]))
            anchors = [e for e in root.iter() if e.get('id') == 'command-title']
            self.assertEqual(len(anchors), 1)
            self.assertEqual(''.join(anchors[0].itertext()), 'Heading')
            breaks = [e for e in root.iter() if e.get('break-before') == 'page']
            self.assertEqual(len(breaks), 1)
            self.assertEqual(''.join(breaks[0].itertext()), 'Extension text')
            self.assertFalse(any(e.get('break-after') for e in root.iter()))
            self.assertIn('Encore planner/Report.ps', ''.join(root.itertext()))
            self.assertNotIn('metadata-only', ''.join(root.itertext()))
            self.assertNotIn('???', ''.join(root.itertext()))
            self.assertIn('[DATE93]', ''.join(root.itertext()))
            self.assertFalse(any(e.get('external-destination') for e in root.iter()))
            self.assertEqual(sum(e.get('id') == 'full' for e in root.iter()), 1)
            self.assertEqual(sum(e.get('id') == 'short' for e in root.iter()), 1)


if __name__ == '__main__':
    unittest.main()
