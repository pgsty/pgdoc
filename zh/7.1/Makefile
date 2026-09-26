# zh/7.1/Makefile

REPO_ROOT := $(abspath $(CURDIR)/../..)
DOC_VERSION := $(notdir $(CURDIR))
PG_VERSION ?= 7.1.3
# Official 7.1.3 release package, checksum pinned from en/SOURCES.json.
PGDOC_SOURCE_ARCHIVE ?= $(REPO_ROOT)/.cache/upstream/postgresql-7.1.3.tar.gz
PGDOC_SOURCE_SHA256 ?= 6daa70b544441dc4237d9ad0605af1e82ec9c9f2342dd06240e33d99093a3332
export PGDOC_SOURCE_ARCHIVE PGDOC_SOURCE_SHA256
# Legacy PG configure predates strict-C99 compilers; keep its implicit-decl probes as warnings.
export CFLAGS := -Wno-error=implicit-int -Wno-error=implicit-function-declaration -Wno-error=int-conversion
# PG 7.x uses DocBook SGML V3.1 and OpenSP; its doc makefile defaults html to
# DSSSL/jade, so the 7x build script reroutes html to the XSL pipeline.
# Catalogs: shared DocBook 4.2/unicode deps + local DocBook 3.1 overlay
# (tmp/pg7x/deps; first SGMLDECL wins, so the shared unicode declaration
# applies and the overlay only adds the 3.1 DTD public-id mappings).
# 现代 clang 跑不通 7.x 的古董 configure；doc 构建只需 VERSION，走桩。
export PGDOC_SKIP_CONFIGURE := 1
PGDOC_SGML_DEPS := $(REPO_ROOT)/deps/sgml
OSX ?= osx
NSGMLS ?= onsgmls
SGML_CATALOG_FILES ?= $(PGDOC_SGML_DEPS)/sgml-unicode.catalog
SP_ENCODING ?= UTF-8
SP_CHARSET_FIXED ?= YES
export OSX NSGMLS SGML_CATALOG_FILES SP_ENCODING SP_CHARSET_FIXED
DOC_LANG := $(notdir $(abspath $(CURDIR)/..))

BUILD_SCRIPT := $(REPO_ROOT)/tmp/pg7x/build_standalone_docsrc_7x.sh
PDF_SCRIPT := $(REPO_ROOT)/bin/build_standalone_pdfsrc.sh
DEFAULT_BUILD_OUT := $(CURDIR)/html
BUILD_OUT ?= $(DEFAULT_BUILD_OUT)
PAPER ?= A4
PDF_OUT ?= $(REPO_ROOT)/tmp/pdf/$(DOC_LANG)/postgresql-$(DOC_VERSION)-$(DOC_LANG)-$(PAPER).pdf
PYTHON ?= python3
HOST ?= 127.0.0.1
PORT ?= 8000

# Files generated during build (not checked into repo)
GENERATED_FILES := version.sgml pgdoccn-notes.sgml postgres-full.xml

.PHONY: all html pdf clean clean-pdf distclean s serve check-deps show-config

all: html

html:
	@"$(BUILD_SCRIPT)" "$(CURDIR)" "$(DOC_LANG)" "$(PG_VERSION)" "$(BUILD_OUT)"

pdf:
	@"$(PDF_SCRIPT)" "$(CURDIR)" "$(DOC_LANG)" "$(PG_VERSION)" "$(PDF_OUT)" "$(PAPER)"

distclean: clean clean-pdf

s: serve
serve:
	@echo "Serving $(BUILD_OUT) at http://$(HOST):$(PORT)/"
	@cd "$(BUILD_OUT)" && "$(PYTHON)" -m http.server "$(PORT)" --bind "$(HOST)"

c: clean
clean:
	rm -rf "$(BUILD_OUT)"

clean-pdf:
	rm -f "$(PDF_OUT)"

check-deps:
	@echo "Checking build dependencies ..."
	@command -v xmllint  >/dev/null 2>&1 || { echo "MISSING: xmllint  (brew install libxml2)"; exit 1; }
	@command -v xsltproc >/dev/null 2>&1 || { echo "MISSING: xsltproc (brew install libxslt)"; exit 1; }
	@command -v rsync    >/dev/null 2>&1 || { echo "MISSING: rsync"; exit 1; }
	@command -v java     >/dev/null 2>&1 || { echo "MISSING: java"; exit 1; }
	@command -v fc-match >/dev/null 2>&1 || { echo "MISSING: fc-match (brew install fontconfig)"; exit 1; }
	@echo "All dependencies found."

show-config:
	@echo "doc_dir=$(CURDIR)"
	@echo "lang=$(DOC_LANG)"
	@echo "version=$(DOC_VERSION)"
	@echo "pg_version=$(PG_VERSION)"
	@echo "pgdoc_source_archive=$(PGDOC_SOURCE_ARCHIVE)"
	@echo "pgdoc_source_sha256=$(PGDOC_SOURCE_SHA256)"
	@echo "build_out=$(BUILD_OUT)"
	@echo "pdf_out=$(PDF_OUT)"
	@echo "paper=$(PAPER)"
	@echo "host=$(HOST)"
	@echo "port=$(PORT)"
