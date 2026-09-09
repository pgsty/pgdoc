"""Generate the additive terminology reconsideration; never install active rules."""
from pathlib import Path
import collections
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
PACK = HERE.parent
REPO = PACK.parent.parent
V2 = REPO / 'outputs/01a08005-ffff-72b1-84e0-109c680e9bc8/v2'

# R: restore original preferred entry; O: optional wording, not an error;
# C: retain with explicit context; K: retain the substantive improvement.
# Each item is an editorial judgment, not a claim of a unique official Chinese term.
DECISIONS = {
    27: ('R', 'B-树是可成立的中文概念名。正文 B-tree 的出现频率不能证明中文应禁用；把数据结构名称列入必须保留英文的清单，是保护范围扩大。恢复原表 B-树；B 树作为排版变体，B-tree 可用于引介或沿用现有英文叙述。'),
    43: ('K', '原译“可强制”缺少被强制转换的含义，补“转换”有实际信息收益。此处可省去转换函数，不等于必须显式 CAST，也不保证双向兼容。'),
    50: ('K', '补出“操作符类”说明对象类别，保留。原来的 Bloom 类在已说明语境中仍可作简称；这次没有把已有中文概念改回英文。'),
    51: ('C', '引导适合计算机 bootstrap，但“初始启动”在确指首次启动时成立。引导模式、初始化、自助法需要按对象区分；v2 已有统计学例外，应继续遵守，不能只按单词替换。'),
    60: ('C', '缓冲区映射表解释了 buffer table 的用途，可保留作说明性名称。原“缓冲表”在作者已经定义的缓冲区管理语境中并不错误，不应为了增补解释而强制改掉每个简称。'),
    68: ('K', '补译 Memoization 为记忆化有实质收益。“行缓存”作标题可用；句中的 caching rows 仍可写“缓存行”，不能把语法调整也当成术语错误。'),
    78: ('K', '正则表达式的 escape 译“转义”，character-entry 表示输入特定字符。“字符项逃逸”在这个语境中应修正。'),
    82: ('O', '命令标识、命令标识符、命令 ID 均可说明同一概念。保留较完整的词表释义，但不能把原“命令标识”作为错译清零；类型名 cid 始终保留。'),
    83: ('K', '补“字符”明确字符类，简写转义也准确说明机制。原“逃逸”应在该正则语境中纠正。'),
    84: ('O', '清理阶段与 VACUUM 用语协调，可作首选；清除阶段在已定义流程中也能成立。清除、清理的选择不足以单独触发跨版正文迁移。'),
    91: ('K', '合并函数直接说明它合并部分聚合状态，能减少与函数组合的混淆，保留。原“组合函数”并非逻辑上必错；收益是具体机制的消歧，不是某个机构规定了唯一中文。'),
    92: ('O', '命令标识已经表达 identifier，补“符”属于全称规范。词表可保留命令标识符，正确的旧正文不必为这一字重写。'),
    103: ('K', '这里是正则的零宽约束转义，修正“逃逸”有明确领域依据；不能迁移到表约束或其他 escape 术语。'),
    127: ('R', '此项完全依赖 B-tree 必须保留英文的错误前提。恢复“默认 B-树操作符类”；实际操作符类标识符仍保持原文。'),
    137: ('O', '离散百分位数适合作完整统计量名称；离散百分位在函数返回值语境中并不缺义。真正要核对的是返回的分位值与输入的 fraction，不能只靠补“数”解决。'),
    139: ('C', '英文完整词组有 DTrace 时保留限定有益。上下文已经限定 DTrace 后，后续单独的 probe 可以写“探针”；不得把所有中文探针都扩写。'),
    140: ('C', '同单数项。中文无需机械区分复数，也无需对后续每个 probes 重复添加原文没有的 DTrace 限定。'),
    150: ('K', '字符及正则语境用转义有明确收益；escape analysis 等完整术语不适用，不能全局删除“逃逸”二字。'),
    165: ('O', '外部排序适合正式词条和首次引介，外排是可用简称。两者的关系类似全称与简称，不构成必须清除外排的理由。'),
    179: ('R', '原作者实际使用 first-committer-win；“以先提交者为准”准确、自然。恢复原词头和原译，wins 与“先提交者胜出”保留为可接受别称；不再把来源写法降为待改旧拼写。'),
    180: ('R', '原作者实际使用 first-updater-win；“以先更新者为准”已准确表达裁决规则。恢复原词头和原译；不从词名概括所有隔离级别的实现。'),
    195: ('O', '冻结事务标识与冻结事务 ID 表达相同对象。统一 ID 写法可以是一项编辑选择，但没有纠错必要；FrozenTransactionId 常量的保护是另一件事。'),
    199: ('R', '整页镜像能够表达 full-page image，整页映像也成立。与前映像、后映像使用同一个 image 英文词，不能单独证明旧复合术语应改。恢复原表首选，撤销镜像到映像的强制迁移。'),
    213: ('R', '首部与头部都是 header 的可用表达；“页头”与“首部数据”也能共存。此次没有修复技术含义，恢复首部数据，保留头部数据作为可接受表达。'),
    215: ('K', '中文已经正确回到堆内元组，本轮不推翻这项回退。heap-only 是官方文档常用词头形式，可保留，同时接受来源中的 heap only 拼写。'),
    242: ('K', '增加操作符类补足对象类别，可保留。实际 *_inclusion_ops 标识符与说明性的类别名称分开处理，不额外宣称 Inclusion 这个普通词永远不能翻译。'),
    258: ('K', '补“状态”点明移动聚合的逆向操作对象，保留。它移除输入对状态的贡献，不是一般转换函数的数学逆，也不保证每一步都能求逆成功。'),
    260: ('K', '“进行中”补出 in progress 的状态含义，标志位也比原来的省略表达清楚。I/O 的排版本身不是纠错依据；内部名称按对应版本保留。'),
    261: ('K', '“进行中”比“进行锁”更完整，保留解释性释义。必须附历史实现语境；这个名称不能证明当前大版本还有同名锁或相同同步机制。'),
    267: ('R', '连接类型和方式已经准确表达原标题。“和/与”“方式/方法”的替换没有提供可说明的技术收益，恢复原译，承认两种标题都可用。'),
    288: ('K', 'Kafka 的按键保留记录机制与字节压缩不同，日志压实能够消歧，保留。既有译著采用带英文的日志压缩时，可保留其定义，不把其他来源统一改写。'),
    297: ('K', '胜出较自然地表达冲突裁决中的 wins，保留这项措辞改进。并不需要为了词族表面一致而同步改掉本来通顺的“以先……者为准”。'),
    301: ('C', 'master 不能固定补“库”：主库、主服务器、主节点、主进程、主密钥取决于对象。v2 限定复制角色是必要的，但仍不足以把角色下的各种对象都说成库。'),
    302: ('C', '主/从能够修饰不同对象；主库/从库只适合以数据库实例为对象的说明。保留该释义的数据库语境，不能把原来的复合用法一概扩写。'),
    311: ('K', '“有序”明确输入已经排好序，能够避免把原译读成归并排序算法，保留。按标题可写归并有序集合，句中也可写归并有序数据集。'),
    313: ('K', '增加操作符类有助于识别 BRIN 对象类别，保留；既有上下文的 Minmax 类仍可用作简称，代码名不改。'),
    314: ('K', '同类名称补足操作符类有益，保留。解释多个值区间时不能误称多列，也不能由名称推导实现细节。'),
    322: ('K', 'Oracle table cluster 的簇与分布式集群含义不同，原“集群表”有实质歧义，应保留簇表修正。适用范围限 Oracle 对比。'),
    324: ('O', '组事务在已定义为 MultiXact 的语境中并不等于组提交，也不是因为含“组”就错误。多事务可以保留作首选；两种中文都需要定义，不能靠名称本身推断实现。'),
    332: ('O', '锁定与加锁均能表达取锁行为。新译可保留，但无等待锁定不是技术错误；还应按原文区分“不等待”与免锁算法。'),
    360: ('O', '页剪枝已经通过“页”与分区剪枝区分，补“内”只能增加解释性。“页内剪枝”可用，但不应据此判旧译不准确。'),
    370: ('C', '保留英文括号中的可选索引限定有精度收益。实际正文说 parameterized path 时应写参数化路径，说 parameterized index path 时写参数化索引路径，不给每次出现强塞括号。'),
    384: ('K', '同等行组可与 peers 的同等行保持对应，保留这项限定语境的消歧改进。平级组在有定义的上下文并非必然错误，不能解释成整行所有列都相同。'),
    385: ('R', '百分位点在指分布分位值时是完整表达，百分位数也成立。此前以“较完整”为由降低原译地位没有充分依据；恢复百分位点首选，取消仅 DDIA 可以沿用的限制。'),
    387: ('K', '在词条指页头校验和字段的前提下，pd_checksum 有官方结构定义依据，保留词表勘误。不能借此把实际代码中的相似 pg_checksum 名字全部改掉。'),
    388: ('K', '在词条指页头标志字段的前提下，pd_flags 是实际名称，保留勘误。代码中的 pg_flag 仍要先核对具体对象，不进行相似字符串改名。'),
    389: ('K', 'pg_lsn 是类型，LSN 是所表示的日志位置；释义补类型有实际消歧收益。组句时若已经写“pg_lsn 类型”，不重复叠加“类型”。'),
    393: ('K', '钉数不易理解，钉住计数可与 pin/pinned 词族对应，保留。它与 usage count 不同；具体计数单位依据版本实现，不能从中文推出进程数或引用次数。'),
    401: ('C', '英文小写 postgres 并不足以证明每处都是可执行程序名。明确引用程序时用 postgres；产品简称 Postgres 在叙述中可以成立，不把大小写统一当作事实纠错。'),
    421: ('O', '快速排序是合适全称，快排是通行简称。词表保留全称即可，不需要清除所有已定义且跨版一致的简称；实际 EXPLAIN 输出保持 quicksort。'),
    423: ('O', '范围摘要可与 BRIN 的摘要叙述协调，但范围提要不是技术错误。若原文强调 summarization 动作，可说生成范围摘要，不强行把句子改成名词。'),
    454: ('O', '重扫描是可理解的技术简称，重新扫描更口语自然。保留新词条，同时撤销把原译视为需要全量整改的依据。'),
    469: ('K', 'savepoint 是 PostgreSQL 文档词头及 SAVEPOINT 对应形式，保留规范词头。save-point 可作来源拼写别名；中文保存点无需改变。'),
    476: ('K', '原译两个“模式”分别指 schema 与 pattern，容易把安全的作用对象读错。模式的安全使用方式更清楚，保留，其他 pattern 不随之全局改成方式。'),
    504: ('C', '倾斜仅适合数据或负载分布不均；偏差在 clock/read/write skew 等完整术语中正确，偏度还可能是统计量。v2 已写出这些边界，应保留并落实，不能据主词头推断旧译都错。'),
    530: ('K', 'START WAL LOCATION 是 backup_label 字段的完整文本，保留词表勘误。英文原文若只用 START WAL 作解释性缩写，不自动把它当输出字段修正。'),
    533: ('K', '状态转移较清楚地描述聚合状态随输入更新，可与逆向状态转移配套，保留。状态转换本身不违背概念；这是一项有机制依据的词族改进，不能扩展到所有 transition。'),
    538: ('C', 'streaming 单独不蕴含复制，原译作为通用词头过窄，应保留修正方向。但传输、处理、执行要按动词对象组词；streaming replication 仍是流复制。'),
    542: ('K', 'C 语言语境结构体比泛称结构更明确，保留。struct 关键字保留，普通 structure 仍按上下文译结构，不能跨词头反向套用。'),
    561: ('O', '两层修改分开：指 C 类型时 TimeLineID 的拼写应保留勘误；中文“时间线标识”本来成立，没有必要仅为 ID 排版换词。实际变量 TimelineID 或 timelineId 不据词表改名。'),
    569: ('O', '事务标识与事务 ID 均可准确表达 transaction id。词表可保留简洁首选，但把“标识”统一换成 ID 不能算技术纠错。'),
    579: ('K', 'pg_trgm 明确定义为三个连续字符，三字符组能避免与数据库元组混淆，保留这项改进。它不是泛 NLP 的所有 trigram；函数名和输出不翻译。'),
    585: ('O', 'txid 原文保留与中文释义选择是两层问题。事务标识无需为“保护标识符”而变成英文 ID；词表首选事务 ID 可保留，正确旧译也应认可。'),
    586: ('O', '事务标识回卷本来正确；改事务 ID 回卷是写法统一。wraparound 可保留为词头形式，并保留旧来源拼写；这不能触发正文或代码的无条件修改。'),
    591: ('C', '不记录 WAL 有助于限定 PostgreSQL UNLOGGED 的实际含义，可保留。但已明确日志指 WAL 的“不记录日志”也成立；必须保留版本及操作范围，不能推导所有相关操作完全不产生 WAL。'),
    600: ('R', '中文标题可以用动宾结构，不必因为英文 Insertion 是名词就改为“值插入”。原“插入值”自然、准确，恢复原译，句子继续按语法表达。'),
    619: ('C', '确指 PostgreSQL 进程时，WAL 接收进程更明确；泛指接收组件或接收端时不能随意补进程。WAL 接收器本身也不是错译，实际名称和输出值保留。'),
    620: ('C', '确指服务器进程时可保留 WAL 发送进程，其他组件名称按具体对象判断。不能把所有 WAL 发送器或发送端都改成进程。'),
}

OVERRIDES = {
    27: '说明性正文首选 B-树，首次可写 B-树（B-tree）；B 树是可接受的排版变体，已成立的 B-tree 英文叙述不因此自动判错。仅真实访问方法名 btree、函数或扩展标识符等保留字面形式；不能把概念名列为强制不翻译项。',
    36: '若原文实际指 full-page image，按整页镜像理解；整页映像为可接受表达。不得把所有 backup block 自动改称整页镜像，也不做映像/镜像的全局替换。',
    51: '计算机 bootstrap 可译引导；确指首次启动时可保留初始启动，构建或初始化语境按对象表达。bootstrap mode 可写引导模式；统计学 bootstrap 为自助法。代码和参数中的 bootstrap 保留。',
    60: '仅 PG 缓冲区管理中的标签到缓冲区编号映射；首用可说明为缓冲区映射表（buffer table）。作者已定义的缓冲表是可接受简称，不据本条强制扩写；不能解释为用户 SQL 表。',
    127: '说明性正文首选默认 B-树操作符类；B 树排版变体可用。具体操作符类名、btree 访问方法名等保持原样；不规定概念 B-tree 必须保留英文。',
    139: '英文明确出现 DTrace probe 时保留 DTrace 限定，可写 DTrace 探针；上下文已限定后的 probe 可以只译探针，不为后续普通词额外补限定。DTrace 名称保留。',
    140: '英文明确出现 DTrace probes 时可写 DTrace 探针；复数不需要中文数量词，后续已限定语境中的 probes 可只译探针。DTrace 名称保留。',
    179: '按来源词头使用 first-committer-win，first-committer-wins 是可接受检索别名；中文首选以先提交者为准，先提交者胜出也可用。原文和代码不改拼写；具体裁决规则以来源文献及版本为准。',
    180: '按来源词头使用 first-updater-win，first-updater-wins 是可接受检索别名；中文首选以先更新者为准，先更新者胜出也可用。原文和代码不改拼写；不推广为所有隔离级别的统一规则。',
    199: 'WAL 中的 full-page image 首选整页镜像；整页映像也可接受，前映像/后映像保留各自稳定用法。词表恢复原首选，不据本条对已一致的正文进行镜像/映像反向替换；函数、配置及输出保持实际文本。',
    213: '正文首选首部数据；头部数据也成立。页头、元组头可按各自词组沿用，不为字面一致扩展替换所有 header。PageHeaderData 等类型名保留。',
    267: '标题首选连接类型和方式，连接类型与方法也可接受；句中按语法表达。不得仅因和/与、方式/方法的偏好触发历史正文迁移。',
    301: '词表主库释义仅指数据库实例的复制角色；master server 译主服务器，master node 译主节点，master process 译主进程，master key 译主密钥。可作为修饰语译主，不能按独立 master 一律补库。实际标识符保留。',
    302: '仅在数据库实例为对象的主从关系中使用主库/从库；其他对象保留主/从或补主服务器/从服务器等合适名词。历史角色与实际标识符不改成其他协议名称。',
    370: '词条参数化（索引）路径保留英文可选限定。正文 parameterized path 译参数化路径，parameterized index path 译参数化索引路径；仅当来源有可选括号或确需涵盖两者时保留括号。',
    385: '指分布分位值时首选百分位点，百分位数也可接受，不限于 DDIA；不能混同百分比、输入的 percentile fraction、百分等级或 percentile rank。percentile_disc 等函数名保留，按原文说明输入和输出。',
    401: '确指可执行程序 postgres 时保持小写；叙述产品时可按原文使用 PostgreSQL 或已有简称 Postgres。不能仅因术语表词头小写，就把已有叙述中的 Postgres 判作程序名大小写错误。',
    504: '数据或负载分布不均用倾斜；统计量的不对称程度按上下文用偏度等表达；clock/read/write skew 按完整词组译时钟/读/写偏差。先匹配完整词组，不把偏差二字作为全局旧译候选。',
    538: 'streaming 按语境写流式传输、流式处理或流式执行；完整 streaming replication 仍译流复制。不得先替换短词 streaming 而破坏完整复制术语，代码和参数中的词不译。',
    570: '区别回卷 wraparound 与回滚 rollback；事务 ID 回卷与已定义的事务标识回卷均可接受，不仅为 ID 写法统一而改动正文。',
    591: '说明性正文可写不记录 WAL 的表；上下文已明确日志为 WAL 时，不记录日志的表也成立。UNLOGGED 关键字保留；相应关系普通数据变更的规则不推导为所有相关操作均不产生 WAL。',
    600: '标题首选插入值；中文可用动宾结构，句中根据实际语法表达，不因英文名词结构而强制名词化。实际 INSERT 关键字和示例保持原样。',
    619: '确指 PostgreSQL WAL 接收进程时使用 WAL 接收进程；接收器、接收端在相应组件语境中可用。进程名 walreceiver 与 backend_type 等实际值保留，不给泛指组件补进程属性。',
    620: '确指 PostgreSQL WAL 发送进程时使用 WAL 发送进程；发送器、发送端在相应组件语境中可用。walsender 及实际输出值保留，不给泛指组件补进程属性。',
}

CATEGORY = {
    'R': ('恢复原表首选', '恢复词条或保护规则的原译地位；正文按逐处证据处理，不把所有新译视为错译。'),
    'O': ('撤销强制迁移', '保留 v2 作为词条首选或全称，认可原译；仅因写法不同不触发正文修改。'),
    'C': ('保留并限定语境', '只在原文满足条目条件时采用新译；越界扩写需要按对象修正。'),
    'K': ('保留修订', '保留有含义、对象类别或可读性收益的修订，仍须结合原文和完整词组。'),
}

def read_tsv(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write_tsv(name, rows):
    with (HERE / name).open('w', newline='') as f:
        w = csv.DictWriter(f, list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def write_json(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def esc(s):
    return str(s).replace('|', '\\|').replace('\n', '<br>')

def pair(en, zh):
    return f'{esc(en)}<br>{esc(zh)}'

def main():
    changes = read_tsv(V2 / 'glossary-changes.final.tsv')
    original = read_tsv(PACK / 'refs/glossary.original.tsv')
    glossary = read_tsv(V2 / 'glossary.final.tsv')
    rules = read_tsv(V2 / 'glossary.rules.tsv')
    assert set(DECISIONS) == {int(r['原序号']) for r in changes}
    counts = collections.Counter(category for category, reason in DECISIONS.values())
    assert counts == {'R': 9, 'O': 16, 'C': 13, 'K': 30}
    assert len(original) == len(glossary) == len(rules) == 631

    decisions = []
    for row in changes:
        i = int(row['原序号'])
        category, reason = DECISIONS[i]
        assert original[i-1] == {'English': row['原英文'], '中文': row['原译']}
        assert glossary[i-1] == {'English': row['最终英文'], '中文': row['最终中文']}
        if category == 'R':
            glossary[i-1] = original[i-1].copy()
        if category == 'O':
            rules[i-1]['使用规则'] += f' 原译“{row["原译"]}”在同一已定义语境中也可接受，不单凭全称、简称或 ID 写法差异触发正文修改；已有正确且跨版一致的新译也不反向替换。'
        decisions.append({
            'id': i, 'category': category, 'decision': CATEGORY[category][0],
            'original': original[i-1],
            'v2': {'English': row['最终英文'], '中文': row['最终中文']},
            'candidate': glossary[i-1], 'reason': reason,
            'migration_policy': CATEGORY[category][1],
            'v2_reason_for_traceability': row['最终理由'],
            'v2_sources_for_traceability': row['来源 URL'],
        })

    for i, rule in OVERRIDES.items():
        rules[i-1]['使用规则'] = rule
    for i, row in enumerate(rules, 1):
        assert int(row['原序号']) == i
        row['English'] = glossary[i-1]['English']
    rules[26]['保留字面形式'] = '按语境'
    for decision in decisions:
        decision['candidate_rule'] = rules[decision['id']-1]['使用规则']

    aliases = read_tsv(V2 / 'glossary-aliases.tsv')
    for row in aliases:
        i = int(row['原序号'])
        if i in (179, 180):
            row['旧英文'] = row['主词头']
            row['中文别称'] = row['主中文']
            row['记录性质'] = '来源词形与可接受中文别称'
        elif i in (199, 385):
            row['中文别称'] = row['主中文']
        row['主词头'] = glossary[i-1]['English']
        row['主中文'] = glossary[i-1]['中文']
    # Keep all original alias and erratum records, then register accepted forms.
    for decision in decisions:
        if decision['category'] not in ('R', 'O'):
            continue
        i = decision['id']
        alias_zh = decision['v2']['中文'] if decision['category'] == 'R' else decision['original']['中文']
        existing = next((r for r in aliases if int(r['原序号']) == i), None)
        if existing:
            variants = [s.strip() for s in existing['中文别称'].split('；') if s.strip()]
            if alias_zh != existing['主中文'] and alias_zh not in variants:
                variants.append(alias_zh)
            existing['中文别称'] = '；'.join(variants)
        else:
            aliases.append({
                '原序号': str(i), '旧英文': '', '主词头': glossary[i-1]['English'],
                '中文别称': alias_zh, '主中文': glossary[i-1]['中文'],
                '记录性质': '可接受中文表达',
                '使用限制': '仅作检索与解释，不是错误清单。不得自动替换；同一概念位置的适用版本应保持一致。',
            })
    aliases.sort(key=lambda row: int(row['原序号']))
    preserve = [row for row in read_tsv(V2 / 'terms-to-preserve.tsv') if int(row['原序号']) != 27]
    for row in preserve:
        i = int(row['原序号'])
        row['English'] = glossary[i-1]['English']
        row['中文释义'] = glossary[i-1]['中文']
        row['使用规则'] = rules[i-1]['使用规则']

    write_tsv('glossary.candidate.tsv', glossary)
    write_tsv('glossary.rules.candidate.tsv', rules)
    write_tsv('aliases.candidate.tsv', aliases)
    write_tsv('preserve.candidate.tsv', preserve)
    write_json('decisions.json', decisions)

    report = '''# 对既有 68 项术语修订的复审

日期：2026-09-08。范围：最初原表至 v2 的全部 68 项净变化，以及关联的不翻译、别名和适用规则。本轮是对既有修订的重新判断；没有重新邀请 Claude，也不把先前三轮达成一致视为正确性的证明。

结论：**9 项恢复原表首选，16 项撤销强制迁移，43 项保留；保留项中 13 项须明确限制语境。** 这些是词条决策的数量，不能当成正文错误或需要回退的位置数量。

本轮已生成配套候选词表与规则，未安装到 `tmp/ref`，未修改六版 SGML。v2、冻结 refs 和已执行的正文校准结果均保留。当前工作区已有 631 份中文 SGML 修改，批量反向替换会混入正确改动；实际回退应利用原执行台账逐处核对。

## 重新判断采用的原则

1. 必须保留的是原文实际出现的代码、标识符、关键字、产品名或缩写等字面形式。可翻译的普通技术概念不能因为外观像名称就列为不翻译项；也不把正文中文反向扩写为原文没有的缩写。
2. 英文权威资料能证明概念、机制与名称拼写，通常不能单独证明某一个中文译法是唯一正确译法。中文首选有时只是本项目的编辑选择。
3. 原译含义准确、新译只是另一种写法时，尊重稳定译法。全称、简称、同义词和排版不应直接变成需要清零的错误。
4. 可读性改善仍可保留，但要说清收益。不能因为“旧译也说得通”就一概否定转义、三字符组、聚合状态等有消歧收益的修订。
5. 词条首选与具体句子的表达分开处理。完整词组优先，译名按对象和语法组词；每个发生修改的语义位置都核对 PG14—19 的适用版本。

项目现行 [译风规范](../../../tmp/ref/style.md) 第 8 行也要求不要因个人偏好替换历史译法。此前我虽然在若干理由里承认原译可以成立，迁移计划却仍把它们列入必须统一的新译集合，这一转换过于武断。

## 应恢复原表首选的 9 项

“恢复首选”指撤回词表或保护规则中缺乏充分依据的变化。其中若两种译法都正确，不意味着已经一致使用新译的六版正文也必须全部改回。

| 原序号 | 原词条与原译 | v2 词条与译法 | 复审理由 |
|---|---|---|---|
'''
    for category in ('R', 'O', 'C', 'K'):
        if category != 'R':
            titles = {
                'O': ('撤销强制迁移的 16 项', '这些新译可保留作正式词条、全称或首选；原译在同一已定义语境中也成立。没有必要为了它们制造一轮新的正向或反向改动。#561 的类型拼写勘误与中文 ID 写法分开处理。'),
                'C': ('保留但须明确语境的 13 项', '不少边界已经写在 v2 规则中；本轮确认这些条件必须生效，并补足容易过度扩写的对象和句法限制。不能把“需要遵守条件”误报为已发现正文违规。'),
                'K': ('保留的其余 30 项', '保留有可说明的收益。部分属于表达改进而非严格误译纠正，仍然不授权对中文旧词做无条件替换。'),
            }
            title, note = titles[category]
            report += f'\n## {title}\n\n{note}\n\n| 原序号 | 原词条与原译 | v2 词条与译法 | 复审理由 |\n|---|---|---|---|\n'
        for d in decisions:
            if d['category'] == category:
                report += f'| {d["id"]} | {pair(d["original"]["English"], d["original"]["中文"])} | {pair(d["v2"]["English"], d["v2"]["中文"])} | {esc(d["reason"])} |\n'

    report += '''
## 几项关键证据与证据边界

- B 树作为中文概念名称确有厂商中文材料用例；这支持“可以翻译”，不能推出 PostgreSQL 必须沿用该厂商的排版或词表。[Oracle 中文教程](https://www.oracle.com/ocom/groups/public/%40otn/documents/webcontent/229002_zhs.htm)
- 原作者分别使用 first-updater-win 和 first-committer-win。来源中的词形应保留；本轮不把该作者对并发机制的简化介绍当作所有 PostgreSQL 隔离级别的实现规范。[InterDB 5.8](https://www.interdb.jp/pg/pgsql05/08.html)、[InterDB 5.9](https://www.interdb.jp/pg/pgsql05/09.html)
- PG 的 combine function 合并两个部分聚合状态，transition function 更新聚合状态。这支持“合并”“状态转移”的消歧收益；不证明原“组合”“状态转换”在中文中必然错误。[PostgreSQL 自定义聚合](https://www.postgresql.org/docs/18/xaggr.html)
- PG 的 trigram 按三个连续字符定义。这为“三字符组”提供对象依据，不能外推为所有语言处理领域的 trigram 都是字符组。[PostgreSQL pg_trgm](https://www.postgresql.org/docs/18/pgtrgm.html)
- Kafka 的日志压实按键淘汰被后续更新覆盖的记录，区别于字节压缩。“压实”是为区别机制采用的中文选择。[Apache Kafka 设计说明](https://kafka.apache.org/41/design/design/)
- 页头字段实际写作 pd_checksum、pd_flags，pg_lsn 是类型；这些是可核对的对象或拼写依据。[PG 页布局](https://www.postgresql.org/docs/18/storage-page-layout.html)、[pg_lsn 类型](https://www.postgresql.org/docs/18/datatype-pg-lsn.html)
- TimeLineID 与 START WAL LOCATION 可分别核对类型声明及备份标签构造。这类勘误不能与“时间线标识改为时间线 ID”的中文选择混为一谈。[xlogdefs.h](https://raw.githubusercontent.com/postgres/postgres/REL_18_STABLE/src/include/access/xlogdefs.h)、[xlogbackup.c](https://raw.githubusercontent.com/postgres/postgres/REL_18_STABLE/src/backend/access/transam/xlogbackup.c)

恢复整页镜像、首部数据、连接类型和方式、百分位点和插入值，是本轮基于含义、中文表达与修改必要性的编辑判断。本轮没有找到能把对应 v2 新译确立为唯一权威中文、从而排除原译的依据；不能将“未证明必须修改”写成“新译已经证实错误”。此前引用的 GitBook 页面本次检索未取得百分位相关正文，因此不作为证明该词中文用法的依据。

## 配套文件与后续使用

- [候选完整词表](glossary.candidate.tsv)：631 条，9 项恢复原表首选，其他条目继承 v2。相对最初原表剩余 59 项字面净变化，**59 不是新的强制替换数量**。
- [候选逐条规则](glossary.rules.candidate.tsv)：631 条；同时修正关联的 backup block 和 Transaction ID Wraparound 规则。
- [候选别名表](aliases.candidate.tsv) 与 [候选字面保护表](preserve.candidate.tsv)：撤销 B-tree 概念名的强制保护，保留真实标识符；旧译的地位与逐条规则一致。
- [完整机器可读结论](decisions.json)：全部 68 条原译、v2、复审候选、理由和执行范围。
- [使用与执行补充](PROMPT-ADDENDUM.md)：用于修正旧开工提示词中的迁移假设。
- [校验结果](VALIDATION.json)：覆盖、数量、候选之间的对应关系、受保护输入的哈希及正文未修改核对。

旧准备包和旧执行台账是历史证据。后续若落实本轮结论，应将本补充与旧提示词一起使用；以本轮候选和适用条件解释词表，保留既有正确正文，并针对真实需要修正的位置完成六版一致性核对。
'''
    (HERE / 'REVIEW.md').write_text(report)
    print(json.dumps({'counts': dict(counts), 'glossary': len(glossary), 'rules': len(rules), 'aliases': len(aliases), 'preserve': len(preserve)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
