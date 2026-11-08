#!/usr/bin/env bash
# Regenerate the six build-time SGML tables the docs need, then produce the
# Chinese variants through the repo's hash-pinned localize-generated.py.
#
# Inputs are fetched once into tools/pgsrc/ from the official postgres git
# (REL_18_6).  Outputs land in tools/generated/ (English) and
# tools/generated-zh/ (Chinese).  Nothing touches the frozen en/ zh/ trees.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
DOC="$REPO/en/18.6"
PGSRC="$HERE/pgsrc"
GEN="$HERE/generated"
GENZH="$HERE/generated-zh"
mkdir -p "$GEN" "$GENZH"

# inputs are fetched from the official postgres git on first use
if [ ! -s "$PGSRC/errcodes.txt" ] || [ ! -s "$PGSRC/kwlist.h" ] \
   || [ ! -s "$PGSRC/wait_event_names.txt" ] \
   || [ ! -s "$PGSRC/generate-wait_event_types.pl" ] \
   || [ ! -s "$PGSRC/sql_feature_packages.txt" ] \
   || [ ! -s "$PGSRC/sql_features.txt" ]; then
  python3 "$HERE/fetch_pgsrc.py"
fi

# generate-keywords-table.pl reads $srcdir/../../../src/include/parser/kwlist.h
PGTREE="$HERE/pgtree"
rm -rf "$PGTREE"
mkdir -p "$PGTREE/doc/src/sgml" "$PGTREE/src/include/parser"
ln -s "$DOC/keywords" "$PGTREE/doc/src/sgml/keywords"
cp "$PGSRC/kwlist.h" "$PGTREE/src/include/parser/kwlist.h"

echo "[1/6] errcodes-table.sgml"
perl "$DOC/generate-errcodes-table.pl" "$PGSRC/errcodes.txt" \
    > "$GEN/errcodes-table.sgml"

echo "[2/6] keywords-table.sgml"
perl "$DOC/generate-keywords-table.pl" "$PGTREE/doc/src/sgml" \
    > "$GEN/keywords-table.sgml"

echo "[3/6] wait_event_types.sgml"
(cd "$GEN" && perl "$PGSRC/generate-wait_event_types.pl" --docs \
    --outdir . "$PGSRC/wait_event_names.txt")

echo "[4/6] features tables"
perl "$DOC/mk_feature_tables.pl" YES \
    "$PGSRC/sql_feature_packages.txt" "$PGSRC/sql_features.txt" \
    > "$GEN/features-supported.sgml"
perl "$DOC/mk_feature_tables.pl" NO \
    "$PGSRC/sql_feature_packages.txt" "$PGSRC/sql_features.txt" \
    > "$GEN/features-unsupported.sgml"

echo "[5/6] targets-meson.sgml"
perl "$DOC/generate-targets-meson.pl" "$DOC/targets-meson.txt" \
    "$DOC/generate-targets-meson.pl" > "$GEN/targets-meson.sgml"

echo "[6/6] Chinese localization (hash-pinned)"
rm -rf "$HERE/.loc-tmp"
mkdir -p "$HERE/.loc-tmp"
cp "$GEN"/*.sgml "$HERE/.loc-tmp/"
python3 "$REPO/zh/18/localize-generated.py" "$HERE/.loc-tmp"
for f in "$HERE/.loc-tmp"/*.sgml; do
    cp "$f" "$GENZH/$(basename "$f")"
done
rm -rf "$HERE/.loc-tmp"

wc -l "$GEN"/*.sgml
echo "done."
