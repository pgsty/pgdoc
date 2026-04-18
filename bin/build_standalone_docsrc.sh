#!/usr/bin/env bash
#
# Build PostgreSQL HTML documentation from a standalone doc source directory.
#
# Usage: build_standalone_docsrc.sh <doc-src-dir> <en|zh> <version> [output-dir]
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

  rm -rf "${cache_dir}"

  echo "Cloning PostgreSQL ${ver} source from ${ref} ..." >&2
  if ! git clone --depth 1 --branch "${ref}" "${official_git_url}" "${cache_dir}"; then
    rm -rf "${cache_dir}"
    echo "Official PostgreSQL git mirror clone failed, falling back to GitHub mirror ..." >&2
    git clone --depth 1 --branch "${ref}" "${fallback_git_url}" "${cache_dir}"
  fi

  local current_hash
  current_hash="$(git -C "${cache_dir}" rev-parse HEAD)"
  if [[ "${current_hash}" != "${expected_hash}" ]]; then
    echo "Cloned git checkout does not match official ${ref} head." >&2
    echo "  expected: ${expected_hash}" >&2
    echo "  actual:   ${current_hash}" >&2
    exit 1
  fi

  printf '%s\n' "${cache_dir}"
}

# --- Prepare work tree ---
work_tree="$(mktemp -d "${REPO_ROOT}/.cache/work/standalone-${lang}-${version}.XXXXXX")"
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

# Overlay our SGML/XSL/CSS sources into the extracted source tree.
# Exclude our project Makefile and .gitignore — the upstream Makefile.in
# (which ./configure will turn into a proper Makefile) must be preserved.
rsync -a \
  --exclude='Makefile' \
  --exclude='.gitignore' \
  "${doc_src_root}/" "${work_tree}/doc/src/sgml/"

# --- Configure (minimal, just enough for docs) ---
echo "Configuring source tree ..."
extra_configure_flags="${CONFIGURE_FLAGS:-}"
(cd "${work_tree}" && ./configure --without-icu --without-readline --without-zlib ${extra_configure_flags} >/dev/null)

# --- Relax XML validation for translated docs ---
# Chinese translations may reference anchors from newer PG versions,
# causing IDREF validation errors.  Keep DTD/entity loading enabled so
# standard DocBook entities still resolve, but skip strict validation.
if [[ "${lang}" != "en" ]]; then
  sed -i.bak \
    -e 's/--valid/--catalogs --loaddtd/g' \
    "${work_tree}/doc/src/sgml/Makefile"
fi

# --- Build HTML ---
echo "Building HTML docs (${lang} ${version}) ..."
(cd "${work_tree}" && "${MAKE_CMD}" -C doc/src/sgml DOC_LANG="${lang}" html)

# --- Copy output ---
mkdir -p "${build_out}"
rsync -a --delete "${work_tree}/doc/src/sgml/html/" "${build_out}/"

echo ""
echo "Build complete: ${build_out}"
echo "  $(find "${build_out}" -name '*.html' | wc -l | tr -d ' ') HTML files generated"
