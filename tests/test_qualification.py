"""Verify evidence boundaries, source graph integrity and fixture preservation helpers."""
import importlib.util
import contextlib
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

SPEC=importlib.util.spec_from_file_location('qualification',Path(__file__).parents[1]/'tools/qualification.py')
q=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(q)

class QualificationTests(unittest.TestCase):
    def test_returned_artifact_identities_survive_later_mutation_in_both_scopes(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            extra=root/'destination';extra.mkdir();prompt=root/'prompt.txt';prompt.write_text('unit fixture')
            args=SimpleNamespace(name='attempt',target=str(target),workspace=str(root),output=str(root/'evidence'),
                                 add_dir=[str(extra)],sandbox='unit-fixture',model='gpt-6-luna',policy='workspace-write',
                                 agents=0,strict_config=False,resume=None,schema=None,prompt=str(prompt),
                                 source=str(Path(__file__).parents[1]))
            def fixture_worker(cmd, input, stdout, stderr):
                (target/'artifact.txt').write_text('returned artifact')
                (extra/'receipt.txt').write_text('returned receipt')
                stdout.write((json.dumps({'type':'turn.completed','usage':{}})+'\n').encode())
                return SimpleNamespace(returncode=0)
            with patch.object(q.subprocess,'run',side_effect=fixture_worker), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(q.run(args),0)
            record=json.loads((root/'evidence/attempt.run.json').read_text())
            self.assertEqual(record['after'],q.snapshot(target))
            self.assertEqual(record['additional_scopes_after'][str(extra.resolve())],q.snapshot(extra))
            (target/'artifact.txt').write_text('later changed artifact');(extra/'receipt.txt').unlink()
            self.assertEqual(q.difference(record['after'],q.snapshot(target))['changed'],['artifact.txt'])
            self.assertEqual(q.difference(record['additional_scopes_after'][str(extra.resolve())],q.snapshot(extra))['removed'],['receipt.txt'])

    def test_run_rejects_path_names_before_any_output(self):
        for name in ('../escape', '/absolute', 'nested/name', '.hidden', ''):
            with self.assertRaisesRegex(ValueError, 'not a path'):
                q.run(SimpleNamespace(name=name))

    def test_existing_evidence_is_preserved_before_execution(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            out=root/'evidence';out.mkdir();log=out/'attempt.jsonl';log.write_text('retained failure')
            args=SimpleNamespace(name='attempt',target=str(target),workspace=str(root),output=str(out))
            with self.assertRaisesRegex(ValueError, 'cannot be overwritten'):q.run(args)
            self.assertEqual(log.read_text(),'retained failure')
            self.assertFalse((out/'attempt.run.json').exists())

    def test_additional_scope_rejects_symlink_escape_before_execution(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as outside:
            root=Path(d);target=root/'fixture';target.mkdir();(target/'.git').mkdir()
            alias=root/'destination';alias.symlink_to(outside,target_is_directory=True)
            out=root/'evidence'
            args=SimpleNamespace(name='attempt',target=str(target),workspace=str(root),output=str(out),add_dir=[str(alias)])
            with self.assertRaisesRegex(ValueError, 'task-owned directories'):q.run(args)
            self.assertEqual(list(out.iterdir()),[])

    def test_inventory_and_matrix_cover_same_25_components(self):
        root=Path(__file__).parents[1];nodes=q.graph(root/'bundle');matrix=json.loads((root/'tools/qualification-matrix.json').read_text())
        self.assertEqual(len(nodes),25)
        self.assertEqual(set(nodes),{x['source'] for x in matrix['components']})
        self.assertTrue(all(x['criteria'] and x['profiles'] for x in matrix['components']))
        self.assertEqual(sum(v['selection']=='required' for v in nodes.values()),10)

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
