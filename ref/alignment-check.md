# 任务流程：中英全书结构对齐检查

用 `bin/check_doc_alignment.py` 比较**固定版本英文与中文当前全文**的结构一致性。完整工具文档见 [docs/doc-alignment.md](../docs/doc-alignment.md)。要点：

- 它不比较两个 Git 提交之间的改动，也不把构建成功视为翻译完整；退出码 0 **不是**语义验收。
- 输出目录必须是新目录且不在输入目录内；检查器不修改正文、术语或构建源目录。

## 运行

```sh
# 1. 准备生成输入（固定源码包或源码目录+提交）
python3 bin/prepare_doc_alignment.py \
  --archive .cache/upstream/postgresql-<版本>.tar.bz2 --sha256 <SHA256> \
  --version <版本> --en en/<版本> --zh zh/<大版本> --out outputs/<prep-dir>
#   （devel/源码 checkout 用 --source-dir <绝对路径> --source-commit <完整SHA> 替代 --archive）

# 2. 结构检查
python3 bin/check_doc_alignment.py \
  --en en/<版本> --zh zh/<大版本> --version <版本> \
  --prepared outputs/<prep-dir> --out outputs/<align-dir>

# 3. 回归测试（对齐器自身）
python3 -m unittest discover -s bin -p 'test_*.py'
```

PG10 原生 SGML 加 `--native-sgml`（OpenSP 环境）；中文附加输入用 `--zh-aux`（如缺失的 `pgdoccn-notes.sgml`，**不要用空占位文件顶替**）。

## 退出码

| 码 | 意义 |
|---:|---|
| 0 | 可检查的结构与确定标识符一致且无配对歧义（**非语义验收**） |
| 1 | 存在确定结构/标识符/事实值差异 |
| 2 | 输入不完整、版本/哈希不符、依赖或解析失败 |
| 3 | 无确定差异但有配对歧义 |

## 解读纪律

`definite` 表示差异确定，不表示都应删改（中文额外的自动列表 ID 是真实差异但通常只需核实用途）。P1 先查缺项、错误归属、表形状、事实值；附加 ID、行序、引用变化一般 P2。数量不是独立缺陷数（父表与子行可能报告同一遗漏）。

## 已知假差异源（判例，勿误报为缺陷）

- **世代形态**：6.x/7.x 大写标签 + HTML 形态文档是历史常态；同构标记跨 DTD 不可同判。
- **生成文件错位级联**：wait-event 等生成表按物化序数错位会级联出成串假差异，先核生成输入。
- **zh-auto-* 锚点**：零引用零碰撞的自动 ID 不是缺陷。
- **内构实体 undefined 口径**：区分实体声明与实际使用；空实体/仅注释实体也计实际消费。
- **弱键空白变体**：行键比对容许键后 `(` 等后随字符；空白变体先实测再报。
- **9.x IDREF 尾空格**：`linkend` 尾部空格是该世代形态，双侧核对后再定性。
- **EN 自身基线缺陷**：英文侧固有错误（如缺 `cols`）单列为上游问题，中文正确时不算差异。

## 限制

无 ID 多候选、未配对行、自然语言技术陈述仍需人工核查（走 [full-review.md](full-review.md)）；检查不验证语义、默认值或代码逻辑。
