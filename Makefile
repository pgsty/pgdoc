# pgdoc top-level Makefile
# Batch build PostgreSQL documentation artifacts across tracked versions.

VERSION ?= 18.3
VERSIONS ?= 14.22 15.17 16.13 17.9 18.3
PAPER ?= A4
PAPERS ?= A4 US
PDF_OUT_ROOT ?= $(CURDIR)/tmp/pdf
PYTHON ?= python3
HOST ?= 0.0.0.0

EN_DIR := en/$(VERSION)
ZH_DIR := zh/$(VERSION)

.NOTPARALLEL: all pdf pdf-all zh-pdf-all en-pdf-all

.PHONY: all html en zh pdf pdf-all zh-pdf zh-pdf-all en-pdf en-pdf-all \
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
		PDF_OUT="$(PDF_OUT_ROOT)/zh/postgresql-$(VERSION)-zh-$(PAPER).pdf"

zh-pdf-all:
	@set -e; \
	for version in $(VERSIONS); do \
		for paper in $(PAPERS); do \
			$(MAKE) -C "zh/$$version" pdf PAPER="$$paper" \
				PDF_OUT="$(PDF_OUT_ROOT)/zh/postgresql-$$version-zh-$$paper.pdf"; \
		done; \
	done

en-pdf:
	$(MAKE) -C $(EN_DIR) pdf PAPER="$(PAPER)" \
		PDF_OUT="$(PDF_OUT_ROOT)/en/postgresql-$(VERSION)-en-$(PAPER).pdf"

en-pdf-all:
	@set -e; \
	for version in $(VERSIONS); do \
		for paper in $(PAPERS); do \
			$(MAKE) -C "en/$$version" pdf PAPER="$$paper" \
				PDF_OUT="$(PDF_OUT_ROOT)/en/postgresql-$$version-en-$$paper.pdf"; \
		done; \
	done

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
	rm -rf "$(PDF_OUT_ROOT)"

clean-all: clean clean-pdf

#----- dependency check -----
check-deps:
	$(MAKE) -C $(ZH_DIR) check-deps
