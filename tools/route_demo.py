#!/usr/bin/env python3
"""Advisory signal-based routing example, NOT an autonomous installer.
Real installation additionally requires context, component interviews and approval.
"""
from validate_bundle import parse
import argparse

def route(signals):
    _,comps,errors=parse()
    if errors: raise RuntimeError(str(errors))
    selected={k for k,v in comps.items() if v['meta']['agentos']['selection']=='required'}
    initial=set(selected)
    selected.update(k for k,v in comps.items() if set(v['meta']['agentos']['when_any']) & set(signals))
    reason={k:('mandatory' if k in initial else 'matching signal') for k in selected}
    def closure(node):
        for dep in comps[node]['meta']['agentos']['requires']:
            if dep not in selected:
                selected.add(dep); reason[dep]='required by '+node;closure(dep)
    for node in list(selected):closure(node)
    return selected,reason,comps

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--signal',action='append',default=[])
    args=ap.parse_args();nodes,why,all_nodes=route(set(args.signal))
    print(f'Advisory selection: {len(nodes)} of {len(all_nodes)} components')
    for n in sorted(nodes):print(f'{n:49} {why[n]}')
    print('Next: inspect selected component follow-up questions; do not auto-install.')
if __name__=='__main__':main()
