# pgdoc top-level Makefile
# Batch build PostgreSQL documentation artifacts across tracked versions.

VERSION ?= 18.6
# Stable archives use X.Y while prereleases use XbetaN/XrcN; both map to zh/X.
ZH_VERSION ?= $(firstword $(subst beta, ,$(subst rc, ,$(basename $(VERSION)))))
EN_VERSION ?= $(VERSION)
ZH_VERSIONS ?= 14 15 16 17 18
EN_VERSIONS ?= 14.24 15.19 16.15 17.11 18.6
EN_LEGACY_VERSIONS := 6.3.2 6.4.2 6.5.3 7.0.3 7.1.3 7.2.8 7.3.21 7.4.30
EN_DEVEL_VERSION ?= 20devel
EN_PDF_FLAGS ?=
PAPER ?= A4
PAPERS ?= A4 US
PDF_OUT_ROOT ?= $(CURDIR)/tmp/pdf
PYTHON ?= python3
HOST ?= 0.0.0.0

EN_DIR := en/$(EN_VERSION)
ZH_DIR := zh/$(ZH_VERSION)

.NOTPARALLEL: all pdf pdf-all zh-pdf-all en-pdf-all en-pdf-legacy en-pdf-devel

.PHONY: all html en zh pdf pdf-all zh-pdf zh-pdf-all en-pdf en-pdf-all en-pdf-legacy en-pdf-devel \
	clean clean-en clean-zh clean-pdf clean-all \
	serve-en serve-zh es zs check-deps

#----- default: build all tracked Chinese PDFs (A4 + US) -----
all: zh-pdf-all

#----- HTML helpers (single version) -----
html: en zh

en:
	$(MAKE) -C $(EN_DIR) html

zh:
	$(MAKE) -C $(ZH_DIR) html

#----- PDF helpers -----
pdf: zh-pdf

pdf-all: zh-pdf-all

zh-pdf:
	$(MAKE) -C $(ZH_DIR) pdf PAPER="$(PAPER)" \
		PDF_OUT="$(PDF_OUT_ROOT)/zh/postgresql-$(ZH_VERSION)-zh-$(PAPER).pdf"

zh-pdf-all:
	@set -e; \
	for version in $(ZH_VERSIONS); do \
		for paper in $(PAPERS); do \
			$(MAKE) -C "zh/$$version" pdf PAPER="$$paper" \
				PDF_OUT="$(PDF_OUT_ROOT)/zh/postgresql-$$version-zh-$$paper.pdf"; \
		done; \
	done

en-pdf:
	$(PYTHON) bin/prepare_english_pdf.py --version "$(EN_VERSION)" --paper "$(PAPER)" \
		--output-root "$(PDF_OUT_ROOT)" $(EN_PDF_FLAGS)

en-pdf-all:
	@set -e; \
	for version in $(EN_VERSIONS); do \
		for paper in $(PAPERS); do \
			$(PYTHON) bin/prepare_english_pdf.py --version "$$version" --paper "$$paper" \
				--output-root "$(PDF_OUT_ROOT)" $(EN_PDF_FLAGS); \
		done; \
	done

# Existing legacy files are frozen in place; only first-time missing files build.
en-pdf-legacy:
	$(MAKE) en-pdf-all EN_VERSIONS="$(EN_LEGACY_VERSIONS)"

# Every devel invocation builds the source snapshot pinned in en/SOURCES.json.
en-pdf-devel:
	$(MAKE) en-pdf-all EN_VERSIONS="$(EN_DEVEL_VERSION)"

#----- serve (single version html; en on 8001, zh on 8000) -----
es: serve-en
serve-en: en
	@echo "Serving English docs at http://$(HOST):8001/"
	@cd "$(EN_DIR)/html" && $(PYTHON) -m http.server 8001 --bind $(HOST)

zs: serve-zh
serve-zh: zh
	@echo "Serving Chinese docs at http://$(HOST):8000/"
	@cd "$(ZH_DIR)/html" && $(PYTHON) -m http.server 8000 --bind $(HOST)

#----- clean -----
clean: clean-en clean-zh

clean-en:
	$(MAKE) -C $(EN_DIR) clean

clean-zh:
	$(MAKE) -C $(ZH_DIR) clean

clean-pdf:
	rm -rf "$(PDF_OUT_ROOT)/zh"
	@echo "English PDFs and provenance retained in $(PDF_OUT_ROOT)/en (includes frozen legacy files)."

clean-all: clean clean-pdf

#----- dependency check -----
check-deps:
	$(MAKE) -C $(ZH_DIR) check-deps
