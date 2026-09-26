#!/usr/bin/env bash
#
# Build PostgreSQL PDF documentation from a standalone doc source directory.
#
# Usage: build_standalone_pdfsrc.sh <doc-src-dir> <en|zh> <version> [output-pdf] [A4|US]
# Fixed source: PGDOC_SOURCE_DIR + PGDOC_SOURCE_COMMIT, or
# PGDOC_SOURCE_ARCHIVE + PGDOC_SOURCE_SHA256 (verified release package).
#
# This script downloads the PostgreSQL source tarball (cached), extracts it,
# overlays the SGML sources, runs configure + GNU make to prepare the expanded
# XML, then uses xsltproc + Apache FOP to render a PDF locally.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

usage() {
  echo "Usage: $0 <doc-src-dir> <en|zh> <version> [output-pdf] [A4|US]" >&2
}

if [[ $# -lt 3 || $# -gt 5 ]]; then
  usage
  exit 1
fi

docsrc_dir="$1"
lang="$2"
version="$3"
paper_input="${5:-A4}"
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

case "${paper_input}" in
  A4|a4)
    paper="A4"
    paper_type="A4"
    ;;
  US|us|USletter|usletter|letter)
    paper="US"
    paper_type="USletter"
    ;;
  *)
    echo "Unsupported paper type: ${paper_input} (expected: A4 or US)" >&2
    exit 1
    ;;
esac

default_out="${docsrc_dir}/postgresql-${version}-${lang}-${paper}.pdf"
output_pdf="${4:-${default_out}}"

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
required_bins=(xmllint xsltproc rsync java)
if [[ "${lang}" == "zh" ]]; then
  required_bins+=(fc-match)
fi

for bin in "${required_bins[@]}"; do
  if ! command -v "${bin}" >/dev/null 2>&1; then
    echo "Missing dependency: ${bin}" >&2
    case "${bin}" in
      xmllint)
        echo "  macOS:  brew install libxml2" >&2
        ;;
      xsltproc)
        echo "  macOS:  brew install libxslt" >&2
        ;;
      fc-match)
        echo "  macOS:  brew install fontconfig" >&2
        ;;
      java)
        echo "  macOS:  brew install openjdk" >&2
        ;;
    esac
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

if [[ -n "${XML_CATALOG_FILES:-}" && -z "${SGML_CATALOG_FILES:-}" ]]; then
  export SGML_CATALOG_FILES="${XML_CATALOG_FILES}"
fi

mkdir -p "${REPO_ROOT}/.cache/upstream" "${REPO_ROOT}/.cache/work" "${REPO_ROOT}/.cache/tools"

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

ensure_fop() {
  if [[ -n "${FOP_BIN:-}" ]]; then
    FOP_CMD="${FOP_BIN}"
    return
  fi

  if command -v fop >/dev/null 2>&1; then
    FOP_CMD="$(command -v fop)"
    return
  fi

  local fop_version="2.11"
  local fop_root="${REPO_ROOT}/.cache/tools/fop-${fop_version}"
  local fop_archive="${REPO_ROOT}/.cache/tools/fop-${fop_version}-bin.tar.gz"
  local fop_url="https://dlcdn.apache.org/xmlgraphics/fop/binaries/fop-${fop_version}-bin.tar.gz"

  if [[ ! -x "${fop_root}/fop/fop" ]]; then
    echo "Downloading Apache FOP ${fop_version} ..."
    curl -fL --connect-timeout 20 --retry 10 --retry-delay 2 --retry-all-errors \
      "${fop_url}" -o "${fop_archive}"
    rm -rf "${fop_root}"
    mkdir -p "${fop_root}"
    tar -xzf "${fop_archive}" -C "${fop_root}" --strip-components=1
  fi

  FOP_CMD="${fop_root}/fop/fop"
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

resolve_font_file() {
  local pattern="$1"
  local file
  file="$(fc-match -f '%{file}\n' "${pattern}" 2>/dev/null | head -n 1 || true)"
  if [[ -n "${file}" && -f "${file}" ]]; then
    printf '%s\n' "${file}"
    return 0
  fi
  return 1
}

xml_escape_attr() {
  local text="$1"
  text="${text//&/&amp;}"
  text="${text//\"/&quot;}"
  text="${text//</&lt;}"
  text="${text//>/&gt;}"
  printf '%s' "${text}"
}

create_fop_config() {
  local dst="$1"
  local cjk_family="$2"
  local cjk_regular="$3"
  local cjk_bold="$4"
  local mono_family="$5"
  local mono_regular="$6"
  local mono_bold="$7"
  local mono_italic="$8"
  local mono_bold_italic="$9"
  local math_family="${10}"
  local math_regular="${11}"
  local math_bold="${12}"

  local cjk_family_xml mono_family_xml cjk_regular_xml cjk_bold_xml
  local mono_regular_xml mono_bold_xml mono_italic_xml mono_bold_italic_xml
  local math_family_xml math_regular_xml math_bold_xml
  cjk_family_xml="$(xml_escape_attr "${cjk_family}")"
  mono_family_xml="$(xml_escape_attr "${mono_family}")"
  cjk_regular_xml="$(xml_escape_attr "${cjk_regular}")"
  cjk_bold_xml="$(xml_escape_attr "${cjk_bold}")"
  mono_regular_xml="$(xml_escape_attr "${mono_regular}")"
  mono_bold_xml="$(xml_escape_attr "${mono_bold}")"
  mono_italic_xml="$(xml_escape_attr "${mono_italic}")"
  mono_bold_italic_xml="$(xml_escape_attr "${mono_bold_italic}")"
  math_family_xml="$(xml_escape_attr "${math_family}")"
  math_regular_xml="$(xml_escape_attr "${math_regular}")"
  math_bold_xml="$(xml_escape_attr "${math_bold}")"

  # Font entries with an empty embed-url would be rejected by FOP's strict
  # configuration; emit each block only when its font file is present.
  local fonts_xml=""
  if [[ -n "${math_regular_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${math_regular_xml}\">
          <font-triplet name=\"${math_family_xml}\" style=\"normal\" weight=\"normal\"/>
          <font-triplet name=\"${math_family_xml}\" style=\"italic\" weight=\"normal\"/>
        </font>
"
  fi
  if [[ -n "${math_bold_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${math_bold_xml}\">
          <font-triplet name=\"${math_family_xml}\" style=\"normal\" weight=\"bold\"/>
          <font-triplet name=\"${math_family_xml}\" style=\"italic\" weight=\"bold\"/>
        </font>
"
  fi
  if [[ -n "${cjk_regular_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${cjk_regular_xml}\">
          <font-triplet name=\"${cjk_family_xml}\" style=\"normal\" weight=\"normal\"/>
          <font-triplet name=\"${cjk_family_xml}\" style=\"italic\" weight=\"normal\"/>
        </font>
"
  fi
  if [[ -n "${cjk_bold_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${cjk_bold_xml}\">
          <font-triplet name=\"${cjk_family_xml}\" style=\"normal\" weight=\"bold\"/>
          <font-triplet name=\"${cjk_family_xml}\" style=\"italic\" weight=\"bold\"/>
        </font>
"
  fi
  if [[ -n "${mono_regular_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${mono_regular_xml}\">
          <font-triplet name=\"${mono_family_xml}\" style=\"normal\" weight=\"normal\"/>
        </font>
"
  fi
  if [[ -n "${mono_bold_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${mono_bold_xml}\">
          <font-triplet name=\"${mono_family_xml}\" style=\"normal\" weight=\"bold\"/>
        </font>
"
  fi
  if [[ -n "${mono_italic_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${mono_italic_xml}\">
          <font-triplet name=\"${mono_family_xml}\" style=\"italic\" weight=\"normal\"/>
        </font>
"
  fi
  if [[ -n "${mono_bold_italic_xml}" ]]; then
    fonts_xml+="        <font kerning=\"yes\" embed-url=\"${mono_bold_italic_xml}\">
          <font-triplet name=\"${mono_family_xml}\" style=\"italic\" weight=\"bold\"/>
        </font>
"
  fi

  cat > "${dst}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<fop version="1.0">
  <strict-configuration>true</strict-configuration>
  <strict-validation>false</strict-validation>
  <renderers>
    <renderer mime="application/pdf">
      <fonts>
${fonts_xml}      </fonts>
    </renderer>
  </renderers>
</fop>
EOF
}

ensure_fop

work_tree="$(mktemp -d "${REPO_ROOT}/.cache/work/standalone-pdf-${lang}-${version}.XXXXXX")"
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

# Do not carry prebuilt English HTML from release tarballs into the isolated
# workspace, even though the PDF target itself does not consume those chunks.
rm -rf "${work_tree}/doc/src/sgml/html"
rm -f "${work_tree}/doc/src/sgml/html-stamp"

rsync -a \
  --exclude='Makefile' \
  --exclude='.gitignore' \
  --exclude='html/' \
  --exclude='html-stamp' \
  "${doc_src_root}/" "${work_tree}/doc/src/sgml/"

# EN archives predating 9.5 either ship no XSL stylesheet family at all
# (6.x-7.x, jade era) or ship one that does not drive the backported pipeline
# (8.x-9.4).  The pgdoc overlay stylesheets kept alongside the matching zh
# major are language-neutral customizations of the same era; use them for EN.
if [[ "${lang}" == "en" && "${version}" =~ ^([0-9]+(\.[0-9]+)?) ]]; then
  zh_major="${BASH_REMATCH[1]}"
  if [[ -f "${REPO_ROOT}/zh/${zh_major}/stylesheet-fo.xsl" ]] \
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


# PG 6.x and 7.0 have no top-level configure; their doc makefiles either are
# standalone (6.x) or include src/Makefile.global only conditionally (7.0).
# Skip configure when the doc makefile has no unconditional include of it;
# otherwise a missing top-level configure is a hard error.
if [[ "${PGDOC_SKIP_CONFIGURE:-0}" == "1" ]]; then
  # PG 7.1 – 7.3 的 configure 在现代工具链上跑不通，而它们的 doc 构建只从
  # Makefile.global 取 VERSION/srcdir 等少量变量；直接写桩。
  echo "Skipping configure (PGDOC_SKIP_CONFIGURE=1); writing stub src/Makefile.global."
  printf 'srcdir = .\ntop_srcdir = ../..\nVERSION = %s\n' "${version}" \
    > "${work_tree}/src/Makefile.global"
elif [[ -x "${work_tree}/configure" ]]; then
  echo "Configuring source tree ..."
  extra_configure_flags="${CONFIGURE_FLAGS:-}"
  (cd "${work_tree}" && ./configure --without-icu --without-readline --without-zlib ${extra_configure_flags} >/dev/null)
elif grep -qE '^include .*Makefile\.global' "${work_tree}/doc/src/sgml/Makefile"; then
  # PG 6.x doc makefiles include src/Makefile.global unconditionally, but
  # their doc targets only use self-defined jade-era variables.  A stub
  # satisfies the include without running a 1998-era configure on a modern
  # toolchain.
  echo "No top-level configure; writing stub src/Makefile.global for the doc build."
  printf '# pgdoc stub: legacy doc makefile include target (doc rules are self-contained).\n' \
    > "${work_tree}/src/Makefile.global"
else
  echo "Skipping configure (legacy standalone doc makefile)."
fi

# XML parsing uses XML_CATALOG_FILES; --catalogs would also load native SGML catalogs.
if [[ "${lang}" != "en" ]]; then
  sed -i.bak \
    -e 's/--valid/--loaddtd/g' \
    "${work_tree}/doc/src/sgml/Makefile"
fi

# PG <= 9.1 doc makefiles lack the include-xslt-index marked section and the
# widened SDATA entity fixup in the SGML->XML step (both needed for an
# index-bearing, accent-clean postgres.xml).  Backport them; no-op for PG >= 9.2.
python3 "${SCRIPT_DIR}/patch_legacy_xsl_pipeline.py" "${work_tree}/doc/src/sgml"
python3 "${SCRIPT_DIR}/prepare_pdf_stylesheet.py" "${work_tree}/doc/src/sgml/stylesheet-fo.xsl"

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

fo_path="${work_tree}/doc/src/sgml/postgres-${paper}.fo"
pdf_tmp="${work_tree}/doc/src/sgml/postgresql-${version}-${lang}-${paper}.pdf"
fop_config=""

echo "Building XSL-FO (${lang} ${version}, ${paper}) ..."
xslprocflags_extra="${XSLTPROCFLAGS:-}"

if [[ "${lang}" == "zh" ]]; then
  pdf_cjk_family="${PDF_CJK_FAMILY:-Alibaba PuHuiTi 3.0}"
  pdf_mono_family="${PDF_MONO_FAMILY:-Courier New}"
  pdf_mono_param="${PDF_MONO_PARAM:-${pdf_mono_family},${pdf_cjk_family}}"

  pdf_cjk_regular="${PDF_CJK_REGULAR:-$(resolve_font_file "${pdf_cjk_family}:style=Regular" || true)}"
  if [[ -z "${pdf_cjk_regular}" ]]; then
    pdf_cjk_regular="$(resolve_font_file "${pdf_cjk_family}" || true)"
  fi
  pdf_cjk_bold="${PDF_CJK_BOLD:-$(resolve_font_file "${pdf_cjk_family}:style=Bold" || true)}"
  if [[ -z "${pdf_cjk_bold}" ]]; then
    pdf_cjk_bold="${pdf_cjk_regular}"
  fi

  pdf_mono_regular="${PDF_MONO_REGULAR:-$(resolve_font_file "${pdf_mono_family}:style=Regular" || true)}"
  pdf_mono_bold="${PDF_MONO_BOLD:-$(resolve_font_file "${pdf_mono_family}:style=Bold" || true)}"
  pdf_mono_italic="${PDF_MONO_ITALIC:-$(resolve_font_file "${pdf_mono_family}:style=Italic" || true)}"
  pdf_mono_bold_italic="${PDF_MONO_BOLD_ITALIC:-$(resolve_font_file "${pdf_mono_family}:style=Bold Italic" || true)}"

  if [[ -z "${pdf_cjk_regular}" || ! -f "${pdf_cjk_regular}" ]]; then
    echo "Unable to locate regular font for ${pdf_cjk_family}." >&2
    echo "Set PDF_CJK_REGULAR or install the font locally first." >&2
    exit 1
  fi
  if [[ -z "${pdf_cjk_bold}" || ! -f "${pdf_cjk_bold}" ]]; then
    echo "Unable to locate bold font for ${pdf_cjk_family}." >&2
    echo "Set PDF_CJK_BOLD or install the font locally first." >&2
    exit 1
  fi

  if [[ -z "${pdf_mono_regular}" || ! -f "${pdf_mono_regular}" ]]; then
    echo "Unable to locate regular mono font for ${pdf_mono_family}." >&2
    echo "Set PDF_MONO_REGULAR or install the font locally first." >&2
    exit 1
  fi
  if [[ -z "${pdf_mono_bold}" || ! -f "${pdf_mono_bold}" ]]; then
    pdf_mono_bold="${pdf_mono_regular}"
  fi
  if [[ -z "${pdf_mono_italic}" || ! -f "${pdf_mono_italic}" ]]; then
    pdf_mono_italic="${pdf_mono_regular}"
  fi
  if [[ -z "${pdf_mono_bold_italic}" || ! -f "${pdf_mono_bold_italic}" ]]; then
    pdf_mono_bold_italic="${pdf_mono_bold}"
  fi

  # 老版本手册（6.x/7.x）的集合论记号（∊∖∃∀…）在正文与代码字体里都没有
  # 字形；注册系统 STIXGeneral 作数学后备，接在所有字体族列表末尾。
  pdf_math_family="${PDF_MATH_FAMILY:-STIXGeneral}"
  pdf_math_regular="${PDF_MATH_REGULAR:-$(resolve_font_file "${pdf_math_family}:style=Regular" || true)}"
  if [[ -z "${pdf_math_regular}" ]]; then
    pdf_math_regular="$(resolve_font_file "${pdf_math_family}" || true)"
  fi
  pdf_math_bold="${PDF_MATH_BOLD:-$(resolve_font_file "${pdf_math_family}:style=Bold" || true)}"
  if [[ -z "${pdf_math_bold}" ]]; then
    pdf_math_bold="${pdf_math_regular}"
  fi
  pdf_math_suffix=""
  if [[ -n "${pdf_math_regular}" ]] && [[ -f "${pdf_math_regular}" ]]; then
    pdf_math_suffix=",${pdf_math_family}"
  else
    pdf_math_family=""
  fi

  fop_config="${work_tree}/doc/src/sgml/fop-local.xconf"
  create_fop_config \
    "${fop_config}" \
    "${pdf_cjk_family}" \
    "${pdf_cjk_regular}" \
    "${pdf_cjk_bold}" \
    "${pdf_mono_family}" \
    "${pdf_mono_regular}" \
    "${pdf_mono_bold}" \
    "${pdf_mono_italic}" \
    "${pdf_mono_bold_italic}" \
    "${pdf_math_family}" \
    "${pdf_math_regular}" \
    "${pdf_math_bold}"
fi

append_xsltproc_flag() {
  if [[ -n "${xslprocflags_extra}" ]]; then
    xslprocflags_extra+=" "
  fi
  xslprocflags_extra+="$1"
}

if [[ "${lang}" == "zh" ]]; then
  append_xsltproc_flag "--stringparam body.font.family '${pdf_cjk_family}${pdf_math_suffix:-}'"
  append_xsltproc_flag "--stringparam sans.font.family '${pdf_cjk_family}${pdf_math_suffix:-}'"
  append_xsltproc_flag "--stringparam title.font.family '${pdf_cjk_family}${pdf_math_suffix:-}'"
  append_xsltproc_flag "--stringparam monospace.font.family '${pdf_mono_param}${pdf_math_suffix:-}'"
fi

# EN builds keep the base-14 body fonts but need the same system math
# fallback as zh: 6.x/7.x use set-theory glyphs (∊∖∃∀) that Times, Helvetica
# and Courier do not carry.  Register STIXGeneral and append it to every
# font-family chain.
if [[ "${lang}" == "en" ]]; then
  pdf_math_family="${PDF_MATH_FAMILY:-STIXGeneral}"
  pdf_math_regular="${PDF_MATH_REGULAR:-$(resolve_font_file "${pdf_math_family}:style=Regular" || true)}"
  if [[ -z "${pdf_math_regular}" ]]; then
    pdf_math_regular="$(resolve_font_file "${pdf_math_family}" || true)"
  fi
  pdf_math_bold="${PDF_MATH_BOLD:-$(resolve_font_file "${pdf_math_family}:style=Bold" || true)}"
  if [[ -z "${pdf_math_bold}" ]]; then
    pdf_math_bold="${pdf_math_regular}"
  fi
  if [[ -n "${pdf_math_regular}" && -f "${pdf_math_regular}" ]]; then
    fop_config="${work_tree}/doc/src/sgml/fop-local.xconf"
    create_fop_config "${fop_config}" \
      "" "" "" "" "" "" "" "" \
      "${pdf_math_family}" "${pdf_math_regular}" "${pdf_math_bold}"
    append_xsltproc_flag "--stringparam body.font.family 'Times,${pdf_math_family}'"
    append_xsltproc_flag "--stringparam sans.font.family 'Helvetica,${pdf_math_family}'"
    append_xsltproc_flag "--stringparam title.font.family 'Helvetica,${pdf_math_family}'"
    append_xsltproc_flag "--stringparam monospace.font.family 'Courier,${pdf_math_family}'"
  fi
fi

(cd "${work_tree}" && XSLTPROCFLAGS="${xslprocflags_extra}" "${MAKE_CMD}" -C doc/src/sgml DOC_LANG="${lang}" "postgres-${paper}.fo" >/dev/null)

if [[ "${lang}" == "zh" ]]; then
  python3 "${SCRIPT_DIR}/prepare_chinese_pdf.py" "${fo_path}" --cjk-family "${pdf_cjk_family}"
fi

echo "Rendering PDF (${lang} ${version}, ${paper}) ..."
export FOP_OPTS="${FOP_OPTS:--Xmx1500m}"

fop_args=()
if [[ -n "${fop_config}" ]]; then
  fop_args+=(-c "${fop_config}")
fi
fop_args+=(-fo "${fo_path}" -pdf "${pdf_tmp}")

fop_log="${work_tree}/doc/src/sgml/fop.log"
if ! LANG=C "${FOP_CMD}" "${fop_args[@]}" >"${fop_log}" 2>&1; then
  cat "${fop_log}" >&2
  exit 1
fi

# FOP can exit successfully while reporting clipped content or unresolved
# references. Retain its complete diagnostics beside the PDF and surface the
# warnings in the build log so a successful renderer is not mistaken for QA.
mkdir -p "$(dirname "${output_pdf}")"
cp "${fop_log}" "${output_pdf%.pdf}.fop.log"
grep -E '(^|[[:space:]])(WARNING:|WARN:|SEVERE:|ERROR:|\[WARN\]|\[ERROR\])' "${fop_log}" >&2 || true
if grep -qE '(^|[[:space:]])(SEVERE:|ERROR:|\[ERROR\])' "${fop_log}"; then
  echo "PDF rendering completed with FOP errors; see ${output_pdf%.pdf}.fop.log" >&2
  exit 1
fi

# U+FFFD reaches the render straight from ancient upstream archives (e.g. a
# 1998-era message string in 6.4); EN body fonts have no glyph for it.  For
# EN builds it is an accepted source artifact -- every other missing glyph
# stays a hard failure.
glyph_denied="$(grep 'not available in font' "${fop_log}" | grep -v '(0xfffd)' || true)"
glyph_any="$(grep -c 'not available in font' "${fop_log}" || true)"
if [[ -n "${glyph_denied}" ]] || { [[ "${lang}" == "zh" ]] && [[ "${glyph_any}" -gt 0 ]]; }; then
  cat "${fop_log}" >&2
  echo "PDF rendering completed with missing glyph warnings." >&2
  exit 1
fi

mkdir -p "$(dirname "${output_pdf}")"
cp "${pdf_tmp}" "${output_pdf}"

echo ""
echo "Build complete: ${output_pdf}"
if command -v pdfinfo >/dev/null 2>&1; then
  echo "  $(pdfinfo "${output_pdf}" | awk -F': *' '/^Pages:/ {print $2}') pages generated"
fi
