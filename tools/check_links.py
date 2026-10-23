#!/usr/bin/env python3
"""Check repository Markdown destinations; optionally request external URLs."""
import argparse
from pathlib import Path
import re
import subprocess
import unicodedata
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN = MarkdownIt('commonmark')


def tokens(path):
    text = path.read_text(encoding='utf-8')
    # OKF metadata is not Markdown, and may contain YAML lists and paths.
    text = re.sub(r'\A---\n.*?\n---\n', '', text, count=1, flags=re.S)
    return MARKDOWN.parse(text)


def descendants(items):
    for item in items:
        yield item
        yield from descendants(item.children or [])


def anchors(path):
    result = set()
    counts = {}
    items = tokens(path)
    for index, item in enumerate(items):
        if item.type != 'heading_open':
            continue
        children = items[index + 1].children or []
        text = ''.join(t.content for t in children if t.type in ('text', 'code_inline', 'image'))
        slug = ''.join(c for c in text.lower() if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        duplicate = counts.get(slug, 0)
        counts[slug] = duplicate + 1
        result.add(f'{slug}-{duplicate}' if duplicate else slug)
    return result


def check(root, files):
    """Return local-link errors and deduplicated external HTTP(S) URLs."""
    root = Path(root).resolve()
    errors, external = [], set()
    heading_cache = {}
    for file in files:
        file = Path(file).resolve()
        label = file.relative_to(root).as_posix()
        for token in descendants(tokens(file)):
            target = token.attrGet('href') if token.type == 'link_open' else token.attrGet('src') if token.type == 'image' else None
            if target is None:
                continue
            url = urlsplit(target)
            if url.scheme in ('http', 'https') or url.netloc:
                external.add(urlunsplit((url.scheme or 'https', url.netloc, url.path, url.query, '')))
                continue
            if url.scheme:
                continue
            path = unquote(url.path)
            dest = (root / path.lstrip('/') if path.startswith('/') else file.parent / path).resolve() if path else file
            error = None
            if not dest.is_relative_to(root):
                error = 'destination escapes repository'
            elif not dest.exists():
                error = 'destination does not exist'
            elif url.fragment and dest.is_file() and dest.suffix.lower() == '.md':
                if dest not in heading_cache:
                    heading_cache[dest] = anchors(dest)
                if unquote(url.fragment) not in heading_cache[dest]:
                    error = 'heading does not exist'
            if error:
                errors.append(f'{label}: {target}: {error}')
    return errors, external


def check_external(urls):
    errors = []
    for url in sorted(urls):
        request = Request(url, headers={'User-Agent': 'AgentOS-link-checker/1.0'})
        try:
            with urlopen(request, timeout=20) as response:
                if response.status >= 400:
                    errors.append(f'{url}: HTTP {response.status}')
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f'{url}: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--external', action='store_true', help='also request external HTTP(S) URLs')
    args = parser.parse_args()
    listed = subprocess.check_output(['git', '-C', str(ROOT), 'ls-files', '--cached', '--others', '--exclude-standard', '-z'])
    files = sorted({ROOT / p.decode() for p in listed.split(b'\0') if p and p.decode().endswith('.md') and (ROOT / p.decode()).is_file()})
    errors, external = check(ROOT, files)
    if args.external:
        errors.extend(check_external(external))
    print(f'Checked {len(files)} Markdown files; {len(external)} external URLs ' + ('requested' if args.external else 'excluded (use --external)'))
    for error in errors:
        print('ERROR:', error)
    if not errors:
        print('PASS: Markdown links')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
