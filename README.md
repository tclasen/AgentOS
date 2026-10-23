# AgentOS

AgentOS is an adaptive installer specification for agent organizations. It helps an AI agent inspect a target repository, interview its owner, and design a small organization with a Director, a Chief of Staff, and the capabilities the project needs.

The installer knowledge graph lives in [bundle/](bundle/index.md) and uses Google's [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md). Its Markdown documents are the source of truth. The `agentos:` frontmatter extension describes AgentOS component selection and dependencies; consuming agents implement those rules.

## Install into a project

1. Choose and review a commit from [tclasen/AgentOS](https://github.com/tclasen/AgentOS). Pin its full SHA so the installation uses a reproducible source.
2. Open your target Git repository in your AI agent.
3. Copy [BOOTSTRAP_PROMPT.md](BOOTSTRAP_PROMPT.md), replace `<PINNED_COMMIT_SHA>`, and give it to the agent.

The agent starts at [INSTALL.md](INSTALL.md), inspects the target read-only, and asks a short adaptive interview. It proposes the installation footprint for approval before writing selected, tailored operational artifacts. The default organization home is `.agentos/`, with a minimal root `AGENTS.md` entrypoint.

For a local source, clone [tclasen/AgentOS](https://github.com/tclasen/AgentOS), check out the reviewed full commit SHA, and provide the absolute checkout path and revision in your prompt.

The repository contains Markdown reference documents; the consuming agent performs the installation.

## Repository map

| Path | Purpose |
| --- | --- |
| [INSTALL.md](INSTALL.md) | Instructions for the temporary installation agent |
| [BOOTSTRAP_PROMPT.md](BOOTSTRAP_PROMPT.md) | Prompt to use from a target repository |
| [bundle/](bundle/index.md) | OKF knowledge graph: core guarantees, phases, interviews, components, and examples |

`bundle/` is the OKF distribution boundary. Paths such as `/components/authority.md` in component metadata are identifiers relative to that boundary; clickable Markdown links use paths relative to their documents so they work on GitHub and in a local checkout.

## Operating guarantees and limits

Every installation retains two permanent roles, Director and Chief of Staff, and the [seven constitutional guarantees](bundle/core/constitution.md). Other capabilities adapt to the project and runtime. Installation preserves existing content and stays inside the approved footprint.

The source graph is an installer specification. Runtime integration, concurrency, scheduling, permissions, and improvement behavior must be implemented and qualified in the target environment. The specification alone does not establish those capabilities.

## References

- [OKF specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
- [agent-org](https://github.com/tclasen/agent-org), inspiration for progressive context, bounded delegation, recovery, and evidence-based acceptance
