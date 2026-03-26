# pgdoc top-level Makefile
# Quick shortcuts for building & serving PG documentation

VERSION ?= 18.3
PYTHON  ?= python3
HOST    ?= 0.0.0.0

# Directories
EN_DIR := en/$(VERSION)
ZH_DIR := zh/$(VERSION)

.PHONY: all en zh clean clean-en clean-zh serve-en serve-zh se sz check-deps

#----- default: build both -----
all: en zh

#----- build -----
en:
	$(MAKE) -C $(EN_DIR) html

zh:
	$(MAKE) -C $(ZH_DIR) html

#----- serve (en on 8001, zh on 8000) -----
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

#----- dependency check -----
check-deps:
	$(MAKE) -C $(EN_DIR) check-deps
