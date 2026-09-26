# zh/6.5/Makefile

REPO_ROOT := $(abspath $(CURDIR)/../..)
DOC_VERSION := $(notdir $(CURDIR))
PG_VERSION ?= 6.5.3
# Official 6.5.3 release package, checksum pinned from en/SOURCES.json.
PGDOC_SOURCE_ARCHIVE ?= $(REPO_ROOT)/.cache/upstream/postgresql-6.5.3.tar.gz
PGDOC_SOURCE_SHA256 ?= bac04371c49ef4c81d505b827c054cf8327c30b44a8d0bb39e0d4964c4e6ac8f
export PGDOC_SOURCE_ARCHIVE PGDOC_SOURCE_SHA256
# Legacy PG configure predates strict-C99 compilers; keep its implicit-decl probes as warnings.
export CFLAGS := -Wno-error=implicit-int -Wno-error=implicit-function-declaration -Wno-error=int-conversion
# PG 6.x uses DocBook SGML V3.0 (Davenport); the shared deps only carry 4.2,
# so the pg6x overlay catalog supplies the V3.0 DTD on top of the shared one.
PGDOC_SGML_DEPS := $(REPO_ROOT)/deps/sgml
OSX ?= osx
NSGMLS ?= onsgmls
SGML_CATALOG_FILES ?= $(PGDOC_SGML_DEPS)/sgml-unicode.catalog
SP_ENCODING ?= UTF-8
SP_CHARSET_FIXED ?= YES
export OSX NSGMLS SGML_CATALOG_FILES SP_ENCODING SP_CHARSET_FIXED
DOC_LANG := $(notdir $(abspath $(CURDIR)/..))

BUILD_SCRIPT := $(REPO_ROOT)/bin/build_standalone_docsrc.sh
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
