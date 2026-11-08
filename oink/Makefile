# PostgreSQL 18 双语文档站（Oink / Hugo Extended）
#
# 常用目标：
#   make theme     获取/恢复 vendored 主题（github.com/pgsty/oink，固定 commit）
#   make gen       生成 6 张构建期 SGML 表（errcodes/keywords/wait-event/features/...）
#   make content   生成 Markdown 内容（en + zh 双语，依赖 gen）
#   make build     构建静态站点到 public/
#   make serve     本地预览（默认 14771 端口）
#   make check     残留标记/内部链接/双语对齐自动化检查
#   make all       gen + content + check + build

OINK_REPO   := https://github.com/pgsty/oink
OINK_COMMIT := ed30247e88f01ae89ef00709fe2e17e211b0a28a
HUGO        ?= hugo
PYTHON      ?= python3
PORT        ?= 14771

.PHONY: theme gen content build serve check clean all

all: gen content check build

theme:
	@test -d themes/oink || { \
	  echo "Fetching Oink theme $(OINK_COMMIT) ..."; \
	  rm -rf themes/.oink-tmp; mkdir -p themes; \
	  git clone --no-checkout $(OINK_REPO) themes/.oink-tmp && \
	  git -C themes/.oink-tmp checkout $(OINK_COMMIT) && \
	  rm -rf themes/.oink-tmp/.git themes/.oink-tmp/tests \
	         themes/.oink-tmp/images themes/.oink-tmp/bin && \
	  echo "$(OINK_COMMIT)" > themes/.oink-tmp/.oink-commit && \
	  mv themes/.oink-tmp themes/oink; }

gen:
	@test -d themes/oink || $(MAKE) theme
	@test -f tools/generated/wait_event_types.sgml || $(PYTHON) tools/fetch_pgsrc.py
	@bash tools/generate_tables.sh

content: gen
	$(PYTHON) tools/convert.py

build: content
	$(HUGO) --gc --minify --printPathWarnings

serve: content
	$(HUGO) server --bind 127.0.0.1 --port $(PORT)

check: content
	$(PYTHON) -m unittest discover -s tools -p 'test_*.py'
	$(PYTHON) tools/check_content.py

clean:
	rm -rf public resources .hugo_build.lock .hugo_cache
