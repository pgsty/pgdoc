# PostgreSQL 19.0 文档更新

PostgreSQL 19 于 **2026-11-19** [正式发布](https://www.postgresql.org/about/news/postgresql-19-released-3449/)。本次将中英文文档从 19rc2 更新至 19.0：英文源码位于 `en/19.0/`，官方 HTML 位于 `en/19.0/html/`，中文源文件在 `zh/19/` 原目录增量同步。`en/current` 指向 `19.0`，`zh/current` 指向 `19`。旧版 `en/19rc2/` 保留作增量对照。

## 固定来源

| 内容 | 官方下载 | 本地路径 | 字节数 |
| --- | --- | --- | ---: |
| 完整源码包 | [postgresql-19.0.tar.bz2](https://ftp.postgresql.org/pub/source/v19.0/postgresql-19.0.tar.bz2) | `.cache/upstream/postgresql-19.0.tar.bz2` | 23,982,241 |
| HTML / man 文档包 | [postgresql-19.0-docs.tar.gz](https://ftp.postgresql.org/pub/source/v19.0/postgresql-19.0-docs.tar.gz) | `.cache/upstream/postgresql-19.0-docs.tar.gz` | 3,959,772 |

源码包 SHA-256 与[官方校验文件](https://ftp.postgresql.org/pub/source/v19.0/postgresql-19.0.tar.bz2.sha256)一致：

```text
a89fd70efbad6a08c7dbed8d4872e3af30170d9e5ca9dc7906523be95b4e692d
```

文档包 SHA-256 为本地对官方下载文件计算；官方目录未列出该包的独立校验文件：

```text
e0a4d43e73a3179bb69acd1d17f74cecf93703ad8796868a019ba8e0d400db0e
```

`configure.ac`、`configure`、`meson.build` 均声明 19.0，`release-19.sgml` 的正式发布日期为 2026-11-19。源码清单登记在 `en/SOURCES.json`；归档、英文源码、HTML 和检查输出均位于 Git 忽略目录。

## 导入与差异

- 478 个源文件（其中 427 个 SGML），共 12,755,796 字节，逐文件与已校验源码包比较，缺失和字节差异均为零。
- 官方文档包中的 HTML 子树原样导入：1,161 个文件，其中 1,155 页 HTML，共 17,415,896 字节。首页声明 `PostgreSQL 19.0 Documentation`，发行说明日期为 2026-11-19。
- 已解析全部 1,155 页 HTML，检查 32,699 个内部引用，未发现缺失文件或锚点。页头 `link rev="made"` 中的 1,155 个作者邮件元数据按用途单列，不作为本地文件引用。
- RC2 与正式版完整源树比较涉及 6 个文件、75 个原始差异块。文件为 `bgworker.sgml`、`file-fdw.sgml`、`plpython.sgml`、`pltcl.sgml`、`ref/pg_combinebackup.sgml`、`release-19.sgml`；发行说明包含大量折行与缩进调整，差异块数不等于语义变更数。
- 完整差异位于 `en/diff/19rc2-vs-19.0/`，包括 `changes-summary.tsv`、`hunks.tsv` 和逐文件 diff；校验清单位于 `outputs/en-19.0-20261119/`。

## 中文增量同步

按 `ref/minor-sync.md`、PG Translate 技能及本轮项目术语和译风规则完成六个文件的增量更新：

| 文件 | 同步内容 |
| --- | --- |
| `bgworker.sgml` | 修正终止信号主体，补充按退出码和 `bgw_restart_time` 重启或注销工作进程的说明。 |
| `file-fdw.sgml` | 补充 `ANALYZE` 从外部表采样行时不应用 `REJECT_LIMIT`。 |
| `plpython.sgml` | 明确 `SD` 的会话作用域、触发器函数按函数与关系分别保存实例；准确表述 `GD` 的 PL/Python 共享范围，并同步段落拆分。 |
| `pltcl.sgml` | 更新 Tcl 官方链接。 |
| `ref/pg_combinebackup.sgml` | 将同步目标改为输出目录，删除普通文件格式条件及不适用的 libpq 环境变量说明。 |
| `release-19.sgml` | 更新正式发布日期、补齐 10 位致谢者；保留现有中文排版及此前人工修订。 |

75 个原始差异块已全部登记处置：7 个正文／结构／链接块、1 个日期块、9 个致谢块、58 个纯排版块。纯排版块不改中文。代码块和既有 ID 均保持原样；无新增术语裁决。按忠实度、术语与字面保护、中文成文分别进行了三轮自检。

`zh/19/Makefile` 固定版本 19.0、上述源码归档及 SHA-256；顶层默认版本改为 19.0，中文批量范围扩至 14–19。英文 PDF 批次仍保留已核验的 14.25–18.7，19.0 官方 PDF 的版本检查状态见下节。

本轮隔离重建了 RC2 与 19.0 的七种生成 SGML 输入；中英文都只有 `version.sgml` 从 19rc2 改为 19.0，其余生成表一致。工作区快照、逐块处置、中文改动对照和校验日志分别保存在 `tmp/zh-19.0-20261119/` 与 `outputs/zh-19.0-20261119/`。

## 中文构建与验证

三项实际构建均以固定 19.0 源码归档运行，退出码均为 0：

| 命令 | 产物 | 页数 |
| --- | --- | ---: |
| `make -C zh/19 html` | `zh/19/html/` | 1,155 |
| `make -C zh/19 pdf PAPER=A4` | `tmp/pdf/zh/postgresql-19-zh-A4.pdf` | 3,046 |
| `make -C zh/19 pdf PAPER=US` | `tmp/pdf/zh/postgresql-19-zh-US.pdf` | 3,248 |

- HTML 全部页面已解析，检查 31,951 个内部链接、2,315 个资源引用及 8 份 CSS，错误为零。
- 两份 PDF 标题均为 `PostgreSQL 19.0 手册`，A4 为 595.275 × 841.889 pt，US 为 612 × 792 pt；各有 4,094 个有效书签。中文字体已嵌入，全文提取未出现替换字符，FOP 未报缺字、缺图、溢出或错误。
- 已渲染并检查 23 个 PDF 物理页，覆盖两种纸型的封面、目录、六个变更文件、致谢、表格、代码、跨页及索引。HTML 已检查六个变更页面的桌面显示，以及 390 px 窄屏的正文、代码和表格。窄屏页头导航沿用既有样式，仍会逐字折行；正文正常，代码和宽表格可局部横向滚动。
- 全书 SGML 解析均无错误。对齐器在 RC2 工作区基线和本次 19.0 均返回 1，各报告 3,088 项既有差异／候选（2,734 项确定差异、127 项配对歧义、227 项待审）。排除位置字段、上下文摘录并归一化版本号后逐项比较，新增和消失的发现均为零。此结果证明本次未新增检查器可识别的差异，不代表原有全书差异已解决。
- 两种纸型各有相同的四条 FOP 通用提示：Symbol 和 ZapfDingbats 粗体回退、缺少 `zh_cn` 断词模式、`span="inherit"` 未找到父值。完整日志保留于 PDF 同目录；本轮抽查未发现相应可见缺陷。开工时没有本地旧 PDF／FOP 日志可供产物比较。
- `git diff --check` 和全版中文假空格检查通过。六个文件以外的中文源文件、术语规则和构建工具保持开工状态；原有人工修订保留。

中文 PDF SHA-256：

```text
A4  9296268c9ae7e083d288ba7da3c4355608f9c9ad42f1a075ee0c4229765859e7
US  87b6371b142b784adb9f7b901fa40e4ffe7912c80447b36cbdaa089aea0d68b5
```

完整证据见 `outputs/zh-19.0-20261119/` 中的构建记录、`hunk-dispositions.tsv`、`source-review.json`、`generated-comparison.json`、`alignment-regression.json`、`html-check.json`、`pdf-check.json` 和页面截图；PDF 同目录另保留来源记录。

## 最终翻译审阅

2026-11-19 在本次修改范围内重新逐项对照 RC2、19.0 英文与开工前后中文，按忠实度、术语一致性、中文行文完成最终自检。结论：**六个文件的修改充分且必要，无需进一步改译，可以交付正式中文版**。这是对本次增量及必要上下文的审阅，不是全书重新审校；未使用独立审者。

| 文件 | 最终核对要点 |
| --- | --- |
| `bgworker.sgml` | 不再指定终止信号发送者；退出码与 `bgw_restart_time` 共同决定重新启动或注销，双标志要求保留。译法与本章后文一致。 |
| `file-fdw.sgml` | 仅在 `ANALYZE` 从外部表采样时不应用限制，统计信息仍来自有效行；没有扩大例外范围。 |
| `plpython.sgml` | 明确同一会话、每个函数，以及触发器函数对每个关系分别持有 `SD` 实例；`GD` 的共享范围限定为 PL/Python 函数。保留“关系”，未缩窄为“表”。 |
| `pltcl.sgml` | 仅替换 Tcl 官方链接，正文和产品名不变。 |
| `ref/pg_combinebackup.sgml` | 两种同步方法均针对输出目录，均删除普通格式条件；完整删除 libpq 段，保留 `PG_COLOR`、WAL、表空间及适用交叉引用。 |
| `release-19.sgml` | 日期与新增十位致谢者的拼写、重音字符、顺序逐项一致；撤销本次日期和姓名变更后，中文逐字节恢复开工状态。 |

重新比较 478 个英文源文件，确认仍只有这六个文件、75 个原始差异块；发行说明其余差异仅为空白排版。现行术语规则、代码块、标识符和既有 ID 均已复核，无新增术语裁决或未决译文问题。已核对全部中文构建输入的指纹、两份 PDF 的哈希与版本，并重新检查 HTML 链接、资源和代表页面；正文与构建输入没有变化，沿用本轮已验收的 HTML、A4/US PDF。最终审阅证据保存在 `outputs/zh-19.0-final-20261119/`。

## 官方 PDF 状态

2026-11-19 分别通过规定入口请求 A4 和 US PDF，两份均被版本检查拒绝：

```text
PDF is '19rc2', requested 19.0; use its actual version or major 19
```

官方文档页面已将 19 列为 Current，但下载文件尚未同步；A4 响应的 `Last-Modified` 仍为 `Thu, 12 Nov 2026 14:03:52 GMT`，带刷新缓存请求也相同。未将 RC2 改名为正式版、未回退到自行构建，未替换已有英文 PDF。此项不影响已核验的 19.0 源码与 HTML。

上游 PDF 更新后，按完整版本号重试并检查实际版本、纸型、哈希及同目录来源记录：

```bash
make en-pdf-all EN_VERSIONS=19.0 EN_PDF_FLAGS=--refresh
```

通过后输出为 `tmp/pdf/en/postgresql-19.0-en-A4.pdf`、`postgresql-19.0-en-US.pdf` 及各自的 `.source.json`。当前默认英文 PDF 批次仍为 14.25–18.7。

## 复现取源

在尚未导入 `en/19.0/` 的工作区执行；已有目录先核对本地差异，不使用 `--force` 覆盖：

```bash
python3 bin/fetch_en_docs.py 19.0 \
  --sha256 a89fd70efbad6a08c7dbed8d4872e3af30170d9e5ca9dc7906523be95b4e692d \
  --register
```

英文 HTML 使用上述官方文档包的 `postgresql-19.0/doc/src/sgml/html/` 子树，逐字节展开至 `en/19.0/html/`，随后检查首页版本、发行日期、内部链接和资源。网站发布在对应网站仓库另行执行，本次更新本地中英文文档。
