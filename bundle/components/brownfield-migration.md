---
type: AgentOS Component
title: Brownfield integration and existing AgentOS migration
description: Preserve and adapt existing roles, instructions and work rather than overwriting installations.
tags:
- agentos
- component
- migration
- brownfield-safety
status: stable
agentos:
  selection: conditional
  when_any:
  - existing_agent_system
  - brownfield_conflicts
  requires:
  - /components/activation.md
  - /components/authority.md
  - /components/context-core.md
  provides:
  - migration
  - brownfield-safety
---

# Trigger

The target already contains an agent operating system, runtime-specific instructions or a mature incompatible layout.

# Follow-up interview

Should we improve, migrate, repair, merge or replace? What existing authority/unfinished tasks must survive? Which runtime conventions must remain? Confirm any destructive replacement explicitly.

# Implementation

Inventory existing configuration and current Git work. Identify duplicate entrypoints, conflicting scope rules, role mappings and versions. Prefer a narrow integration plan. Never silently import another project's grants, history or telemetry as current authority. Plan rollback and handoff for nonterminal work. Do not write outside the approved footprint.

# Verification

Diff old/new startup behavior and content, preserve unrelated instructions, ensure old references and active roles are reconciled. Validate Director activation in the selected runtime.

## Graph relationships

- Requires [Activation](activation.md)
- Requires [Authority](authority.md)
- Requires [Context Core](context-core.md)
