# PG20 devel 增量翻译提示词

本目录提供 [可直接执行的两阶段总提示词](PROMPT.md)。最终目标是以当前 PG18 中文为底稿，通过固定英文 `18.6 → 20devel` 的完整差异形成 PG20 中文；本总提示词执行到准备完成并生成正式翻译提示词为止。

使用方式：把下面的短指令交给执行者。

```text
请完整读取并执行 /Users/vonng/pgsty/pgdoc/plans/pg20-from-18.6/PROMPT.md。
完成两个准备阶段：先固定 PG20 devel 源码，以 en/18.6 和当前 zh/18 为基线，创建 en/20 与中文继承底稿 zh/20，生成递归完整 diff 及结构迁移映射；再根据实测差异、历史译文和当前术语规则，生成本轮专用的 TRANSLATE-PG20.md、逐项任务表与执行计划。
本次交付到正式翻译提示词准备完毕，尚不执行新增或变化正文的翻译。
```

2026-09-09 准备提示词时核实了以下事实：

- 官方 devel 文档显示 PostgreSQL 20devel，官方源码 `configure.ac` 也声明 20devel。真正执行时仍须固定当时选定的完整源码提交；网页构建可能滞后于 Git HEAD。[官方开发文档](https://www.postgresql.org/docs/devel/index.html)、[官方源码版本声明](https://github.com/postgres/postgres/blob/master/configure.ac)
- 本地已有 `en/18.6/`、`zh/18/`；中文 Makefile 的 `PG_VERSION` 为 18.6。检查时尚无 `en/20/`、`zh/20/`。
- `en/current` 仍指向 18.3，因此提示词使用明确的 18.6 路径，不依赖 current 链接。
- 历史 PG19 工作流已经提供逐文件摘要、逐 hunk 清单和 `func.sgml` 拆分映射。对应旧报告指出，只扫顶层会漏掉 `ref/`、`func/` 等内容。本轮采用递归盘点，并对目标实际结构重新建映射。[历史报告](../../en/diff/19-vs-18.3/README.md)、[历史执行提示词](../../tmp/pg19-easydict-prompt.md)
- 当前术语表仍保留用户确认的九项原译；其后已有新的校正记录。因此启动时须固定最新中文与现用规则，历史 v2 和复审候选不能充当当前规范。[当前规范状态](../terminology-14-19/ACTIVE.md)、[现用术语表](../../tmp/ref/glossary.tsv)
- 两个现有构建脚本会动态解析开发分支，缓存 snapshot 的标记也不足以独立证明源码提交一致；中文构建还会放宽严格验证。提示词据此要求固定源码、核对真实内容来源，并单独验证结构与链接。[HTML 构建脚本](../../bin/build_standalone_docsrc.sh)、[PDF 构建脚本](../../bin/build_standalone_pdfsrc.sh)

本次仅创建提示词和使用说明，没有下载 PG20 源码、生成 PG20 diff、创建英文/中文 20 目录或执行翻译和构建。阶段一、阶段二执行时才会产生对应实测产物。
