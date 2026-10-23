# AgentOS v3 — OKF-based adaptive installer

**Status:** repository-ready v3 starter bundle. This source package is an installer knowledge graph, **not an installed AgentOS**.

The bundle conforms to Google's [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md): Markdown concept documents with YAML frontmatter, standard Markdown cross-links, and small progressive-disclosure indexes. A deliberately small `agentos:` frontmatter extension adds component-selection metadata; this extension is **AgentOS-specific, not an OKF standard**.

## Start

- In an AI agent at a target Git repository, provide the content of [BOOTSTRAP_PROMPT.md](BOOTSTRAP_PROMPT.md), substituting a **trusted, pinned** URL to this installer repository (or a local unpacked path).
- The agent reads [INSTALL.md](INSTALL.md), then [bundle/index.md](bundle/index.md), [bundle/start.md](bundle/start.md), and the small required core. It inspects the target repository read-only and runs an adaptive interview.
- Component answers activate additional linked components and their local follow-up questions. Dependencies are resolved before a proposed install plan. Only **selected, tailored operational artifacts** go into the target repository.
- A source OKF concept is a specification, not necessarily a file to copy into the installed organization. The installed system should prefer native structured runtime configuration where useful.

## Design boundaries

- Exactly two mandatory *permanent roles*: Director and Chief of Staff.
- Seven constitutional guarantees are immutable under ordinary organizational evolution.
- A repository-root `AGENTS.md` remains the portable entrypoint; the default organizational home is `.agentos/`, but runtime-specific needs and the user can override the home.
- Do not edit the target repository outside the approved installation footprint, and do not execute scripts fetched from a remote installer automatically.
- Do not claim OKF itself enforces dependencies, permissions, agent concurrency, background execution, or autonomous improvement. The consuming agent/runtime implements those requirements.

## Validate and explore

```sh
python3 -m pip install PyYAML
python3 tools/validate_bundle.py
python3 tools/route_demo.py --signal long_running_work --signal external_effects
python3 tools/route_demo.py --signal native_agents --signal parallel_workers
```

The Python tools are **optional contributor utilities**; installing AgentOS requires only readable Markdown and normal agent capabilities. `validate_bundle.py` checks a stricter AgentOS authoring profile *in addition to* baseline OKF compliance; e.g., it intentionally rejects broken required-component dependencies even though OKF itself tolerates broken links.

## Sources

- [Google's current OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
- [agent-org](https://github.com/tclasen/agent-org), inspiration for progressive context, bounded delegation, evidence-based improvement, recovery, and acceptance; **not** a dependency.

This bundle is a starting architectural implementation ready for repository review. Its runtime-specific behavior has not been qualified against all supported agent harnesses.

## Publish as a Git repository

Unzip this folder, run `git init`, commit it and push to a repository you control. Pin a tag or full commit SHA in the bootstrap prompt. Alternatively, provide the unpacked directory as a trusted local source to the installation agent. The installer should not treat an unpinned moving branch as a reproducible release.
