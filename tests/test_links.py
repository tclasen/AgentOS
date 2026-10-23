import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from check_links import check


class Links(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, text):
        file = self.root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding='utf-8')
        return file

    def test_relative_reference_image_and_encoded_fragment(self):
        self.write('docs/with space.md', '# Hello, world!\n# Hello, world!\n')
        self.write('image.svg', '<svg/>')
        file = self.write('README.md', '[inline](docs/with%20space.md#hello-world)\n[reference][doc]\n![image](image.svg)\n\n[doc]: docs/with%20space.md#hello-world-1\n')
        self.assertEqual(check(self.root, [file]), ([], set()))

    def test_missing_file_heading_and_escape_reported(self):
        self.write('doc.md', '# Existing\n')
        file = self.write('README.md', '[missing](missing.md)\n[heading](doc.md#absent)\n[escape](../outside.md)\n')
        errors, _ = check(self.root, [file])
        self.assertEqual(len(errors), 3)
        self.assertIn('heading does not exist', errors[1])
        self.assertIn('escapes repository', errors[2])

    def test_metadata_and_code_are_not_links(self):
        file = self.write('README.md', '---\ntype: Example\nsource: "[metadata](missing.md)"\n---\n`[code](missing.md)`\n\n```md\n[example](missing.md)\n```\n')
        self.assertEqual(check(self.root, [file]), ([], set()))

    def test_external_urls_are_deduplicated_and_fragments_removed(self):
        file = self.write('README.md', '[one](https://example.com/doc#one)\n<https://example.com/doc#two>\n[mail](mailto:hello@example.com)\n')
        self.assertEqual(check(self.root, [file]), ([], {'https://example.com/doc'}))


if __name__ == '__main__':
    unittest.main()
