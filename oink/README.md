# PostgreSQL 18 双语文档站（Oink）

`oink/` 是一个自包含的 Hugo 站点，把仓库内的 PostgreSQL 18 官方文档
（英文 `en/18.6`，中文 `zh/18`）转换为**中英双语、逐页对照**的 Oink 静态站点。

- 英文原版与中文翻译共用同一套 URL 与标题锚点，任意页面可通过右上角语言切换器互跳，
  深层锚点链接（`#guc-work-mem` 这类）在两种语言之间同样对齐。
- 全书 DocBook 结构完整保留：章节层级、表格（含编号 `Table 27.4`）、图、示例、
  告示（note/tip/warning → Oink callout）、变量列表（→ Oink fields）、步骤
  （→ `{.steps}`）、以及全部 `linkend` 交叉引用（转换为普通 Markdown 链接）。
- 每页 front matter 带上游署名（`upstream_link` 指向 postgresql.org 对应页）与
  索引词（`search_keywords`，来自 DocBook indexterm），中文页自动显示「译自英文」。

## 快速开始

```bash
cd oink
make serve        # http://127.0.0.1:14771  （首次会自动拉取主题与生成表）
```

依赖：Hugo Extended ≥ 0.168.0、Go 不需要（主题为 vendored 副本）、perl、python3 + lxml。

## 构建管线

| 步骤 | 命令 | 产物 |
| --- | --- | --- |
| 1. 主题 | `make theme` | `themes/oink/`（vendored Oink v1.4.0，commit 记录于 `.oink-commit`） |
| 2. 生成表 | `make gen` | `tools/generated/`（英文）与 `tools/generated-zh/`（经 zh/18 哈希钉子本地化） |
| 3. 转换 | `make content` → `tools/convert.py` | `content/docs/**.md` + `.zh.md`（792 页/语言）、`static/images/` |
| 4. 质检 | `make check` → `tools/check_content.py` | 残留标签 / 内部链接与锚点 / 双语对齐三项检查 |
| 5. 构建 | `make build` | `public/`（含全文搜索索引、打印视图、`llms.txt`） |

### 关于生成表（`make gen`）

PG 文档有 6 个 SGML 文件是构建期从源码生成的（错误代码表、SQL 关键字表、
wait event 表、SQL 特性表、meson 目标表）。冻结的 `en/18.6`/`zh/18` 树不带它们，
`tools/fetch_pgsrc.py` 会从官方 postgres git（REL_18_6）拉取生成器输入，
`tools/generate_tables.sh` 在本地重跑上游生成器；中文版经 `zh/18/localize-generated.py`
的**哈希钉子**逐字节校验后落地，保证与项目钉住的翻译完全一致。

### 页面拆分规则

- 一个 part 一个目录（`/docs/tutorial/` … `/docs/appendixes/`），顺序与编号同官方
  （Reference 为第 VI 部分，附录 A–N）。
- 一般章节一页；源文件超过 2500 行的大章（func/config/libpq/catalogs/protocol 等 23 章）
  按 sect1 拆成子页，与官方在线文档的分页方式一致。
- Reference：每个命令/程序一页（218 页，按官方分组顺序加权）。
- contrib 附录（附录 F）：每个附加模块一页（50 页）。

### 未纳入的内容（有意为之）

- 书后自动生成的总索引页（index.sgml 本就不在树内）：由站内全文搜索
  （含中文子串匹配）与每页 `search_keywords` 替代。
- `pgdoccn-notes`（zh 侧自动生成的翻译说明占位）：与站点读者无关。

## 目录内什么进 Git

`.gitignore` 排除：`themes/oink/`（18MB 第三方 vendored 主题，`make theme` 可恢复）、
`content/docs/` 与 `static/images/`（由 SGML 生成，`make content` 重建）、
`public/` 等构建产物、`tools/pgsrc|pgtree|generated*`（可再生的生成器输入与输出）。
入库的是：站点配置、落地页数据、转换/生成/质检脚本与本说明。
