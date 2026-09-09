#!/usr/bin/env python3
"""Generate read-only preparation artifacts from this run's frozen inputs."""
import csv
import difflib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from sgml_index import Corpus, COMMENT, norm, sha, signature, visible

PLAN = Path(__file__).resolve().parents[1]
CFG = json.loads((PLAN/'RUN.json').read_text())
ROOT, STATE, REPORT = (Path(CFG[k]) for k in ('root','state','report'))
INITIAL = json.loads((STATE/'initial-state.json').read_text())
OLD, NEW = STATE/'inputs/en/18.6', ROOT/'en/20'
GEN = set('version.sgml features-supported.sgml features-unsupported.sgml errcodes-table.sgml keywords-table.sgml targets-meson.sgml wait_event_types.sgml'.split())


def tsv(path, rows, fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    fields = fields or (list(rows[0]) if rows else ['status'])
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
        w.writeheader()
        for row in rows:
            w.writerow({k:json.dumps(v,ensure_ascii=False,separators=(',',':')) if isinstance(v,(list,dict)) else v for k,v in row.items()})


def jsonl(path,rows):
    with path.open('w') as f:
        for row in rows:
            f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')


def files(root):
    return {str(p.relative_to(root)):p for p in sorted(root.rglob('*')) if p.is_file() or p.is_symlink()}


def kind(p):
    if p is None:return 'absent'
    if p.is_symlink():return 'symlink'
    data=p.read_bytes()
    try:data.decode('utf-8')
    except UnicodeDecodeError:return 'binary'
    return 'binary' if b'\0' in data else 'text'


def category(rel):
    if rel in GEN:return 'generated_table_or_version'
    if rel in {'Makefile','meson.build','.gitignore','xmltools_dep_wrapper'} or rel.endswith(('.pl','.xsl','.css','.xml')) or rel.startswith('images/') and Path(rel).suffix not in {'.svg','.gv','.txt'}:
        return 'build_resource'
    if rel.startswith('images/'):return 'image_resource'
    if rel.startswith('keywords/'):return 'generator_input'
    if rel in {'version.sgml.in'} or Path(rel).name.startswith('README'):return 'metadata'
    if rel.endswith('allfiles.sgml') or rel=='filelist.sgml':return 'include_structure'
    if rel.endswith('.sgml'):return 'document_source'
    return 'build_resource'


def classify(old,new,kind_='para'):
    if old==new:return 'unchanged'
    if norm(old)==norm(new):
        return 'comment_or_formatting'
    if kind_ in {'programlisting','screen','synopsis','cmdsynopsis','funcsynopsis','literallayout'}:
        return 'literal_example_with_translatable_placeholders_review'
    def prose(s):
        s=COMMENT.sub('',s)
        s=re.sub(r'<(programlisting|screen|synopsis|literallayout)\b[^>]*>.*?</\1>','',s,flags=re.S)
        s=re.sub(r'<(function|varname|structname|structfield|command|filename|option|type|envar|symbol|token|literal)\b[^>]*>.*?</\1>','',s,flags=re.S)
        s=re.sub(r'<![^>]*>|<[^>]*>|&[\w.:-]+;',' ',s)
        return ' '.join(s.split())
    a,b=prose(old),prose(new)
    if a==b:return 'structure_or_literal'
    if not re.search(r'[A-Za-z]',a+b):return 'structure_or_literal'
    if kind_=='title' and re.fullmatch(r'Release [0-9.]+',visible(new)):
        return 'structure_or_literal'
    if not a and not b:return 'structure_only'
    if not old.strip():return 'new_explanatory_text'
    if not new.strip():return 'removed_explanatory_text'
    return 'changed_explanatory_text'


def ref(corpus,seg):
    if seg is None:return None
    doc=corpus.docs[seg['file']]
    return {**doc.ref(seg['start'],seg['end'],anchor=seg['anchor'],relative_path=seg['relative_path']), 'text':seg['text'],'context':doc.context(seg)}


def overlapping(seg, ranges):
    return any(seg['start_line'] <= end and seg['end_line'] >= start for start,end in ranges)


def parse_raw_diff(rel,oldpath,newpath):
    # System diff preserves exact bytes, including missing-final-newline evidence.
    p=subprocess.run(['diff','-U3','--label','en/18.6/'+rel if oldpath else '/dev/null','--label','en/20/'+rel if newpath else '/dev/null',str(oldpath or '/dev/null'),str(newpath or '/dev/null')],capture_output=True)
    if p.returncode not in (0,1):raise RuntimeError(p.stderr.decode())
    text=p.stdout.decode();lines=text.splitlines();starts=[i for i,x in enumerate(lines) if x.startswith('@@ ')]
    hunks=[]
    for no,i in enumerate(starts,1):
        m=re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',lines[i]);assert m
        os,ol,ns,nl=int(m[1]),int(m[2] or 1),int(m[3]),int(m[4] or 1)
        body=lines[i+1:starts[no] if no<len(starts) else len(lines)]
        old_ranges,new_ranges=[],[];oi,ni=os,ns
        for line in body:
            if line.startswith('-'):old_ranges.append([oi,oi]);oi+=1
            elif line.startswith('+'):new_ranges.append([ni,ni]);ni+=1
            elif line.startswith(' '):oi+=1;ni+=1
        oldtext='\n'.join(x[1:] for x in body if x.startswith('-'))
        newtext='\n'.join(x[1:] for x in body if x.startswith('+'))
        hid='H20-'+sha(rel+'\n'+str(no)+'\n'+'\n'.join(body))[:16]
        hunks.append({'hunk_id':hid,'file':rel,'old_file':'en/18.6/'+rel if oldpath else '', 'new_file':'en/20/'+rel if newpath else '', 'hunk_no':no,'old_start':os,'old_length':ol,'new_start':ns,'new_length':nl,'removed_lines':len(old_ranges),'added_lines':len(new_ranges),'old_changed_ranges':old_ranges,'new_changed_ranges':new_ranges,'old_anchors':[],'new_anchors':[],'preliminary_classification':classify(oldtext,newtext),'unit_ids':[],'diff_path':str(REPORT/'diffs'/f'{rel}.diff')})
    return text,hunks


def main():
    a,b=files(OLD),files(NEW)
    inventory,changes,hunks,binary=[],[],[],[]
    full=[]
    for rel in sorted(a.keys()|b.keys()):
        op,np=a.get(rel),b.get(rel);ot,nt=kind(op),kind(np)
        oh,nh=sha(op.read_bytes()) if op else '',sha(np.read_bytes()) if np else ''
        action='added' if not op else 'deleted' if not np else 'type_changed' if ot!=nt else 'unchanged' if oh==nh else 'modified'
        own=category(rel)
        row={'path':rel,'action':action,'old_type':ot,'new_type':nt,'ownership':own,'old_sha256':oh,'new_sha256':nh,'old_size':op.stat().st_size if op else 0,'new_size':np.stat().st_size if np else 0}
        inventory.append(row)
        hs=[];dp=''
        if action!='unchanged':
            if 'binary' in {ot,nt} or 'symlink' in {ot,nt}:
                binary.append(row)
                diff=f'Binary or type resource: en/18.6/{rel} -> en/20/{rel}\nold {ot} SHA256 {oh}\nnew {nt} SHA256 {nh}\n'
            else:diff,hs=parse_raw_diff(rel,op,np)
            out=REPORT/'diffs'/f'{rel}.diff';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(diff);dp=str(out)
            full.append(diff);hunks.extend(hs)
        changes.append({'file':rel,'action':action,'added_lines':sum(h['added_lines'] for h in hs),'removed_lines':sum(h['removed_lines'] for h in hs),'hunks':len(hs),'type':own,'diff_path':dp})
    (REPORT/'full.diff').write_text(''.join(full))
    tsv(REPORT/'inventory.tsv',inventory);tsv(REPORT/'changes-summary.tsv',changes);tsv(REPORT/'binary-resources.tsv',binary,list(inventory[0]))
    print('Raw inventory',Counter(x['action'] for x in inventory),'hunks',len(hunks),flush=True)
    print('Indexing fixed English and Chinese contexts',flush=True)
    old,new=Corpus(OLD),Corpus(NEW)
    zh18,history,zh19=Corpus(STATE/'inputs/zh/18'),Corpus(STATE/'inputs/en/19beta3'),Corpus(STATE/'inputs/zh/19')
    literal_names={visible(body) for corpus in [old,new,history] for doc in corpus.docs.values() for _,body in re.findall(r'<(function|varname|structname|structfield|command|application|type)\b[^>]*>(.*?)</\1>',doc.text,re.S)}
    print('Segment counts',[(len(c.docs),sum(len(d.segments) for d in c.docs.values())) for c in (old,new,zh18,history,zh19)],flush=True)
    parser_issues=[{'corpus':str(c.root),'file':p,'issues':d.errors} for c in (old,new,zh18,history,zh19) for p,d in c.docs.items() if d.errors]
    jsonl(REPORT/'lexical-index-issues.jsonl',parser_issues)

    # Every stable ID that changes path or parent is listed. Nested mappings
    # are evidence, not extra file moves. A parent map marks each maximal cut.
    structural=[]
    for anchor in sorted(old.ids.keys() & new.ids.keys()):
        if len(old.ids[anchor])!=1 or len(new.ids[anchor])!=1:continue
        op,oi=old.ids[anchor][0];np,ni=new.ids[anchor][0]
        od,nd=old.docs[op],new.docs[np];on,nn=od.nodes[oi],nd.nodes[ni]
        def parent_id(doc,node):
            return next((doc.nodes[i]['id'] for i in doc.ancestors(node['parent']) if doc.nodes[i]['id']),'')
        oa,na=parent_id(od,on),parent_id(nd,nn)
        if op==np and oa==na:continue
        z=zh18.ids.get(anchor,[]);zp,zi=z[0] if len(z)==1 else ('',None)
        oz=zh18.docs[zp] if zp else None;zn=oz.nodes[zi] if oz else None
        structural.append({'mapping_id':'M20-'+sha(anchor+'|'+op+'|'+np)[:14],'action':'relocate_or_split' if op!=np else 'update_structure','anchor':anchor,'old_file':op,'new_file':np,'old_start':od.line(on['start']),'old_end':od.line(on['end']-1),'new_start':nd.line(nn['start']),'new_end':nd.line(nn['end']-1),'old_parent_anchor':oa,'new_parent_anchor':na,'old_sha256':sha(od.text[on['start']:on['end']]),'new_sha256':sha(nd.text[nn['start']:nn['end']]),'english_equal_normalized':norm(od.text[on['start']:on['end']])==norm(nd.text[nn['start']:nn['end']]),'pg18_chinese_source':str(oz.root/zp) if oz else '', 'zh_start':oz.line(zn['start']) if oz else '', 'zh_end':oz.line(zn['end']-1) if oz else '', 'zh_sha256':sha(oz.text[zn['start']:zn['end']]) if oz else '', 'parent_mapping_id':'','evidence':'unique SGML ID in old/new English and independent Chinese ID; compare internal delta before reuse','status':'mapped_english;chinese_semantics_review_required' if oz else 'baseline_unresolved_missing_chinese_anchor'})
    by_anchor={x['anchor']:x for x in structural}
    for row in structural:
        op,oi=old.ids[row['anchor']][0];doc=old.docs[op]
        # Prefer maximal moved section within the same destination file.
        for idx in doc.ancestors(doc.nodes[oi]['parent']):
            parent=by_anchor.get(doc.nodes[idx]['id'])
            if parent and parent['new_file']==row['new_file']:
                row['parent_mapping_id']=parent['mapping_id'];break
    tsv(REPORT/'structural-map.tsv',structural)
    # A supplementary semantic diff uses mapped old sections, never replaces
    # the complete path-level diff (notably deleted func.sgml / new func/*).
    for row in structural:
        if row['parent_mapping_id']:continue
        op,oi=old.ids[row['anchor']][0];np,ni=new.ids[row['anchor']][0]
        od,nd=old.docs[op],new.docs[np];on,nn=od.nodes[oi],nd.nodes[ni]
        d=''.join(difflib.unified_diff(od.text[on['start']:on['end']].splitlines(True),nd.text[nn['start']:nn['end']].splitlines(True),fromfile=f"en/18.6/{op}#{row['anchor']}",tofile=f"en/20/{np}#{row['anchor']}"))
        out=REPORT/'mapped-diffs'/f"{row['mapping_id']}.diff";out.parent.mkdir(exist_ok=True);out.write_text(d)

    # Segment keys are source offsets, not translated line numbers.
    candidates=defaultdict(lambda:{'old':[],'new':[]});hby={h['hunk_id']:h for h in hunks}
    for h in hunks:
        rel=h['file']
        for side,corpus in [('old',old),('new',new)]:
            if rel not in corpus.docs:continue
            for seg in corpus.docs[rel].segments:
                if overlapping(seg,h[f'{side}_changed_ranges']):
                    candidates[(side,rel,seg['start'])]['segment']=seg
                    candidates[(side,rel,seg['start'])]['hunks']=list(dict.fromkeys(candidates[(side,rel,seg['start'])].get('hunks',[])+[h['hunk_id']]))
                    if seg['anchor'] and seg['anchor'] not in h[f'{side}_anchors']:h[f'{side}_anchors'].append(seg['anchor'])

    units=[];represented_old=set();new_records={}
    old_changed={k:v for k,v in candidates.items() if k[0]=='old'}
    for key,data in sorted(candidates.items()):
        if key[0]!='new':continue
        seg=data['segment'];rel=seg['file'];cat=classify('',seg['text'],seg['kind'])
        exact=old.exact(seg) if seg['kind']!='shell' else None
        before=exact or (old.counterpart(seg) if seg['kind']!='shell' else None)
        if before and not exact and not (seg['kind'] in {'row','varlistentry'} and seg['identity'] and seg['identity']==before['identity']):
            retained=new.exact(before)
            if retained and (retained['file'],retained['start'])!=(seg['file'],seg['start']):
                before=None
        # A modified counterpart is a navigation candidate, never proof of
        # same meaning; within-anchor ordered matching will be reviewed.
        historic=history.exact(seg) if seg['kind']!='shell' else None
        historic_partial=None if historic else (history.counterpart(seg) if seg['kind']!='shell' else None)
        if historic_partial and not (seg['kind'] in {'row','varlistentry'} and seg['identity'] and seg['identity']==historic_partial['identity']):
            retained=new.exact(historic_partial)
            if retained and (retained['file'],retained['start'])!=(seg['file'],seg['start']):
                historic_partial=None
        z18=zh18.chinese(old.docs[before['file']],before) if before else None
        hz=zh19.chinese(history.docs[historic['file']],historic) if historic else None
        pz=zh19.chinese(history.docs[historic_partial['file']],historic_partial) if historic_partial else None
        action=[];reuse='none';classification=classify(before['text'] if before else '',seg['text'],seg['kind'])
        if seg['kind']=='shell':
            # Shells have no independent semantic correspondence. They keep
            # raw structure/comments/spacing; visible text still needs review.
            action=['update_structure'];reuse='structure_or_formatting'
            shell_text=visible(re.sub(r'<![^>]*>','',COMMENT.sub('',seg['text'])))
            if re.search(r'[A-Za-z]{3}',re.sub(r'[&%][\w.:-]+;','',shell_text)):
                action.append('baseline_unresolved');reuse='shell_visible_text_review'
        elif exact:
            action=['relocate_or_split' if exact['file']!=rel else 'copy_unchanged'];reuse='pg18_exact_english'
            if exact['text']!=seg['text']:action.append('update_structure')
            if z18 is None or z18['confidence'] in {'anchor_context_only','file_context_only'}:action.append('baseline_unresolved')
        elif historic and hz and hz['confidence'] not in {'anchor_context_only','file_context_only'}:
            action=['translate_changed_content' if before else 'translate_new_content'];reuse='pg19_exact_english_candidate'
        elif classification in {'structure_only','structure_or_literal','literal_example_with_translatable_placeholders_review'} or (seg['kind']=='indexterm' and visible(seg['text']) in literal_names):
            action=['sync_literal_or_resource'];reuse='literal_or_structure_review'
        else:
            action=['translate_changed_content' if before or historic_partial else 'translate_new_content']
            reuse='pg19_partial_context_candidate' if historic_partial else 'pg18_changed_context' if before else 'no_aligned_history_first_translation_candidate'
        hids=list(data['hunks'])
        if before:
            ok=('old',before['file'],before['start'])
            if ok in old_changed:
                hids=list(dict.fromkeys(hids+old_changed[ok]['hunks']));represented_old.add(ok)
        uid='U20-'+sha('new|'+rel+'|'+str(seg['start'])+'|'+seg['sha256'])[:16]
        u={'unit_id':uid,'file':rel,'kind':seg['kind'],'actions':action,'classification':classification,'reuse':reuse,'status':'prepared_not_applied','hunk_ids':hids,'old_english':ref(old,before),'new_english':ref(new,seg),'pg18_chinese':z18,'historical_english':ref(history,historic or historic_partial),'historical_chinese':hz or pz,'english_alignment':'exact_normalized' if exact else 'same_anchor_structural_path_candidate' if before else 'no_pg18_match','historical_alignment':'exact_normalized' if historic else 'same_anchor_structural_path_context_only' if historic_partial else 'not_found','canonical_group':'C20-'+seg['normalized_sha256'][:20],'edit_scope':'Only target differences inside this complete semantic unit; context is read-only, never whole-chapter rewriting.','term_review_status':'pending_formal_context_review'}
        units.append(u);new_records[(rel,seg['start'])]=u

    for key,data in sorted(old_changed.items()):
        if key in represented_old:continue
        seg=data['segment'];rel=seg['file'];target=new.exact(seg) if seg['kind']!='shell' else None
        if target and (target['file'],target['start']) in new_records:
            u=new_records[(target['file'],target['start'])];u['hunk_ids']=list(dict.fromkeys(u['hunk_ids']+data['hunks']));continue
        z=zh18.chinese(old.docs[rel],seg)
        target_file=target['file'] if target else rel
        if not target and seg['node'] is not None:
            od=old.docs[rel]
            for idx in od.ancestors(seg['node']):
                anchor=od.nodes[idx]['id']
                if anchor and len(new.ids.get(anchor,[]))==1:
                    target_file=new.ids[anchor][0][0]
                    break
        uid='U20-'+sha('old|'+rel+'|'+str(seg['start'])+'|'+seg['sha256'])[:16]
        units.append({'unit_id':uid,'file':target_file,'source_file':rel,'kind':seg['kind'],'actions':['relocate_or_split'] if target else ['delete'],'classification':'old_span_reused_elsewhere' if target else 'removed_or_replaced_old_span_review','reuse':'pg18_exact_english' if target else 'old_source_saved_before_removal','status':'prepared_not_applied','hunk_ids':data['hunks'],'old_english':ref(old,seg),'new_english':ref(new,target),'pg18_chinese':z,'historical_english':None,'historical_chinese':None,'english_alignment':'exact_normalized' if target else 'unpaired_old_span','historical_alignment':'not_applicable','canonical_group':'C20-'+seg['normalized_sha256'][:20],'edit_scope':'Do not remove until all target replacements/moves in this anchor are checked. Unpaired means pairing review, not automatic semantic deletion. For moved sections apply the deletion/replacement to file, not to the old source_file.','term_review_status':'pending_formal_context_review'})

    # Non-SGML and exceptional hunks get explicit units, including resources,
    # generated metadata, or differences landing on empty lines only.
    covered={h for u in units for h in u['hunk_ids']}
    for h in hunks:
        if h['hunk_id'] in covered:continue
        rel=h['file'];own=category(rel)
        action='regenerate' if own=='generated_table_or_version' else 'update_structure' if own=='include_structure' or rel.endswith('.sgml') else 'sync_literal_or_resource'
        units.append({'unit_id':'U20-'+sha(h['hunk_id'])[:16],'file':rel,'kind':own,'actions':[action],'classification':h['preliminary_classification'],'reuse':'resource_or_structure','status':'prepared_not_applied','hunk_ids':[h['hunk_id']],'old_english':{'path':str(OLD/rel),'start_line':h['old_start'],'end_line':h['old_start']+h['old_length']-1} if rel in a else None,'new_english':{'path':str(NEW/rel),'start_line':h['new_start'],'end_line':h['new_start']+h['new_length']-1} if rel in b else None,'pg18_chinese':None,'historical_english':None,'historical_chinese':None,'canonical_group':'','edit_scope':'Apply only this raw hunk; preserve project customization separately.','term_review_status':'not_body_translation'})

    # Semantic unit coverage and contextual terminology review. Search aliases
    # only when the English headword also matches, with no replacement action.
    aliases=list(csv.DictReader((STATE/'inputs/tmp/ref/glossary-aliases.tsv').open(),delimiter='\t'))
    print('Units constructed',len(units),'; checking terminology references',flush=True)
    for u in units:
        oe,ne=u.get('old_english') or {},u.get('new_english') or {}
        if u.get('english_alignment')=='exact_normalized' and oe.get('text') is not None and ne.get('text') is not None and norm(oe['text'])!=norm(ne['text']):
            u['english_alignment']='identical_content_after_id_zone_normalization'
        he=u.get('historical_english') or {}
        if u.get('historical_alignment')=='exact_normalized' and he.get('text') is not None and ne.get('text') is not None and norm(he['text'])!=norm(ne['text']):
            u['historical_alignment']='identical_content_after_id_zone_normalization'
    rules=list(csv.DictReader((STATE/'inputs/tmp/ref/glossary.rules.tsv').open(),delimiter='\t'))
    rule_patterns=[(r['原序号'],re.compile(r'(?<![\w])'+re.escape(r['English'])+r'(?![\w])',re.I)) for r in rules]
    alias_patterns=[(r,re.compile(r'(?<![\w])'+re.escape(r['主词头'])+r'(?![\w])',re.I)) for r in aliases]
    term_rows=[]
    for u in units:
        for hid in u['hunk_ids']:hby[hid]['unit_ids'].append(u['unit_id'])
        english=visible((u.get('new_english') or u.get('old_english') or {}).get('text',''))
        u['term_rule_ids']=[rid for rid,pattern in rule_patterns if pattern.search(english)]
        for source in ('pg18_chinese','historical_chinese'):
            z=u.get(source)
            if not z:continue
            for r,pattern in alias_patterns:
                if pattern.search(english):
                    found=[x.strip() for x in r['中文别称'].split('；') if x.strip() and x.strip() in z['text']]
                    if found:term_rows.append({'unit_id':u['unit_id'],'source':source,'rule_id':r['原序号'],'headword':r['主词头'],'current_chinese':r['主中文'],'matched_aliases':found,'status':'context_review_only_no_replacement','source_path':z['path'],'source_start':z['start_line']})
    for h in hunks:
        h['unit_ids']=sorted(set(h['unit_ids']));assert h['unit_ids'],h
    jsonl(REPORT/'translation-units.jsonl',units);tsv(REPORT/'hunks.tsv',hunks)
    tsv(REPORT/'terminology-review.tsv',term_rows,['unit_id','source','rule_id','headword','current_chinese','matched_aliases','status','source_path','source_start'])
    reuse_rows=[]
    for u in units:
        if u.get('historical_english') or u.get('pg18_chinese'):
            reuse_rows.append({'unit_id':u['unit_id'],'target_file':u['file'],'hunk_ids':u['hunk_ids'],'reuse':u['reuse'],'pg18_english':(u.get('old_english') or {}).get('path',''),'pg18_anchor':(u.get('old_english') or {}).get('anchor',''),'pg18_chinese':{k:v for k,v in (u.get('pg18_chinese') or {}).items() if k!='text'},'historical_english':{k:v for k,v in (u.get('historical_english') or {}).items() if k not in {'text','context'}},'historical_chinese':{k:v for k,v in (u.get('historical_chinese') or {}).items() if k!='text'},'historical_alignment':u.get('historical_alignment',''),'terminology_status':u['term_review_status']})
    tsv(REPORT/'historical-reuse.tsv',reuse_rows)
    # Record baseline ID discrepancies independently of PG20 English changes.
    issues=[]
    for en,zh,ver in [(old,zh18,'18.6'),(history,zh19,'19beta3')]:
        for anchor in sorted(en.ids.keys()-zh.ids.keys()):
            p,i=en.ids[anchor][0];n=en.docs[p].nodes[i]
            issues.append({'issue_id':'BI-'+sha(ver+'|'+anchor)[:14],'version':ver,'kind':'missing_chinese_id_candidate','anchor':anchor,'english_file':p,'english_line':en.docs[p].line(n['start']),'english_context':en.docs[p].text[n['start']:n['end']],'target_pg20_present':anchor in new.ids,'status':'baseline_unresolved_not_proof_of_missing_translation'})
        for anchor in sorted(zh.ids.keys()-en.ids.keys()):
            if anchor.startswith('zh18-auto-'):continue
            p,i=zh.ids[anchor][0]
            issues.append({'issue_id':'BI-'+sha(ver+'|extra|'+anchor)[:14],'version':ver,'kind':'extra_chinese_id_candidate','anchor':anchor,'english_file':'','chinese_file':p,'target_pg20_present':anchor in new.ids,'status':'baseline_unresolved_custom_or_version_difference_review'})
    jsonl(REPORT/'baseline-id-issues.jsonl',issues)
    stats={'files':dict(Counter(x['action'] for x in inventory)),'old_files':len(a),'new_files':len(b),'union_files':len(inventory),'raw_hunks':len(hunks),'added_lines':sum(h['added_lines'] for h in hunks),'removed_lines':sum(h['removed_lines'] for h in hunks),'units':len(units),'unit_actions':dict(Counter(x for u in units for x in u['actions'])),'reuse':dict(Counter(u['reuse'] for u in units)),'classifications':dict(Counter(u['classification'] for u in units)),'structural_mapping_rows':len(structural),'structural_roots':len([x for x in structural if not x['parent_mapping_id']]),'moved_target_files':sorted({x['new_file'] for x in structural if x['old_file']!=x['new_file']}),'binary_changes':len(binary),'lexical_index_issue_files':len(parser_issues),'baseline_issue_candidates':len(issues),'terminology_review_candidates':len(term_rows),'sgml_files':dict(Counter(x['action'] for x in inventory if x['path'].endswith('.sgml')))}
    (REPORT/'statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    (REPORT/'preparation-coverage.json').write_text(json.dumps({'path_equations':len(a)==sum(stats['files'].get(k,0) for k in ['unchanged','modified','deleted','type_changed']) and len(b)==sum(stats['files'].get(k,0) for k in ['unchanged','modified','added','type_changed']),'hunks_without_units':[],'unique_unit_ids':len({u['unit_id'] for u in units})==len(units),'all_units_prepared_not_applied':all(u['status']=='prepared_not_applied' for u in units),'translation_performed':False},indent=2)+'\n')
    print(json.dumps(stats,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
