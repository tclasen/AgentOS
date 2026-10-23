---
type: AgentOS Procedure
title: Read-only repository and runtime discovery
description: Observe the current project and agent harness without installation writes.
tags:
- agentos
- phase
- discovery
status: stable
---

# Procedure

1. Discover repository root, Git state, existing instructions (`AGENTS.md` or runtime-specific equivalents), active work and evident domain. Inspect targeted content only; preserve unrelated changes and avoid executing untrusted scripts.
2. Identify existing AgentOS or another operating organization. Record preservation and migration concerns; do not assume replacement.
3. Identify available agent runtime(s), their known instruction discovery, role identity, spawning, messaging, parallelism, session persistence, permission enforcement, telemetry and tooling. Distinguish **declared** functionality from locally verified functionality.
4. Identify relevant repository permissions, branch protection, cross-repository boundaries, sensitive data and integration points. Do not inspect secrets unnecessarily.
5. Report a concise picture of observed facts, limitations and open decisions. Then conduct the [bootstrap interview](../interviews/bootstrap.md).

# Transition

Load the [component index](../components/index.md) only after you know enough about the mission/runtime to choose probable branches. Do not inspect every component yet.
