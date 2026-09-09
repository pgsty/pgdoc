"""Lossless lexical SGML spans; no rewriting, entity expansion, or translation.

Character offsets are zero based/end exclusive. Lines are one based/inclusive.
Comments/CDATA/declarations are skipped as markup. This is an index, not a DTD
validator. All malformed nesting is reported; Chinese candidates require review.
"""
import bisect
import hashlib
import re
from collections import defaultdict
from pathlib import Path

TOKEN = re.compile(r'<!--[\s\S]*?-->|<!\[CDATA\[[\s\S]*?\]\]>|<\?[\s\S]*?\?>|<![^>]*>|</?[A-Za-z][^>]*>')
ID = re.compile(r'\bid\s*=\s*["\']([^"\']+)["\']')
COMMENT = re.compile(r'<!--[\s\S]*?-->')
LITERAL = re.compile(r'<(programlisting|screen|synopsis|literallayout)\b[^>]*>[\s\S]*?</\1>', re.I)
ATOMIC = set('row varlistentry listitem glossentry para simpara title titleabbrev indexterm refpurpose programlisting screen synopsis cmdsynopsis funcsynopsis literallayout term bridgehead bibliomixed refname refdescriptor refentrytitle refmiscinfo member'.split())
EMPTY = set('xref anchor imagedata graphic inlinegraphic colspec spanspec area sbr beginpage void'.split())


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def norm(value):
    """Ignore comments/formatting in prose, preserve literal-block whitespace."""
    value = COMMENT.sub('', value)
    literals = []
    def hold(m):
        literals.append(m[0])
        return f'@@PGDOC_LITERAL_{len(literals)-1}@@'
    value = LITERAL.sub(hold, value)
    value = re.sub(r'\s+', ' ', value).strip()
    for i, literal in enumerate(literals):
        value = value.replace(f'@@PGDOC_LITERAL_{i}@@', literal)
    return value


def visible(value):
    value = COMMENT.sub('', value)
    value = re.sub(r'<[^>]*>', ' ', value)
    return ' '.join(value.split())


def content_norm(value):
    # Anchor and visible-index zoning changes are structural evidence, not a
    # new translation. Link destinations and all literal content remain intact.
    literals=[]
    def hold(m):
        literals.append(m[0]);return f'@@PGDOC_CONTENT_LITERAL_{len(literals)-1}@@'
    value=LITERAL.sub(hold,value)
    value=re.sub(r'<[A-Za-z][^>]*>',lambda m:re.sub(r'\s+(?:id|zone)\s*=\s*["\'][^"\']*["\']','',m[0]),value)
    for i,literal in enumerate(literals):value=value.replace(f'@@PGDOC_CONTENT_LITERAL_{i}@@',literal)
    return norm(value)


def identity(value):
    names=re.findall(r'<(function|varname|structfield|structname)\b[^>]*>(.*?)</\1>',COMMENT.sub('',value),re.S)
    return tuple(sorted(set((tag,visible(body)) for tag,body in names)))


def signature(value):
    value = COMMENT.sub('', value)
    # IDs/format can differ in the inherited Chinese; names and references
    # provide correspondence evidence but are not an exhaustive protection list.
    names = re.findall(r'<(function|varname|structname|structfield|command|filename|option|type)\b[^>]*>(.*?)</\1>', value, re.S)
    return sorted((tag, visible(body)) for tag, body in names)


class Document:
    def __init__(self, root, rel):
        self.root, self.rel = Path(root), rel
        self.text = (self.root / rel).read_text()
        self.line_starts = [0] + [m.end() for m in re.finditer('\n', self.text)]
        self.nodes, self.errors, self.ids = [], [], defaultdict(list)
        stack, counts = [], defaultdict(lambda: defaultdict(int))
        for m in TOKEN.finditer(self.text):
            token = m[0]
            if token.startswith(('<!--', '<!', '<?')):
                continue
            tag = re.match(r'</?([\w:.-]+)', token)[1].lower()
            if token.startswith('</'):
                if not stack or self.nodes[stack[-1]]['tag'] != tag:
                    self.errors.append({'line': self.line(m.start()), 'closing': tag, 'stack': [self.nodes[x]['tag'] for x in stack[-4:]]})
                    found = next((i for i in range(len(stack)-1, -1, -1) if self.nodes[stack[i]]['tag'] == tag), None)
                    if found is None:
                        continue
                    while len(stack)-1 > found:
                        self.nodes[stack.pop()]['end'] = m.start()
                self.nodes[stack.pop()]['end'] = m.end()
                continue
            parent = stack[-1] if stack else None
            counts[parent][tag] += 1
            idx = len(self.nodes)
            attr = ID.search(token)
            node = {'index': idx, 'tag': tag, 'id': attr[1] if attr else '', 'start': m.start(), 'end': m.end(), 'parent': parent, 'ordinal': counts[parent][tag], 'children': []}
            self.nodes.append(node)
            if parent is not None:
                self.nodes[parent]['children'].append(idx)
            if node['id']:
                self.ids[node['id']].append(idx)
            if not token.endswith('/>') and tag not in EMPTY:
                stack.append(idx)
        for idx in stack:
            self.nodes[idx]['end'] = len(self.text)
            self.errors.append({'line': self.line(self.nodes[idx]['start']), 'unclosed': self.nodes[idx]['tag']})
        self.segments = []
        cursor = 0
        for node in self.nodes:
            if node['start'] < cursor or node['tag'] not in ATOMIC:
                continue
            if node['start'] > cursor:
                self.segment(cursor, node['start'], None)
            self.segment(node['start'], node['end'], node['index'])
            cursor = node['end']
        if cursor < len(self.text):
            self.segment(cursor, len(self.text), None)

    def line(self, pos):
        return bisect.bisect_right(self.line_starts, pos)

    def ancestors(self, idx):
        out = []
        while idx is not None:
            out.append(idx)
            idx = self.nodes[idx]['parent']
        return out

    def containing(self, start, end):
        candidates = [n for n in self.nodes if n['start'] <= start and n['end'] >= end]
        return min(candidates, key=lambda n: n['end']-n['start']) if candidates else None

    def segment(self, start, end, node_idx):
        node = self.nodes[node_idx] if node_idx is not None else self.containing(start, end)
        chain = self.ancestors(node['index']) if node else []
        anchor = next((self.nodes[i]['id'] for i in chain if self.nodes[i]['id']), '')
        text = self.text[start:end]
        path = []
        ancestry=[]
        for i in chain:
            n = self.nodes[i]
            if n['id']:
                ancestry.append((n['id'],'/'.join(reversed(path))))
            path.append(f"{n['tag']}[{n['ordinal']}]")
        ancestry.append((self.rel+'#@file','/'.join(reversed(path))))
        path=[]
        for i in chain:
            n=self.nodes[i]
            if n['id'] == anchor and anchor:
                break
            path.append(f"{n['tag']}[{n['ordinal']}]")
        self.segments.append({'file': self.rel, 'start': start, 'end': end, 'start_line': self.line(start), 'end_line': self.line(max(start, end-1)), 'node': node_idx, 'anchor': anchor, 'relative_path': '/'.join(reversed(path)), 'ancestor_paths':ancestry, 'kind': self.nodes[node_idx]['tag'] if node_idx is not None else 'shell', 'text': text, 'normalized_sha256': sha(norm(text)), 'content_sha256':sha(content_norm(text)), 'identity':identity(text),'sha256': sha(text)})

    def context(self, segment):
        if segment['anchor'] in self.ids and len(self.ids[segment['anchor']]) == 1:
            node = self.nodes[self.ids[segment['anchor']][0]]
            return self.ref(node['start'], node['end'], anchor=node['id'])
        return self.ref(0, len(self.text), anchor='')

    def ref(self, start, end, **extra):
        text = self.text[start:end]
        return {'path': str(self.root/self.rel), 'file': self.rel, 'char_start': start, 'char_end': end, 'start_line': self.line(start), 'end_line': self.line(max(start,end-1)), 'sha256': sha(text), **extra}


class Corpus:
    def __init__(self, root):
        self.root = Path(root)
        self.docs = {str(p.relative_to(self.root)): Document(self.root,str(p.relative_to(self.root))) for p in sorted(self.root.rglob('*.sgml'))}
        self.ids, self.hashes, self.keys = defaultdict(list), defaultdict(list), defaultdict(list)
        self.content_hashes,self.identities=defaultdict(list),defaultdict(list)
        for rel, doc in self.docs.items():
            for anchor, nodes in doc.ids.items():
                for i in nodes:
                    self.ids[anchor].append((rel,i))
            for seg in doc.segments:
                if seg['kind'] != 'shell':
                    self.hashes[seg['normalized_sha256']].append(seg)
                    self.content_hashes[seg['content_sha256']].append(seg)
                    for anchor,path in seg['ancestor_paths']:
                        self.keys[(anchor,path,seg['kind'])].append(seg)
                    if seg['identity']:
                        self.identities[(seg['kind'],seg['identity'])].append(seg)

    def exact(self, seg):
        found = self.content_hashes.get(seg['content_sha256'], [])
        same = [x for x in found if x['anchor'] == seg['anchor']]
        if same:
            return min(same,key=lambda x: (x['file']!=seg['file'],x['start']))
        same_file=[x for x in found if x['file']==seg['file']]
        if len(same_file)==1:
            return same_file[0]
        if seg['kind']=='title' and seg['file'].startswith('release-'):
            release_titles=[x for x in found if x['file'].startswith('release-')]
            if release_titles:return release_titles[0]
        # Short generic labels must not be borrowed from an unrelated context.
        if len(visible(seg['text'])) >= 60 and found:
            return min(found,key=lambda x: (x['file']!=seg['file'],x['start']))
        return None

    def counterpart(self, seg):
        # Name-identified rows survive movement between function subtrees.
        named=self.identities.get((seg['kind'],seg['identity']),[]) if seg['identity'] else []
        if seg['kind'] in {'row','varlistentry'} and len(named)==1:
            return named[0]
        for anchor,path in seg['ancestor_paths']:
            found = self.keys.get((anchor,path,seg['kind']),[])
            if len(found)==1:return found[0]
            same = [x for x in found if x['file']==seg['file']]
            if len(same)==1:return same[0]
        return None

    def chinese(self, english_doc, segment):
        """ID then same-tag structural path, with explicit candidate confidence."""
        if segment['node'] is None:
            return None
        idx = segment['node']
        chain = english_doc.ancestors(idx)
        for ancestor_idx in chain:
            ancestor = english_doc.nodes[ancestor_idx]
            anchor = ancestor['id']
            if not anchor or len(self.ids.get(anchor,[])) != 1:
                continue
            rel, candidate_idx = self.ids[anchor][0]
            candidate_doc = self.docs[rel]
            anchor_node = candidate_doc.nodes[candidate_idx]
            wanted=english_doc.nodes[idx]
            sig=signature(segment['text'])
            if sig:
                exact_nodes=[n for n in candidate_doc.nodes if n['tag']==wanted['tag'] and n['start']>=anchor_node['start'] and n['end']<=anchor_node['end'] and signature(candidate_doc.text[n['start']:n['end']])==sig]
                if len(exact_nodes)==1:
                    node=exact_nodes[0]
                    text=candidate_doc.text[node['start']:node['end']]
                    return {**candidate_doc.ref(node['start'],node['end'],anchor=anchor),'text':text,'confidence':'unique_literal_signature_within_anchor_candidate','literal_signature_equal':True,'status':'needs_semantic_and_current_terminology_review'}
            descendant_path = list(reversed(chain[:chain.index(ancestor_idx)]))
            confidence, valid = 'anchor_and_structural_path_candidate', True
            for child_idx in descendant_path:
                child = english_doc.nodes[child_idx]
                siblings = [n for n in candidate_doc.nodes[candidate_idx]['children'] if candidate_doc.nodes[n]['tag']==child['tag']]
                if len(siblings)<child['ordinal']:
                    valid=False
                    break
                candidate_idx=siblings[child['ordinal']-1]
            anchor_node = candidate_doc.nodes[self.ids[anchor][0][1]]
            if not valid:
                return {**candidate_doc.ref(anchor_node['start'],anchor_node['end'],anchor=anchor), 'text': candidate_doc.text[anchor_node['start']:anchor_node['end']], 'confidence':'anchor_context_only', 'literal_signature_equal':False, 'status':'needs_alignment_review'}
            node=candidate_doc.nodes[candidate_idx]
            text=candidate_doc.text[node['start']:node['end']]
            sig=signature(segment['text'])
            same=bool(sig) and sig==signature(text)
            if segment['anchor']==anchor and segment['relative_path']=='':
                confidence='direct_unique_id_candidate'
            elif same:
                confidence='anchor_path_and_literal_signature_candidate'
            return {**candidate_doc.ref(node['start'],node['end'],anchor=anchor), 'text':text,'confidence':confidence,'literal_signature_equal':same,'status':'needs_semantic_and_current_terminology_review'}
        # A same-path file is usable context, never pretend it is an aligned span.
        if english_doc.rel in self.docs:
            doc=self.docs[english_doc.rel]
            return {**doc.ref(0,len(doc.text),anchor=''),'text':doc.text,'confidence':'file_context_only','literal_signature_equal':False,'status':'needs_alignment_review'}
        return None
