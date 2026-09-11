"""Validate native DocBook SGML through OpenSP and retain original locations.

The XML conversion follows PostgreSQL 10's Makefile mangle-xml rule. ESIS
locations are matched to converted XML by the complete element event stream.
No SGML tag is deleted or repaired to make the XML parser accept the input.
"""
import os
from pathlib import Path
import re
import shutil
import subprocess


def local_source(system, staging, sources):
    """Map an OpenSP OSFILE identifier to a staged, explicitly supplied input."""
    staging = staging.resolve()
    path = Path(system.removeprefix('<OSFILE>'))
    path = path if path.is_absolute() else staging / path
    path = path.resolve()
    if not path.is_relative_to(staging):
        return None
    relative = str(path.relative_to(staging))
    return relative if relative in sources else None


def external_declarations(sources, book):
    """Inventory declarations, without treating their presence as consumption.

    This is metadata discovery only. OpenSP performs the SGML validation and
    emits the evidence used to decide whether an external entity was consumed.
    """
    declarations = []
    for rel, path in sources.items():
        if path.suffix not in {'.sgml', '.ent', '.dtd', '.mod'}:
            continue
        text = path.read_text()
        for m in re.finditer(r'''<!ENTITY\s+(%\s+)?([\w.-]+)\s+SYSTEM\s+(["'])(.*?)\3''', text, re.S):
            target = os.path.normpath(str(Path(rel).parent / m[4]))
            declarations.append({'file': book.label(path), 'relative_file': rel,
                                 'line': text.count('\n', 0, m.start()) + 1,
                                 'name': m[2], 'parameter': bool(m[1]),
                                 'system': m[4], 'target': target})
    return declarations


def consumed_entities(records, staging, sources, declarations, entry):
    """Read actual ESIS consumption, excluding unused general declarations.

    OpenSP emits parameter entities when expanded. With -oentity it also emits
    every declared general entity before the document element, including unused
    and nonexistent ones. A general T event in the document instance is a use.
    L records also cover text-only and comment-only source entities. A namespace
    collision that prevents distinguishing a prolog T event fails explicitly.
    """
    used, witnesses = {entry}, []
    instance, system = False, None
    for number, record in enumerate(records, 1):
        if record.startswith('L'):
            parts = record[1:].split(' ', 1)
            if len(parts) == 2:
                rel = local_source(parts[1], staging, sources)
                if rel:
                    used.add(rel)
        elif record.startswith('('):
            instance = True
        elif record.startswith('f'):
            system = record[1:]
        elif record[:1] in {'T', 'E', 'S', 'N'}:
            if record.startswith('T') and system:
                rel = local_source(system, staging, sources)
                name = record[1:]
                matches = [d for d in declarations if d['name'] == name and d['target'] == rel]
                kinds = {d['parameter'] for d in matches}
                if not instance and kinds == {False, True}:
                    raise ValueError(f'Ambiguous native entity namespaces: {name} ({rel})')
                if rel and (instance or kinds == {True}):
                    used.add(rel)
                    witnesses.append({'name': name, 'target': rel,
                                      'parameter': not instance,
                                      'esis_line': number})
            system = None
    return used, witnesses


def load_sgml_book(book, work, entry='postgres.sgml'):
    from check_doc_alignment import Book, file_hash, source_manifest, write_json
    work = Path(work).resolve()
    work.mkdir(parents=True, exist_ok=False)
    staging = work / 'source'
    staging.mkdir()
    sources = {}
    for root in (book.root, book.generated, book.auxiliary):
        if not root:
            continue
        for row in source_manifest(root)['files']:
            rel = row['path']
            if rel in sources:
                continue
            sources[rel] = root / rel
            dest = staging / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / rel, dest)
    commands = []
    try:
        env = os.environ.copy()
        env.setdefault('SP_ENCODING', 'UTF-8')
        env.setdefault('SP_CHARSET_FIXED', 'YES')
        nsgmls = env.get('NSGMLS') or shutil.which('onsgmls') or shutil.which('nsgmls')
        osx = env.get('OSX') or shutil.which('osx')
        if not nsgmls or not osx:
            raise ValueError('Native SGML needs NSGMLS and OSX (OpenSP)')
        for command, name in [
            ([nsgmls, '-l', '-oentity', '-ocomment', entry], 'validated.esis'),
            ([osx, '-x', 'lower', entry], 'converted.xml.tmp'),
        ]:
            with (work / name).open('w') as stdout, (work / (name + '.log')).open('w') as stderr:
                result = subprocess.run(command, cwd=staging, env=env, stdout=stdout, stderr=stderr)
            commands.append({'command': command, 'cwd': str(staging), 'exit_code': result.returncode})
            if result.returncode:
                raise ValueError(f'OpenSP validation/conversion failed: {work / (name + ".log")}')
        xml = (work / 'converted.xml.tmp').read_text()
        chars = 'aacute|acirc|aelig|agrave|amp|aring|atilde|auml|bull|copy|eacute|egrave|gt|iacute|lt|mdash|nbsp|ntilde|oacute|ocirc|oslash|ouml|pi|quot|scaron|uuml'
        xml = re.sub(r'\[(' + chars + r') *\]', lambda m: '&' + m[1] + ';', xml, flags=re.I)
        first, rest = xml.split('\n', 1)
        (work / 'postgres.xml').write_text(first + '\n<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN" "http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd">\n' + rest)
        converted = Book(work, catalogs=book.catalogs).parse('postgres.xml')
        if not converted.complete:
            raise ValueError('; '.join(converted.errors))
        records = (work / 'validated.esis').read_text().splitlines()
        declarations = external_declarations(sources, book)
        consumed, witnesses = consumed_entities(records, staging, sources, declarations, entry)
        nodes = iter(converted.nodes)
        stack, mapping, seen, current_file, line = [], [], set(), entry, 1
        for record in records:
            if record.startswith('L'):
                parts = record[1:].split(' ', 1)
                line = int(parts[0])
                if len(parts) == 2:
                    current_file = parts[1]
            elif record.startswith('('):
                node = next(nodes)
                if node.tag != record[1:].lower():
                    raise ValueError('OpenSP ESIS and converted XML element streams differ')
                rel = local_source(current_file, staging, sources)
                if rel is None:
                    raise ValueError(f'Cannot map SGML location: {current_file}')
                node.file, node.line = book.label(sources[rel]), line
                node.end_line = line
                mapping.append({'xml_order': node.order, 'tag': node.tag, 'file': node.file, 'line': line})
                seen.add(rel)
                stack.append(node)
            elif record.startswith(')'):
                node = stack.pop()
                if node.tag != record[1:].lower():
                    raise ValueError('Unbalanced ESIS element stream')
                rel = local_source(current_file, staging, sources)
                if rel is not None and node.file == book.label(sources[rel]):
                    node.end_line = line
            elif record.startswith('_'):
                book.events.update(['comments'])
        if stack or next(nodes, None) is not None:
            raise ValueError('Incomplete ESIS to XML location mapping')
        book.nodes, book.tree = converted.nodes, converted.tree
        # Staging a file is not evidence that the parser read it. Keep unused
        # inputs in the source inventory, but exclude them from dependencies.
        for rel in sorted(consumed):
            path = sources[rel]
            book.dependencies[str(path)] = {'file': book.label(path), 'path': str(path), 'sha256': file_hash(path)}
        for declaration in declarations:
            declaration['declaration_file_consumed'] = declaration['relative_file'] in consumed
            uses = [w for w in witnesses if w['name'] == declaration['name']
                    and w['target'] == declaration['target']]
            declaration['consumption_witnesses'] = uses
            book.declarations.append(declaration)
            if declaration['declaration_file_consumed'] and uses:
                book.edges.append({'from': declaration['file'], 'line': declaration['line'],
                                   'line_kind': 'declaration', 'to': declaration['target'],
                                   'kind': 'native_sgml_entity_use', 'esis_witnesses': uses,
                                   'has_parsed_elements': declaration['target'] in seen})
        book.complete = True
        write_json(work / 'source-locations.json', mapping)
        write_json(work / 'conversion.json', {'commands': commands, 'xml_sha256': file_hash(work / 'postgres.xml'),
                                            'esis_sha256': file_hash(work / 'validated.esis'), 'mapped_nodes': len(mapping),
                                            'consumed_source_files': sorted(consumed),
                                            'staged_source_files': len(sources)})
    except (OSError, ValueError, StopIteration, subprocess.SubprocessError) as error:
        book.complete = False
        book.errors.append(str(error))
    return book
