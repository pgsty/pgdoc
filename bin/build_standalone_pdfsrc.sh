#!/usr/bin/env bash
#
# Build PostgreSQL PDF documentation from a standalone doc source directory.
#
# Usage: build_standalone_pdfsrc.sh <doc-src-dir> <en|zh> <version> [output-pdf] [A4|US]
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
  [[ "$1" =~ ^[0-9]+\.[0-9]+$ ]]
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

  local cjk_family_xml mono_family_xml cjk_regular_xml cjk_bold_xml
  local mono_regular_xml mono_bold_xml mono_italic_xml mono_bold_italic_xml
  cjk_family_xml="$(xml_escape_attr "${cjk_family}")"
  mono_family_xml="$(xml_escape_attr "${mono_family}")"
  cjk_regular_xml="$(xml_escape_attr "${cjk_regular}")"
  cjk_bold_xml="$(xml_escape_attr "${cjk_bold}")"
  mono_regular_xml="$(xml_escape_attr "${mono_regular}")"
  mono_bold_xml="$(xml_escape_attr "${mono_bold}")"
  mono_italic_xml="$(xml_escape_attr "${mono_italic}")"
  mono_bold_italic_xml="$(xml_escape_attr "${mono_bold_italic}")"

  cat > "${dst}" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<fop version="1.0">
  <strict-configuration>true</strict-configuration>
  <strict-validation>false</strict-validation>
  <renderers>
    <renderer mime="application/pdf">
      <fonts>
        <font kerning="yes" embed-url="${cjk_regular_xml}">
          <font-triplet name="${cjk_family_xml}" style="normal" weight="normal"/>
          <font-triplet name="${cjk_family_xml}" style="italic" weight="normal"/>
        </font>
        <font kerning="yes" embed-url="${cjk_bold_xml}">
          <font-triplet name="${cjk_family_xml}" style="normal" weight="bold"/>
          <font-triplet name="${cjk_family_xml}" style="italic" weight="bold"/>
        </font>
        <font kerning="yes" embed-url="${mono_regular_xml}">
          <font-triplet name="${mono_family_xml}" style="normal" weight="normal"/>
        </font>
        <font kerning="yes" embed-url="${mono_bold_xml}">
          <font-triplet name="${mono_family_xml}" style="normal" weight="bold"/>
        </font>
        <font kerning="yes" embed-url="${mono_italic_xml}">
          <font-triplet name="${mono_family_xml}" style="italic" weight="normal"/>
        </font>
        <font kerning="yes" embed-url="${mono_bold_italic_xml}">
          <font-triplet name="${mono_family_xml}" style="italic" weight="bold"/>
        </font>
      </fonts>
    </renderer>
  </renderers>
</fop>
EOF
}

ensure_fop

work_tree="$(mktemp -d "${REPO_ROOT}/.cache/work/standalone-pdf-${lang}-${version}.XXXXXX")"
trap '[[ "${keep_work}" == "1" ]] || rm -rf "${work_tree}"' EXIT

echo "Preparing build workspace: ${work_tree}"
if is_release_version "${version}"; then
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

rsync -a \
  --exclude='Makefile' \
  --exclude='.gitignore' \
  "${doc_src_root}/" "${work_tree}/doc/src/sgml/"

echo "Configuring source tree ..."
extra_configure_flags="${CONFIGURE_FLAGS:-}"
(cd "${work_tree}" && ./configure --without-icu --without-readline --without-zlib ${extra_configure_flags} >/dev/null)

if [[ "${lang}" != "en" ]]; then
  sed -i.bak \
    -e 's/--valid/--catalogs --loaddtd/g' \
    "${work_tree}/doc/src/sgml/Makefile"
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
    "${pdf_mono_bold_italic}"
fi

append_xsltproc_flag() {
  if [[ -n "${xslprocflags_extra}" ]]; then
    xslprocflags_extra+=" "
  fi
  xslprocflags_extra+="$1"
}

if [[ "${lang}" == "zh" ]]; then
  append_xsltproc_flag "--stringparam body.font.family '${pdf_cjk_family}'"
  append_xsltproc_flag "--stringparam sans.font.family '${pdf_cjk_family}'"
  append_xsltproc_flag "--stringparam title.font.family '${pdf_cjk_family}'"
  append_xsltproc_flag "--stringparam monospace.font.family '${pdf_mono_param}'"
fi

(cd "${work_tree}" && XSLTPROCFLAGS="${xslprocflags_extra}" "${MAKE_CMD}" -C doc/src/sgml DOC_LANG="${lang}" "postgres-${paper}.fo" >/dev/null)

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

if grep -q 'not available in font' "${fop_log}"; then
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
