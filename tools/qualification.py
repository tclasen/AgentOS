#!/usr/bin/env python3
"""Bounded native AgentOS qualification helpers; never grade semantics from a model's claim."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

MODELS = ('gpt-6.1-sol', 'gpt-6-luna')

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

def graph(bundle: Path) -> dict:
    """Read the deliberately small AgentOS metadata profile, not arbitrary YAML."""
    bundle = bundle.resolve()
    nodes = {}
    for path in sorted((bundle / 'components').glob('*.md')):
        if not path.resolve().is_relative_to(bundle):
            raise ValueError(f'component escapes bundle: {path.name}')
        content = path.read_text()
        front = content.split('---\n', 2)[1] if content.startswith('---\n') else ''
        marker = re.search(r'^agentos:\n', front, re.M)
        if marker is None:
            continue
        profile = front[marker.end():]
        selection = re.search(r'^  selection: (required|conditional)$', profile, re.M)
        requires = re.search(r'^  requires:(?: \[\])?\n((?:  - [^\n]+\n)*)', profile, re.M)
        if not selection or not requires:
            raise ValueError(f'invalid AgentOS metadata profile: {path.name}')
        deps = re.findall(r'^  - (\S+)$', requires.group(1), re.M)
        for dep in deps:
            target = (bundle / dep.lstrip('/')).resolve()
            if not target.is_relative_to(bundle) or not target.is_file():
                raise ValueError(f'missing or escaping dependency: {path.name} -> {dep}')
        key = path.relative_to(bundle).as_posix()
        nodes[key] = {'selection': selection.group(1), 'requires': [x.lstrip('/') for x in deps],
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
    def visit(node):
        if node in result:
            return
        if node not in nodes:
            raise ValueError(f'unknown component: {node}')
        if nodes[node].get('status') == 'deprecated':
            raise ValueError(f'selected component is deprecated: {node}')
        result.add(node)
        for dep in nodes[node]['requires']:
            visit(dep)
    for node in selected:
        visit(node)
    return sorted(result)

def select_components(bundle: Path, requested: list[str]) -> dict:
    """Compute structural selection only; this grants no authority or source-read credit."""
    nodes = graph(bundle)
    required = sorted(k for k, v in nodes.items() if v['selection'] == 'required')
    requested = sorted(set(requested))
    selected = closure(nodes, required + requested)
    return {'required': required, 'requested': requested, 'selected': selected,
            'components': {k: nodes[k] for k in selected},
            'limits': 'Structural selection only. Read full selected sources, reconcile user requirements, '
                      'and obtain applicable authority before installation or effects.'}

def snapshot(root: Path) -> dict:
    """Never follow symlinks into another project or credential directory."""
    root = root.resolve()
    result = {}
    for folder, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.pytest_cache')]
        base = Path(folder)
        for name in files + [d for d in dirs if (base / d).is_symlink()]:
            p = base / name
            key = p.relative_to(root).as_posix()
            if p.is_symlink():
                result[key] = {'symlink': os.readlink(p)}
            else:
                result[key] = {'sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
    return result

def difference(before: dict, after: dict) -> dict:
    return {'added': sorted(after.keys() - before.keys()), 'removed': sorted(before.keys() - after.keys()), 'changed': sorted(k for k in before.keys() & after.keys() if before[k] != after[k])}

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
    return result

def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

def run(args):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', args.name):
        raise ValueError('run name must be a simple evidence filename, not a path')
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
    record = {'name': args.name, 'task': 'TASK-000176', 'status': 'running', 'started_epoch': time.time(), 'owner': 'Coordinator', 'scope': str(target), 'additional_scopes_before': {str(p): snapshot(p) for p in extra}, 'requested_model': args.model, 'actual_model': 'unknown until session metadata collected', 'policy': args.policy, 'native_child_cap': args.agents, 'command': cmd, 'prompt_sha256': sha(Path(args.prompt).read_bytes()), 'before': before, 'source_components': graph(source / 'bundle'), 'monetary_cost': 'unknown'}
    record['source_bundle'] = snapshot(source / 'bundle')
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
    p = sub.add_parser('snapshot'); p.add_argument('root'); p.add_argument('output')
    p = sub.add_parser('inspect'); p.add_argument('log'); p.add_argument('--source')
    p = sub.add_parser('run')
    for name in ('target', 'workspace', 'sandbox', 'output', 'name', 'prompt', 'source'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--model', choices=MODELS, required=True)
    p.add_argument('--policy', choices=('read-only', 'workspace-write'), default='workspace-write')
    p.add_argument('--agents', type=int, choices=(0, 1, 2), default=0)
    p.add_argument('--resume')
    p.add_argument('--schema')
    p.add_argument('--strict-config', action='store_true')
    p.add_argument('--add-dir', action='append', default=[], help='Explicit additional task-owned local destination; must be within workspace')
    args = parser.parse_args()
    if args.command == 'graph':
        print(json.dumps(graph(Path(args.bundle)), indent=2)); return 0
    if args.command == 'select':
        try:
            result = select_components(Path(args.bundle), args.component)
        except ValueError as error:
            parser.error(str(error))
        print(json.dumps(result, indent=2)); return 0
    if args.command == 'snapshot':
        write_json(Path(args.output), snapshot(Path(args.root))); return 0
    if args.command == 'inspect':
        print(json.dumps(summarize(Path(args.log), Path(args.source) if args.source else None), indent=2)); return 0
    return run(args)

if __name__ == '__main__':
    raise SystemExit(main())
