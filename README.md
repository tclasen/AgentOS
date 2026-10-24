# AgentOS

AgentOS helps an AI agent set up a small organization tailored to your project, led by a permanent Director and Chief of Staff. It is a Markdown installer and reference bundle; your agent inspects the project, proposes a setup, then creates the approved instructions.

**Preview:** installation needs your review and approval. Historical Codex trials include successful installations and real application work after corrections, alongside retained failures. Current local helper checks do not establish reliable first-pass onboarding across models or environments. See the [release status and evidence](docs/releases/2026-10-24-preview.md) before adopting it.

Open your target project in an AI agent that can read repository files and propose edits, then paste:

> Install AgentOS into this project using the latest version on the main branch of https://github.com/tclasen/AgentOS. Read `bundle/start.md` and follow its instructions. Inspect the project, ask any necessary questions, and get my approval for the proposed setup before changing files.

The agent must read the actual source files. If it cannot retrieve them, clone this repository separately and give it that source location. Run installation from your target project, keeping the installer source separate. Pin the resolved source revision or exact byte manifest in the proposal so approval and implementation use the same source.

Review the proposed components, file paths, permissions and checks before approving. The default footprint is a minimal root `AGENTS.md` and a compact `.agentos/` directory; existing instructions and user changes must be preserved. Missing required contracts or failed checks mean the installation remains incomplete. After qualification and handoff, new unassigned sessions enter through the Director; delegated sessions keep their assigned role.

Start with the [installer guide](bundle/start.md) and browse the [knowledge graph](bundle/index.md) as needed. The [optional Python helpers](tools/README.md) check source identity and component dependencies and record bounded trials. They do not install AgentOS or certify generated organizations.

For local verification from a source checkout (Python 3.9+; the full test suite uses POSIX process controls):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/qualification.py graph bundle
python3 tools/qualification.py identity bundle --verify docs/releases/2026-10-24-source.json
```

Keep your own project backup or Git checkpoint before installation. AgentOS supplies instructions, not an isolation or permission enforcement system. Background execution, external integrations and publication require the relevant real runtime support and explicit authority.
