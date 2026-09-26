#!/usr/bin/env bash
#
# Build PostgreSQL HTML documentation from a standalone doc source directory.
#
# Usage: build_standalone_docsrc.sh <doc-src-dir> <en|zh> <version> [output-dir]
# Fixed source: PGDOC_SOURCE_DIR + PGDOC_SOURCE_COMMIT, or
# PGDOC_SOURCE_ARCHIVE + PGDOC_SOURCE_SHA256 (verified release package).
#
# This script downloads the PG source tarball (cached), extracts it,
# overlays your SGML files, runs configure + make to produce HTML docs.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ $# -lt 3 || $# -gt 4 ]]; then
  echo "Usage: $0 <doc-src-dir> <en|zh> <version> [output-dir]" >&2
  exit 1
fi

docsrc_dir="$1"
lang="$2"
version="$3"
build_out="${4:-${docsrc_dir}/html}"
keep_work="${KEEP_WORK:-0}"

# Fixed Git and archive sources are opt-in; incomplete input never falls back.
if [[ -n "${PGDOC_SOURCE_ARCHIVE:-}" || -n "${PGDOC_SOURCE_SHA256:-}" ]]; then
  if [[ -n "${PGDOC_SOURCE_DIR:-}" || -n "${PGDOC_SOURCE_COMMIT:-}" ]]; then
    echo "Fixed Git and archive source options are mutually exclusive." >&2
    exit 1
  fi
  if [[ -z "${PGDOC_SOURCE_ARCHIVE:-}" || -z "${PGDOC_SOURCE_SHA256:-}" ]]; then
    echo "PGDOC_SOURCE_ARCHIVE and PGDOC_SOURCE_SHA256 must be supplied together." >&2
    exit 1
  fi
fi
if [[ -n "${PGDOC_SOURCE_DIR:-}" || -n "${PGDOC_SOURCE_COMMIT:-}" ]]; then
  if [[ -z "${PGDOC_SOURCE_DIR:-}" || -z "${PGDOC_SOURCE_COMMIT:-}" ]]; then
    echo "PGDOC_SOURCE_DIR and PGDOC_SOURCE_COMMIT must be supplied together." >&2
    exit 1
  fi
fi

case "${lang}" in
  en|zh) ;;
  *)
    echo "Unsupported language: ${lang} (expected: en or zh)" >&2
    exit 1
    ;;
esac

# Accept both layouts: dir containing postgres.sgml directly, or dir/sgml/
if [[ -d "${docsrc_dir}/sgml" ]]; then
  doc_src_root="${docsrc_dir}/sgml"
elif [[ -f "${docsrc_dir}/postgres.sgml" ]]; then
  doc_src_root="${docsrc_dir}"
else
  echo "Doc source directory not found: ${docsrc_dir}" >&2
  echo "  Expected postgres.sgml in ${docsrc_dir} or ${docsrc_dir}/sgml/" >&2
  exit 1
fi

# --- GNU Make ---
if command -v gmake >/dev/null 2>&1; then
  MAKE_CMD="gmake"
else
  MAKE_CMD="make"
fi

if ! "${MAKE_CMD}" --version 2>/dev/null | head -n 1 | grep -q "GNU Make"; then
  echo "GNU Make is required. Install gmake (brew install make) first." >&2
  exit 1
fi

# --- Required tools ---
for bin in xmllint xsltproc; do
  if ! command -v "${bin}" >/dev/null 2>&1; then
    echo "Missing dependency: ${bin}" >&2
    echo "  macOS:  brew install libxml2 libxslt" >&2
    echo "  Debian: apt-get install libxml2-utils xsltproc" >&2
    exit 1
  fi
done

# --- XML catalog (for resolving DocBook DTDs/XSL URIs) ---
if [[ -z "${XML_CATALOG_FILES:-}" ]]; then
  catalog_files=""
  for c in /etc/xml/catalog /usr/local/etc/xml/catalog /opt/homebrew/etc/xml/catalog; do
    if [[ -f "${c}" ]]; then
      if [[ -z "${catalog_files}" ]]; then
        catalog_files="${c}"
      else
        catalog_files="${catalog_files}:${c}"
      fi
    fi
  done
  if [[ -n "${catalog_files}" ]]; then
    export XML_CATALOG_FILES="${catalog_files}"
  fi
fi

# xmllint --catalogs consults SGML_CATALOG_FILES as well.
if [[ -n "${XML_CATALOG_FILES:-}" && -z "${SGML_CATALOG_FILES:-}" ]]; then
  export SGML_CATALOG_FILES="${XML_CATALOG_FILES}"
fi

# --- Cache directories ---
mkdir -p "${REPO_ROOT}/.cache/upstream" "${REPO_ROOT}/.cache/work"

official_git_url="https://git.postgresql.org/git/postgresql.git"
fallback_git_url="https://github.com/postgres/postgres.git"

is_release_version() {
  [[ "$1" =~ ^[0-9]+(\.[0-9]+|beta[0-9]+|rc[0-9]+)$ ]]
}

download_archive() {
  local ver="$1"
  local dst="$2"
  local url="https://ftp.postgresql.org/pub/source/v${ver}/postgresql-${ver}.tar.bz2"
  echo "Downloading: ${url}"
  if command -v wget >/dev/null 2>&1; then
    wget -c --tries=0 --timeout=30 --read-timeout=30 --waitretry=2 \
      --progress=dot:giga -O "${dst}" "${url}"
  else
    curl -fL --connect-timeout 20 --retry 10 --retry-delay 2 --retry-all-errors \
      --continue-at - "${url}" -o "${dst}"
  fi
}

download_dev_snapshot() {
  local ver="$1"
  local expected_hash="$2"
  local cache_dir="$3"
  local url="https://ftp.postgresql.org/pub/snapshot/dev/postgresql-snapshot.tar.bz2"
  local archive="${REPO_ROOT}/.cache/upstream/postgresql-${ver}-snapshot.tar.bz2"

  echo "Downloading PostgreSQL development snapshot: ${url}" >&2
  if [[ ! -f "${archive}" ]]; then
    if command -v wget >/dev/null 2>&1; then
      wget -c --tries=0 --timeout=30 --read-timeout=30 --waitretry=2 \
        --progress=dot:giga -O "${archive}" "${url}"
    else
      curl -fL --connect-timeout 20 --retry 10 --retry-delay 2 --retry-all-errors \
        --continue-at - "${url}" -o "${archive}"
    fi
  fi

  if ! tar -tjf "${archive}" >/dev/null 2>&1; then
    echo "Snapshot archive invalid, re-downloading: ${archive}" >&2
    rm -f "${archive}"
    if command -v wget >/dev/null 2>&1; then
      wget -c --tries=0 --timeout=30 --read-timeout=30 --waitretry=2 \
        --progress=dot:giga -O "${archive}" "${url}"
    else
      curl -fL --connect-timeout 20 --retry 10 --retry-delay 2 --retry-all-errors \
        --continue-at - "${url}" -o "${archive}"
    fi
    tar -tjf "${archive}" >/dev/null
  fi

  rm -rf "${cache_dir}"
  mkdir -p "${cache_dir}"
  tar -xjf "${archive}" -C "${cache_dir}" --strip-components=1
  printf '%s\n' "snapshot" > "${cache_dir}/.pgdoc-upstream-kind"
  printf '%s\n' "${expected_hash}" > "${cache_dir}/.pgdoc-upstream-ref"
  printf '%s\n' "${url}" > "${cache_dir}/.pgdoc-upstream-source"
}

resolve_git_ref() {
  local ver="$1"
  local stable_ref="REL_${ver}_STABLE"
  local hash

  hash="$(git ls-remote --heads "${official_git_url}" "${stable_ref}" 2>/dev/null | awk 'NR==1 {print $1}')"
  if [[ -n "${hash}" ]]; then
    printf '%s %s %s\n' "${stable_ref}" "${hash}" "${REPO_ROOT}/.cache/upstream/postgresql-${ver}-stable"
    return
  fi

  hash="$(git ls-remote --heads "${official_git_url}" master 2>/dev/null | awk 'NR==1 {print $1}')"
  if [[ -z "${hash}" ]]; then
    echo "Unable to resolve PostgreSQL git ref for version ${ver}" >&2
    exit 1
  fi

  printf '%s %s %s\n' "master" "${hash}" "${REPO_ROOT}/.cache/upstream/postgresql-${ver}devel"
}

sync_git_checkout() {
  local ver="$1"
  local ref expected_hash cache_dir
  read -r ref expected_hash cache_dir < <(resolve_git_ref "${ver}")

  if [[ -d "${cache_dir}/.git" ]]; then
    local current_hash
    current_hash="$(git -C "${cache_dir}" rev-parse HEAD 2>/dev/null || true)"
    if [[ "${current_hash}" == "${expected_hash}" ]]; then
      printf '%s\n' "${cache_dir}"
      return
    fi
  fi

  if [[ -f "${cache_dir}/.pgdoc-upstream-kind" &&
        -f "${cache_dir}/.pgdoc-upstream-ref" &&
        -x "${cache_dir}/configure" ]]; then
    local cache_kind cache_ref
    cache_kind="$(cat "${cache_dir}/.pgdoc-upstream-kind")"
    cache_ref="$(cat "${cache_dir}/.pgdoc-upstream-ref")"
    if [[ "${cache_kind}" == "snapshot" ]]; then
      if [[ "${cache_ref}" != "${expected_hash}" ]]; then
        echo "Using cached PostgreSQL development snapshot; current ${ref} head differs." >&2
        echo "  snapshot ref marker: ${cache_ref}" >&2
        echo "  current ${ref} head: ${expected_hash}" >&2
      fi
      printf '%s\n' "${cache_dir}"
      return
    fi
  fi

  rm -rf "${cache_dir}"

  echo "Cloning PostgreSQL ${ver} source from ${ref} ..." >&2
  if ! git clone --depth 1 --branch "${ref}" "${official_git_url}" "${cache_dir}"; then
    rm -rf "${cache_dir}"
    echo "Official PostgreSQL git mirror clone failed, falling back to GitHub mirror ..." >&2
    if ! git clone --depth 1 --branch "${ref}" "${fallback_git_url}" "${cache_dir}"; then
      rm -rf "${cache_dir}"
      echo "GitHub mirror clone failed, using PostgreSQL development snapshot ..." >&2
      download_dev_snapshot "${ver}" "${expected_hash}" "${cache_dir}"
    fi
  fi

  if [[ -d "${cache_dir}/.git" ]]; then
    local current_hash
    current_hash="$(git -C "${cache_dir}" rev-parse HEAD)"
    if [[ "${current_hash}" != "${expected_hash}" ]]; then
      echo "Cloned git checkout does not match official ${ref} head." >&2
      echo "  expected: ${expected_hash}" >&2
      echo "  actual:   ${current_hash}" >&2
      exit 1
    fi
  elif [[ ! -f "${cache_dir}/.pgdoc-upstream-kind" || ! -x "${cache_dir}/configure" ]]; then
    echo "Unable to prepare PostgreSQL ${ver} source checkout." >&2
    exit 1
  fi

  printf '%s\n' "${cache_dir}"
}

# --- Prepare work tree ---
work_tree="$(mktemp -d "${REPO_ROOT}/.cache/work/standalone-${lang}-${version}.XXXXXX")"
trap '[[ "${keep_work}" == "1" ]] || rm -rf "${work_tree}"' EXIT

echo "Preparing build workspace: ${work_tree}"
if [[ -n "${PGDOC_SOURCE_DIR:-}" ]]; then
  python3 "${SCRIPT_DIR}/prepare_pinned_doc_source.py" \
    "${PGDOC_SOURCE_DIR}" "${PGDOC_SOURCE_COMMIT}" "${version}" "${work_tree}"
elif [[ -n "${PGDOC_SOURCE_ARCHIVE:-}" ]]; then
  python3 "${SCRIPT_DIR}/prepare_pinned_doc_source.py" --archive \
    "${PGDOC_SOURCE_ARCHIVE}" "${PGDOC_SOURCE_SHA256}" "${version}" "${work_tree}"
elif is_release_version "${version}"; then
  archive="${REPO_ROOT}/.cache/upstream/postgresql-${version}.tar.bz2"

  if [[ ! -f "${archive}" ]]; then
    echo "Downloading source archive for PostgreSQL ${version} ..."
    download_archive "${version}" "${archive}"
  fi

  if ! tar -tjf "${archive}" >/dev/null 2>&1; then
    echo "Archive invalid, re-downloading: ${archive}"
    rm -f "${archive}"
    download_archive "${version}" "${archive}"
    tar -tjf "${archive}" >/dev/null
  fi

  tar -xjf "${archive}" -C "${work_tree}" --strip-components=1
else
  git_checkout="$(sync_git_checkout "${version}")"
  rsync -a --exclude='.git' "${git_checkout}/" "${work_tree}/"
fi

# Release tarballs can contain prebuilt English HTML.  Remove it before the
# overlay/build so the output contains only chunks generated from this source.
rm -rf "${work_tree}/doc/src/sgml/html"
rm -f "${work_tree}/doc/src/sgml/html-stamp"

# Overlay our SGML/XSL/CSS sources into the extracted source tree.
# Exclude our project Makefile and .gitignore — the upstream Makefile.in
# (which ./configure will turn into a proper Makefile) must be preserved.
rsync -a \
  --exclude='Makefile' \
  --exclude='.gitignore' \
  --exclude='html/' \
  --exclude='html-stamp' \
  "${doc_src_root}/" "${work_tree}/doc/src/sgml/"

# EN archives predating 9.5 either ship no XSL stylesheet family at all
# (6.x-7.x, jade era) or ship one that does not chunk under the backported
# pipeline (8.x-9.4).  The pgdoc overlay stylesheets kept alongside the
# matching zh major are language-neutral customizations of the same era and
# drive this pipeline directly; use them for EN builds too.
if [[ "${lang}" == "en" && "${version}" =~ ^([0-9]+(\.[0-9]+)?) ]]; then
  zh_major="${BASH_REMATCH[1]}"
  if [[ -f "${REPO_ROOT}/zh/${zh_major}/stylesheet.xsl" ]] \
     && awk -v m="${zh_major}" 'BEGIN{exit !(m < 9.5)}'; then
    cp "${REPO_ROOT}/zh/${zh_major}"/stylesheet*.xsl "${work_tree}/doc/src/sgml/" 2>/dev/null || true
    cp "${REPO_ROOT}/zh/${zh_major}"/stylesheet.css "${REPO_ROOT}/zh/${zh_major}"/stylesheet.dsl \
       "${work_tree}/doc/src/sgml/" 2>/dev/null || true
    # The pgdoc speedup layer hard-codes zh_cn gentext; EN documents carry no
    # lang attribute, so the override must be neutralised for English output.
    sed -i.bak 's|<xsl:template name="l10n.language">zh_cn</xsl:template>|<xsl:template name="l10n.language">en</xsl:template>|' \
      "${work_tree}/doc/src/sgml/stylesheet-speedup-common.xsl" 2>/dev/null \
      && rm -f "${work_tree}/doc/src/sgml/stylesheet-speedup-common.xsl.bak"
    echo "EN build: using pgdoc overlay stylesheets from zh/${zh_major}." >&2
  fi
fi

# 7.x-era upstream SGML references figures without a file extension
# (<imagedata fileref="connections">); jade resolved those by probing
# extensions, osx/XSL/FOP do not.  Point them at the shipped .gif files.
if [[ "${lang}" == "en" ]]; then
  python3 - "$work_tree/doc/src/sgml" <<'PYFIX'
import re, sys, glob, os
d = sys.argv[1]
gifs = {os.path.basename(g)[:-4] for g in glob.glob(os.path.join(d, '*.gif'))}
n = 0
for f in glob.glob(os.path.join(d, '*.sgml')):
    s = open(f, encoding='utf-8', errors='surrogateescape').read()
    def sub(m):
        global n
        if m.group(1) in gifs:
            n += 1
            return 'fileref="%s.gif"' % m.group(1)
        return m.group(0)
    s2 = re.sub(r'fileref="([A-Za-z0-9_-]+)"', sub, s)
    if s2 != s:
        open(f, 'w', encoding='utf-8', errors='surrogateescape').write(s2)
if n:
    print("EN build: added .gif to %d extension-less filerefs." % n)
PYFIX
fi

# Upstream 7.0.3's inherit.sgml closes its paragraph prematurely (a jade-era
# OMITTAG artifact); with the XSL pipeline the orphan text lands at FO root
# and FOP rejects it.  Repair the work-tree copy only.
if [[ "${lang}" == "en" && "${version}" == "7.0.3" ]]; then
  python3 - "$work_tree/doc/src/sgml/inherit.sgml" <<'PY7'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8', errors='surrogateescape').read()
fixed = []
bad = '   </note>\n  </para>\n\n   For example'
if bad in s:
    s = s.replace(bad, '   </note>\n\n   For example', 1)
    fixed.append('premature </para>')
bad2 = '</chapter>\n  <para>\n'
if bad2 in s:
    s = s.replace(bad2, '</chapter>\n', 1)
    fixed.append('stray trailing <para>')
if fixed:
    open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s)
    print('EN build: repaired 7.0.3 inherit.sgml (%s).' % ', '.join(fixed))
PY7
fi


# --- Configure (minimal, just enough for docs) ---
echo "Configuring source tree ..."
extra_configure_flags="${CONFIGURE_FLAGS:-}"
if [[ "${PGDOC_SKIP_CONFIGURE:-0}" == "1" ]]; then
  # PG 7.1 – 7.3 的 configure 在现代工具链上跑不通，而它们的 doc 构建只从
  # Makefile.global 取 VERSION/srcdir 等少量变量；直接写桩。
  echo "Skipping configure (PGDOC_SKIP_CONFIGURE=1); writing stub src/Makefile.global."
  printf 'srcdir = .\ntop_srcdir = ../..\nVERSION = %s\n' "${version}" \
    > "${work_tree}/src/Makefile.global"
elif [[ -f "${work_tree}/configure" ]]; then
  (cd "${work_tree}" && ./configure --without-icu --without-readline --without-zlib ${extra_configure_flags} >/dev/null)
elif [[ -f "${work_tree}/src/configure" ]]; then
  # PG 6.x ships configure only under src/.  Its doc makefile treats
  # Makefile.global as optional, so a configure failure (ancient config.guess
  # on modern hosts) is non-fatal for the doc build.
  (cd "${work_tree}/src" && ./configure --without-icu --without-readline --without-zlib ${extra_configure_flags} >/dev/null) || \
    echo "NOTE: src/configure failed; 6.x doc makefile runs without Makefile.global" >&2
fi

# --- Relax XML validation for translated docs ---
# Chinese translations may reference anchors from newer PG versions,
# causing IDREF validation errors.  Keep DTD/entity loading enabled so
# standard DocBook entities still resolve, but skip strict validation.
# XML parsing uses XML_CATALOG_FILES; --catalogs would also load native SGML catalogs.
if [[ "${lang}" != "en" ]]; then
  sed -i.bak \
    -e 's/--valid/--loaddtd/g' \
    "${work_tree}/doc/src/sgml/Makefile"
fi

# Pre-PG10 doc makefiles build HTML via DSSSL (jade) by default.  Reroute the
# html target to the XSL pipeline (xslthtml-stamp, osx -> postgres.xml ->
# xsltproc chunked HTML) that those makefiles already provide, matching what
# PG10+ do natively.  The guard is a no-op for PG10 and later.
# PG <= 9.2 only provide the xslthtml target (no xslthtml-stamp variant);
# backport the 9.4-recipe xslthtml-stamp (index marked section, SDATA entity
# fixup, css copy) first, then the stamp branch below takes over.  The
# backport is a no-op for PG >= 9.3.
python3 "${SCRIPT_DIR}/patch_legacy_xsl_pipeline.py" "${work_tree}/doc/src/sgml"
if grep -q '^xslthtml-stamp:' "${work_tree}/doc/src/sgml/Makefile"; then
  sed -i.bak \
    -e 's/^html: html-stamp$/html: xslthtml-stamp/' \
    "${work_tree}/doc/src/sgml/Makefile"
elif grep -q '^xslthtml:' "${work_tree}/doc/src/sgml/Makefile"; then
  sed -i.bak \
    -e 's/^html: html-stamp$/html: xslthtml/' \
    "${work_tree}/doc/src/sgml/Makefile"
fi

# Incremental generated-text overlays are kept with each Chinese source.
# Generate from the selected upstream inputs before applying exact-hash edits.
if [[ "${lang}" == "zh" && -f "${doc_src_root}/localize-generated.py" ]]; then
  # Use this version's generated-file list, including pre-Meson releases.
  printf '.PHONY: pgdoc-generated\npgdoc-generated: $(GENERATED_SGML)\n' \
    > "${work_tree}/doc/src/sgml/Makefile.pgdoc-generated"
  (cd "${work_tree}" && "${MAKE_CMD}" -C doc/src/sgml \
    -f Makefile -f Makefile.pgdoc-generated pgdoc-generated)
  python3 "${doc_src_root}/localize-generated.py" "${work_tree}/doc/src/sgml"
fi

if [[ "${ALLOW_NET:-0}" == "1" ]]; then
  sed -i.bak \
    -e 's/[[:space:]]--nonet//g' \
    "${work_tree}/doc/src/sgml/Makefile"
fi

# Backported HTML stylesheets use the upstream CSS entity wrapper too.
# Older source archives predate that file; generate it from their real CSS
# so DocBook can emit the stylesheet without a missing-XML diagnostic.
if [[ -f "${work_tree}/doc/src/sgml/stylesheet.css" &&
      ! -f "${work_tree}/doc/src/sgml/stylesheet.css.xml" ]]; then
  cat > "${work_tree}/doc/src/sgml/stylesheet.css.xml" <<'CSS_XML'
<!DOCTYPE style [
<!ENTITY css SYSTEM "stylesheet.css">
]>
<style>&css;</style>
CSS_XML
fi

# --- Build HTML ---
echo "Building HTML docs (${lang} ${version}) ..."
(cd "${work_tree}" && "${MAKE_CMD}" -C doc/src/sgml DOC_LANG="${lang}" html)

if [[ "${lang}" == "zh" ]]; then
  html_spacing_args=(--report "${work_tree}/doc/src/sgml/html-spacing-report.json")
  if [[ "${keep_work}" == "1" ]]; then
    html_spacing_args+=(--before-dir "${work_tree}/doc/src/sgml/html-before-spacing")
  fi
  python3 "${SCRIPT_DIR}/prepare_chinese_html.py" \
    "${work_tree}/doc/src/sgml/html" "${html_spacing_args[@]}"
fi

# Older XSL targets do not copy every referenced image or stylesheet.
# Populate those resources from this build's sources and fail on missing
# local files before publishing the output, even if make ignored a failed cp.
python3 "${SCRIPT_DIR}/prepare_html_resources.py" "${work_tree}/doc/src/sgml" \
    --localization-report "${work_tree}/doc/src/sgml/html-localization-report.json" \
    --style-report "${work_tree}/doc/src/sgml/html-legacy-css-report.json"

# --- Copy output ---
mkdir -p "${build_out}"
rsync -a --delete "${work_tree}/doc/src/sgml/html/" "${build_out}/"

echo ""
echo "Build complete: ${build_out}"
echo "  $(find "${build_out}" -name '*.html' | wc -l | tr -d ' ') HTML files generated"
