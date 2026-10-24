"""Exercise the public identity CLI against actual filesystem changes and invalid inputs."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).parents[1] / 'tools/qualification.py'


class SourceIdentityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bundle = self.root / 'bundle'
        self.bundle.mkdir()
        (self.bundle / 'start.md').write_bytes(b'entry\r\n')
        (self.bundle / 'nested').mkdir()
        (self.bundle / 'nested/bytes.bin').write_bytes(bytes(range(256)))

    def cli(self, *args, stdin=None, bundle=None):
        return subprocess.run([sys.executable, str(SCRIPT), 'identity', str(bundle or self.bundle), *args],
                              input=stdin, text=True, capture_output=True)

    def generated(self):
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_exact_bytes_determinism_relocation_and_no_writes(self):
        before = {p.relative_to(self.bundle): p.read_bytes() for p in self.bundle.rglob('*') if p.is_file()}
        first = self.generated()
        self.assertEqual(first, self.generated())
        expected = {p.as_posix(): {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
                    for p, data in before.items()}
        self.assertEqual(json.loads(first), {'format': 'agentos-source-v1', 'files': expected})
        moved = self.root / 'relocated source'
        shutil.copytree(self.bundle, moved)
        self.assertEqual(first, self.cli(bundle=moved).stdout)
        result = self.cli('--verify', '-', stdin=first, bundle=moved)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['match'])
        self.assertEqual(before, {p.relative_to(self.bundle): p.read_bytes() for p in self.bundle.rglob('*') if p.is_file()})

    def test_added_removed_changed_and_tampered_entries_do_not_match(self):
        approved = self.generated()
        (self.bundle / 'new.md').write_text('new optional source')
        (self.bundle / 'nested/bytes.bin').unlink()
        (self.bundle / 'start.md').write_text('different instructions')
        result = self.cli('--verify', '-', stdin=approved)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout), {'match': False, 'delta': {
            'added': ['new.md'], 'removed': ['nested/bytes.bin'], 'changed': ['start.md']}})
        manifest = json.loads(self.generated())
        manifest['files']['start.md']['sha256'] = '0' * 64
        result = self.cli('--verify', '-', stdin=json.dumps(manifest))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['delta']['changed'], ['start.md'])

    def test_same_git_head_cannot_hide_dirty_bundle(self):
        def git(*args):
            return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.DEVNULL, text=True)
        git('init'); git('add', 'bundle')
        git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'initial')
        head = git('rev-parse', 'HEAD'); approved = self.generated()
        (self.bundle / 'start.md').write_text('locally modified')
        self.assertEqual(head, git('rev-parse', 'HEAD'))
        self.assertEqual(self.cli('--verify', '-', stdin=approved).returncode, 1)
        shutil.rmtree(self.root / '.git')
        self.assertEqual(self.cli('--verify', '-', stdin=approved).returncode, 1)
        current = self.generated()
        self.assertEqual(self.cli('--verify', '-', stdin=current).returncode, 0)

    def test_file_input_and_invalid_json_never_write_or_succeed(self):
        approved = self.root / 'approved.json'; approved.write_text(self.generated())
        self.assertEqual(self.cli('--verify', str(approved)).returncode, 0)
        forms = ['{', 'null', '[]', '{}', '{"format":"agentos-source-v1","files":{},"files":{}}',
                 approved.read_text().replace('"sha256":', '"bytes":0,"sha256":', 1)]
        for data in forms:
            with self.subTest(data=data):
                result = self.cli('--verify', '-', stdin=data)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual(result.stdout, '')
        self.assertEqual(self.cli('--verify', str(self.root / 'absent.json')).returncode, 2)
        self.assertEqual(set(p.name for p in self.root.iterdir()), {'bundle', 'approved.json'})

    def test_invalid_manifest_schema_and_paths_are_refused(self):
        original = json.loads(self.generated())
        mutations = [lambda m: m.update(format='other'), lambda m: m.update(extra=True),
                     lambda m: m.update(files=[]), lambda m: m['files'].pop('start.md'),
                     lambda m: m['files']['start.md'].update(bytes=True),
                     lambda m: m['files']['start.md'].update(bytes=-1),
                     lambda m: m['files']['start.md'].update(sha256='not a hash'),
                     lambda m: m['files']['start.md'].update(extra=True)]
        for path in ['/outside', '../outside', 'nested/../outside', './start.md', 'nested//other']:
            mutations.append(lambda m, path=path: m['files'].update({path: m['files']['start.md']}))
        for change in mutations:
            manifest = json.loads(json.dumps(original)); change(manifest)
            result = self.cli('--verify', '-', stdin=json.dumps(manifest))
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(result.stdout, '')

    def test_links_and_special_files_are_refused_without_following(self):
        outside = self.root / 'outside'; outside.write_text('outside source scope')
        for target in [outside, self.bundle / 'start.md', self.bundle / 'nested', self.root / 'missing']:
            link = self.bundle / 'link'; link.symlink_to(target)
            result = self.cli(); link.unlink()
            self.assertEqual(result.returncode, 2, result.stdout)
            self.assertEqual(result.stdout, '')
        fifo = self.bundle / 'fifo'; os.mkfifo(fifo)
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertEqual(outside.read_text(), 'outside source scope')

    def test_missing_bundle_or_entrypoint_refuses_empty_match(self):
        self.assertEqual(self.cli(bundle=self.root / 'missing').returncode, 2)
        (self.bundle / 'start.md').unlink()
        result = self.cli()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
