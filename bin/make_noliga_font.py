#!/usr/bin/env python3
"""Copy a font file with its GSUB table removed.

FOP 2.x applies the standard ligatures declared in a font's GSUB table
unconditionally: kerning="no" in fop.xconf does not disable them and U+200C
does not block them (both verified on FOP 2.11).  With the CJK body font
first in the font chain this mangles every Latin identifier rendered outside
monospace markup (pg_con<fb01>guration, extra_<fb02>oat_digits, IPv6
addresses), breaks text search and copies.  Dropping GSUB removes the
substitutions while keeping GPOS kerning and all metrics intact.
"""
import sys

from fontTools.ttLib import TTFont


def main():
    if len(sys.argv) != 3:
        sys.exit('usage: make_noliga_font.py <src-font> <dst-font>')
    src, dst = sys.argv[1], sys.argv[2]
    font = TTFont(src)
    if 'GSUB' in font:
        del font['GSUB']
    font.save(dst)
    print(f'noliga font: wrote {dst} (GSUB stripped from {src})')


if __name__ == '__main__':
    main()
