<div align="center">

# PostgreSQL 中文文档

**读懂 PostgreSQL，从文档原典开始。**

覆盖 PostgreSQL 10–20 的简体中文手册 · 对照上游原文 · 跨版本一致翻译

[![官方网站](https://img.shields.io/badge/官方网站-pgsql.cc%2Fdocs-336791?style=flat-square)](https://pgsql.cc/docs/) [![版本范围](https://img.shields.io/badge/PostgreSQL-10–20-4169E1?style=flat-square)](#版本导航) [![阅读格式](https://img.shields.io/badge/阅读格式-HTML%20%2F%20PDF-2F855A?style=flat-square)](https://pgsql.cc/docs/)

[**开始阅读 →**](https://pgsql.cc/docs/current/index.html) · [版本导航](#版本导航) · [翻译方法](#翻译方法) · [参与贡献](#参与贡献)

</div>

---

**[pgsql.cc/docs](https://pgsql.cc/docs/) 是本翻译项目的官方网站**，提供多版本中文手册在线阅读、文档检索，以及 A4 / US Letter 两种纸型的 PDF 下载。本仓库维护对应的中文 SGML 源文件、术语规范与构建工具。

项目由 [冯若航](https://vonng.com/)与 [Pigsty](https://pigsty.io/) 项目组维护，致力于让中文读者能够直接、准确地使用 PostgreSQL 的完整参考手册。配套网站 [PostgreSQL 中文网（pgsql.cc）](https://pgsql.cc/) 的源码见 [pgsty/pgweb](https://github.com/pgsty/pgweb)，涵盖中文网站内容。



## 内容范围

翻译以对应版本的 [PostgreSQL 上游文档](https://www.postgresql.org/docs/)为准，沿用原书的章节组织、覆盖从入门到数据库内部实现的主要内容。

| 面向读者 | 手册内容 |
| :--- | :--- |
| **应用开发者** | 入门教程、SQL 语言、数据类型、函数与运算符、索引、事务、性能优化、客户端接口 |
| **数据库管理员** | 安装部署、配置、身份认证、日常维护、备份恢复、高可用、流复制、逻辑复制、监控 |
| **扩展与内核开发者** | 系统目录、系统视图、前后端协议、存储结构、扩展接口、数据库内部实现 |
| **所有使用者** | SQL 命令参考、客户端与服务器工具、错误码、SQL 标准兼容性、版本发行说明 |

## 版本导航

阅读时请选用与你的数据库大版本一致的手册；网站上的“当前版本”入口会随正式版本更新。

| PostgreSQL | 译文基线 | 在线阅读 | 离线下载 |
| :--- | :--- | :--- | :--- |
| **18** | 18.6 | [中文手册](https://pgsql.cc/docs/18/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/18/postgresql-18-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/18/postgresql-18-US.pdf) |
| **17** | 17.11 | [中文手册](https://pgsql.cc/docs/17/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/17/postgresql-17-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/17/postgresql-17-US.pdf) |
| **16** | 16.15 | [中文手册](https://pgsql.cc/docs/16/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/16/postgresql-16-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/16/postgresql-16-US.pdf) |
| **15** | 15.19 | [中文手册](https://pgsql.cc/docs/15/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/15/postgresql-15-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/15/postgresql-15-US.pdf) |
| **14** | 14.24 | [中文手册](https://pgsql.cc/docs/14/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/14/postgresql-14-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/14/postgresql-14-US.pdf) |
| **19 · 测试版** | 19beta4 | [中文手册](https://pgsql.cc/docs/19/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/19/postgresql-19-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/19/postgresql-19-US.pdf) |
| **20 · 开发版** | 20devel | [开发快照](https://pgsql.cc/docs/devel/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/20/postgresql-20-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/20/postgresql-20-US.pdf) |

<details>
<summary><strong>历史版本：PostgreSQL 10–13</strong></summary>

这些版本的手册用于维护旧系统和查阅历史行为，统一收录于[旧版手册归档](https://pgsql.cc/docs/manuals/archive/)。

| PostgreSQL | 译文基线 | 在线阅读 | 离线下载 |
| :--- | :--- | :--- | :--- |
| **13** | 13.23 | [中文手册](https://pgsql.cc/docs/13/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/13/postgresql-13-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/13/postgresql-13-US.pdf) |
| **12** | 12.22 | [中文手册](https://pgsql.cc/docs/12/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/12/postgresql-12-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/12/postgresql-12-US.pdf) |
| **11** | 11.22 | [中文手册](https://pgsql.cc/docs/11/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/11/postgresql-11-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/11/postgresql-11-US.pdf) |
| **10** | 10.23 | [中文手册](https://pgsql.cc/docs/10/index.html) | [A4](https://pgsql.cc/files/documentation/pdf/10/postgresql-10-A4.pdf) · [US](https://pgsql.cc/files/documentation/pdf/10/postgresql-10-US.pdf) |

</details>

## 翻译方法

**准确 > 一致 > 流畅 > 本土化润色。**

1. **以上游为准。** 每个中文版本对应自己的英文版本，保留原文的定义、约束、例外和技术事实。开发版应固定源码提交，避免把不断变化的上游分支当作同一份输入。
2. **按差异更新。** 小版本更新先比较英文差异，只修改受影响的内容；跨大版本迁移先处理文件增删与结构变化，再处理文件内部差异。
3. **同文同译。** 相同英文在适用版本中复用同一译文；各版本独有的参数、默认值、接口、结构与链接分别保留。
4. **术语统一。** 优先遵循[不翻译词表](tmp/ref/exclude.tsv)，再查[术语表](tmp/ref/glossary.tsv)和[逐条使用规则](tmp/ref/glossary.rules.tsv)，并按[译风规范](tmp/ref/style.md)组织中文。SQL、标识符、命令、代码和 SGML 标签保持原样，随上游变化同步必要调整。
5. **检查并构建。** 翻译完成后核对差异、术语、结构与链接，按交付范围实际构建 HTML 和两种纸型的 PDF，并抽查页面、表格、代码和中文字体。

## 仓库结构

```text
pgdoc/
├── zh/                   # PostgreSQL 10–20 中文源文档，按大版本维护
│   ├── 18/               # 每版包含 SGML、样式、图示与独立 Makefile
│   └── current -> 18     # 当前正式版的本地入口
├── bin/                  # HTML / PDF 构建与固定上游源码校验工具
├── tmp/ref/              # 纳入版本管理的译风、术语与翻译规则
├── Makefile              # 单版本构建、批量 PDF 与本地预览入口
└── README.md
```

英文对照位于本地 `en/<版本>/`。下载缓存、生成的 HTML / PDF、临时工作区、执行计划和审计输出由 `.gitignore` 排除；`tmp/ref/` 中的共享翻译规则随仓库维护。

## 本地构建

以 PostgreSQL 18 为例，在仓库根目录执行：

```bash
# 检查依赖
make check-deps

# 构建中文 HTML，输出到 zh/18/html/
make zh VERSION=18.6

# 构建 A4 / US Letter PDF，输出到 tmp/pdf/zh/
make zh-pdf VERSION=18.6 PAPER=A4
make zh-pdf VERSION=18.6 PAPER=US

# 构建并预览：http://127.0.0.1:8000/
make serve-zh VERSION=18.6 HOST=127.0.0.1
```

构建工具会准备 PostgreSQL 上游源码，将中文源文件叠加到独立工作区，再沿用上游的 DocBook 构建流程。需要 GNU Make、Python 3、C 编译器、`xmllint`、`xsltproc`、`rsync` 及 DocBook DTD / XSL；PDF 另需 Java、Fontconfig 和中文字体，脚本可自动下载 Apache FOP。完整依赖与可选参数见 [HTML 构建脚本](bin/build_standalone_docsrc.sh)和 [PDF 构建脚本](bin/build_standalone_pdfsrc.sh)。

<details>
<summary><strong>其他版本、批量构建与固定源码</strong></summary>

```bash
# 指定中文大版本，使用该目录 Makefile 中的上游版本
make -C zh/17 html
make -C zh/19 pdf PAPER=A4

# 批量构建 PostgreSQL 14–18 的 A4 / US Letter PDF
make zh-pdf-all

# 指定批量构建范围和纸型
make zh-pdf-all ZH_VERSIONS="17 18" PAPERS="A4 US"
```

- 默认批量范围是 PostgreSQL 14–18，可通过 `ZH_VERSIONS` 指定；`VERSION` 是英文版本号，`ZH_VERSION` 是中文大版本目录。
- 固定上游源码时，同时提供 `PGDOC_SOURCE_DIR` 与 `PGDOC_SOURCE_COMMIT`，或同时提供 `PGDOC_SOURCE_ARCHIVE` 与 `PGDOC_SOURCE_SHA256`。脚本会检查对应提交或归档校验和。
- PostgreSQL 10–13 默认使用各版 Makefile 指定的已校验归档包，首次构建需准备相应文件，或覆盖 `PGDOC_SOURCE_ARCHIVE` 路径。PostgreSQL 10 还需要 OpenSP、DocBook SGML 4.2 和 SGML catalog，相关路径见 [PG10 构建入口](zh/10/Makefile)。
- PostgreSQL 20 的译文基线固定于上游提交 [`86f7c82cf1023e3599f40f939727791a7090cd44`](https://github.com/postgres/postgres/commit/86f7c82cf1023e3599f40f939727791a7090cd44)。复现时通过 `PGDOC_SOURCE_DIR` 指向该提交的完整源码，并设置 `PGDOC_SOURCE_COMMIT`；开发分支的后续内容可能已变化。
- PDF 默认使用阿里巴巴普惠体 3.0 和 Courier New，可通过 `PDF_CJK_FAMILY`、`PDF_MONO_FAMILY` 或对应字体文件变量指定本机字体。

`make check-deps` 只检查部分可执行程序是否存在；完整验证应以实际 HTML / PDF 构建和页面检查为准。

</details>

## 参与贡献

欢迎通过 [Issue](https://github.com/pgsty/pgdoc/issues) 反馈错译、漏译、术语、链接或排版问题，也欢迎直接提交 [Pull Request](https://github.com/pgsty/pgdoc/pulls)。反馈时请附上**文档版本、页面链接、英文原文和建议译文**，便于核对与同步修正。

修改前请阅读[译风规范](tmp/ref/style.md)。提交时保留现有格式、SGML 结构、代码和标识符；同一问题涉及多个版本时，对照各版英文确认适用范围。新增或调整术语时同步更新词表和[变更记录](tmp/ref/change.md)。

## 致谢与版权

感谢 **PostgreSQL Global Development Group** 与历代文档贡献者编写和维护上游手册，也感谢参与中文翻译、校对和问题反馈的社区成员。上游文档的版权与许可声明保留于各版本的 `legal.sgml`，例如 [PostgreSQL 18 版权声明](zh/18/legal.sgml)。中文翻译与维护：[冯若航](https://vonng.com/) · [Pigsty 项目组](https://pigsty.io/)。

---

<div align="center">

**[在 pgsql.cc 阅读 PostgreSQL 中文文档 →](https://pgsql.cc/docs/)**

</div>
