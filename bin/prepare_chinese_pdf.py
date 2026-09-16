#!/usr/bin/env python3
"""Add invisible line-break opportunities to Chinese prose in generated XSL-FO.

FOP can otherwise treat an entire list of Latin identifiers separated by U+3001
as one word and paint it outside the page.  Change the generated print layout,
not the SGML, identifiers, links, or whitespace-preserving code examples.
"""

from pathlib import Path
import argparse
import re
import xml.etree.ElementTree as ET


def prepare(path, cjk_family='Alibaba PuHuiTi 3.0'):
    path = Path(path)
    for _, (prefix, uri) in ET.iterparse(path, events=('start-ns',)):
        if not prefix.startswith('ns'):
            ET.register_namespace(prefix, uri)
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True, insert_pis=True))
    tree = ET.parse(path, parser=parser)
    added = 0

    def break_prose(text):
        nonlocal added
        if not text:
            return text
        # Idempotent if the same FO is rendered more than once.
        broken = re.sub(r'(?:[、，；。）_.]|(?<=[A-Za-z])-(?=[A-Za-z]))(?!\u200b)',
                        lambda m: m[0] + '\u200b', text)
        added += broken.count('\u200b') - text.count('\u200b')
        return broken

    def visit(node, preserve=False, in_cell=False, centered_cell=False):
        if not isinstance(node.tag, str):
            return
        preserve = (preserve or node.get('white-space-treatment') == 'preserve'
                    or node.tag.endswith('}instream-foreign-object'))
        in_cell = in_cell or node.tag.endswith('}table-cell')
        centered_cell = centered_cell or (node.tag.endswith('}table-cell') and node.get('text-align') == 'center')
        family = node.get('font-family', '')
        if (node.tag.endswith('}inline') and cjk_family in [x.strip() for x in family.split(',')]
                and family != cjk_family
                and re.search(r'[\u3400-\u9fff]', ''.join(node.itertext()))):
            # Use the CJK font's own metrics for translated inline parameters.
            node.set('font-family', cjk_family)
        if (in_cell and not preserve and node.tag.endswith('}inline') and not len(node)
                and re.fullmatch(r'[A-Za-z0-9]{20,}', (node.text or '').strip())):
            # Long type names such as anycompatiblemultirange must fit the
            # datatype column without introducing breaks inside the name.
            node.set('font-size', '8.5pt')
        if (preserve and node.tag.endswith('}block') and family
                and cjk_family in [x.strip() for x in family.split(',')]
                and family != cjk_family
                and re.search(r'[^\s\u200b]{70,}', ''.join(node.itertext()))):
            # Preserve verbatim separators and examples, including oid2name's
            # wide dashed table rule; only their print size changes.
            node.set('font-size', '8.5pt')
        if in_cell and not preserve and node.tag.endswith('}block') and not len(node):
            value = (node.text or '').strip().replace('\u200b', '')
            # Compact, otherwise unbreakable values in the equal-width columns
            # used by the datatype and replication comparison tables.
            if (re.fullmatch(r'[A-Za-z0-9_:+.\-]{9,}', value)
                    or re.search(r'\d{16,}', value)
                    or (centered_cell and re.search(r'[A-Za-z]{8,}', value))):
                node.set('font-size', '7.8pt' if centered_cell else '8.5pt')
        if not preserve:
            node.text = break_prose(node.text)
        for child in node:
            visit(child, preserve, in_cell, centered_cell)
            if not preserve:
                child.tail = break_prose(child.tail)
        if node.tag.endswith('}list-item-label'):
            for child in node:
                if child.tag.endswith('}block') and re.fullmatch(r'\d{2,}\.\u200b?', (child.text or '').strip()):
                    child.set('font-size', '8.9pt')

    visit(tree.getroot())
    temporary = path.with_name(path.name + '.linebreaks.tmp')
    tree.write(temporary, encoding='utf-8', xml_declaration=True)
    temporary.replace(path)
    return added


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('fo', type=Path)
    cli.add_argument('--cjk-family', default='Alibaba PuHuiTi 3.0')
    args = cli.parse_args()
    print(f'Chinese PDF: added {prepare(args.fo, args.cjk_family)} prose line-break opportunities.')
