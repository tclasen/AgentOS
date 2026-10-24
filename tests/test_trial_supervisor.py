"""Exercise real deadline processes and runner failure/evidence boundaries."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
SUPERVISOR = ROOT / 'tools/trial_supervisor.py'
SPEC = importlib.util.spec_from_file_location('deadline_qualification', ROOT / 'tools/qualification.py')
q = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(q)


class SupervisorTests(unittest.TestCase):
    def invoke(self, code, seconds=1, args=(), input=None):
        result = subprocess.run([sys.executable, '-B', str(SUPERVISOR), str(seconds), 'test',
                                 sys.executable, '-B', '-c', code, *args],
                                input=input, text=True, capture_output=True, timeout=12)
        rows = []
        for line in result.stdout.splitlines():
            try: row = json.loads(line)
            except ValueError: continue
            if isinstance(row, dict) and row.get('type') == 'agentos.run_control': rows.append(row)
        return result, rows

    def test_success_preserves_stdin_argv_and_real_exit_124_is_not_timeout(self):
        value = 'literal spaces; $(not-a-command)\n'
        result, rows = self.invoke('import sys,json; print(json.dumps([sys.argv[1],sys.stdin.read()]))',
                                   args=(value,), input='prompt\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(json.dumps([value, 'prompt\n']), result.stdout)
        self.assertFalse(rows[-1]['timed_out']); self.assertEqual(rows[-1]['signals'], [])
        for code in [7, 124]:
            with self.subTest(code=code):
                result, rows = self.invoke('raise SystemExit('+str(code)+')')
                self.assertEqual(result.returncode, code)
                self.assertFalse(rows[-1]['timed_out']); self.assertEqual(rows[-1]['child_returncode'], code)

    def test_deadline_preserves_partial_output_even_with_fake_completed_turn(self):
        result, rows = self.invoke('import time; print(\'{"type":"turn.completed"}\',flush=True); print("partial",end="",flush=True); time.sleep(30)')
        self.assertEqual(result.returncode, 124); self.assertIn('partial', result.stdout)
        self.assertTrue(rows[-1]['timed_out']); self.assertIn('SIGINT', rows[-1]['signals'])
        self.assertGreaterEqual(rows[-1]['elapsed_seconds'], 1)
        self.assertLess(rows[-1]['elapsed_seconds'], 4)

    def test_interrupt_ignored_is_killed_and_unrelated_process_survives(self):
        unrelated = subprocess.Popen([sys.executable, '-B', '-c', 'import time; time.sleep(30)'], start_new_session=True)
        try:
            result, rows = self.invoke('import signal,time; signal.signal(signal.SIGINT,signal.SIG_IGN); print("ready",flush=True); time.sleep(30)')
            self.assertEqual(result.returncode, 124); self.assertTrue(rows[-1]['timed_out'])
            self.assertEqual(rows[-1]['signals'], ['SIGINT', 'SIGKILL'])
            self.assertEqual(rows[-1]['child_returncode'], -signal.SIGKILL)
            self.assertLess(rows[-1]['elapsed_seconds'], 9)
            self.assertIsNone(unrelated.poll())
        finally:
            unrelated.kill(); unrelated.wait(timeout=3)

    def test_same_group_descendant_cannot_continue_writing_after_deadline(self):
        with tempfile.TemporaryDirectory() as d:
            marker = Path(d)/'late'
            child = 'import signal,time,pathlib; signal.signal(signal.SIGINT,signal.SIG_IGN); time.sleep(3); pathlib.Path('+repr(str(marker))+').write_text("escaped")'
            code = 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-B","-c",'+repr(child)+']); time.sleep(30)'
            result, rows = self.invoke(code)
            self.assertEqual(result.returncode, 124); self.assertIn('SIGKILL', rows[-1]['signals'])
            time.sleep(2.5)
            self.assertFalse(marker.exists())

    def test_launch_failure_and_invalid_limit_do_not_become_success(self):
        result = subprocess.run([sys.executable,'-B',str(SUPERVISOR),'1','test','/does/not/exist'],capture_output=True,text=True,timeout=3)
        self.assertEqual(result.returncode,127); self.assertIn('launch_failed',result.stdout)
        for limit in ['0','-1','86401','nan']:
            result = subprocess.run([sys.executable,'-B',str(SUPERVISOR),limit,'test',sys.executable,'-c','print("STARTED")'],capture_output=True,text=True,timeout=3)
            self.assertNotEqual(result.returncode,0); self.assertNotIn('STARTED',result.stdout)

    def test_closed_transport_output_does_not_leave_new_command_running(self):
        with tempfile.TemporaryDirectory() as d:
            marker = Path(d)/'late'
            code = 'import time,pathlib; time.sleep(1); pathlib.Path('+repr(str(marker))+').write_text("orphan")'
            process = subprocess.Popen([sys.executable,'-B',str(SUPERVISOR),'10','test',sys.executable,'-B','-c',code],
                                       stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
            process.stdout.close()
            self.assertNotEqual(process.wait(timeout=3),0)
            time.sleep(1.2)
            self.assertFalse(marker.exists())


class RunnerDeadlineTests(unittest.TestCase):
    def args(self, root):
        target=root/'target'; target.mkdir(); (target/'.git').mkdir()
        prompt=root/'prompt'; prompt.write_text('fixture')
        return SimpleNamespace(name='deadline',task='TASK-000205',target=str(target),workspace=str(root),
            output=str(root/'evidence'),add_dir=[],sandbox='unit',model='gpt-6-luna',policy='read-only',
            agents=0,strict_config=False,resume=None,schema=None,prompt=str(prompt),source=str(ROOT),timeout_seconds=1)

    def test_invalid_timeout_has_no_effect(self):
        for value in [0,-1,86401,True,1.5,'1',None]:
            with self.subTest(value=value), patch.object(q.subprocess,'run') as native:
                with self.assertRaisesRegex(ValueError,'timeout seconds'): q.run(SimpleNamespace(timeout_seconds=value))
                native.assert_not_called()

    def test_missing_ambiguous_and_timeout_receipts_fail_closed(self):
        common={'type':'agentos.run_control','version':1,'control_id':'deadline','timeout_seconds':1,'pid':123,'process_group':123,'grace_seconds':5}
        start=dict(common,phase='started'); end=dict(common,phase='finished',timed_out=False,exit_code=0,child_returncode=0,elapsed_seconds=0.1,signals=[])
        for rows,returncode in [([start,dict(end,elapsed_seconds=None)],0),([start,dict(end,child_returncode=None)],0),([start,dict(end,elapsed_seconds=float('nan'))],0),([],0),([start,end,end],0),([start,dict(end,control_id='wrong')],0),
                                ([start,dict(end,timed_out=True,exit_code=124)],124),
                                ([start,dict(end,timed_out=True)],0)]:
            with self.subTest(rows=rows),tempfile.TemporaryDirectory() as d:
                root=Path(d);args=self.args(root)
                def fixture(cmd,input,stdout,stderr,timeout):
                    self.assertEqual(timeout,31)
                    for row in [{'type':'turn.completed'},*rows]: stdout.write((json.dumps(row)+'\n').encode())
                    return SimpleNamespace(returncode=returncode)
                with patch.object(q.subprocess,'run',side_effect=fixture),contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(q.run(args),1)
                record=json.loads((root/'evidence/deadline.run.json').read_text())
                self.assertEqual(record['status'],'failed')
                self.assertEqual(json.dumps(record['run_control'],sort_keys=True),json.dumps(rows,sort_keys=True))
                self.assertEqual(record['summary']['turn_completed'],1)

    def test_transport_timeout_retains_partial_evidence_and_after_state(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);args=self.args(root)
            def stalled(cmd,input,stdout,stderr,timeout):
                stdout.write(b'{"type":"thread.started","thread_id":"observed"}\npartial line')
                (root/'target/artifact').write_text('observed effect')
                raise subprocess.TimeoutExpired(cmd,timeout)
            with patch.object(q.subprocess,'run',side_effect=stalled),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(q.run(args),1)
            record=json.loads((root/'evidence/deadline.run.json').read_text())
            self.assertTrue(record['transport_timed_out']); self.assertIsNone(record['timed_out'])
            self.assertIsNone(record['returncode']); self.assertFalse(record['control_evidence_valid'])
            self.assertEqual(record['summary']['threads'],['observed'])
            self.assertEqual(record['delta']['added'],['artifact'])
            self.assertTrue((root/'evidence/deadline.jsonl').read_text().endswith('partial line'))

if __name__=='__main__': unittest.main()
