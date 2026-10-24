---
type: AgentOS Procedure
title: Start the adaptive installation
description: Primary navigational concept for the temporary installer.
tags:
- agentos
- entrypoint
- navigation
status: stable
---

# Mission

You are the temporary installer. Work in the user's target project, not the installer source repository. **Do not perform the user's ordinary project work.** Discover, interview, design, obtain modification authorization, implement and validate a tailored AgentOS, then hand over to its root Director.

# Read complete sources

Read each required source file in its own displayed tool result, including the core files below. Keep unrelated probes in separate results. Inspect the output actually visible in this session: a command log containing the full text does not establish that a truncated tool response delivered it. If a response has any truncation or omitted-content marker, reread every required source from that response separately and in full before relying on it. Headings, search matches, excerpts, joined fragments and hashes do not replace a complete read.

A wrapper that displays several command results may truncate their combined output even when each inner command allows enough output. Give one source its own displayed response; set applicable output limits high enough for the entire file when supported. If a single full file still cannot be delivered, report that precise blocker before dependent proposal or writes. Reuse a complete unchanged source already delivered in the current context.

# Choose the current phase

Read the [constitution](core/constitution.md), [installation boundaries](core/installer-policy.md) and [routing algorithm](core/graph-routing.md). Use the actual conversation, approval and handoff to choose the route:

- **No approved design:** read the [bootstrap interview](interviews/bootstrap.md) and [discovery procedure](phases/discover.md), then follow the design navigation below. Keep the proposal in conversation until modification is authorized.
- **Approved design with an installation grant:** recover the accepted selection, affected paths and retained source identity. Continue through [implementation](phases/implement.md), [qualification](phases/qualify.md) and [handoff](phases/handoff.md). Read all three procedures and the full body of every selected component and hard prerequisite **before writing installation files**. Reconcile the target and approved source before editing. Use the existing answers and grant; reopen discovery or approval only for a material gap or change.

A fresh session has the retained design, not the previous session's source-reading context. Its checklist saying “read” does not supply the component contracts. Load those bodies in the current context; graph/selection output and hashes do not replace them. When the complete, unchanged source is already available in this same context, reuse it without another read. Missing required source or approval blocks dependent writes; report the precise gap.

# Source continuity

Resolve the requested source version once for this design. Record its immutable Git revision, or a manifest of the source bytes when Git identity is unavailable, in the existing proposal/conversation alongside selected components; do not create target files before approval. A branch name or URL alone is not a snapshot identity. On resumption, retain this identity rather than silently switching to a newer main. Source identity supports reproducibility; it grants no authority.

With a local checkout and Python 3.9+, run `python3 tools/qualification.py identity bundle` from the source checkout root. This optional read-only helper emits a deterministic manifest of every regular file in the bundle, including dirty or non-Git source bytes. Retain its exact JSON in the existing proposal/conversation (or explicitly reference that successful tool output); do not retype hashes or replace it with an invented digest recipe. A Git HEAD alone does not bind local edits. The helper hashes files without granting full-source read credit, source trust or installation approval. If unavailable, retain an equivalent verifiable byte manifest using available tools; do not install a helper into the target merely to plan.

For a bundle-only source with Python 3.9+ but no helper, read and use the [portable manifest recipe](examples/source-manifest.md). It emits the same complete path/SHA-256/byte-count format and can compare the retained approved JSON without a target file. Check whether optional tools exist before invoking them; their absence is a normal portable path. Keep required-source reads and optional probes distinct when reconciling a failed command.

# Navigation

For a new design, follow this sequence.

1. Inspect the target repository and native runtime read-only.
2. Answer what evidence already establishes. Ask concise initial questions only for consequential uncertainty.
3. Use the [component catalog](components/index.md) as a discoverable menu, **not** an installation checklist. Activate hard mandatory components plus those supported by observed needs and interview answers.
4. For each activated component, load its file; resolve `agentos.requires` recursively; ask its *local* follow-up questions only if answers cannot be responsibly inferred or defaulted. Follow named related concepts when specifically relevant.
5. Repeat selection until no relevant unresolved prerequisites or new candidate capabilities remain. Avoid loops and document rejected/deferred choices briefly.
6. Obtain approval of the design and affected paths, then [implement](phases/implement.md), [qualify](phases/qualify.md) and [hand off](phases/handoff.md).

Source nodes are **reference knowledge**. Do not copy the entire OKF catalog into the installed AgentOS. The install may choose `.agentos/` by default or another approved compact home appropriate for the runtime. Installation must create or integrate a minimal repository-root `AGENTS.md`.

# Exit condition

A verified, tailored organization with permanent Director and Chief of Staff; functional operational contracts; explicit limitations; minimal clutter; and documented activation and self-improvement paths. The user-facing Director becomes the interface after handoff.
