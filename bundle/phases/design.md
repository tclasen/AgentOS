---
type: AgentOS Procedure
title: Synthesize and approve selected component graph
description: Translate the interview and dependency closure into an implementable architecture.
tags:
- agentos
- phase
- design
status: stable
---

# Procedure

1. Revisit [graph routing](../core/graph-routing.md). Stabilize the selection, including required nodes, conditional nodes, transitive prerequisites, and conflict/limitation analysis. Reconcile its selection/read checklist with all required catalog entries and selected hard dependencies. Resolve missing reads before presenting the proposal; do not infer coverage from role names or a batch command's intent.
2. Synthesize operational contracts; multiple selected components may share a single target file or runtime-native mechanism. **Component count does not dictate target file count.**
3. For each capability, distinguish desired, available, implementation mechanism, whether enforceable vs procedural, validation approach and expected overhead.
4. Define minimal root `AGENTS.md` role-aware startup, compact AgentOS home (normally `.agentos/`), approval boundaries, migration preservation, organization/project data ownership and runtime-native extra paths requiring authorization.
5. Present a concise proposal: mission, selected/deferred components with rationales, initial roles, runtime integration, governance, memory/recovery/quality, repository paths, known unsupported behavior, tests and handoff strategy.
6. Obtain explicit user approval for actual target mutations and consequential external effects. Do not interpret a prior interview answer as permission for destructive Git operations, new providers or publication.

# Transition

Proceed to [implementation](implement.md) only after approval, resolving blockers or narrowing scope honestly.
