# 文档与 PDF 来源

本文件规定 `pgdoc` 的英文、中文 PDF 来源，以及交付给网站时的核验方式。处理文档取源、PDF 下载、构建或发布前先读这里；翻译规范见 [style.md](style.md)，排版验收见 [../ref/pdf-html.md](../ref/pdf-html.md)。

## 来源规则

每个版本、每种语言分别提供 **A4** 和 **US Letter** 两份 PDF；构建参数和文件名用 `A4`、`US`。

| 内容 | 来源与处理 | 产物身份 |
| --- | --- | --- |
| 上游已提供的英文 PDF | 直接下载 PostgreSQL 官方 A4、US 成品，逐字节保留 | 官方原件 |
| PostgreSQL 6.3–7.4 英文 PDF | 仅首次缺失时用同版本英文源码补建两种纸型，之后冻结复用 | 一次性构建的英文版 |
| 中文 PDF | 在本项目翻译、维护 `zh/<大版本>/`，再构建两种纸型 | 本项目构建的中文版 |
| 开发快照英文 PDF | 按 `en/SOURCES.json` 的固定英文快照构建两种纸型，随开发版更新 | 开发快照自建版 |

英文原件不翻译，不套中文字体或排版后处理，也不重新导出、压缩、加水印或改写元数据。文件名可以按站点约定映射，文件内容必须与下载的上游原件完全一致。用相同英文源码重新编译，并不能保证得到相同的 PDF。

6.3–7.4 是历史正式版本中的补建范围，共八个分支。开发快照另行处理：**2026-10-03 核对时，官方也未提供 20devel PDF**，不能将已有的自建开发版写成官方原件。以后上游开始提供成品时，重新核对来源。

## 官方英文成品

以官方页面实际列出的链接为准：

- [当前手册及测试版](https://www.postgresql.org/docs/)：核对时列出 14–18 和 19 beta 的 A4 / US PDF；Development snapshot 标为无 PDF。
- [历史手册归档](https://www.postgresql.org/docs/manuals/archive/)：核对时列出 8.0–13 的 A4 / US PDF；6.3–7.4 标为无 PDF。

已核对的链接形式如下，以 PostgreSQL 18 为例：

```text
https://www.postgresql.org/files/documentation/pdf/18/postgresql-18-A4.pdf
https://www.postgresql.org/files/documentation/pdf/18/postgresql-18-US.pdf
```

大版本 URL 可能随小版本或 beta 更新而改变内容，URL 本身不是固定版本凭据。每次取源应保存下载日期、原始 URL、最终 URL、PDF 中的实际版本、纸型、字节数与 SHA-256；不要把大版本相同当作小版本或开发修订相同。

下载后检查文件确实可解析为 PDF，核对封面版本和纸张尺寸，并记录 SHA-256。发布时比较“官方原件 → 本地待发布文件 → 网站完整下载文件”的哈希。上游未发布校验和时，应注明哈希是本地对官方下载文件计算的；不能声称它是官方签名或官方校验清单。

入口统一使用 [prepare_english_pdf.py](../bin/prepare_english_pdf.py)，由 [Makefile](../Makefile) 调用：

```bash
# 下载当前 PostgreSQL 18 官方 PDF；同时提供两种纸型
make en-pdf-all EN_VERSIONS=18

# 只处理一个版本、一个纸型
make en-pdf EN_VERSION=18 PAPER=A4

# 检查上游更新；未指定时复用已核实的下载
make en-pdf-all EN_VERSIONS=18 EN_PDF_FLAGS=--refresh

# 只查看分流、来源和输出路径，不写文件
make en-pdf EN_VERSION=18 EN_PDF_FLAGS=--dry-run
```

`en-pdf-all` 的默认范围仍为 14.24、15.19、16.15、17.11、18.6，可用 `EN_VERSIONS` 指定其他版本。完整版本号会校验 PDF 中的版本必须一致；若官方大版本 URL 的成品版本不同，应核对后改用实际版本号，或使用 `EN_VERSION=18` 这样的分支号。分支号下载仍会记录实际 PDF 版本，不能用它掩盖与站内 HTML 基线的差异。

版本优先读取 PDF 元数据，没有时从封面读取；需要 Poppler 的 `pdfinfo` 和 `pdftotext`。旧版 pdfTeX 的 A4 尺寸允许 4 pt 内的历史偏差，实际尺寸照实记录，不重新排版。例如 2026-10-03 下载的官方 8.0 A4 是 **8.0.0**，尺寸为 **593.051 × 838.744 pt**，不能把它记作本地英文源码的 8.0.26。

官方下载失败、文件无法解析、纸型不符或完整版本不匹配时退出，保留旧文件，不自动改成本地重建。新产物先在临时目录下载或构建并检查，再替换目标；已有文件及来源记录先保存到 `tmp/pdf/en/history/<文件名>/<旧 SHA-256>/`。

## 6.3–7.4 英文补建

英文源码位于 `en/<完整版本>/`，原始归档、URL 和校验值记录在 `en/SOURCES.json`。当前对应关系为：

| 分支 | 英文源码版本 |
| --- | --- |
| 6.3 | 6.3.2 |
| 6.4 | 6.4.2 |
| 6.5 | 6.5.3 |
| 7.0 | 7.0.3 |
| 7.1 | 7.1.3 |
| 7.2 | 7.2.8 |
| 7.3 | 7.3.21 |
| 7.4 | 7.4.30 |

古早版本一次性构建，之后不随排版工具或其他版本更新而重编。在仓库根目录执行：

```bash
# 八个分支，默认各 A4 / US；已有文件就冻结复用
make en-pdf-legacy

# 单独处理一个古早版本
make en-pdf EN_VERSION=7.4 PAPER=A4
```

- 已有 PDF、尚无来源记录：检查 PDF 和纸型，记录当前哈希并冻结；不改动 PDF 字节与修改时间，来源标为 `existing-local`，不推测旧构建时的源码哈希。
- PDF 与来源记录都不存在：从 `en/SOURCES.json` 读取固定归档、SHA-256 和英文目录，调用 [独立 PDF 构建脚本](../bin/build_standalone_pdfsrc.sh) 的 `en` 分支，首次构建成功后冻结。
- 已有冻结记录：只校验哈希并复用。即使传入 `--refresh` 也不重建；文件缺失或哈希不一致时应恢复原件，不自动生成另一个版本。

记录位于 PDF 同目录的 `*.source.json`，`mode` 为 `legacy-once`。迁移或备份必须同时保留 PDF 和记录。`make clean-pdf` 及 `clean-all` 的 PDF 清理只移除中文构建产物，保留整个英文目录；不要按 `tmp/` 目录名把冻结成品当作可随意删除的缓存。

脚本在 `.cache/work/` 中准备独立工作区，经 SGML/XML、DocBook XSL、XSL-FO 和 Apache FOP 生成 PDF。旧版兼容调整仅作用于构建副本；可借用同版 `zh/` 下的排版样式并将本地化切回英文，正文仍来自英文源码。正常维护使用上述统一入口，不直接调用低层脚本绕过冻结规则，也不依赖 `en/<版本>/` 中保留的上游 Makefile。

## devel 英文构建

```bash
# 构建当前固定开发快照的 A4 / US
make en-pdf-devel

# 检查固定输入；此命令不会取 moving master 或生成 PDF
make en-pdf-devel EN_PDF_FLAGS=--dry-run
```

`EN_DEVEL_VERSION` 当前默认 `20devel`。每次执行构建时从 `en/SOURCES.json` 读取该版本的 `archive`、`archive_sha256` 和 `doc_dir`，显式传给独立构建脚本；不会继承外部环境中另一套 Git / 归档输入。固定输入缺失时退出，不回退到移动分支。

每次显式调用都会重新构建所选纸型，来源记录的 `mode` 为 `devel`。更新开发快照时先同步英文源码及清单，再按中文更新流程同步 `zh/20/Makefile` 和译文。英文 PDF 配置本身不更新源码、不运行定时任务，也不发布到网站。

## 中文 PDF

中文正文的权威来源是本仓库的 `zh/<大版本>/`，翻译依据对应版本的 `en/<完整版本>/`。中文 PDF 必须从中文源文档生成，不能用英文 PDF 改语言标签代替。

在仓库根目录执行，例如：

```bash
# 采用该目录 Makefile 指定的英文基线
make -C zh/18 pdf PAPER=A4
make -C zh/18 pdf PAPER=US

# 显式指定批量范围和两种纸型
make zh-pdf-all ZH_VERSIONS="17 18" PAPERS="A4 US"
```

默认产物为 `tmp/pdf/zh/postgresql-<大版本>-zh-A4.pdf` 和 `...-US.pdf`。顶层批量构建默认只覆盖 14–18；需要其他版本时必须显式指定范围。开发版使用 `zh/20/Makefile` 与 `en/SOURCES.json` 中核对一致的固定输入，不追随变化中的 master。

中文构建使用同一个独立 PDF 脚本的 `zh` 分支，以及中文字体和 [中文 FO 后处理](../bin/prepare_chinese_pdf.py)。字体、SGML/DocBook 工具与固定源码准备方式以脚本和各版本 Makefile 为准。`make check-deps` 只检查部分依赖，不能代替实际构建。

本项目构建的 PDF 按 [PDF / HTML 验收](../ref/pdf-html.md) 检查实际产物：两种纸型都要构建，保留完整 `*.fop.log`，核对版本、页数、书签、文字提取、字体和缺图，并渲染抽查封面、表格、代码、跨页与页脚。构建成功不等于排版验收通过。

## 目录、清单与网站交付

- `docs/`：项目维护说明、译风与术语规则；本文件负责来源规则。
- `ref/`：可复用的任务和验收流程。
- `en/`、`en/SOURCES.json`、`.cache/upstream/`：英文基线与固定源码归档；来源清单描述源码，不能直接当作 PDF 的官方下载凭据。
- `zh/`：中文源文件；`tmp/pdf/en/`、`tmp/pdf/zh/`：现有本地构建产物位置。
- 英文统一入口将来源写入同目录的 `*.source.json`：语言、请求版本、PDF 实际版本（若可提取）及其提取位置、纸型、页数、字节数、SHA-256 和记录时间。官方下载另记录原始与最终 URL，新构建记录固定归档与英文目录。中文沿用本次构建 / 发布清单，保留译文状态、固定来源、日志和产物哈希。

PG.CENTER（`~/pgsty/pg.center`）的英文下载与 PGSQL.CC（`~/pgsty/pgweb`）的中文下载分别维护。两站可使用相同的 URL 形式 `/files/documentation/pdf/<大版本>/postgresql-<大版本>-<A4|US>.pdf`，所以文件名本身不能证明语言。分发时按语言映射，保留已有两种语言的有效下载入口。

站点导入、下载清单、文件复制和公开访问验证在对应网站项目进行。PG.CENTER 的现有清单是 `data/manuals/english.json`；其中的旧 `built_at`、`source_mode` 或源码 URL 不能被解释为 PDF 的官方下载证据。先备份、传输和校验文件，再同步清单；是否公开交付以完整下载和哈希核对为准。

## 2026-10-03 本地核对与待校准项

- 配置前 `tmp/pdf/en/` 和 `tmp/pdf/zh/` 各已有 62 份 PDF（31 个版本各两种纸型）。其中 6.3–7.4 的 16 份英文 PDF 已检查纸型、记录哈希并冻结；连续执行两次确认 PDF 字节、修改时间和重复执行后的来源记录均未改变。此项不代表重新完成整书排版验收或网站发布。
- PG.CENTER 的 `docs/english-manual-import.md` 记载此前重建了全部 31 版英文 PDF，`data/manuals/english.json` 也保留了相应构建记录。这是历史实施情况；以后应按本文件对有官方成品的版本改用原件。
- 对 8.0–19 已有官方成品的 22 个分支，共 44 份英文 PDF，后续校准应重新下载官方原件、核对实际版本与哈希，再按网站流程替换需要更新的文件和清单。不能仅修改来源标签；本次未对现有站点文件完成这项替换与验收。
- 20devel 的本地源码清单和 `zh/20/Makefile` 已固定开发快照；已有中英文 PDF 保留各自构建身份。这里不把开发版自建归入“官方下载”。

配置已落到 Makefile 与英文 PDF 分流脚本；现有古早文件已冻结，网站文件与生产环境未改动。每次实际取源或发布都应重新检查上游及本地状态。
