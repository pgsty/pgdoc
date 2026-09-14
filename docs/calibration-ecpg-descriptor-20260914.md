**PG10—PG20：ECPG 描述符全节校准结果**

已完整对照 28 个列表条目变体、47 个外层段落、16 个节框架和 37 个程序/输出变体，包括完整示例、旧版注释差异及三种逐版输出。实际覆盖十一版的 110 个节范围、308 个条目、1232 个文本段；36 个修订稿变体已复读。374 个代码与输出块保持原样并逐一核对各版英文。

主要修复：十一版将动态 SQL 的“结果列可能未知”错译为“结果行无法预知”、将“释放内存”写成“关闭内存”、将附加规则误作适用条件；PG14—20 遗漏 v.sqltype，并把 SCALE 错译为“比例”。同时明确结果集与元数据的存储位置、多行 FETCH 对数组主变量的要求、描述符字段术语和在命令中指定 SQLDA 的方式。

原文疑点单列：输出 SQLDA 步骤把 sqln 称为记录数，同章定义及十一版固定源码却均表明它是列数。保留固定英文对应说明并记录证据，没有把这项上游问题计作中文新增缺陷，也未声称执行过示例。

下表包含缺陷、措辞校准、回归检查与源文疑点，231 格不代表 231 个独立缺陷。修＝修复或措辞统一，核＝该项原本正确，源疑＝保留固定英文并记录疑点。

| 检查组 | 级别 | PG10 | PG11 | PG12 | PG13 | PG14 | PG15 | PG16 | PG17 | PG18 | PG19 | PG20 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C19-ECPG-DESCRIPTOR-001 动态 SQL 可能未知的是结果列，而非结果行 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-002 释放输入 SQLDA 内存误译为关闭内存 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-003 PG14—20 缺失 v.sqltype 及对应说明 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-004 PG14—20 将 numeric SCALE 误译为比例 | P2 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-005 补充规则误译成适用条件 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-006 结果集与元数据均位于描述符区域 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-007 FETCH 多行数据使用数组主变量的条件 | P2 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-008 PG14—20 NAME 通用类型注释未译 | P3 | 核 | 核 | 核 | 核 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-009 描述符元数据与 C 结构体的字段术语 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-010 预备语句和查询的同义用法 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-011 在命令中指定 SQLDA 的语法关系 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-012 DB2 SQLDA、结构体保存值及参数数量说明 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-013 循环读取与相同英文说明共用译文 | P3 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 | 修 |
| C19-ECPG-DESCRIPTOR-014 命名描述符与 C SQLDA 的 SQL 关键词区别 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-015 头部 COUNT 是列数、CARDINALITY 是行数 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-016 长度的字符与字节单位、空值和截断指示 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-017 日期时间类型代码与尚未实现的字段 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-018 一条 SQLDA 对应一行及 desc_next 链表 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-019 输入参数内存尺寸、赋值顺序和显式释放 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-020 完整示例、分段代码和逐版输出保持对应英文 | CHECK | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 | 核 |
| C19-ECPG-DESCRIPTOR-021 英文步骤将 sqln 列数称作记录数的原文疑点 | SOURCE | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 | 源疑 |

十一版新快照检查完成，原始退出码保留为 PG10—12 的 3、PG13—20 的 1；不是原始检查器全零。范围内 58 条提示逐一绑定 56 个完整条目和 2 个完整章节的既有 ID，接受后零未决、零漂移。初次分类的两个章节提示保留在原文件，最终结论以 accepted-classification/accepted-unresolved 为准。源文差异检查通过。ECPG 其余各节、全书通读与最终 33 项 HTML/A4/US 构建仍未完成。

证据：[十一版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-descriptor-full-issue-version-matrix.json)、[修订稿](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-descriptor-full-parent-plans.json)、[源码核对](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-descriptor-pinned-source-proof.json)、[原生精确核验](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-descriptor-native-validation.json)、[58条提示处理](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/ecpg-descriptor-native-accepted-classification.json)。
