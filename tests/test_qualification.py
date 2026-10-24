"""Verify evidence boundaries, source graph integrity and fixture preservation helpers."""
import importlib.util
import contextlib
import io
import json
from pathlib import Path
import tempfile
import subprocess
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SPEC=importlib.util.spec_from_file_location('qualification',Path(__file__).parents[1]/'tools/qualification.py')
q=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(q)

class QualificationTests(unittest.TestCase):
    def test_status_spellings_cannot_bypass_cli_deprecation_check(self):
        script=Path(__file__).parents[1]/'tools/qualification.py'
        for scalar in ['deprecated', '"deprecated"', "'deprecated'", 'deprecated # old', '"deprecated" # old', "'deprecated' # old"]:
            with self.subTest(scalar=scalar), tempfile.TemporaryDirectory() as d:
                root=Path(d);self.fixture_graph(root);p=root/'components/b.md'
                p.write_text(p.read_text().replace('---\n','---\nstatus: '+scalar+'\n',1))
                result=subprocess.run([sys.executable,str(script),'select',str(root)],capture_output=True,text=True)
                self.assertEqual(result.returncode,2);self.assertEqual(result.stdout,'')
                self.assertIn('deprecated: components/b.md',result.stderr)
                p.write_text(p.read_text().replace('deprecated','stable'))
                result=subprocess.run([sys.executable,str(script),'select',str(root)],capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(json.loads(result.stdout)['components']['components/b.md']['status'],'stable')

    def test_invalid_or_duplicate_status_declarations_fail_closed(self):
        for declaration in ['status: [deprecated]', 'status: |\n  deprecated', 'status:',
                            'status: "deprecated', 'status: stable\nstatus: deprecated']:
            with self.subTest(declaration=declaration), tempfile.TemporaryDirectory() as d:
                root=Path(d);self.fixture_graph(root);p=root/'components/b.md'
                p.write_text(p.read_text().replace('---\n','---\n'+declaration+'\n',1))
                with self.assertRaisesRegex(ValueError,'status'):
                    q.select_components(root,[])

    def test_requires_blank_comments_and_trailing_space_preserve_dependencies(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root);p=root/'components/a.md'
            p.write_text(p.read_text().replace('  requires:\n  - /components/b.md',
                '  requires:\n\n  # hard dependency\n  - /components/b.md   '))
            self.assertEqual(q.select_components(root,[])['selected'],['components/a.md','components/b.md'])

    def test_ambiguous_metadata_cannot_silently_remove_dependencies(self):
        original='agentos:\n  selection: required\n  requires:\n  - /components/b.md\n  provides: []\n'
        forms=[original.replace('  - /components/b.md','    - /components/b.md'),
               original.replace('  requires:\n','  requires: []\n  requires:\n'),
               'agentos:\n  selection: required\n  requires: []\n'+original,
               original.replace('  selection: required\n','  selection: required\n  selection: conditional\n'),
               original.replace('agentos:\n','agentos:\n  when_any: []\nother:\n'),
               original.replace('  - /components/b.md\n',''),
               original.replace('requires:\n  - /components/b.md','requires: [/components/b.md]'),
               original.replace('/components/b.md','/components/b.md extra'),
               original.replace('/components/b.md','"/components/b.md"')]
        script=Path(__file__).parents[1]/'tools/qualification.py'
        for front in forms:
            with self.subTest(front=front),tempfile.TemporaryDirectory() as d:
                root=Path(d);self.fixture_graph(root);(root/'components/a.md').write_text('---\n'+front+'---\n# A\n')
                before=q.snapshot(root)
                result=subprocess.run([sys.executable,str(script),'select',str(root)],capture_output=True,text=True)
                self.assertEqual(result.returncode,2,result.stderr);self.assertEqual(result.stdout,'')
                self.assertIn('metadata profile',result.stderr);self.assertEqual(q.snapshot(root),before)

    def test_unterminated_frontmatter_cannot_borrow_body_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root);p=root/'components/a.md'
            p.write_text(p.read_text().replace('---\n# a','\n# a'))
            with self.assertRaisesRegex(ValueError,'unterminated frontmatter'):q.select_components(root,[])

    def test_selection_seeds_required_and_closes_requested_dependencies(self):
        root=Path(__file__).parents[1];nodes=q.graph(root/'bundle')
        minimal=q.select_components(root/'bundle',[])
        self.assertEqual(set(minimal['selected']),{k for k,v in nodes.items() if v['selection']=='required'})
        requested=['components/parallel-coordination.md']
        extended=q.select_components(root/'bundle',requested*2)
        self.assertEqual(extended['requested'],requested)
        self.assertTrue(set(minimal['selected']) <= set(extended['selected']))
        self.assertIn('components/work-ledger.md',extended['selected'])
        for key in extended['selected']:
            self.assertTrue(set(nodes[key]['requires']) <= set(extended['selected']))
            self.assertEqual(extended['components'][key]['sha256'],q.sha((root/'bundle'/key).read_bytes()))

    def test_selected_deprecated_node_and_prerequisite_rejected_but_unselected_allowed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root)
            b=root/'components/b.md';b.write_text(b.read_text().replace('---\n','---\nstatus: deprecated\n',1))
            with self.assertRaisesRegex(ValueError,'deprecated: components/b.md'):
                q.select_components(root,[])  # a requires b, so even the minimal closure is blocked.
            a=root/'components/a.md';a.write_text(a.read_text().replace('requires:\n  - /components/b.md\n','requires: []\n'))
            self.assertEqual(q.select_components(root,[])['selected'],['components/a.md'])
            with self.assertRaisesRegex(ValueError,'deprecated: components/b.md'):
                q.select_components(root,['components/b.md'])
            a.write_text(a.read_text().replace('---\n','---\nstatus: deprecated\n',1))
            with self.assertRaisesRegex(ValueError,'deprecated: components/a.md'):
                q.select_components(root,[])

    def test_selection_cli_is_read_only_and_rejects_unknown_nodes(self):
        script=Path(__file__).parents[1]/'tools/qualification.py'
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root);before=q.snapshot(root)
            cmd=[sys.executable,str(script),'select',str(root)]
            good=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(good.returncode,0,good.stderr)
            self.assertEqual(json.loads(good.stdout)['selected'],['components/a.md','components/b.md'])
            bad=subprocess.run(cmd+['--component','components/absent.md'],capture_output=True,text=True)
            self.assertNotEqual(bad.returncode,0);self.assertIn('unknown component',bad.stderr)
            self.assertEqual(bad.stdout,'');self.assertEqual(q.snapshot(root),before)

    def test_returned_artifact_identities_survive_later_mutation_in_both_scopes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            extra=root/'destination';extra.mkdir();prompt=root/'prompt.txt';prompt.write_text('unit fixture')
            args=SimpleNamespace(name='attempt',task='TASK-000178',target=str(target),workspace=str(root),output=str(root/'evidence'),
                                 add_dir=[str(extra)],sandbox='unit-fixture',model='gpt-6-luna',policy='workspace-write',
                                 agents=0,strict_config=False,resume=None,schema=None,prompt=str(prompt),
                                 source=str(Path(__file__).parents[1]))
            def fixture_worker(cmd, input, stdout, stderr):
                (target/'artifact.txt').write_text('returned artifact')
                (target/'empty').mkdir();(extra/'empty/nested').mkdir(parents=True)
                (extra/'receipt.txt').write_text('returned receipt')
                stdout.write((json.dumps({'type':'turn.completed','usage':{}})+'\n').encode())
                return SimpleNamespace(returncode=0)
            with patch.object(q.subprocess,'run',side_effect=fixture_worker), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(q.run(args),0)
            record=json.loads((root/'evidence/attempt.run.json').read_text())
            self.assertEqual(record['task'],'TASK-000178')
            self.assertEqual(record['delta']['added'],['artifact.txt','empty'])
            self.assertEqual(record['additional_scope_deltas'][str(extra.resolve())]['added'],['empty','empty/nested','receipt.txt'])
            self.assertEqual(record['after'],q.snapshot(target))
            self.assertEqual(record['additional_scopes_after'][str(extra.resolve())],q.snapshot(extra))
            (target/'artifact.txt').write_text('later changed artifact');(extra/'receipt.txt').unlink()
            self.assertEqual(q.difference(record['after'],q.snapshot(target))['changed'],['artifact.txt'])
            self.assertEqual(q.difference(record['additional_scopes_after'][str(extra.resolve())],q.snapshot(extra))['removed'],['receipt.txt'])

    def test_missing_or_invalid_task_is_rejected_before_native_effects(self):
        script=Path(__file__).parents[1]/'tools/qualification.py'
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out=root/'evidence'
            cmd=[sys.executable,str(script),'run','--name','attempt','--target',str(root),
                 '--workspace',str(root),'--output',str(out),'--sandbox','not-a-real-sandbox',
                 '--source',str(Path(__file__).parents[1]),'--prompt',str(root/'absent-prompt'),
                 '--model','gpt-6-luna']
            missing=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(missing.returncode,2);self.assertIn('--task',missing.stderr)
            for task in ['', 'TASK-1', 'task-000178', 'TASK-000178/other', 'TASK-000178\n', 'TASK-１２３４５６']:
                with self.subTest(task=task), patch.object(q.subprocess,'run') as native:
                    with self.assertRaisesRegex(ValueError,'TASK-NNNNNN'):
                        q.run(SimpleNamespace(name='attempt',task=task,output=str(out)))
                    native.assert_not_called()
            self.assertFalse(out.exists())

    def test_distinct_task_ids_are_not_replaced_with_historical_task(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            prompt=root/'prompt';prompt.write_text('bounded fixture')
            for task in ['TASK-000178','TASK-123456']:
                args=SimpleNamespace(name=task,task=task,target=str(target),workspace=str(root),
                    output=str(root/'evidence'),add_dir=[],sandbox='unit-fixture',model='gpt-6-luna',
                    policy='workspace-write',agents=0,strict_config=False,resume=None,schema=None,
                    prompt=str(prompt),source=str(Path(__file__).parents[1]))
                def returned(cmd,input,stdout,stderr):
                    stdout.write(b'{"type":"turn.completed","usage":{}}\n')
                    return SimpleNamespace(returncode=0)
                with patch.object(q.subprocess,'run',side_effect=returned),contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(q.run(args),0)
                record=json.loads((root/'evidence'/f'{task}.run.json').read_text())
                self.assertEqual(record['task'],task)

    def test_reasoning_override_and_unset_preserve_fresh_and_resume_commands(self):
        for effort in [None, *q.REASONING_EFFORTS]:
            for resume in [None, 'observed-thread']:
                with self.subTest(effort=effort, resume=resume), tempfile.TemporaryDirectory() as d:
                    root=Path(d); target=root/'target'; target.mkdir(); (target/'.git').mkdir()
                    prompt=root/'prompt'; prompt.write_text('bounded fixture')
                    args=SimpleNamespace(name='effort',task='TASK-000188',target=str(target),workspace=str(root),
                        output=str(root/'evidence'),add_dir=[],sandbox='unit-fixture',model='gpt-6-luna',
                        policy='read-only',agents=0,strict_config=False,resume=resume,schema=None,
                        prompt=str(prompt),source=str(Path(__file__).parents[1]),reasoning_effort=effort)
                    def returned(cmd,input,stdout,stderr):
                        overrides=[(i,x) for i,x in enumerate(cmd) if x.startswith('model_reasoning_effort=')]
                        if effort is None:
                            self.assertEqual(overrides,[])
                        else:
                            self.assertEqual(len(overrides),1)
                            i,value=overrides[0];self.assertEqual(cmd[i-1],'-c')
                            self.assertEqual(json.loads(value.split('=',1)[1]),effort)
                            if resume:self.assertLess(i,cmd.index('resume'))
                        self.assertIn('agents.enabled=false',cmd)
                        self.assertEqual(cmd[cmd.index('--sandbox')+1],'read-only')
                        self.assertEqual(cmd[-2:] if resume else cmd[-1:], [resume,'-'] if resume else ['-'])
                        stdout.write(b'{"type":"turn.completed","usage":{}}\n')
                        return SimpleNamespace(returncode=0)
                    with patch.object(q.subprocess,'run',side_effect=returned),contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(q.run(args),0)
                    record=json.loads((root/'evidence/effort.run.json').read_text())
                    self.assertEqual(record['requested_reasoning_effort'],effort)
                    self.assertEqual(record['actual_reasoning_effort'],'unknown until session metadata collected')
                    self.assertEqual(record['delta'],{'added':[],'removed':[],'changed':[]})

    def test_invalid_reasoning_effort_is_rejected_before_any_effect(self):
        script=Path(__file__).parents[1]/'tools/qualification.py'
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out=root/'evidence'
            for effort in ['', 'HIGH', 'high\n', 'high; command', 'unsupported']:
                with self.subTest(effort=effort),patch.object(q.subprocess,'run') as native:
                    with self.assertRaisesRegex(ValueError,'reasoning effort'):
                        q.run(SimpleNamespace(reasoning_effort=effort))
                    native.assert_not_called()
                result=subprocess.run([sys.executable,str(script),'run','--name','invalid',
                    '--task','TASK-000188','--target',str(root),'--workspace',str(root),'--output',str(out),
                    '--sandbox','not-a-real-sandbox','--source',str(root),'--prompt',str(root/'absent'),
                    '--model','gpt-6-luna','--reasoning-effort',effort],capture_output=True,text=True)
                self.assertEqual(result.returncode,2);self.assertIn('--reasoning-effort',result.stderr)
                self.assertFalse(out.exists())

    def test_run_rejects_path_names_before_any_output(self):
        for name in ('../escape', '/absolute', 'nested/name', '.hidden', ''):
            with self.assertRaisesRegex(ValueError, 'not a path'):
                q.run(SimpleNamespace(name=name))

    def test_existing_evidence_is_preserved_before_execution(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            out=root/'evidence';out.mkdir();log=out/'attempt.jsonl';log.write_text('retained failure')
            args=SimpleNamespace(name='attempt',task='TASK-000178',target=str(target),workspace=str(root),output=str(out))
            with self.assertRaisesRegex(ValueError, 'cannot be overwritten'):q.run(args)
            self.assertEqual(log.read_text(),'retained failure')
            self.assertFalse((out/'attempt.run.json').exists())

    def test_additional_scope_rejects_symlink_escape_before_execution(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            alias=root/'destination';alias.symlink_to(outside,target_is_directory=True)
            out=root/'evidence'
            args=SimpleNamespace(name='attempt',task='TASK-000178',target=str(target),workspace=str(root),output=str(out),add_dir=[str(alias)])
            with self.assertRaisesRegex(ValueError, 'task-owned directories'):q.run(args)
            self.assertEqual(list(out.iterdir()),[])

    def test_inventory_and_matrix_cover_same_25_components(self):
        root=Path(__file__).parents[1];nodes=q.graph(root/'bundle');matrix=json.loads((root/'tools/qualification-matrix.json').read_text())
        self.assertEqual(len(nodes),25)
        self.assertEqual(set(nodes),{x['source'] for x in matrix['components']})
        self.assertTrue(all(x['criteria'] and x['profiles'] for x in matrix['components']))
        self.assertEqual(sum(v['selection']=='required' for v in nodes.values()),10)

    def test_selection_ignores_unselected_broken_edges_but_graph_audits_them(self):
        for dep in ['/components/missing.md','../outside.md']:
            with self.subTest(dep=dep),tempfile.TemporaryDirectory() as d:
                root=Path(d);self.fixture_graph(root)
                a=root/'components/a.md';a.write_text(a.read_text().replace('requires:\n  - /components/b.md','requires: []'))
                b=root/'components/b.md';b.write_text(b.read_text().replace('requires: []','requires:\n  - '+dep))
                self.assertEqual(q.select_components(root,[])['selected'],['components/a.md'])
                with self.assertRaisesRegex(ValueError,'unknown component'):q.select_components(root,['components/b.md'])
                with self.assertRaisesRegex(ValueError,'missing or escaping'):q.graph(root)

    def test_closure_detects_cycles_and_only_selected_cycles_block_selection(self):
        nodes={'a':{'requires':['b']},'b':{'requires':['a']},'c':{'requires':[]}}
        self.assertEqual(q.closure(nodes,['c']),['c'])
        with self.assertRaisesRegex(ValueError,'cycle'):q.closure(nodes,['a'])
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root)
            a=root/'components/a.md';a.write_text(a.read_text().replace('requires:\n  - /components/b.md','requires: []'))
            b=root/'components/b.md';b.write_text(b.read_text().replace('requires: []','requires:\n  - /components/b.md'))
            self.assertEqual(q.select_components(root,[])['selected'],['components/a.md'])
            with self.assertRaisesRegex(ValueError,'cycle'):q.select_components(root,['components/b.md'])
            with self.assertRaisesRegex(ValueError,'cycle'):q.graph(root)

    def test_selection_and_full_audit_cli_keep_distinct_read_only_contracts(self):
        script=Path(__file__).parents[1]/'tools/qualification.py'
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root)
            a=root/'components/a.md';a.write_text(a.read_text().replace('requires:\n  - /components/b.md','requires: []'))
            b=root/'components/b.md';b.write_text(b.read_text().replace('requires: []','requires:\n  - /components/missing.md'));before=q.snapshot(root)
            minimal=subprocess.run([sys.executable,str(script),'select',str(root)],capture_output=True,text=True)
            self.assertEqual(minimal.returncode,0,minimal.stderr);self.assertEqual(json.loads(minimal.stdout)['selected'],['components/a.md'])
            for command,extra in [('graph',[]),('select',['--component','components/b.md'])]:
                result=subprocess.run([sys.executable,str(script),command,str(root),*extra],capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0);self.assertEqual(result.stdout,'')
            self.assertEqual(q.snapshot(root),before)

    def test_dependency_closure_includes_transitive_prerequisites(self):
        nodes={'a':{'requires':['b']},'b':{'requires':['c']},'c':{'requires':[]}}
        self.assertEqual(q.closure(nodes,['a']),['a','b','c'])
        with self.assertRaises(ValueError):q.closure(nodes,['unknown'])

    def fixture_graph(self,root,dep='/components/b.md'):
        c=root/'components';c.mkdir()
        (c/'index.md').write_text('## Required\n[A](a.md)\n## Conditional components\n[B](b.md)\n')
        for name,selection,requires in [('a','required',f'\n  - {dep}\n'),('b','conditional',' []\n')]:
            (c/f'{name}.md').write_text(f'---\nagentos:\n  selection: {selection}\n  requires:{requires}  provides: []\n---\n# {name}\n')

    def test_missing_dependency_and_escape_are_rejected(self):
        for dep in ('/components/missing.md','../outside.md'):
            with tempfile.TemporaryDirectory() as d:
                root=Path(d)/'bundle';root.mkdir();self.fixture_graph(root,dep)
                with self.assertRaisesRegex(ValueError,'missing or escaping dependency'):q.graph(root)

    def test_cyclic_graph_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture_graph(root)
            (root/'components/b.md').write_text('---\nagentos:\n  selection: conditional\n  requires:\n  - /components/a.md\n  provides: []\n---\n')
            with self.assertRaisesRegex(ValueError,'cycle'):q.graph(root)

    def test_symlinked_source_cannot_escape(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'bundle';root.mkdir();self.fixture_graph(root)
            outside=Path(d)/'private.md';outside.write_text('private')
            (root/'components/b.md').unlink();(root/'components/b.md').symlink_to(outside)
            with self.assertRaisesRegex(ValueError,'escap'):q.graph(root)

    def test_empty_directory_add_remove_and_type_changes_are_observable(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'removed').mkdir();(root/'to-file').mkdir();(root/'to-link').mkdir()
            before=q.snapshot(root)
            (root/'removed').rmdir();(root/'to-file').rmdir();(root/'to-file').write_text('replacement')
            (root/'to-link').rmdir();(root/'to-link').symlink_to('missing-directory',target_is_directory=True)
            (root/'added/nested').mkdir(parents=True)
            after=q.snapshot(root)
            self.assertEqual(q.difference(before,after),{'added':['added','added/nested'],
                'removed':['removed'],'changed':['to-file','to-link']})
            self.assertEqual(after['added/nested'],{'directory':True})
            self.assertEqual(after['to-link'],{'symlink':'missing-directory'})
            self.assertEqual(after['to-file']['sha256'],q.sha(b'replacement'))
            self.assertNotIn('.',after)

    def test_directory_snapshot_cli_is_read_only_preserves_exclusions_and_links(self):
        script=Path(__file__).parents[1]/'tools/qualification.py'
        with tempfile.TemporaryDirectory() as d:
            parent=Path(d);root=parent/'fixture';root.mkdir();outside=parent/'outside';outside.mkdir()
            (outside/'secret').write_text('not snapshot content')
            (root/'link').symlink_to(outside,target_is_directory=True);(root/'empty').mkdir()
            for excluded in ['.git','__pycache__','.pytest_cache']:
                (root/excluded/'nested').mkdir(parents=True);(root/excluded/'nested/private').write_text('omitted')
            inventory=lambda: sorted(str(p.relative_to(root)) for p in root.rglob('*'))
            before=inventory();out=parent/'snapshot.json'
            result=subprocess.run([sys.executable,str(script),'snapshot',str(root),str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(out.read_text()),{'empty':{'directory':True},'link':{'symlink':str(outside)}})
            self.assertEqual(inventory(),before);self.assertEqual((outside/'secret').read_text(),'not snapshot content')

    def test_snapshot_tracks_untracked_edits_without_following_symlink(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project';root.mkdir();outside=Path(d)/'private';outside.write_text('secret')
            (root/'link').symlink_to(outside);(root/'untracked').write_text('one')
            before=q.snapshot(root);(root/'untracked').write_text('two');(root/'new').write_text('new')
            delta=q.difference(before,q.snapshot(root))
            self.assertEqual(delta,{'added':['new'],'removed':[],'changed':['untracked']})
            self.assertEqual(before['link'],{'symlink':str(outside)})
            self.assertNotIn('secret',json.dumps(before))

    def test_only_successfully_completed_full_source_reads_are_credited(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'bundle/components').mkdir(parents=True);(root/'bundle/components/a.md').write_text('complete source text')
            log=root/'run.jsonl'
            log.write_text('\n'.join(json.dumps(x) for x in [
                {'type':'item.started','item':{'type':'command_execution','aggregated_output':'complete source text'}},
                {'type':'item.completed','item':{'type':'command_execution','exit_code':1,'aggregated_output':'complete source text'}},
                {'type':'item.completed','item':{'type':'agent_message','text':'I read complete source text'}}]))
            self.assertEqual(q.summarize(log,root)['full_component_reads_observed'],[])
            with log.open('a') as f:f.write('\n'+json.dumps({'type':'item.completed','item':{'type':'command_execution','exit_code':0,'aggregated_output':'complete source text'}}))
            self.assertEqual(q.summarize(log,root)['full_component_reads_observed'],['components/a.md'])

    def test_noise_and_error_are_retained_without_becoming_a_pass(self):
        with tempfile.TemporaryDirectory() as d:
            log=Path(d)/'run.jsonl';log.write_text('sandbox starting\n'+json.dumps({'type':'turn.failed','error':{'message':'blocked'}}))
            s=q.summarize(log)
            self.assertEqual(s['turn_completed'],0);self.assertEqual(len(s['errors']),1)

if __name__=='__main__':unittest.main()
