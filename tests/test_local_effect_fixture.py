import json
import hashlib
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

    def test_lookup_binds_committed_candidate_without_echoing_payload(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'destination.sqlite';payload='approved candidate payload'
            self.assertEqual(self.call(p,'attempt','--payload',payload,'--drop-ack')[0],75)
            code,receipt=self.call(p,'lookup')
            self.assertEqual(code,0);self.assertEqual(receipt['outcome'],'present')
            expected=hashlib.sha256(payload.encode()).hexdigest()
            self.assertEqual(receipt['observed_payload_sha256'],expected)
            self.assertNotIn(payload,json.dumps(receipt))
            self.assertEqual(self.call(p,'attempt','--payload','conflicting candidate')[0],65)
            self.assertEqual(self.call(p,'lookup')[1]['observed_payload_sha256'],expected)

    def test_absent_or_unavailable_lookup_cannot_claim_candidate_binding(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'destination.sqlite'
            code,absent=self.call(p,'lookup')
            self.assertEqual(code,0);self.assertEqual(absent['outcome'],'absent')
            self.assertIsNone(absent['observed_payload_sha256'])
            self.call(p,'attempt')
            code,offline=self.call(p,'lookup','--offline')
            self.assertEqual(code,75);self.assertEqual(offline['outcome'],'unknown')
            self.assertFalse(offline['lookup_is_available'])
            self.assertIsNone(offline['observed_payload_sha256'])
            self.assertIsNotNone(self.call(p,'lookup')[1]['observed_payload_sha256'])

if __name__=='__main__':unittest.main()
