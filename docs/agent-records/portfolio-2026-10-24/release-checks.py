"""Reproduce the CPU-only release checks; creates evidence beside this script.

Does not perform an agent installation or grant qualification to one.
"""
from pathlib import Path
import datetime
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
# parents: portfolio -> agent-records -> docs -> repo
LOG = OUT / 'release-checks.log'
REPORT = OUT / 'release-checks.json'
BASE = 'e352574dc4b932ae1cdc8e5d94a98a5e86f619ae'
report = {'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'baseline': BASE, 'python': sys.version, 'platform': platform.platform(),
          'limits': 'CPU-only local checks; no AI installation, native model trial, external effect or runtime qualification',
          'checks': []}
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
if LOG.exists() or REPORT.exists():
    raise SystemExit('Evidence exists: run a copied source checkout or preserve the prior attempt before retrying.')
LOG.write_text('AgentOS CPU-only release verification\n')
REPORT.write_text('{}\n')

def run(name, args, *, cwd=ROOT, expected=0, timeout=60):
    start = time.monotonic()
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    output = p.stdout + p.stderr
    with LOG.open('a') as log:
        log.write('\n## ' + name + '\n' + json.dumps(args) + '\n' + output + '\n')
    row = {'name': name, 'argv': args, 'cwd': str(cwd), 'expected_exit': expected,
           'actual_exit': p.returncode, 'elapsed_seconds': time.monotonic()-start,
           'output_sha256': hashlib.sha256(output.encode()).hexdigest(),
           'pass': p.returncode == expected}
    report['checks'].append(row)
    assert row['pass'], (name, p.returncode, output[-3000:])
    return p.stdout

try:
    py = sys.executable
    run('existing-regressions', [py, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], timeout=600)
    graph = json.loads(run('bundle-graph', [py, '-B', 'tools/qualification.py', 'graph', 'bundle']))
    assert len(graph) == 25
    matrix = json.loads((ROOT/'tools/qualification-matrix.json').read_text())
    for profile, count in [('portable', 10), ('engineering', 22), ('portfolio', 18)]:
        command = [py, '-B', 'tools/qualification.py', 'select', 'bundle']
        for component in matrix['components']:
            if profile in component['profiles'] and component['selection'] != 'required':
                command += ['--component', component['source']]
        selected = json.loads(run(profile+'-selection', command))
        # Structural coverage, not implementation or behavioral admission.
        observed = selected.get('selected', selected.get('components', selected.get('closure')))
        assert len(observed) == count, (profile, selected)
    run('release-manifest', [py, '-B', 'tools/qualification.py', 'identity', 'bundle', '--verify',
                            'docs/releases/2026-10-24-source.json'])
    with tempfile.TemporaryDirectory(prefix='agentos-release-smoke-') as temp:
        fixture = Path(temp)
        shutil.copytree(ROOT/'bundle', fixture/'bundle')
        shutil.copytree(ROOT/'tools', fixture/'tools')
        shutil.copy2(ROOT/'docs/releases/2026-10-24-source.json', fixture/'approved.json')
        # Run as a separate copied checkout with no Git metadata or dependencies.
        run('copied-source-graph', [py, '-B', 'tools/qualification.py', 'graph', 'bundle'], cwd=fixture)
        run('copied-source-identity', [py, '-B', 'tools/qualification.py', 'identity', 'bundle', '--verify', 'approved.json'], cwd=fixture)
        with (fixture/'bundle/start.md').open('a') as stream:
            stream.write('\ncontrolled release smoke alteration\n')
        changed = json.loads(run('copied-source-change-refused', [py, '-B', 'tools/qualification.py', 'identity', 'bundle', '--verify', 'approved.json'], cwd=fixture, expected=1))
        assert changed == {'match': False, 'delta': {'added': [], 'removed': [], 'changed': ['start.md']}}
    links = 0
    broken = []
    # Local file resolution only; do not request URLs or treat prose/code as source reads.
    for doc in [ROOT/'README.md', *sorted((ROOT/'bundle').rglob('*.md')), ROOT/'tools/README.md', ROOT/'docs/releases/2026-10-24-preview.md']:
        for raw in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', doc.read_text()):
            dest = raw.split('#', 1)[0]
            if not dest or re.match(r'[A-Za-z][A-Za-z0-9+.-]*:', dest):
                continue
            target = (doc.parent/unquote(dest)).resolve()
            links += 1
            if not target.exists():
                broken.append([str(doc.relative_to(ROOT)), raw])
    report['checks'].append({'name': 'published-entrypoint-and-bundle-local-links', 'links': links,
                             'broken': broken, 'pass': not broken,
                             'limit': 'local file destinations only; no fragment or external URL validation'})
    assert not broken, broken
    before = json.loads((OUT/'governance-before.json').read_text())
    after = {p: hashlib.sha256((Path('/Users/Shared/agent-org')/p).read_bytes()).hexdigest() for p in before}
    report['governance_before'] = before
    report['governance_after'] = after
    assert before == after
    report['bundle_files'] = len(json.loads((ROOT/'docs/releases/2026-10-24-source.json').read_text())['files'])
    report['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for base in ('bundle', 'tools', 'tests') for p in sorted((ROOT/base).rglob('*')) if p.is_file()}
    report['pass'] = True
except Exception as error:
    report['pass'] = False
    report['error'] = repr(error)
    raise
finally:
    report['log_sha256'] = hashlib.sha256(LOG.read_bytes()).hexdigest()
    report['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'pass': report['pass'], 'checks': len(report['checks']), 'report': str(REPORT)}))
