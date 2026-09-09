# PG20 固定源码构建适配

本次只给出可执行设计和任务 B20-FIX-SOURCE，尚未修改公共脚本，也没有构建 PG20 中文。

现有 HTML 脚本第 143—235 行、PDF 脚本第 219—297 行的 resolve_git_ref/sync_git_checkout 动态查询开发分支；HTML 第 237—265 行、PDF 第 378—401 行准备源码。snapshot 的 .pgdoc-upstream-ref 只是查询得到的标记，不能证明日更压缩包内容相符。源码固定必须在这些分支之前处理。

最小兼容实现：给两个脚本添加可选环境变量 PGDOC_SOURCE_DIR、PGDOC_SOURCE_COMMIT。两项同时提供时，读取该目录真实 Git HEAD，要求等于指定完整提交，要求 Git tracked 内容无修改，并核对 configure.ac/configure/meson.build 的版本声明。核验通过后，将源码复制到独立 work_tree（排除 .git），完全跳过在线 ref 查询、clone 和 snapshot 分支；日志写入提交、源码目录及各输入哈希。两项没有提供时保持全部现有版本位置参数、稳定包路径与默认行为；只提供一项时明确报错。不要在固定路径失败后悄悄回退联网。

本轮固定源码目录：`/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20`；提交：`86f7c82cf1023e3599f40f939727791a7090cd44`。该目录已 detached，7,680 个文件的 SHA256 在 `/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20-files.json`，继续使用前必须复核。不要直接在缓存源码中 configure 或覆盖中文；每个构建在新工作目录进行。

zh/20/Makefile 当前为 PG18 原样继承，正式阶段仅将 PG_VERSION 默认设为 20；脚本版本位置参数传 20，目标目录也为 20，真实显示版本必须由固定源码生成的 version.sgml 得到 20devel。顶层 VERSION、ZH_VERSIONS、EN_VERSIONS 和旧版输出位置保持现状。en/20/Makefile 是完整上游 Makefile，依赖上游源码树，不能把它作为独立项目 Makefile 直接覆盖 zh/20/Makefile。

适配后执行的命令如下（这些命令依赖 B20-FIX-SOURCE 已完成）：

```bash
cd /Users/vonng/pgsty/pgdoc
export PGDOC_SOURCE_DIR='/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/upstream-pg20'
export PGDOC_SOURCE_COMMIT='86f7c82cf1023e3599f40f939727791a7090cd44'
KEEP_WORK=1 bin/build_standalone_docsrc.sh zh/20 zh 20 '/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/html'
KEEP_WORK=1 bin/build_standalone_pdfsrc.sh zh/20 zh 20 '/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/postgresql-20-zh-A4.pdf' A4
KEEP_WORK=1 bin/build_standalone_pdfsrc.sh zh/20 zh 20 '/Users/vonng/pgsty/pgdoc/tmp/pg20-from-18.6/20260909-085948-37d573/execution/builds/postgresql-20-zh-US.pdf' US
```

逐项重定向完整日志到 execution/builds，检查退出码；同时保存 work_tree 内的 configure、make、FOP 日志及源码/产物 SHA256。FOP 不在 PATH 时现有 .cache/tools/fop-2.11/fop/fop 可用，字体使用已检出的 Alibaba PuHuiTi 3.0 与 Courier New；仍需实际查看两个纸型的字体、代码和表格。

验证公共脚本改动：bash -n；原有位置参数和稳定包分支仍可用；精确提交/版本不匹配与脏输入应失败；固定源码模式确认未进入 git ls-remote/clone/download 分支；实际 PG20 HTML、A4/US PDF；另在独立输出目录做一次 PG18.6 HTML 兼容性冒烟构建，不更改旧版源文件。新中文不会因为 HTML 脚本把 --valid 放宽为 --catalogs --loaddtd 就视为引用合格，必须独立检查包含链、重复 ID、linkend/endterm/zone/otherterm 以及未闭合实体。

两版生成表本轮已实际重建，见 generated-files.json。PG20 正式构建必须用 PG20 生成器与对应源码输入。需要本地化本轮新增或变更的生成说明时，保留可再生成的 PG20 专用覆盖步骤和逐项台账；不要直接提交构建目录中的派生表，也不要为此重译英文未变的整张表。
