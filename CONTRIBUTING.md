# Contributing to AgentOS

Clone [tclasen/AgentOS](https://github.com/tclasen/AgentOS) and create a branch for your change. Keep installer content in [bundle/](bundle/index.md), contributor utilities in [tools/](tools/), and regression tests in [tests/](tests/).

## Set up and validate

Use Python 3.11 or later:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python tools/validate_bundle.py
python tools/check_links.py
python -m unittest discover -s tests -v
```

`validate_bundle.py` checks OKF structure and AgentOS component dependencies. `check_links.py` checks Markdown links throughout the tracked repository, including file paths and heading fragments. It understands inline links, reference links, images, and autolinks, and ignores code examples. Checks run from any working directory.

To also check external HTTP(S) destinations, run:

```sh
python tools/check_links.py --external
```

External checks require network access and may fail because of authentication, rate limits, or an unavailable host. Review those failures explicitly. CI checks local links without depending on external services.

## Authoring conventions

- Keep the OKF `bundle/` boundary and its concept identifiers stable. Concept documents have YAML frontmatter; directory indexes remain small navigation aids.
- Use document-relative Markdown links, including links to neighboring components. Metadata `agentos.requires` paths remain relative to the bundle root and begin with `/`.
- Link prerequisites in the document body as well as declaring them in metadata. Resolve dependencies without cycles.
- Preserve progressive disclosure: a link is a navigation option, not an instruction to read the whole graph.
- Use the canonical repository URL, `https://github.com/tclasen/AgentOS`, in onboarding. Pin full reviewed commit SHAs for installations; do not present a moving branch as a release.
- Keep contributor tooling optional for installer consumers. Add regression coverage when changing validation or routing behavior.

Submit a pull request describing the problem, resulting behavior, and checks performed. Repository cleanup must preserve the constitutional guarantees and installer authorization boundaries.
