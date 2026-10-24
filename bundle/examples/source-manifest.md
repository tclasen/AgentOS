---
type: AgentOS Example
title: Portable source manifest generation and comparison
description: Read-only source identity for bundle-only installations without the optional checkout helper.
tags:
- agentos
- example
- portability
status: stable
---

# When this applies

Use this when the supplied source contains only the bundle, the optional `tools/qualification.py` is absent, and Python 3.9+ is available. It uses only Python's standard library and writes nothing. Do not install it into the target, fetch another source, or create an unapproved manifest file. If Python is unavailable, use another equivalent read-only method and retain its actual complete result; do not claim this recipe ran.

Invoke the code below with `PYTHONDONTWRITEBYTECODE=1 python3 -B -c '<code>' /absolute/path/to/bundle`. Supply the code as a command argument, preserving its literal text. Replace only the bundle argument with the agreed source root. The default mode prints the full `agentos-source-v1` JSON, including every regular file's relative path, SHA-256 and **byte count**. Counts use bytes read, not Unicode character counts or a guessed file size. The format interoperates with the optional helper.

For later verification, append `--verify` and provide the **exact original approved JSON as stdin data**, for example through the execution tool's input or a quoted here-document. Keep code in the `-c` argument so stdin remains available for that JSON. This does not require a target file. Do not evaluate the JSON as code, retype hashes, fill omitted fields, or substitute the newly generated identity for the approved one. A nonzero result is a refusal or mismatch to reconcile before editing; only exit0 with `{"match": true}` establishes this comparison passed.

```python
from pathlib import Path
import hashlib
import json
import os
import stat
import sys

if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and sys.argv[2] != "--verify"):
    raise SystemExit("usage: code BUNDLE [--verify]; approved JSON on stdin for verification")
root = Path(sys.argv[1]).resolve()
if not root.is_dir() or not (root / "start.md").is_file():
    raise SystemExit("source bundle must be a directory containing start.md")

def fail(error):
    raise error

files = {}
for folder, directories, names in os.walk(root, followlinks=False, onerror=fail):
    for name in directories + names:
        path = Path(folder) / name
        mode = path.lstat().st_mode
        relative = path.relative_to(root).as_posix()
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise SystemExit("source identity requires regular files: " + relative)
        data = path.read_bytes()
        files[relative] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
manifest = {"format": "agentos-source-v1", "files": dict(sorted(files.items()))}

def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate manifest key: " + key)
        result[key] = value
    return result

def invalid_constant(value):
    raise ValueError("invalid JSON constant: " + value)

if len(sys.argv) == 3:
    approved = json.load(sys.stdin, object_pairs_hook=unique_keys, parse_constant=invalid_constant)
    # Canonical JSON preserves number types: true or 1.0 cannot stand in for 1.
    if json.dumps(approved, sort_keys=True) != json.dumps(manifest, sort_keys=True):
        raise SystemExit("source manifest mismatch; reconcile the approved identity before edits")
    print(json.dumps({"match": True}))
else:
    print(json.dumps(manifest, indent=2))
```

Retain the actual generation output with the proposal, or explicitly reference that complete tool output so it accompanies the approval and handoff. On resumption compare against those same approved bytes before writes. Relocation alone does not alter a bundle-relative manifest. Added, removed or changed files, a missing field or a different format must not silently pass comparison. Approved manifest paths are data for comparison and are never opened.

This checks local source identity only. It does not prove full-source reading, trust, permission, instruction quality or successful installation. Links and special files are refused rather than followed; reconcile the source with its owner instead of silently omitting them. The code does not lock the source against concurrent changes, so use the agreed frozen snapshot and reconcile any later change under the implementation procedure. A successful comparison never authorizes an otherwise unapproved target mutation.
