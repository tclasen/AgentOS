#!/usr/bin/env python3
"""Validate OKF v0.2 structure plus stricter optional AgentOS graph integrity.
PyYAML is a contributor-only dependency, not required to consume the bundle.
"""
from pathlib import Path
import re, sys
try:
    import yaml
except ImportError:
    raise SystemExit('Run: python3 -m pip install -r requirements-dev.txt')
BUNDLE = Path(__file__).resolve().parents[1] / 'bundle'
REQUIRED = {'director','chief-of-staff','activation','authority','capability-routing','delegation','delivery-acceptance','context-core','self-improvement','role-lifecycle'}
LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)')

def parse(bundle=BUNDLE):
    root=Path(bundle).resolve(); nodes={}; errors=[]
    for file in sorted(root.rglob('*.md')):
        rel=file.relative_to(root).as_posix(); s=file.read_text(encoding='utf-8')
        if file.name in ('index.md','log.md'):
            if file.name=='index.md' and s.startswith('---\n'):
                if file!=root/'index.md': errors.append(f'{rel}: only root index may have version frontmatter')
                else:
                    m=re.match(r'^---\n(.*?)\n---\n',s,re.S)
                    if not m or yaml.safe_load(m.group(1))!={'okf_version':'0.2'}:
                        errors.append(f'{rel}: invalid root okf_version')
            if file.name=='log.md':
                for line in s.splitlines():
                    if line.startswith('## ') and not re.fullmatch(r'## \d{4}-\d{2}-\d{2}',line):
                        errors.append(f'{rel}: log date must be YYYY-MM-DD')
        else:
            m=re.match(r'^---\n(.*?)\n---\n',s,re.S)
            if not m:
                errors.append(f'{rel}: missing YAML frontmatter'); continue
            try: meta=yaml.safe_load(m.group(1))
            except yaml.YAMLError as e: errors.append(f'{rel}: YAML parse error {e}'); continue
            if not isinstance(meta,dict) or not isinstance(meta.get('type'),str) or not meta['type'].strip():
                errors.append(f'{rel}: type required');continue
            s=s[m.end():]
            nodes['/'+rel]={'meta':meta,'body':s}
        for target in LINK.findall(s):
            target=target.split('#')[0].split('?')[0]
            if not target or re.match(r'^[a-z][a-z0-9+.-]*:',target,re.I) or target.startswith('//'):continue
            dest=((root/target.lstrip('/')) if target.startswith('/') else (file.parent/target)).resolve()
            if not dest.is_relative_to(root): errors.append(f'{rel}: link escapes bundle: {target}')
            elif not dest.exists(): errors.append(f'{rel}: link missing: {target}')
    comps={k:v for k,v in nodes.items() if v['meta']['type']=='AgentOS Component'}
    for key in REQUIRED:
        id_='/components/'+key+'.md'
        if id_ not in comps or comps[id_]['meta'].get('agentos',{}).get('selection')!='required':
            errors.append(f'Missing mandatory component: {id_}')
    for name,obj in comps.items():
        a=obj['meta'].get('agentos')
        if not isinstance(a,dict) or a.get('selection') not in ('required','conditional'):
            errors.append(f'{name}: bad AgentOS extension');continue
        for field in ('when_any','requires','provides'):
            if not isinstance(a.get(field),list) or not all(isinstance(x,str) for x in a[field]):
                errors.append(f'{name}: expected list agentos.{field}')
        if a['selection']=='required' and a['when_any']:
            errors.append(f'{name}: required node must not depend on optional signals')
        for dep in a['requires']:
            if dep not in comps: errors.append(f'{name}: missing hard prerequisite {dep}')
            elif not any(
                (root / name.lstrip('/')).parent.joinpath(link).resolve()
                == (root / dep.lstrip('/')).resolve()
                for link in LINK.findall(obj['body'])
            ):
                errors.append(f'{name}: hard prerequisite lacks graph link {dep}')
    visiting=set();done=set()
    def visit(name):
        if name in visiting:errors.append('Dependency cycle at '+name);return
        if name in done:return
        visiting.add(name)
        for dep in comps[name]['meta']['agentos']['requires']:
            if dep in comps: visit(dep)
        visiting.remove(name);done.add(name)
    for name in comps:visit(name)
    return nodes,comps,errors

def main():
    nodes,comps,errors=parse()
    print(f'{len(nodes)} OKF concepts, {len(comps)} components ({len(REQUIRED)} mandatory)')
    for e in errors:print('ERROR:',e)
    if errors:return 1
    print('PASS: OKF structure and stricter AgentOS graph checks')
    return 0
if __name__=='__main__':sys.exit(main())
