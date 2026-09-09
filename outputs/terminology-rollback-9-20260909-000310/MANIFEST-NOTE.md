# 交付封存说明

MANIFEST.json 记录本目录普通文件和符号链接，并记录 run/MANIFEST.json 的 SHA-256。run、audit、ledgers、diff、reviews、builds 使用本项目内的相对符号链接；builds 只指向本轮最终 builds-r3。实际构建命令、完整日志、PDF 及 HTML 的指纹均可由这条清单链追溯。

rules/ 与 materials/ 为逐字节快照，原文件入口见 SNAPSHOTS.md。旧两次术语校准交付未覆盖，最终验收再次验证其原 MANIFEST 条目。
