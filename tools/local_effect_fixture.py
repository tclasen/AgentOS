#!/usr/bin/env python3
"""A LOCAL test destination for lost-acknowledgment trials, never a real provider."""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
import time

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['attempt','lookup'])
    p.add_argument('--store',required=True)
    p.add_argument('--id',required=True)
    p.add_argument('--payload',default='bounded-test-output')
    p.add_argument('--drop-ack',action='store_true')
    p.add_argument('--offline',action='store_true')
    a=p.parse_args();path=Path(a.store);path.parent.mkdir(parents=True,exist_ok=True)
    db=sqlite3.connect(path,timeout=10)
    db.execute('CREATE TABLE IF NOT EXISTS receipts (identity TEXT PRIMARY KEY, digest TEXT NOT NULL, created REAL NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS calls (sequence INTEGER PRIMARY KEY, action TEXT NOT NULL, identity TEXT NOT NULL, result TEXT NOT NULL)')
    db.execute('BEGIN IMMEDIATE')
    row=db.execute('SELECT digest FROM receipts WHERE identity=?',(a.id,)).fetchone()
    code=0
    if a.offline:
        result='unknown';code=75
    elif a.action=='lookup':
        result='present' if row else 'absent'
    else:
        digest=hashlib.sha256(a.payload.encode()).hexdigest()
        if row and row[0]!=digest:
            result='candidate_conflict';code=65
        elif row:
            result='already_present'
        else:
            db.execute('INSERT INTO receipts VALUES(?,?,?)',(a.id,digest,time.time()));result='created'
        if a.drop_ack and code==0:
            result='acknowledgment_lost';code=75
    db.execute('INSERT INTO calls(action,identity,result) VALUES(?,?,?)',(a.action,a.id,result));db.commit();db.close()
    print(json.dumps({'fixture':'LOCAL_DESTINATION_ONLY','id':a.id,'outcome':result,'lookup_is_available':not a.offline,'note':'Does not establish any real provider behavior or idempotence guarantee.'}))
    return code

if __name__=='__main__':raise SystemExit(main())
