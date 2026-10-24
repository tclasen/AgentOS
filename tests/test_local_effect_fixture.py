import json
from contextlib import closing
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

CLIENT=Path(__file__).parents[1]/'tools/local_effect_fixture.py'

class LocalEffectTests(unittest.TestCase):
    def call(self,path,action,*args):
        p=subprocess.run([sys.executable,str(CLIENT),action,'--store',str(path),'--id','case-1',*args],capture_output=True,text=True)
        return p.returncode,json.loads(p.stdout)

    def test_lost_ack_preserves_effect_and_fresh_lookup_observes_it(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'destination.sqlite'
            code,result=self.call(p,'attempt','--drop-ack');self.assertEqual(code,75)
            self.assertEqual(result['outcome'],'acknowledgment_lost')
            self.assertEqual(self.call(p,'lookup')[1]['outcome'],'present')
            with closing(sqlite3.connect(p)) as db:
                self.assertEqual(db.execute('SELECT count(*) FROM receipts').fetchone()[0],1)
                self.assertEqual(db.execute("SELECT count(*) FROM calls WHERE action='attempt'").fetchone()[0],1)

    def test_unavailable_lookup_does_not_claim_absence_or_create_effect(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'destination.sqlite';code,result=self.call(p,'lookup','--offline')
            self.assertEqual(code,75);self.assertEqual(result['outcome'],'unknown')
            with closing(sqlite3.connect(p)) as db:self.assertEqual(db.execute('SELECT count(*) FROM receipts').fetchone()[0],0)

    def test_replay_is_detectable_and_changed_candidate_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'destination.sqlite'
            self.assertEqual(self.call(p,'attempt')[1]['outcome'],'created')
            self.assertEqual(self.call(p,'attempt')[1]['outcome'],'already_present')
            self.assertEqual(self.call(p,'attempt','--payload','different')[0],65)
            with closing(sqlite3.connect(p)) as db:
                self.assertEqual(db.execute('SELECT count(*) FROM receipts').fetchone()[0],1)
                self.assertEqual(db.execute("SELECT count(*) FROM calls WHERE action='attempt'").fetchone()[0],3)

if __name__=='__main__':unittest.main()
