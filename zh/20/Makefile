# zh/20/Makefile

REPO_ROOT := $(abspath $(CURDIR)/../..)
DOC_VERSION := $(notdir $(CURDIR))
PG_VERSION ?= 20
# Match the English baseline recorded in en/SOURCES.json (2026-09-11).
# Never silently replace this manual's generators with a moving master.
ifeq ($(strip $(PGDOC_SOURCE_DIR)$(PGDOC_SOURCE_COMMIT)),)
PGDOC_SOURCE_ARCHIVE ?= $(REPO_ROOT)/.cache/upstream/postgresql-20devel-97c64fe3d54d.tar.bz2
PGDOC_SOURCE_SHA256 ?= 97c64fe3d54d9cdf570c9dab054463881695c388e6b77ceab889709ba6f025cb
endif
export PGDOC_SOURCE_ARCHIVE PGDOC_SOURCE_SHA256
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
	@echo "build_out=$(BUILD_OUT)"
	@echo "pdf_out=$(PDF_OUT)"
	@echo "paper=$(PAPER)"
	@echo "host=$(HOST)"
	@echo "port=$(PORT)"
