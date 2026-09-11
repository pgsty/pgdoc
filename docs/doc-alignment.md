# 中英文整本书对齐检查

`bin/check_doc_alignment.py` 比较**固定版本英文与中文当前全文**。它不比较两个 Git 提交之间的改动，也不把构建成功视为翻译完整。输出目录必须是新目录，且不能位于输入目录内；检查器不修改正文、术语或构建源目录。

## 固定输入与运行

依赖 Python 3.14+（需要可设置实体展开上限的 Expat）、本机 DocBook XML catalog、`xmlcatalog`。生成输入另外需要 PostgreSQL 文档构建使用的 GNU Make、Perl、C 编译器及 configure 依赖。无 Python 第三方包依赖。检查本身不访问网络，也不会解析 `en/current` 或查询最新版本。

以下是 PG18.6 基线的实际输入示例；换版本时显式替换版本、英文目录、中文目录和源码包哈希。

```sh
python3 bin/prepare_doc_alignment.py \
  --archive /Users/vonng/pgsty/pgdoc/.cache/upstream/postgresql-18.6.tar.bz2 \
  --sha256 555610c24d53e4316da5b7d3fc25c279d96856d5e0e23ee308c328c5fa881d9f \
  --version 18.6 \
  --en /Users/vonng/pgsty/pgdoc/en/18.6 \
  --zh zh/18 \
  --out outputs/pg18-prepared

python3 bin/check_doc_alignment.py \
  --en /Users/vonng/pgsty/pgdoc/en/18.6 \
  --zh zh/18 \
  --version 18.6 \
  --prepared outputs/pg18-prepared \
  --out outputs/pg18-alignment
```

`prepare_doc_alignment.py` 复用 `prepare_pinned_doc_source.py` 验证源码包哈希及包内版本声明，并逐个核对给定英文 SGML 与包内同名文件。只在自己的输出目录解压和 configure。两种语言分别覆盖自己的生成器与输入，通过上游 `GENERATED_SGML` 目标实际重建生成文件。PG18 有七个生成输入：版本实体、SQL 功能支持/不支持表、错误码、关键字、Meson 目标、等待事件表。记录生成命令、日志、每个源文件和产物的 SHA-256。不会把源码包的正文作为中文缺文件的后备输入。

固定 Git 源码使用 `--source-dir /absolute/path/to/checkout --source-commit FULL_SHA`，替代 `--archive` / `--sha256`；两组不能混用，也不能缺少配对参数。准备器核验完整提交、跟踪文件状态、版本声明和英文输入；PG20 的版本参数是其 Makefile 使用的 `20`。所有准备步骤使用隔离的源码副本，保存来源身份及生成输入、输出哈希。

PG10 的原生 SGML 使用 `--native-sgml`。设置 `NSGMLS`、`OSX` 为 OpenSP 可执行文件路径，并设置 `SGML_CATALOG_FILES` 为该版本的 SGML catalog；中文还需 `SP_ENCODING=UTF-8 SP_CHARSET_FIXED=YES`。先对实际原文运行 OpenSP 验证，成功后按 PostgreSQL 10 的转换规则生成 XML；逐个匹配完整 ESIS 与 XML 元素流，将节点映射回原文件及行号。转换文件、原始 ESIS、诊断、命令、哈希和位置映射保存在 `native-en/` 与 `native-zh/`。

原生模式分别记录已暂存文件、实体声明和实际消费的文件。OpenSP 在文档元素之前输出的普通实体声明不代表该实体被使用；依赖以实际位置事件、展开的参数实体及文档实例中的实体使用事件为证据。空实体和仅含注释的实体也计入实际消费；未使用的声明保留在清单中，不能据此把文件标为已读。若参数/普通实体同名同目标而无法明确区分证据，检查明确失败。原生包含边上的行号是声明位置，实际使用证据另附 ESIS 行号。

第一次准备后，只要两侧输入哈希没有变化，可以重复使用 `--prepared`。准备清单与源目录或生成文件不符会返回 2。若目录本身已经包含全部生成输入，可省略 `--prepared`；此时哈希会记录，但检查器不能证明其上游版本，版本标签是调用者声明。

被忽略的 `pgdoccn-notes.sgml` 若在新 worktree 中缺失，应先从明确来源复制到自己的附加输入目录，并使用 `--zh-aux /absolute/path/to/auxiliary`。附加文件的实际路径和哈希会进入包含依赖清单。**不要用空占位文件自动代替缺失正文。** 本轮读取的已存在项目占位文件只有 `<!-- pgdoccn notes placeholder -->` 注释，SHA-256 为 `b981d191f97b8921e8d6cec88410805add9c62c01f3f6962ee8994247faed823`。

`--entry` 可指定其他整书入口；`--catalog` 可重复指定本机 XML catalog。默认查找 `/etc/xml/catalog`、Homebrew 的 `/opt/homebrew/etc/xml/catalog` 和 `/usr/local/etc/xml/catalog`。

## 检查层次

1. **文件和整书覆盖。** 递归清点源目录；从入口解析实际参数实体、外部实体和外部 DTD，区分实体声明与实际使用。给出包含边及其源行、每个文件的角色、孤立 SGML、生成文件、样式/构建/资产差异。注释不产生正文节点；CDATA 保留为文本。缺文件、未定义或跳过实体、解析失败均明确失败。默认支持项目实际使用的 XML 形式 DocBook；原生 SGML 必须显式使用 OpenSP 模式，XInclude 不会静默接受。
2. **数量、身份、归属与顺序。** 先输出每文件/标签/深度计数，再核对所有 `id`/`xml:id` 出现次数、重复值、所有标题容器、任意 `sectN`/`refsectN`、递归 `section`、显式 anchor 和内部引用。全局唯一 ID 支持跨文件定位，并检查父级、层级、文件移动及兄弟顺序。未带 ID 的列表项也参与结构树，避免中文增加列表锚点后把其正文误识别成新内容。
3. **配对后的 sanity check。** 所有配对标题保留中英文文本和位置，语义状态始终是 `not_automatically_verified`。表格核对行列数量、CALS 列/跨行位置、函数名及出现次数、签名/重载、`func_signature`、类型、参数和完整单元格事实值。段落、列表、代码块及内部引用差异提供进一步定位信号。

每个解析节点都记录源文件、行号与整书 XPath；实体展开不会丢失文件来源。生成文件使用 `@generated/` 前缀，真实绝对路径及哈希见 inventory 的 `dependencies`。`en/zh-nodes.jsonl` 包含全部节点，便于复核没有 ID 的节点。注释和 CDATA 使用解析事件统计，绝不使用去掉若干正则匹配后计数的方法。

## 配对、归一化和保留的歧义

- 优先用全局唯一 ID；没有唯一 ID 时使用已配对父节点下的唯一标题/术语/函数等稳定内容，以及已配对的前后邻居。中文额外 ID 不会使英文没有 ID 的同一类节点从结构树消失；额外 ID 本身仍报告。
- 命令参考页的常见标题允许显式同义配对：Description/描述，See Also/另见/参见/又见，Examples/Example/示例/例子，Compatibility/兼容性，Parameters/Arguments/参数，Notes/注解/注意/注释，Return Value/返回值，Options/选项，Environment/环境，Outputs/输出，Diagnostics/诊断，Exit Status/退出状态，Usage/用法/使用，Files/文件，How It Works/工作原理，Author/作者。只在同一已配对父节点下且候选唯一时使用；若 Parameters 和 Arguments 同时存在，不会强行合并。该词表仅用于建立关系，不验收正文含义。
- 同名函数的不同重载使用唯一类型/参数组合区分。无法唯一辨别的重载与无 ID 行均保留歧义；不会只因数量相同就按序号配对。单独一个表头行或一个无标识行，允许在对应行组中按唯一上下文配对，方法会写入证据。
- 标题、代码及签名仅折叠空白并移除排版零宽空格。ASCII 保护标签作为确定字面证据；包含中文的占位符和说明不被武断判成错误。缺函数定义标识符是确定差异；签名文字、类型/参数差异保留并排复核候选。
- Yes/No/yes/no/是/否只在**完整单元格**上归一化，且仅在对应行和列已配对后比较。不对任意中文段落作自动事实判断。
- CALS 列名和 span 名只是本表内部别名，比较其解析后的坐标；不要求宽度、对齐、语言等样式属性字节一致。`xref` 与 `link` 的相同 `linkend` 视为同一目标，原始标签仍保存在引用清单中。
- 不忽略 `func.sgml`，不忽略生成内容，不自动生成豁免。附加 ID、行序和跨文件嵌入等结构差异仍保留；人工报告可以说明它们的性质，但不能改变原始检查退出码。

## 结果与退出码

| 文件 | 内容 |
|---|---|
| `manifest.json` | 调用参数、Git 状态、版本、完整输入哈希、生成出处、规则哈希 |
| `en/zh-inventory.json` | 文件角色、实际包含图、实体声明、依赖位置与哈希、解析错误 |
| `counts.tsv`, `counts-diff.tsv` | 文件/标签/深度数量及差值 |
| `en/zh-nodes.jsonl`, `en/zh-references.json` | 所有节点、内部引用出现位置和目标 |
| `landmark-pairs.jsonl` | 全部结构节点配对、方法及两侧定位 |
| `findings.json`, `findings.tsv` | 每条差异的分类、优先级、两侧位置、原始证据 |
| `title-pairs.json/tsv`, `tables.json` | 标题、表格、函数定义、签名和逐行配对台账 |
| `files.tsv`, `assets.tsv` | 文件优先级清单、构建与样式资产盘点 |
| `coverage.json`, `REPORT.md` | 覆盖率、限制和完整机器生成报告 |

| 退出码 | 意义 |
|---:|---|
| 0 | 本次可检查的结构与确定标识符一致，且无结构配对歧义；**不是翻译语义验收** |
| 1 | 存在确定结构/标识符/事实值差异；可能同时有歧义和语义候选 |
| 2 | 输入不完整、版本/哈希不符、依赖或解析失败；不能给出完整对齐结论 |
| 3 | 无已确定差异，但尚有结构或表格配对歧义；不能给出完全对齐结论 |

`definite` 表示差异本身确定，并不表示每项都应删除或补译。比如中文额外的自动列表 ID 属于真实结构差异，通常只需要核实其用途。P1 优先检查缺项、错误归属、表形状和事实值；附加 ID、单纯行序及引用变化一般为 P2。数量不是独立缺陷数，父表和子行可能报告同一遗漏。

## 验证

```sh
python3 -m unittest discover -s tests -v
# 只对未经修复的 738d5de PG18 基线运行；修复之后不应继续要求缺陷存在。
python3 tests/assert_pg18_baseline.py outputs/pg18-alignment
```

合成测试覆盖相等数量下的 ID 替换、重复 ID、父级与顺序变化、无 ID 节点、包含链、缺文件、实体、注释、CDATA、列别名/跨度、正常翻译标题及退出码。基线集成断言要求实际发现 SQL/JSON 测试表缺失、聚合表 27/20 行与 11 个缺失函数名、三处部分模式事实值错配。

检查不运行全文机器翻译判卷，也不验证所有自然语言语义、默认值或代码逻辑。无 ID 多候选、未配对行、文本中的技术陈述仍需人工核查。此任务只新增审计工具，生成输入构建成功不等于 HTML/PDF 构建或发布成功。
