#!/usr/bin/env python3
"""Compile this run's measured evidence into formal translation tasks."""
import csv
import json
import re
from collections import Counter,defaultdict
from pathlib import Path
from sgml_index import Corpus,sha,visible
from analyze import PLAN,CFG,ROOT,STATE,REPORT,INITIAL,tsv,jsonl
csv.field_size_limit(32*1024*1024)


def read_tsv(path):
    return list(csv.DictReader(path.open(),delimiter='\t'))


def read_jsonl(path):
    return [json.loads(x) for x in path.open()]


def main():
    stats=json.loads((REPORT/'statistics.json').read_text())
    units=read_jsonl(REPORT/'translation-units.jsonl');hunks=read_tsv(REPORT/'hunks.tsv')
    inventory=read_tsv(REPORT/'inventory.tsv');changes=read_tsv(REPORT/'changes-summary.tsv')
    maps=read_tsv(REPORT/'structural-map.tsv');custom=read_tsv(REPORT/'project-customizations.tsv')
    source=json.loads((STATE/'target-source.json').read_text());releases=json.loads((STATE/'release-sources.json').read_text())
    # Generated differences are auxiliary evidence, never folded into raw
    # path counts. Their source scripts and external inputs are all hashed.
    genunits=[];genhunks=[]
    gc={v:Corpus(STATE/'generated'/v) for v in ['18.6','20']}
    for p in sorted((REPORT/'generated-diffs').glob('*.diff')):
        rel=p.name.removesuffix('.diff');lines=p.read_text().splitlines(True)
        starts=[i for i,x in enumerate(lines) if x.startswith('@@ ')]
        for no,i in enumerate(starts,1):
            m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',lines[i]);assert m
            body=''.join(lines[i:starts[no] if no<len(starts) else len(lines)])
            hid='GH20-'+sha(rel+'|'+body)[:16];uid='GU20-'+sha(hid)[:16]
            sides={}
            for v,start,length in [('18.6',int(m[1]),int(m[2] or 1)),('20',int(m[3]),int(m[4] or 1))]:
                d=gc[v].docs[rel];end=start+length-1
                segs=[x for x in d.segments if x['start_line']<=end and x['end_line']>=start]
                lo=min((x['start'] for x in segs),default=0);hi=max((x['end'] for x in segs),default=0)
                sides[v]={**d.ref(lo,hi),'text':d.text[lo:hi]}
            genhunks.append({'hunk_id':hid,'file':rel,'hunk_no':no,'old_start':m[1],'old_length':m[2] or 1,'new_start':m[3],'new_length':m[4] or 1,'diff_path':str(p),'unit_id':uid,'scope':'generated_output_not_authored_source'})
            genunits.append({'unit_id':uid,'file':rel,'source_scope':'generated_output','actions':['regenerate'],'hunk_ids':[hid],'old_english':sides['18.6'],'new_english':sides['20'],'pg18_chinese_source':str(STATE/'inputs/zh/18'),'status':'prepared_not_applied','disposition':'Reproduce from pinned PG20 inputs; inspect changed visible labels/descriptions separately from identifiers. Preserve inherited treatment of unchanged generated English; record any localization as a reproducible PG20 overlay, not a hand-edited disposable output.','generator_manifest':str(REPORT/'generated-files.json')})
    tsv(REPORT/'generated-hunks.tsv',genhunks)
    jsonl(REPORT/'generated-translation-units.jsonl',genunits)
    # Distinguish maximal roots from nested evidence and the functions wrapper.
    for row in maps:
        row['extraction_policy']='retain_anchor_then_apply_internal_delta'
        if row['anchor']=='functions':
            row['extraction_policy']='copy_chapter_opening_title_indexes_intro_and_closing_only;child_sections_are_separate_maps;install_PG20_entity_include_order'
        elif row['anchor'] in {'contrib-spi-refint','libpq-fastpath'}:
            row['extraction_policy']='historical_anchor_identity_only;replacement_obsolete_notice_changes_meaning;do_not_retain_removed_API_or_extension_body'
    tsv(REPORT/'structural-map.tsv',maps)
    anchor_evidence=[]
    for u in units:
        target_ref=u.get('new_english') or {}
        for field,label in [('old_english','18.6'),('historical_english','19beta3')]:
            old_ref=u.get(field) or {}
            alignment=u.get('english_alignment' if label=='18.6' else 'historical_alignment','')
            if alignment in {'exact_normalized','identical_content_after_id_zone_normalization'} and old_ref.get('anchor')!=target_ref.get('anchor') and old_ref.get('text') is not None and target_ref.get('text') is not None:
                anchor_evidence.append({'unit_id':u['unit_id'],'source_version':label,'old_file':old_ref['file'],'new_file':target_ref['file'],'old_anchor':old_ref['anchor'],'new_anchor':target_ref['anchor'],'comparison':alignment,'evidence':'same content; changed IDs/anchor context must be synchronized as structure, not first translated','status':'mapped_candidate_review'})
    tsv(REPORT/'historical-anchor-map.tsv',anchor_evidence,['unit_id','source_version','old_file','new_file','old_anchor','new_anchor','comparison','evidence','status'])
    # A shared group uses identical visible English, while the source SGML and
    # technical context remain independently reviewable. No automatic reuse.
    canonical=defaultdict(list)
    for u in units:
        en=(u.get('new_english') or {}).get('text','')
        if u['kind']!='shell' and len(visible(en))>=60:
            canonical[sha(visible(en))].append(u)
    cr=[]
    for key,group in sorted(canonical.items()):
        cr.append({'canonical_id':'CS20-'+key[:20],'unit_ids':[u['unit_id'] for u in group],'target_files':sorted({u['file'] for u in group}),'visible_english_sha256':key,'status':'reuse_one_confirmed_chinese_only_after_context_and_literal_review','reference_reuse':sorted({u['reuse'] for u in group})})
    tsv(REPORT/'canonical-groups.tsv',cr)

    tasks=[]
    def task(tid,batch,deps,targets,actions,hids=None,uids=None,ledger='',zh='',old='',new='',hist='',acceptance='',evidence='',status='pending_formal_execution'):
        row={'task_id':tid,'batch':batch,'dependencies':list(dict.fromkeys(deps)),'target_files':targets,'actions':actions,'hunk_ids':hids or [],'unit_ids':uids or [],'unit_ledger':ledger,'pg18_chinese_source':zh,'old_english':old,'new_english':new,'historical_reference':hist,'status':status,'acceptance':acceptance,'evidence':evidence}
        tasks.append(row);return tid
    pre=task('P20-INPUT',0,[],['zh/20'],['verify_frozen_inputs'],acceptance='Run verify_preparation.py --check-draft on first execution. On resume omit --check-draft and reconcile execution ledger hashes; never restore the whole inherited tree over later work.',evidence=str(REPORT/'source-manifest.json'))
    b1=[]
    for row in inventory:
        if row['action']!='unchanged':continue
        rel=row['path'];action='retain_project_customization' if rel in {x['path'] for x in custom} else 'copy_unchanged'
        b1.append(task('F20-'+sha(rel)[:12],1,[pre],['zh/20/'+rel],[action],zh=str(STATE/'inputs/zh/18'/rel),old=str(STATE/'inputs/en/18.6'/rel),new=str(ROOT/'en/20'/rel),acceptance='Verify the existing inherited file hash against inheritance-manifest.tsv; unchanged English is not permission to retranslate. Record baseline exceptions separately.',evidence=str(REPORT/'inventory.tsv'),status='inherited_pending_formal_audit'))
    gate1=task('P20-INHERITANCE',1,b1 or [pre],['zh/20'],['verify_inheritance'],acceptance='435 inherited source/resource files match initial draft provenance; excluded build products are not source inputs.',evidence=str(REPORT/'inheritance-manifest.tsv'))
    b2=[]
    map_tasks=defaultdict(list)
    for row in maps:
        if row['parent_mapping_id']:continue
        rel=row['new_file'];tid='S20-'+row['mapping_id'][4:]
        hids=[h['hunk_id'] for h in hunks if h['file'] in {row['old_file'],rel}]
        b2.append(task(tid,2,[gate1],['zh/20/'+rel],[row['action']],hids,[],zh=row['pg18_chinese_source'],old=str(STATE/'inputs/en/18.6'/row['old_file'])+'#'+row['anchor'],new=str(ROOT/'en/20'/rel)+'#'+row['anchor'],hist=str(REPORT/'historical-reuse.tsv'),acceptance=row['extraction_policy']+'; verify all nested mappings and preserved source SHA before old-path deletion.',evidence=str(REPORT/'mapped-diffs'/(row['mapping_id']+'.diff'))))
        map_tasks[rel].append(tid)
    # Unit batches: shells before body; actual old replacements/deletions after
    # all new-body tasks. Grouping is scheduling, not a license to batch-rewrite.
    buckets=defaultdict(list)
    resource_kinds={'build_resource','image_resource','generator_input','metadata','generated_table_or_version'}
    for u in units:
        batch=5 if u['actions']==['delete'] else 2 if u['kind']=='shell' else 4 if u['kind'] in resource_kinds else 3
        buckets[(batch,u['file'],tuple(u['actions']),u['reuse'])].append(u)
    pending=defaultdict(list)
    unit_tasks={}
    for (batch,rel,actions,reuse),group in sorted(buckets.items()):
        for offset in range(0,len(group),24):
            chunk=group[offset:offset+24];ids=[u['unit_id'] for u in chunk]
            tid='T20-'+sha('|'.join(ids))[:14]
            pending[batch].append((tid,rel,actions,reuse,chunk))
            for uid in ids:unit_tasks[uid]=tid
    gates={1:gate1}
    for batch in [2,3,4,5]:
        tids=list(b2) if batch==2 else []
        for tid,rel,actions,reuse,chunk in pending[batch]:
            deps=[gates[batch-1]]
            # Same-file ownership is required in the prompt. A batch barrier
            # prevents a unit deletion before its replacement is available.
            hids=sorted({h for u in chunk for h in u['hunk_ids']})
            z=sorted({(u.get('pg18_chinese') or {}).get('path','') for u in chunk}-{''})
            oe=sorted({(u.get('old_english') or {}).get('path','') for u in chunk}-{''})
            ne=sorted({(u.get('new_english') or {}).get('path','') for u in chunk}-{''})
            tids.append(task(tid,batch,deps,['zh/20/'+rel],list(actions),hids,[u['unit_id'] for u in chunk],str(REPORT/'translation-units.jsonl'),z,oe,ne,str(REPORT/'historical-reuse.tsv'),acceptance=f'Reuse class {reuse}. Read complete units, old/new contexts, and raw hunks. Candidate locations require semantic confirmation. Save before/after exact spans, terminology IDs, preserved text and validation. Old unpaired spans require replacement pairing, never automatic deletion.',evidence=str(REPORT/'hunks.tsv')))
        if batch==4:
            fixed=task('B20-FIX-SOURCE',4,[gates[3]],['bin/build_standalone_docsrc.sh','bin/build_standalone_pdfsrc.sh','zh/20/Makefile'],['update_structure','retain_project_customization'],acceptance='Implement optional PGDOC_SOURCE_DIR and PGDOC_SOURCE_COMMIT in both scripts before dynamic resolution. Validate exact commit, clean source and 20devel declaration, copy to fresh work tree, skip all branch/snapshot download paths. Set only zh/20 PG_VERSION=20. Keep old positional invocations/defaults compatible; verify failure cases and one stable-version smoke build.',evidence=str(PLAN/'BUILD-ADAPTATION.md'));tids.append(fixed)
            for row in custom:
                tids.append(task('C20-'+sha(row['path'])[:12],4,[fixed]+[t[0] for t in pending[4] if t[1]==row['path']],['zh/20/'+row['path']],['retain_project_customization'],zh=str(STATE/'inputs/zh/18'/row['path']),old=str(STATE/'inputs/en/18.6'/row['path']),new=str(ROOT/'en/20'/row['path']),acceptance='Retain recorded project delta and integrate only required PG20 upstream/build changes. Do not overwrite the standalone project Makefile with the upstream Makefile.',evidence=row['evidence']))
            for filename in sorted({u['file'] for u in genunits}):
                group=[u for u in genunits if u['file']==filename]
                tids.append(task('G20-'+sha(filename)[:12],4,[fixed],['zh/20/'+filename],['regenerate'],[h for u in group for h in u['hunk_ids']],[u['unit_id'] for u in group],str(REPORT/'generated-translation-units.jsonl'),str(STATE/'inputs/zh/18'),str(STATE/'generated/18.6'/filename),str(STATE/'generated/20'/filename),acceptance='Generate in isolated build workspace from the exact PG20 generator and external inputs; review generated visible-English delta. Do not add a disposable generated table as an authored source file or retain PG18 table contents.',evidence=str(REPORT/'generated-files.json')))
            tids.append(task('G20-VERSION',4,[fixed],[str(STATE/'execution/builds/generated/version.sgml')],['regenerate'],old=str(STATE/'upstream-pg18.6/postgresql-18.6/configure'),new=str(STATE/'upstream-pg20/configure'),acceptance='Use configure/make in the isolated build to generate version=20devel and majorversion=20; retain a copy at target_files for evidence, and confirm HTML/PDF visible version independently.',evidence=str(STATE/'target-source.json')))
        if batch==5:
            for row in inventory:
                if row['action']!='deleted':continue
                rel=row['path'];deps=[gates[4]]+list(tids)
                tids.append(task('D20-'+sha(rel)[:12],5,deps,['zh/20/'+rel],['delete'],[h['hunk_id'] for h in hunks if h['file']==rel],zh=str(STATE/'inputs/zh/18'/rel),old=str(STATE/'inputs/en/18.6'/rel),acceptance='Delete only this obsolete PG20 target path after every affected mapping/replacement is verified and saved; update entity/include/xref chains. Frozen PG18 and all old-version trees remain unchanged.',evidence=str(REPORT/'structural-map.tsv')))
            tids.append(task('P20-BASELINE',5,[gates[4]],['zh/20'],['baseline_unresolved'],acceptance='Triage every baseline-id-issues.jsonl item and all low-confidence Chinese candidates. Missing IDs are not automatically missing translations; extra IDs may be local structure. Verify unchanged-English baseline discrepancies separately, document necessary PG20 corrections or exact remaining unresolved scope.',evidence=str(REPORT/'baseline-issues.md')))
        gates[batch]=task(f'P20-BATCH-{batch}',batch,tids or [gates[batch-1]],['zh/20'],['verify_batch'],acceptance='All prior tasks have evidence-backed dispositions; unresolved items remain explicitly open. Reconcile same-file edits and canonical shared meanings before the next batch.',evidence=str(PLAN/'TASKS.tsv'))
    audit=task('A20-SOURCE',6,[gates[5]],['zh/20'],['audit_source'],acceptance='Verify all raw/generated hunks and units, unchanged Chinese provenance, tags/entities/IDs/linkend/endterm/zone/otherterm, include closure, visible indexes, literals/numbers and current terminology. Include independent strict structural/link checks; inherited relaxed HTML validation is insufficient.',evidence=str(PLAN/'TRANSLATE-PG20.md'))
    builds=[]
    for flavor in ['HTML','A4','US']:
        artifact=STATE/'execution/builds'/('html/index.html' if flavor=='HTML' else f'postgresql-20-zh-{flavor}.pdf')
        builds.append(task('B20-'+flavor,7,[audit,'B20-FIX-SOURCE'],[str(artifact)],['build_'+flavor.lower()],acceptance='Actual build from exact pinned PG20 source and final Chinese tree. Keep stdout/stderr/internal FOP log, exit code, input SHA, artifact SHA/path and visible 20devel version. check-deps is not build evidence.',evidence=str(PLAN/'BUILD-ADAPTATION.md')))
    visual=task('A20-RENDER',8,builds,['PG20 HTML and A4/US PDF'],['verify_rendered_output'],acceptance='Inspect added/changed/moved pages, TOC/index, CJK fonts, code and tables in HTML and both PDFs; record exact pages/screenshots and inherited versus new diagnostics.',evidence=str(PLAN/'PLAN.md'))
    task('P20-DELIVER',9,[visual],['zh/20','execution ledgers and artifacts'],['deliver'],acceptance='Deliver source diff, complete task/unit ledgers, terminology decisions, provenance, actual HTML/A4/US artifacts and unresolved baseline items. No commit, push or publication.',evidence=str(PLAN/'TRANSLATE-PG20.md'))
    tasks.sort(key=lambda t:(t['batch'],t['task_id']))
    tsv(PLAN/'TASKS.tsv',tasks)
    stats['generated_hunks']=len(genhunks);stats['generated_units']=len(genunits);stats['tasks']=len(tasks);stats['canonical_groups']=len(cr);stats['canonical_repeated_groups']=sum(len(x['unit_ids'])>1 for x in cr)
    stats['task_batches']=dict(sorted(Counter(t['batch'] for t in tasks).items()))
    stats['first_translation_candidate_files']=sorted({u['file'] for u in units if u['reuse']=='no_aligned_history_first_translation_candidate'})
    stats['history_exact_files']=sorted({u['file'] for u in units if u['reuse']=='pg19_exact_english_candidate'})
    stats['low_confidence_chinese_units']=sum((u.get('pg18_chinese') or {}).get('confidence') in {'file_context_only','anchor_context_only'} for u in units)
    (REPORT/'statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    active=['style.md','exclude.tsv','glossary.tsv','glossary.rules.tsv','glossary-aliases.tsv','terms-to-preserve.tsv','change.md']
    rf={n:INITIAL['inputs']['tmp/ref']['files'][n] for n in active}
    active_sha=sha(''.join(n+'\t'+rf[n]['sha256']+'\n' for n in sorted(rf)))
    manifest={'run':CFG,'project_git_head':INITIAL['git_head'],'project_branch':INITIAL['git_branch'],'git_start_status':str(STATE/'git-status-start.txt'),'git_start_diff':str(STATE/'git-diff-start.patch'),'target':source,'english_18_6':INITIAL['inputs']['en/18.6'],'chinese_18':INITIAL['inputs']['zh/18'],'historical_english_19beta3':INITIAL['inputs']['en/19beta3'],'historical_chinese_19':INITIAL['inputs']['zh/19'],'rules':{'frozen_root':str(STATE/'inputs/tmp/ref'),'live_root':str(ROOT/'tmp/ref'),'active_files':rf,'active_tree_sha256':active_sha,'full_snapshot_tree_sha256':INITIAL['inputs']['tmp/ref']['tree_sha256'],'extra_snapshot_file':'calibrate.md is archived context, not a higher-priority translation rule'},'releases':releases,'official_local_comparison':json.loads((STATE/'baseline-upstream-comparison.json').read_text()),'inheritance':{'target':str(ROOT/'zh/20'),'file_count':INITIAL['inheritance']['inherited_count'],'manifest':str(REPORT/'inheritance-manifest.tsv'),'status':'PG18_inherited_draft_NOT_PG20_adapted','excluded_generated':INITIAL['inheritance']['excluded_generated'],'pending_metadata':INITIAL['inheritance']['pending_metadata']},'generated_tables_manifest':str(REPORT/'generated-files.json'),'statistics':stats,'preparation_only':True,'body_translation_performed':False,'html_pdf_builds_performed':False}
    (REPORT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    # Human-readable scope tables avoid conflating file additions with entirely
    # new body text. Titles, indexes and whitespace are explicit separate units.
    ranges=[]
    for rel in sorted({u['file'] for u in units}):
        us=[u for u in units if u['file']==rel];c=Counter(u['reuse'] for u in us)
        ranges.append({'file':rel,'raw_action':next((x['action'] for x in inventory if x['path']==rel),'mapped_target'),'pg18_exact_units':c['pg18_exact_english'],'pg19_exact_candidates':c['pg19_exact_english_candidate'],'pg19_partial_context':c['pg19_partial_context_candidate'],'no_aligned_history_first_candidates':c['no_aligned_history_first_translation_candidate'],'old_removal_or_replacement_spans':c['old_source_saved_before_removal'],'structure_or_resource_units':sum(c[k] for k in ['structure_or_formatting','resource_or_structure','literal_or_structure_review']),'scope_status':'prepared; semantic and terminology acceptance remains formal work'})
    tsv(REPORT/'translation-scope.tsv',ranges)
    tsv(PLAN/'TERMS-NEW.tsv',[],['term_id','english','chinese','context','unit_ids','existing_family','official_evidence','decision','status'])
    (PLAN/'LEDGER-SCHEMA.json').write_text(json.dumps({'unit_id':'required existing U20/GU20 ID','task_id':'required existing task ID','status':['pending','in_progress','applied','reused','deleted','structure_only','literal_synced','regenerated','verified','baseline_unresolved'],'source_commit':source['commit_sha'],'input_files':'path and SHA256 of every used input','reuse_basis':'PG18 or PG19 exact/context reference plus semantic confirmation','before':'target path, original char offsets, exact text and SHA256','after':'target path, final offsets, exact text and SHA256','context_decision':'why this unit needs the selected action; preserve unchanged subspans','term_rule_ids':'current frozen rules plus logged later user decisions','canonical_group':'confirmed shared Chinese with context exceptions','checks':'structural, literal/numeric, terminology, hunk coverage, rendered evidence','unresolved_reason':'required while unresolved; never mark verified without evidence'},ensure_ascii=False,indent=2)+'\n')
    render_docs(stats,source,manifest,units,maps,tasks)
    print(json.dumps({'tasks':len(tasks),'generated_hunks':len(genhunks),'active_rules_sha256':active_sha,'low_confidence_units':stats['low_confidence_chinese_units']},ensure_ascii=False,indent=2))


def render_docs(st,source,manifest,units,maps,tasks):
    oldhash=manifest['chinese_18']['tree_sha256'];rulehash=manifest['rules']['active_tree_sha256'];commit=source['commit_sha']
    s,r,p=str(STATE),str(REPORT),str(PLAN)
    count=st['reuse'];first=count.get('no_aligned_history_first_translation_candidate',0);hist=count.get('pg19_exact_english_candidate',0);partial=count.get('pg19_partial_context_candidate',0)
    baseline=read_jsonl(REPORT/'baseline-id-issues.jsonl')
    missing=[x for x in baseline if x['kind']=='missing_chinese_id_candidate']
    btext='\n'.join(f"- `{x['anchor']}`：`en/{x['version']}/{x['english_file']}:{x['english_line']}`；PG20 保留该 ID：{x['target_pg20_present']}。" for x in missing)
    (REPORT/'baseline-issues.md').write_text(f"""# 基线问题与准备边界

英文来源已解决：本地 en/18.6 的 435 个文件、en/19beta3 的 491 个文件均与本轮重新取官方 SHA256 核验的源码包逐字节一致，没有本地英文偏差。本地两版文档树与相应官方源码包的文档路径集合也一致；七个 GENERATED_SGML 目标均不在这两棵输入树中，不能称为 PG20 删除功能。完整结果见 source-manifest.json 与 generated-files.json。

中文基线来自 {INITIAL['started_at']} 冻结的工作区，当前入口是今天的术语订正 GO，九项回退有效；不是从 Git HEAD 导出。zh/20 的 435 个继承文件尚未适配 PG20，Makefile PG_VERSION=18.6 原样保存，生成占位 pgdoccn-notes.sgml 已排除，未复制 HTML/PDF/FO/展开 XML。stylesheet.css.xml 是上游构建输入，images/*.svg 是随源码供构建使用的资源，保留它们不等于保留构建输出。

本轮索引发现 {len(baseline)} 条基线 ID 差异候选：PG18 有 {len(missing)} 个英文 ID 在中文缺位、36 个中文额外 ID；PG19 没有英文 ID 缺位，有 45 个中文额外 ID。已过滤 zh18-auto-* 项目自动 ID。这些数字描述结构差异，不证明同数目的缺文；逐条英文上下文在 baseline-id-issues.jsonl。额外 ID 可能是旧版本残留、人工结构或重命名，应按对应英文定位复核。不能把这些历史问题算成 PG20 新功能。

{btext}

译文定位仍有 {st['low_confidence_chinese_units']} 个语义单元只有章节或文件语境；必须在正式阶段补足段落/表格/列表对应证明。其他基于 ID、同标签路径、字面签名的定位也标为 candidate，尚未作人工语义验收。词表别名扫描有 {st['terminology_review_candidates']} 条观察，仅用于检索；当前观察里的“百分位数”可能属于独立 discrete percentile 词条，禁止据此批量替换。

结构迁移共 {st['structural_mapping_rows']} 条锚点记录，其中 40 个根映射（35 个跨路径根、5 个同文件重归属根）。functions 章总节点与其拆分子章节的旧范围重叠，章映射只提取章头/简介/章尾，不计为又复制了一份全部函数章。refint 与 libpq-fastpath 的旧锚点迁到废弃附录，但正文改为删除/弃用说明，不能因 ID 相同就沿用过时的 API/扩展描述；查看 mapped-diffs。

release-20.sgml 当前上游仅有 Release 20、2026-??-?? 和占位说明。这是所固定源码的真实内容；正式翻译应如实承接，不推断发布日期，不把 PG19 发布说明整篇移植到 PG20。PG19 旧工作流中的 PROPERTY GRAPH 三个命令页不在本轮目标中，不能从旧任务表复活它们。

构建能力尚待正式阶段适配：当前两个脚本会动态查询分支、可能接受无法由源码内容证明的 snapshot 标记；没有固定源码参数。B20-FIX-SOURCE 明确安排最小兼容改动。本轮依赖检查通过，GNU Make、DocBook catalog 与中文字体可见；fop 不在 PATH，但项目 FOP 2.11 缓存存在。这不是 HTML 或 PDF 构建成功证明。本轮仅实际生成两版共 12 张生成表，未构建中文底稿。

既有术语订正报告记录过监控表阶段字面译法、历史链接/缺位和 BKI PDF 长行越界。此处不搬用旧数字为 PG20 验收；正式阶段独立检查新输出并区分继承问题与新增问题。只允许为目标 PG20 的真实缺口做有证据的必要处置，不扩大成整章重译或回改 PG14—19。
""")
    (REPORT/'README.md').write_text(f"""# PostgreSQL 18.6 → 20devel 准备交付

状态：两个准备阶段完成；PG20 增量正文翻译尚未执行。正式入口为 [{PLAN/'TRANSLATE-PG20.md'}]({PLAN/'TRANSLATE-PG20.md'})。

固定上游：[官方镜像提交 {commit}](https://github.com/postgres/postgres/commit/{commit})；提交时间 {source['commit_time']}，下载验证时间 {source['download_verified_at']}。configure.ac、configure、meson.build 均声明 20devel；目录名为 20。完整源码留在 `{s}/upstream-pg20`，处于 detached HEAD；Git 对象及 7,680 个源码文件有校验清单。在线 devel 页当时构建自 140fdfcdf12，未将它冒充本次固定提交。

PG18 中文工作区快照：`{s}/inputs/zh/18`，树 SHA256 `{oldhash}`。435 个继承文件在 zh/20；现用七项规则集合 SHA256 `{rulehash}`，位于 `{s}/inputs/tmp/ref`。PG19 参考只来自固定的当前 zh/19 及经官方校验的 en/19beta3；它不替代 PG18 主基线。

| 原始路径指标 | 实测 |
|---|---:|
| 旧 en/18.6 文件 | 435 |
| 新 en/20 文件 | 488 |
| 不变 | 254 |
| 修改 | 179 |
| 删除 | 2 |
| 新增 | 55 |
| 文件联合集 | 490 |
| 原始 hunk | 1,133 |
| 原始新增/删除行 | +45,519 / -48,461 |
| SGML 新增/删除/修改/不变 | 42 / 2 / 169 / 218 |
| 二进制变化 / 类型变化 | 0 / 0 |

435 = 254 + 179 + 2；488 = 254 + 179 + 55。原始全量 diff 包含 func.sgml 与 release-18.sgml 的删除，不按重命名展示抵消行数。35 个跨路径根映射中，32 个来自 func.sgml，另有 RADIUS、fast-path 和 refint；5 个根映射记录 logicaldecoding 内部归属变化。全部 276 条锚点映射含嵌套证据，不能当成 276 次独立搬移。

逐块分析形成 {st['units']:,} 个完整语义/结构单元，包括空白、注释、旧内容删除和替换配对；不是同数目的待翻译段落。分类中 PG18 英文完全匹配的继承/搬移单元 {count.get('pg18_exact_english',0):,} 个，PG19 英文完全匹配的历史中文候选 {hist:,} 个，PG19 部分语境参考 {partial} 个，未找到对齐历史基础的首次翻译候选 {first} 个。其余是结构/资源、旧片段删除或少量仅有 PG18 变更语境的单元；详见 statistics.json 与 translation-scope.tsv。

上述“完全匹配”指英文字节或仅忽略非字面块空白、注释及 id/zone 属性的内容比较，代码块及链接目标不会被归一化丢弃。结构属性仍由原始 diff 与 historical-anchor-map.tsv 跟踪；中文均保留候选状态并提供独立路径/锚点/行号/哈希，不表示已经翻译、校准或审核完毕。{first} 个首次候选也可能在人工缩小单元后找到部分共用译文，因此任务先核对语境，绝不整文件重译。

生成文件另表：分别运行本版生成器，12 次命令退出 0；派生差异 {st['generated_hunks']} 块，不混入 1,133 个 authored-source 原始 hunk。外部输入包括 src/backend/catalog/sql_feature_packages.txt、sql_features.txt、src/backend/utils/errcodes.txt、src/include/parser/kwlist.h、src/backend/utils/activity/wait_event_names.txt 及其生成脚本；全部路径、命令和哈希在 generated-files.json。

## 可直接读取的交付

- [source-manifest.json](source-manifest.json)：源码、中文、规则身份及完整校验信息。
- [inventory.tsv](inventory.tsv)、[changes-summary.tsv](changes-summary.tsv)、[full.diff](full.diff)、diffs/：递归全部路径、原始逐文件/逐块差异；新增与删除文本文件同样保留差异。
- [hunks.tsv](hunks.tsv)、[translation-units.jsonl](translation-units.jsonl)：原始行范围、变动行、SGML 锚点、完整单元及中英文语境。
- [structural-map.tsv](structural-map.tsv)、mapped-diffs/：章/节与嵌套锚点迁移及迁移后的内部差异。
- [historical-reuse.tsv](historical-reuse.tsv)、[translation-scope.tsv](translation-scope.tsv)、[canonical-groups.tsv](canonical-groups.tsv)：PG18/PG19 复用证据与可协调的共有含义。
- [generated-files.json](generated-files.json)、[generated-hunks.tsv](generated-hunks.tsv)、[generated-translation-units.jsonl](generated-translation-units.jsonl)：两版生成表及上游树外依赖。
- [inheritance-manifest.tsv](inheritance-manifest.tsv)、[project-customizations.tsv](project-customizations.tsv)：中文复制来源，以及 Makefile、CSS、XSL 三项项目定制。
- [baseline-issues.md](baseline-issues.md)、[baseline-id-issues.jsonl](baseline-id-issues.jsonl)、[terminology-review.tsv](terminology-review.tsv)：基线未决和语境观察。
- [{PLAN/'TRANSLATE-PG20.md'}]({PLAN/'TRANSLATE-PG20.md'})、[TASKS.tsv]({PLAN/'TASKS.tsv'})、[PLAN.md]({PLAN/'PLAN.md'})：已填入本轮实测数据的正式执行材料。

本轮检查和方法限制见 [preparation-validation.json](preparation-validation.json)；审计器使用五棵固定 SGML 树，词法标签配对错误为 0，但这不替代正式阶段的 DTD/引用验证。源码和规则漂移通过 SHA256 核对；原始 diff 应用到隔离的英文旧树后重建 en/20 的文件与内容。未提交、推送或发布。
""")
    build_doc=f"""# PG20 固定源码构建适配

本次只给出可执行设计和任务 B20-FIX-SOURCE，尚未修改公共脚本，也没有构建 PG20 中文。

现有 HTML 脚本第 143—235 行、PDF 脚本第 219—297 行的 resolve_git_ref/sync_git_checkout 动态查询开发分支；HTML 第 237—265 行、PDF 第 378—401 行准备源码。snapshot 的 .pgdoc-upstream-ref 只是查询得到的标记，不能证明日更压缩包内容相符。源码固定必须在这些分支之前处理。

最小兼容实现：给两个脚本添加可选环境变量 PGDOC_SOURCE_DIR、PGDOC_SOURCE_COMMIT。两项同时提供时，读取该目录真实 Git HEAD，要求等于指定完整提交，要求 Git tracked 内容无修改，并核对 configure.ac/configure/meson.build 的版本声明。核验通过后，将源码复制到独立 work_tree（排除 .git），完全跳过在线 ref 查询、clone 和 snapshot 分支；日志写入提交、源码目录及各输入哈希。两项没有提供时保持全部现有版本位置参数、稳定包路径与默认行为；只提供一项时明确报错。不要在固定路径失败后悄悄回退联网。

本轮固定源码目录：`{s}/upstream-pg20`；提交：`{commit}`。该目录已 detached，7,680 个文件的 SHA256 在 `{s}/upstream-pg20-files.json`，继续使用前必须复核。不要直接在缓存源码中 configure 或覆盖中文；每个构建在新工作目录进行。

zh/20/Makefile 当前为 PG18 原样继承，正式阶段仅将 PG_VERSION 默认设为 20；脚本版本位置参数传 20，目标目录也为 20，真实显示版本必须由固定源码生成的 version.sgml 得到 20devel。顶层 VERSION、ZH_VERSIONS、EN_VERSIONS 和旧版输出位置保持现状。en/20/Makefile 是完整上游 Makefile，依赖上游源码树，不能把它作为独立项目 Makefile 直接覆盖 zh/20/Makefile。

适配后执行的命令如下（这些命令依赖 B20-FIX-SOURCE 已完成）：

```bash
cd /Users/vonng/pgsty/pgdoc
export PGDOC_SOURCE_DIR='{s}/upstream-pg20'
export PGDOC_SOURCE_COMMIT='{commit}'
KEEP_WORK=1 bin/build_standalone_docsrc.sh zh/20 zh 20 '{s}/execution/builds/html'
KEEP_WORK=1 bin/build_standalone_pdfsrc.sh zh/20 zh 20 '{s}/execution/builds/postgresql-20-zh-A4.pdf' A4
KEEP_WORK=1 bin/build_standalone_pdfsrc.sh zh/20 zh 20 '{s}/execution/builds/postgresql-20-zh-US.pdf' US
```

逐项重定向完整日志到 execution/builds，检查退出码；同时保存 work_tree 内的 configure、make、FOP 日志及源码/产物 SHA256。FOP 不在 PATH 时现有 .cache/tools/fop-2.11/fop/fop 可用，字体使用已检出的 Alibaba PuHuiTi 3.0 与 Courier New；仍需实际查看两个纸型的字体、代码和表格。

验证公共脚本改动：bash -n；原有位置参数和稳定包分支仍可用；精确提交/版本不匹配与脏输入应失败；固定源码模式确认未进入 git ls-remote/clone/download 分支；实际 PG20 HTML、A4/US PDF；另在独立输出目录做一次 PG18.6 HTML 兼容性冒烟构建，不更改旧版源文件。新中文不会因为 HTML 脚本把 --valid 放宽为 --catalogs --loaddtd 就视为引用合格，必须独立检查包含链、重复 ID、linkend/endterm/zone/otherterm 以及未闭合实体。

两版生成表本轮已实际重建，见 generated-files.json。PG20 正式构建必须用 PG20 生成器与对应源码输入。需要本地化本轮新增或变更的生成说明时，保留可再生成的 PG20 专用覆盖步骤和逐项台账；不要直接提交构建目录中的派生表，也不要为此重译英文未变的整张表。
"""
    (PLAN/'BUILD-ADAPTATION.md').write_text(build_doc)
    prompt=f"""# 正式执行：PostgreSQL 20devel 中文增量翻译

请实际完成本轮正式翻译与验收。当前准备已经完成；这份提示词被明确交付执行后，才开始翻译。工作目录 `/Users/vonng/pgsty/pgdoc`。唯一中文目标 `/Users/vonng/pgsty/pgdoc/zh/20/`。不提交、推送或发布。

## 固定身份与先读材料

- 上游为 PostgreSQL 官方 GitHub 镜像 master 上已固定的完整提交 `{commit}`，提交时间 `{source['commit_time']}`，版本声明 `20devel`。固定完整源码 `{s}/upstream-pg20`；英文目标 `/Users/vonng/pgsty/pgdoc/en/20`，488 个文件。
- 唯一主英文差异：`en/18.6 → en/20`。冻结英文旧树 `{s}/inputs/en/18.6`，435 个文件，与官方 18.6 源码包逐字节一致；不使用 en/current，不改为 19→20。
- 中文主底稿是本轮开工工作区冻结的 `{s}/inputs/zh/18`，树 SHA256 `{oldhash}`；zh/20 已继承 435 个源文件/资源。它仍是 PG18 底稿，PG_VERSION=18.6 未适配，不能当作已经完成的 PG20。
- 现用规则固定在 `{s}/inputs/tmp/ref`，七个生效文件集合 SHA256 `{rulehash}`。读取其中 style.md、exclude.tsv、glossary.tsv、glossary.rules.tsv、glossary-aliases.tsv、terms-to-preserve.tsv、change.md。目录中额外的 calibrate.md 仅作历史背景。
- 历史可复用来源：`{s}/inputs/en/19beta3` 与 `{s}/inputs/zh/19`。英文已与官方 19beta3 源码包 491 个文件逐字节核验；不能整树复制中文 PG19 代替 PG18。
- 完整报告 `{r}`。先读取 README.md、source-manifest.json、baseline-issues.md、translation-scope.tsv、structural-map.tsv、project-customizations.tsv；随后按具体任务读 raw diffs、hunks.tsv、translation-units.jsonl 和 historical-reuse.tsv。
- 执行任务表 `{p}/TASKS.tsv`，共 {st['tasks']} 行；执行计划 `{p}/PLAN.md`；固定源码适配 `{p}/BUILD-ADAPTATION.md`；台账字段 `{p}/LEDGER-SCHEMA.json`。`python3 '{p}/scripts/task_view.py' TASK_ID` 可输出一个任务及全部中英文单元，不执行修改。

首次执行先运行 `python3 '{p}/scripts/verify_preparation.py' --check-draft`。续作运行同脚本但不带 --check-draft，并核对 `{s}/execution` 的实际修改台账。不要重新初始化或覆盖 zh/20 中已完成的工作。源文件、规则或上游提交若漂移，记录具体文件和哈希差异；有用户后续订正则落实该明确决定，保留新旧规则身份，不静默混用，也不默认重新抓 master。

## 实测范围

完整路径：新增 55、删除 2、修改 179、不变 254；原始 1,133 个 hunk，+45,519/-48,461 行。SGML 是新增 42、删除 2、修改 169、不变 218；其余为图片、脚本、生成输入、样式和元数据。类型变化和二进制变化均为 0。共有源文件不能整文件重译。

276 条结构锚点记录含 40 个根映射：func.sgml 拆为 32 个目标文件，RADIUS、libpq fast-path、refint 各迁到一个废弃附录；另外 5 个为 logicaldecoding 同文件归属调整。32 是本次实测，完整列表在结构表，不引用旧 PG19 文件清单。functions 章映射只搬章头、简介和章尾，子节按各自映射搬移；先保存并验证全部中文片段，再删除目标旧 func.sgml。libpq-fastpath/refint 的锚点虽继承，正文已改为废弃/移除说明，要按新语义更新。

{st['units']:,} 个原始差异语义/结构单元中，有 {count.get('pg18_exact_english',0):,} 个 PG18 英文完全匹配继承/迁移单元、{hist:,} 个 PG19 英文完全匹配的中文候选、{partial} 个 PG19 部分语境参考、{first} 个无对齐历史基础的首次翻译候选。其余包含结构、注释、空白、资源及旧片段删除/替换配对，不能当成首次翻译工作量。生成表另有 {st['generated_hunks']} 个辅助 hunk，见 generated-hunks.tsv 与 generated-translation-units.jsonl；它们不抵消主差异。

## 翻译合同

1. 只处理英文新增或发生实际变化的内容；英文未变的 PG18 中文原样复用，不整文件重译，不顺手润色。同一文件允许同时有 copy_unchanged、relocate_or_split、delete、update_structure、translate_new_content、translate_changed_content、sync_literal_or_resource、regenerate、retain_project_customization、baseline_unresolved 等动作；不能为便于分工把文件全标为一种正文翻译动作。
2. 内容比较仅允许忽略非字面块空白、注释和 id/zone 属性，不能丢弃代码或链接目标。id/zone 的原始变化仍必须同步；historical-anchor-map.tsv 记录新增 ID/更名的复用线索。新路径先查结构来源；已有文件新增段落同样先查历史译文。搬移/拆分先使用 PG18 中文，再处理该片段内部英文增量。历史复用必须证明所对应的 PG19beta3 英文与目标片段一致，局部不同则只借用共有内容。old_english/historical_english 标为 structural_path_candidate 或 partial_context 时只是导航，绝非自动替换依据。
3. 按章节 ID、实体入口、标题、相邻段落、列表/表格结构与字面签名定位中文。char_start/char_end 是从零计数的 Unicode 字符偏移，右端不含；行号从一计数，片段 SHA256 基于 UTF-8 字节。所有行号分别来自各自文件；绝不把英文行号用于中文编辑。单位 text 是完整语义上下文，context 字段可能指整章，只供阅读，实际修改范围限于原始差异对应的文本节点。逐项确认边界再写入。
4. 纯移动、空白、注释、结构和代码变动分别处置。旧侧 unpaired_old_span 是尚需与目标替换配对的片段，不是已确认功能删除；同一文件先处理新增/修改，再核对删改台账，避免重复删除替换内容。旧文件删除仅限 zh/20，必须在所有迁移片段保存并核对后进行；同时维护包含链、索引和交叉引用。
5. PG20 英文决定最终技术事实、条件、数值、函数/参数、代码示例及 SGML 层级。原文变更的代码、名称和例子原样同步新版本；保护字面形式不是保留过时 PG18 示例的理由。没有变化的字面内容和手工排版继续保留。不能将所有内联标签内容一概冻结：title、indexterm 可见索引、replaceable 占位说明、lineannotation 和说明性 type/literal 等须按语境判断；真实标识符和命令值必须保护。
6. 规则顺序：先确认对应版本英文语义，再按 exclude.tsv 保护真实字面形式，再按 glossary.tsv 与逐条适用规则选译名，最后应用译风与稳定既有中文。glossary-aliases.tsv 只用于检索/消歧，不作为批量替换字典。禁止用 plans/terminology-14-19/refs 的旧 v2 或 reconsideration 候选整体覆盖当前规则。
7. 九项已确认译法继续有效：B-树、默认 B-树操作符类、以先提交者为准、以先更新者为准、整页镜像、首部数据、连接类型和方式、百分位点、插入值。只按完整词条和语境应用，discrete percentile 的离散百分位数独立处理。继续区分 index vacuuming/索引清理与并列 index cleanup/索引收尾清理，保留 streaming=parallel 的并行应用动作和字符输入转义等现行订正。
8. 同一英文含义出现在多个章节或历史版本时，复用一份确认的中文；canonical-groups.tsv 提供检索组，结构/字面/适用条件不同须记录例外。只读核对并利用 PG14—19，不因 PG20 特性回改旧版，也不能抹平真实大版本差异。一个文件在同一阶段由同一执行者统一处理，其关联术语族使用同一决策记录。
9. 新术语仅对本轮真实新增概念定稿，先查现有同族和技术语境，在 `{p}/TERMS-NEW.tsv` 或 execution 的可追溯术语台账记录英文、中文、单元、依据与决定。不重开既有正确词条的审美修订。输入规则保持冻结；需要记录后来用户订正时单独追加来源和哈希。
10. 不调用通用翻译 API 批量重译，不从网上拼接中文手册。可复用本项目已与英文核对的中文，必要技术查证用固定官方源码及官方文档。release-20.sgml 的日期和说明当前是上游占位，保持其真实开发状态，不编造发布日期或移植 PG19 发布说明。

## 执行与台账

按 TASKS.tsv 的 dependencies 组成的有向无环图执行，batch 是粗粒度阶段，不能仅按 task_id 字面顺序运行；P20-BATCH-* 是阶段核对任务。首次动作是检查现有继承底稿，随后进行结构迁移、增量内容、资源/生成/固定构建适配、删除与基线复核、源码验收、实际构建及视检。新建 `{s}/execution` 保存逐单元台账、目标文件工作前后快照、术语记录、检查和日志。

每个原始/生成 hunk 必须关联实际处置，每个语义单元恰好由一个内容任务负责（结构映射任务提供同一内容的来源证据，不重复翻译）。逐单元记录输入来源与哈希、复用方式、修改前后精确片段、语境判断、当前术语规则 ID、独立检查及未决原因。文件存在、有中文、marker 或自报完成都不能作为完成证明。词法定位候选与 {len(baseline)} 条基线 ID 差异要经过审查；未变英文的基线问题单列，必要修复须有同版英文及目标 PG20 需求依据，不伪装成 PG20 增量，不因此整章重译。

## 验收与交付

- 目标目录、包含链、实体、ID 与 PG20 对齐；新增没有遗漏，删除没有错误残留，35 个跨路径根映射及 5 个同文件归属调整全部有处置证据。
- 1,133 个原始 hunk、{st['generated_hunks']} 个生成 hunk 与所有单元覆盖可审计；未决项不能标为完成。未变化中文有文件哈希/片段映射证明，额外修改逐项有必要性与来源。
- 独立检查标签/实体、重复与缺失 ID、linkend/endterm/zone/otherterm、包含文件、可见索引、代码/示例、数字和版本条件、当前术语。原脚本放宽中文 IDREF 验证，HTML 构建成功不代替这些检查。
- 按 BUILD-ADAPTATION.md 完成固定源码参数的最小兼容改动；不改旧版默认目标。使用同一固定 PG20 源码和最终中文实际构建 HTML、A4 PDF、US PDF，显示为 20devel；保存命令、退出码、内部日志、最终源码哈希与产物哈希/路径。
- 检查代表性新增页（如 pgplanadvice/ref/repack/func-tid）、实际变更页（monitoring/config/mvcc）、结构迁移页（函数子树、废弃附录）、目录/索引，以及两个 PDF 的中文字体、代码和表格。记录具体可见结果、继承问题与本轮新增问题；check-deps 不能代替实际构建和视检。
- 最终提供 zh/20 源码差异、动作/翻译台账、术语记录、完整 PG20 源码身份、三个实际构建产物、验证结果、基线问题和确切未决项。不要提交、推送或发布。

现在从 P20-INPUT 开始，持续完成上述正式任务；断点续作先对照台账，不覆盖已有成果。
"""
    (PLAN/'TRANSLATE-PG20.md').write_text(prompt)
    rows='\n'.join(f'| {k} | {v} |' for k,v in st['task_batches'].items())
    firstpaths='\n'.join('- `'+x+'`' for x in st['first_translation_candidate_files'])
    (PLAN/'PLAN.md').write_text(f"""# PG20 正式执行计划

准备阶段一、二均已完成，本次停在生成正式翻译提示词；未执行新增/变更正文翻译。唯一执行入口为 [TRANSLATE-PG20.md](TRANSLATE-PG20.md)，任务源 [TASKS.tsv](TASKS.tsv)，固定提交 `{commit}`。

输入和所有绝对路径见 [RUN.json](RUN.json) 与 [{r}/source-manifest.json]({r}/source-manifest.json)。本轮 Git HEAD `{INITIAL['git_head']}`，工作区已有未跟踪的历史交付证据；已保存开工状态，保留原文/旧版及人工修改。

| 批次 | 任务行数 |
|---|---:|
{rows}

0：复核固定输入/后续人工修改。1：核对继承和 254 个英文不变路径。2：结构迁移及结构外壳；35 个跨路径根映射（函数章 32 个、废弃附录 3 个）和 5 个 logicaldecoding 重归属根按本轮结构表实施。3：真正新增、局部修改、历史译文复用以及其范围内的字面更新。4：资源、七类派生目标、三项项目定制和固定源码能力。5：先新后旧核对删改配对，最后删除 zh/20/func.sgml 与 release-18.sgml，审查基线差异。6：源码/引用/术语/覆盖验收。7：三个实际构建。8：视检。9：本地交付。

任务表依赖是权威顺序，同一批次内也要遵守依赖。按文件维度协调修改，避免不同单元任务相互覆盖。翻译单元通常是完整段落、列表条目、选项或表格行；结构/空白单元有单独动作。old/new 文本是上下文，不能因单元较大而重写未变中文；同文件 unpaired_old_span 在目标新增和修改完成后统一核对替换关系。

主英文原始范围：490 路径联合集、1,133 块。{st['units']:,} 个单元含 {count.get('pg18_exact_english',0):,} 个 PG18 英文完全匹配复用、{hist:,} 个 PG19 英文完全匹配的中文候选、{partial} 个 PG19 部分语境候选、{first} 个首次翻译候选。其余是结构/资源和删除/替换配对。生成表 {st['generated_hunks']} 块单列。逐文件数字在 [translation-scope.tsv]({r}/translation-scope.tsv)。

未检索到对齐历史基础的首次候选出现在以下具体文件（同文件其他内容仍应继承或历史复用）：

{firstpaths}

优先协调 monitoring/config/system-views 的监控和配置含义、logical-replication/ref/create_subscription 的复制语义、func/* 的函数和术语、ref/repack 与旧 CLUSTER/存储叙述、废弃附录与主章节引用。新增 pgplanadvice、pgstashadvice、func-tid 等已有 PG19 参考，不等于首次全文翻译。release-20 当前是上游占位，不沿用旧发布说明清单或 PROPERTY GRAPH 页面。

历史方法取舍：继承旧流程的递归路径清单、原始 unified diff、逐块唯一 ID、按英文共义归并、逐处前后哈希、SGML/字面/引用审计和真实 HTML/A4/US 构建。纠正旧流程中小版本中文目录、先删除后迁移、全部内联标签冻结、仅检查 marker/文件存在、旧统计写死、忽略 generated inputs、自动用开发 snapshot 和宽松 IDREF 构建充当验收的问题。已读历史材料的 217 份文件/表/差异及 SHA256 在 `{s}/historical-inputs.json`；只借鉴方法，不复用其中过时术语决定。

本次没有构建中文继承底稿；12 个两版生成表命令成功，依赖检查成功，固定源码参数还未实现。所有正文与构建验收任务仍处于 formal execution 待执行状态。源码固定、哈希、原始 diff 重建、文件/hunk/unit/任务覆盖及无旧文件修改的准备验收见 [preparation-validation.json]({r}/preparation-validation.json)。
""")


if __name__=='__main__':main()
