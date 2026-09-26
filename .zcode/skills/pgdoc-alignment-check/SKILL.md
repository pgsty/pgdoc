---
name: pgdoc-alignment-check
description: PostgreSQL 中英全书结构对齐检查：bin/check_doc_alignment.py 的准备、运行、退出码解读与假差异源判例。需要核验中英 SGML 文件覆盖、ID/结构/表格一致性时使用。流程见 ref/alignment-check.md，完整工具文档 docs/doc-alignment.md。
---

执行 pgdoc 结构对齐检查任务。

1. 完整读取 `ref/alignment-check.md` 与 `docs/doc-alignment.md`。
2. 按 prepare（固定源码，devel 用 --source-dir + --source-commit）→ check → 解读 REPORT/findings 的顺序执行；回归用 `python3 -m unittest discover -s bin -p 'test_*.py'`。
3. 核心约束：退出码 0 不是语义验收；'definite' 不等于应删改；先排除假差异源（世代形态、生成文件错位级联、zh-auto 锚点、实体口径、空白变体、9.x IDREF 尾空格、EN 自身基线缺陷）再定性缺陷。
4. 无 ID 多候选、未配对行、自然语言语义仍需人工核查（转 ref/full-review.md）。
