---
name: pgdoc-en-fetch
description: PostgreSQL 英文文档获取与固定：下载官方 tarball、校验、提取 doc/src/sgml 到 en/<版本>/ 并登记 SOURCES.json。需要新增英文基线版本（新小版本/beta/快照）或从缓存恢复 en/ 树时使用。脚本 bin/fetch_en_docs.py。
---

执行 pgdoc 英文文档获取任务。

1. 先读 `AGENTS.md` 共用纪律；脚本用法见 `python3 bin/fetch_en_docs.py --help`，布局与核验口径见 `en/README.md` 与 `en/SOURCES.json`。
2. 标准流程：`python3 bin/fetch_en_docs.py <版本> --register`。发布版自动定位 `https://ftp.postgresql.org/pub/source/v<版本>/` 的 tar.bz2/tar.gz，获取并校验 `.sha256`/`.md5` 边车（BSD 格式兼容），核对 configure.ac/configure/meson.build 版本声明一致，提取 `doc/src/sgml`；6.3–7.3 自动复制 `graphics/` 并把全部 GIF 复制到文档根。归档保留在 `.cache/upstream/`（灾备基线，勿清理）。
3. 开发快照与 git 导出必须 `--url` 显式给源（快照在 `https://ftp.postgresql.org/pub/snapshot/dev/`）；本地已有 tarball 用 `--archive`；`--no-keep` 仅在明确不留档时使用。
4. 核验：提取后报告的 files/bytes/sgml/graphics 计数须与 `--register` 写入 SOURCES.json 的登记一致，并与相邻版本数量级对照；对不上立即停下报告，不得静默接受。恢复场景（缓存重建）必须逐项核对 SOURCES.json 既有条目的 `documentation_files_verified`/`documentation_bytes`/`doc_sgml_files`。
5. 纪律：绝不删除既有 `en/` 树；`--force` 刷新前先确认旧树可由 `.cache/upstream` 归档恢复；清理任务涉及 `en/` 时必须先向用户确认精确的保留清单再动手（2026-09-25 误删教训）。
