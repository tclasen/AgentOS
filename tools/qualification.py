#!/usr/bin/env python3
"""Bounded native AgentOS qualification helpers; never grade semantics from a model's claim."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import time

MODELS = ('gpt-6.1-sol', 'gpt-6-luna')
REASONING_EFFORTS = ('low', 'medium', 'high', 'xhigh', 'max', 'ultra')

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def component_status(front: str) -> str | None:
    """Parse the simple status scalar profile; do not silently ignore malformed declarations."""
    declarations = re.findall(r'^status[ \t]*:(.*)$', front, re.M)
    if not declarations:
        return None
    if len(declarations) != 1:
        raise ValueError('duplicate status declaration')
    value = re.fullmatch(
        r'''(?:([A-Za-z][A-Za-z0-9_-]*)|"([A-Za-z][A-Za-z0-9_-]*)"|'([A-Za-z][A-Za-z0-9_-]*)')(?:[ \t]+\#.*)?''',
        declarations[0].strip())
    if not value:
        raise ValueError('unsupported status scalar; use a plain or quoted word, optionally followed by a comment')
    return next(part for part in value.groups() if part is not None)

def component_profile(front: str) -> dict | None:
    """Parse one bounded agentos mapping without dropping unrecognized dependencies."""
    markers = list(re.finditer(r'^agentos[ \t]*:(.*)$', front, re.M))
    if not markers:
        return None
    if len(markers) != 1 or markers[0].group(1).strip():
        raise ValueError('agentos must be one block mapping')
    lines = []
    for line in front[markers[0].end():].splitlines():
        if line and not line[0].isspace() and not line.startswith('#'):
            break
        lines.append(line)
    fields = [(i, match) for i, line in enumerate(lines)
              if (match := re.fullmatch(r'  ([A-Za-z_][A-Za-z0-9_-]*)[ \t]*:(.*)', line))]
    values = {}
    for key in ('selection', 'requires'):
        matches = [(n, i, m) for n, (i, m) in enumerate(fields) if m.group(1) == key]
        if len(matches) != 1:
            raise ValueError(f'agentos needs exactly one {key} declaration')
        n, start, match = matches[0]
        end = fields[n + 1][0] if n + 1 < len(fields) else len(lines)
        body = [line.rstrip() for line in lines[start + 1:end]
                if line.strip() and not line.lstrip().startswith('#')]
        value = match.group(2).strip()
        if key == 'selection':
            if value not in ('required', 'conditional') or body:
                raise ValueError('unsupported agentos selection scalar')
            values[key] = value
        elif value == '[]' and not body:
            values[key] = []
        elif not value and body:
            deps = [re.fullmatch(r'  - ([A-Za-z0-9_./-]+)', line) for line in body]
            if not all(deps):
                raise ValueError('unsupported agentos requires list entry')
            values[key] = [dep.group(1) for dep in deps]
        else:
            raise ValueError('agentos requires must be [] or a two-space dash list')
    return values

def graph(bundle: Path, *, validate_dependencies: bool = True) -> dict:
    """Read bounded metadata and, by default, audit every component's dependencies."""
    bundle = bundle.resolve()
    nodes = {}
    for path in sorted((bundle / 'components').glob('*.md')):
        if not path.resolve().is_relative_to(bundle):
            raise ValueError(f'component escapes bundle: {path.name}')
        content = path.read_text()
        lines = content.splitlines()
        front = ''
        if lines and lines[0] == '---':
            try:
                end = lines.index('---', 1)
            except ValueError:
                raise ValueError(f'unterminated frontmatter: {path.name}') from None
            front = '\n'.join(lines[1:end]) + '\n'
        try:
            profile = component_profile(front)
        except ValueError as error:
            raise ValueError(f'invalid AgentOS metadata profile: {path.name}: {error}') from None
        if profile is None:
            continue
        deps = profile['requires']
        if validate_dependencies:
            for dep in deps:
                target = (bundle / dep.lstrip('/')).resolve()
                if not target.is_relative_to(bundle) or not target.is_file():
                    raise ValueError(f'missing or escaping dependency: {path.name} -> {dep}')
        key = path.relative_to(bundle).as_posix()
        nodes[key] = {'selection': profile['selection'], 'requires': [x.lstrip('/') for x in deps],
                      'status': component_status(front), 'sha256': sha(path.read_bytes())}
    def visit(node, visiting, visited):
        if node in visiting:
            raise ValueError(f'dependency cycle: {node}')
        if node not in nodes:
            raise ValueError(f'not a component: {node}')
        if node in visited:
            return
        for dep in nodes[node]['requires']:
            visit(dep, visiting | {node}, visited)
        visited.add(node)
    visited = set()
    if validate_dependencies:
        for node in nodes:
            visit(node, set(), visited)
    catalog = (bundle / 'components/index.md').read_text().split('## Conditional components')[0]
    listed = {'components/' + x for x in re.findall(r'\]\(([^)]+\.md)\)', catalog)}
    required = {k for k, v in nodes.items() if v['selection'] == 'required'}
    if required != listed:
        raise ValueError(f'required catalog differs from metadata: {required ^ listed}')
    return nodes

def closure(nodes: dict, selected: list[str]) -> list[str]:
    result = set()
    def visit(node, visiting):
        if node in visiting:
            raise ValueError(f'dependency cycle: {node}')
        if node in result:
            return
        if node not in nodes:
            raise ValueError(f'unknown component: {node}')
        if nodes[node].get('status') == 'deprecated':
            raise ValueError(f'selected component is deprecated: {node}')
        for dep in nodes[node]['requires']:
            visit(dep, visiting | {node})
        result.add(node)
    for node in selected:
        visit(node, set())
    return sorted(result)

def select_components(bundle: Path, requested: list[str]) -> dict:
    """Compute structural selection only; this grants no authority or source-read credit."""
    nodes = graph(bundle, validate_dependencies=False)
    required = sorted(k for k, v in nodes.items() if v['selection'] == 'required')
    requested = sorted(set(requested))
    selected = closure(nodes, required + requested)
    return {'required': required, 'requested': requested, 'selected': selected,
            'components': {k: nodes[k] for k in selected},
            'limits': 'Structural selection only. Read full selected sources, reconcile user requirements, '
                      'and obtain applicable authority before installation or effects.'}

def verify_selection(bundle: Path, declared: list[str]) -> dict:
    """Check a proposed set as supplied; never silently complete or replace it."""
    if not isinstance(declared, list) or any(not isinstance(p, str) for p in declared):
        raise ValueError('selection must be a JSON list of component paths')
    if len(declared) != len(set(declared)):
        raise ValueError('selection contains duplicate component paths')
    nodes = graph(bundle, validate_dependencies=False)
    required = sorted(k for k, v in nodes.items() if v['selection'] == 'required')
    declared = sorted(declared)
    needed = closure(nodes, required + declared)
    missing = set(needed) - set(declared)
    return {'complete': not missing, 'declared': declared, 'required': required,
            'closure': needed, 'missing_required': sorted(missing & set(required)),
            'missing_dependencies': sorted(missing - set(required)),
            'components': {k: nodes[k] for k in needed},
            'limits': 'Structural completeness only. Independently bind this exact list to the actual '
                      'proposal, resolve contradictory deferrals, and assess every selected duty. '
                      'No source-read, implementation, independence or authority credit.'}

def snapshot(root: Path) -> dict:
    """Record entries without opening special files or following symlinks."""
    root = root.resolve()
    result = {}
    for folder, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.pytest_cache')]
        base = Path(folder)
        for name in sorted(dirs):
            p = base / name
            if not p.is_symlink():
                result[p.relative_to(root).as_posix()] = {'directory': True}
        for name in sorted(files + [d for d in dirs if (base / d).is_symlink()]):
            p = base / name
            key = p.relative_to(root).as_posix()
            mode = p.lstat().st_mode
            if stat.S_ISLNK(mode):
                result[key] = {'symlink': os.readlink(p)}
            elif stat.S_ISREG(mode):
                result[key] = {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
            else:
                result[key] = {'special': stat.S_IFMT(mode)}
    return result

def difference(before: dict, after: dict) -> dict:
    return {'added': sorted(after.keys() - before.keys()), 'removed': sorted(before.keys() - after.keys()), 'changed': sorted(k for k in before.keys() & after.keys() if before[k] != after[k])}

def source_identity(bundle: Path) -> dict:
    """Hash the whole local bundle without granting source-read credit or writing files."""
    bundle = bundle.resolve()
    if not bundle.is_dir() or not (bundle / 'start.md').is_file():
        raise ValueError('source bundle must be a directory containing start.md')
    files = {}
    def fail(error):
        raise error
    for folder, dirs, names in os.walk(bundle, followlinks=False, onerror=fail):
        for name in dirs + names:
            path = Path(folder) / name
            mode = path.lstat().st_mode
            key = path.relative_to(bundle).as_posix()
            if stat.S_ISDIR(mode):
                continue
            if not stat.S_ISREG(mode):
                raise ValueError(f'source identity requires regular files, not links or special files: {key}')
            data = path.read_bytes()
            files[key] = {'sha256': sha(data), 'bytes': len(data)}
    return {'format': 'agentos-source-v1', 'files': dict(sorted(files.items()))}

def unique_json_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate manifest key: {key}')
        result[key] = value
    return result

def verify_source_identity(actual: dict, approved: dict) -> dict:
    """Compare complete maps; manifest paths are data and are never opened."""
    if (not isinstance(approved, dict) or set(approved) != {'format', 'files'}
            or approved['format'] != 'agentos-source-v1' or not isinstance(approved['files'], dict)
            or 'start.md' not in approved['files']):
        raise ValueError('unsupported or incomplete source identity manifest')
    for path, entry in approved['files'].items():
        if (not path or path.startswith('/') or any(p in ('', '.', '..') for p in path.split('/'))
                or not isinstance(entry, dict) or set(entry) != {'sha256', 'bytes'}
                or not isinstance(entry['sha256'], str) or not re.fullmatch(r'[0-9a-f]{64}', entry['sha256'])
                or type(entry['bytes']) is not int or entry['bytes'] < 0):
            raise ValueError(f'invalid source identity entry: {path}')
    delta = difference(approved['files'], actual['files'])
    return {'match': not any(delta.values()), 'delta': delta}

def events(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(errors='replace').splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if isinstance(d, dict):
            rows.append(d)
    return rows

def source_content_exposures(rows: list[dict], bundle: Path) -> dict:
    """Locate complete canonical text without inferring read success or comprehension."""
    commands = [(index, row.get('item', {})) for index, row in enumerate(rows)
                if row.get('type') == 'item.completed'
                and row.get('item', {}).get('type') == 'command_execution']
    result = {}
    for path in sorted(bundle.rglob('*.md')):
        relative = path.relative_to(bundle)
        if not path.is_file() or any((bundle / Path(*relative.parts[:end])).is_symlink()
                                     for end in range(1, len(relative.parts) + 1)):
            continue
        data = path.read_bytes()
        body = data.decode('utf-8')
        if not body.strip():
            continue
        observations = []
        for index, item in commands:
            command, output = item.get('command'), item.get('aggregated_output')
            if isinstance(command, str) and command and isinstance(output, str) and body in output:
                observations.append({
                    'event_index': index,
                    'item_id': item.get('id'),
                    'command_sha256': sha(command.encode()),
                    'output_sha256': sha(output.encode()),
                    'outer_exit_code': item.get('exit_code'),
                    'outer_status': item.get('status'),
                })
        if observations:
            result[relative.as_posix()] = {
                'sha256': sha(data), 'bytes': len(data), 'observations': observations,
            }
    return result


def summarize(path: Path, source: Path | None = None) -> dict:
    rows = events(path)
    complete = [d.get('item', {}) for d in rows if d.get('type') == 'item.completed']
    result = {
        'threads': [d['thread_id'] for d in rows if d.get('type') == 'thread.started'],
        'turn_completed': sum(d.get('type') == 'turn.completed' for d in rows),
        'errors': [d for d in rows if d.get('type') in ('error', 'turn.failed')],
        'messages': [i.get('text', '') for i in complete if i.get('type') == 'agent_message'],
        'failed_commands': [{k: i.get(k) for k in ('command', 'exit_code', 'aggregated_output')} for i in complete if i.get('type') == 'command_execution' and i.get('exit_code') not in (0, None)],
        'usage': [d.get('usage') for d in rows if d.get('type') == 'turn.completed'],
    }
    if source:
        outputs = [i.get('aggregated_output', '') for i in complete if i.get('type') == 'command_execution' and i.get('exit_code') == 0]
        result['full_component_reads_observed'] = [p.relative_to(source / 'bundle').as_posix() for p in sorted((source / 'bundle/components').glob('*.md')) if p.name != 'index.md' and any(p.read_text().strip() in out for out in outputs)]
        result['read_evidence_limit'] = 'Only complete source text in completed successful command output is credited; truncated/other tool output is inconclusive, not evidence of a skipped read.'
        result['source_content_exposures'] = source_content_exposures(rows, source / 'bundle')
        result['source_exposure_limit'] = ('Exact nonempty Markdown content in completed command output, with zero-based parsed-event indexes. '
            'Aggregate failure is preserved and does not erase content exposure. This does not prove the source read exit status, '
            'command provenance, comprehension, semantic acceptance or before-write ordering; inspect the pinned source and raw events. '
            'Partial outputs are not combined. Missing exposure is inconclusive, not proof of a skipped read. '
            'The successful-command-only full_component_reads_observed measurement remains unchanged.')
    return result

def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def run(args):
    effort = getattr(args, 'reasoning_effort', None)
    if effort is not None and effort not in REASONING_EFFORTS:
        raise ValueError('reasoning effort must be one of: ' + ', '.join(REASONING_EFFORTS))
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', args.name):
        raise ValueError('run name must be a simple evidence filename, not a path')
    if not re.fullmatch(r'TASK-[0-9]{6}', args.task):
        raise ValueError('task must be an explicit TASK-NNNNNN identifier')
    target = Path(args.target).resolve()
    workspace = Path(args.workspace).resolve()
    if not target.is_relative_to(workspace) or not (target / '.git').exists():
        raise ValueError('target must be a disposable Git fixture within the authorized workspace')
    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)
    log = out / (args.name + '.jsonl')
    manifest = out / (args.name + '.run.json')
    if log.exists() or manifest.exists():
        raise ValueError('existing run evidence cannot be overwritten; allocate a new run name')
    before = snapshot(target)
    extra = [Path(p).resolve() for p in args.add_dir]
    if any(not p.is_relative_to(workspace) or not p.is_dir() for p in extra):
        raise ValueError('additional writes must name existing task-owned directories within workspace')
    cmd = ['sbx', 'exec', '-i', '-w', str(target), args.sandbox, 'codex', 'exec', '-m', args.model, '--sandbox', args.policy,
           '-c', 'agents.enabled=' + ('true' if args.agents else 'false'),
           '-c', f'agents.max_concurrent_threads_per_session={max(args.agents, 1)}',
           '-c', 'agents.default_subagent_model=' + json.dumps(args.model)]
    if effort is not None:
        cmd += ['-c', 'model_reasoning_effort=' + json.dumps(effort)]
    if args.strict_config:
        cmd += ['--strict-config']
    for path in extra:
        cmd += ['--add-dir', str(path)]
    if args.resume:
        cmd += ['resume']
    cmd += ['--json', '-o', '/tmp/' + args.name + '-final.txt']
    if args.schema:
        cmd += ['--output-schema', str(Path(args.schema).resolve())]
    if args.resume:
        cmd += [args.resume]
    cmd += ['-']
    source = Path(args.source).resolve()
    record = {'name': args.name, 'task': args.task, 'status': 'running', 'started_epoch': time.time(), 'owner': 'Coordinator', 'scope': str(target), 'additional_scopes_before': {str(p): snapshot(p) for p in extra}, 'requested_model': args.model, 'actual_model': 'unknown until session metadata collected', 'policy': args.policy, 'native_child_cap': args.agents, 'command': cmd, 'prompt_sha256': sha(Path(args.prompt).read_bytes()), 'before': before, 'source_components': graph(source / 'bundle'), 'monetary_cost': 'unknown'}
    record['source_bundle'] = snapshot(source / 'bundle')
    record['requested_reasoning_effort'] = effort
    record['actual_reasoning_effort'] = 'unknown until session metadata collected'
    write_json(manifest, record)
    with log.open('wb') as stream:
        proc = subprocess.run(cmd, input=Path(args.prompt).read_bytes(), stdout=stream, stderr=subprocess.STDOUT)
    summary = summarize(log, source)
    after = snapshot(target)
    record.update(status='returned' if proc.returncode == 0 and summary['turn_completed'] and not summary['errors'] else 'failed', returncode=proc.returncode, ended_epoch=time.time(), summary=summary, after=after, delta=difference(before, after))
    record['additional_scopes_after'] = {str(p): snapshot(p) for p in extra}
    record['additional_scope_deltas'] = {str(p): difference(record['additional_scopes_before'][str(p)], record['additional_scopes_after'][str(p)]) for p in extra}
    write_json(manifest, record)
    print(json.dumps({'name': args.name, 'status': record['status'], 'threads': summary['threads'], 'delta': record['delta'], 'last_message': summary['messages'][-1] if summary['messages'] else '', 'failed_commands': len(summary['failed_commands'])}, indent=2), flush=True)
    return 0 if record['status'] == 'returned' else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('graph'); p.add_argument('bundle')
    p = sub.add_parser('select', help='Read-only required and requested dependency closure')
    p.add_argument('bundle')
    p.add_argument('--component', action='append', default=[], help='Requested bundle-relative component path; repeatable')
    p = sub.add_parser('verify-selection', help='Check an actual proposed set without filling omissions')
    p.add_argument('bundle')
    p.add_argument('--selection', required=True, metavar='JSON', help='JSON list of proposed paths; use - for stdin')
    p = sub.add_parser('identity', help='Read-only whole-bundle byte manifest or comparison')
    p.add_argument('bundle')
    p.add_argument('--verify', metavar='MANIFEST', help='Compare saved JSON; use - to read stdin')
    p = sub.add_parser('snapshot'); p.add_argument('root'); p.add_argument('output')
    p = sub.add_parser('inspect'); p.add_argument('log'); p.add_argument('--source')
    p = sub.add_parser('run')
    for name in ('target', 'workspace', 'sandbox', 'output', 'name', 'task', 'prompt', 'source'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--model', choices=MODELS, required=True)
    p.add_argument('--reasoning-effort', choices=REASONING_EFFORTS,
                   help='Optional native Codex effort override; omission preserves native configuration. Verify model support separately.')
    p.add_argument('--policy', choices=('read-only', 'workspace-write'), default='workspace-write')
    p.add_argument('--agents', type=int, choices=(0, 1, 2), default=0)
    p.add_argument('--resume')
    p.add_argument('--schema')
    p.add_argument('--strict-config', action='store_true')
    p.add_argument('--add-dir', action='append', default=[], help='Explicit additional task-owned local destination; must be within workspace')
    args = parser.parse_args()
    if args.command == 'graph':
        print(json.dumps(graph(Path(args.bundle)), indent=2)); return 0
    if args.command in ('select', 'verify-selection'):
        try:
            if args.command == 'select':
                result = select_components(Path(args.bundle), args.component)
            else:
                data = sys.stdin.read() if args.selection == '-' else Path(args.selection).read_text()
                result = verify_selection(Path(args.bundle), json.loads(data, object_pairs_hook=unique_json_keys))
        except (ValueError, OSError) as error:
            parser.error(str(error))
        print(json.dumps(result, indent=2))
        return 1 if result.get('complete') is False else 0
    if args.command == 'identity':
        try:
            result = source_identity(Path(args.bundle))
            if args.verify is not None:
                data = sys.stdin.read() if args.verify == '-' else Path(args.verify).read_text()
                approved = json.loads(data, object_pairs_hook=unique_json_keys)
                result = verify_source_identity(result, approved)
        except (ValueError, OSError) as error:
            parser.error(str(error))
        print(json.dumps(result, indent=2))
        return 1 if result.get('match') is False else 0
    if args.command == 'snapshot':
        write_json(Path(args.output), snapshot(Path(args.root))); return 0
    if args.command == 'inspect':
        print(json.dumps(summarize(Path(args.log), Path(args.source) if args.source else None), indent=2)); return 0
    return run(args)

if __name__ == '__main__':
    raise SystemExit(main())
