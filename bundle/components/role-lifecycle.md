---
type: AgentOS Component
title: Dynamic role and capability lifecycle
description: Enable the Chief of Staff to create, revise, consolidate and retire nonpermanent roles coherently.
tags:
- agentos
- component
- role-evolution
- capability-lifecycle
status: stable
agentos:
  selection: required
  when_any: []
  requires:
  - /components/capability-routing.md
  provides:
  - role-evolution
  - capability-lifecycle
---

# Operational contract

Roles and capability identities remain discoverable and evolve without breaking active assignments. Preserve Director and CoS. Before changing or retiring another role, check each of:

- In-flight work and accountable owners.
- Instruction versions pinned to those assignments; preserve their old contracts until explicitly transferred.
- Historical role identity and retained decision lineage.
- Routing/discovery tables and dependent capabilities.

Transfer responsibility explicitly and update discovery before retirement. Never delete responsibility midtask. A short record in an existing file is sufficient; this contract does not require a separate ledger.

# Follow-up interview

Only if significant: Should routine role changes be autonomous? Is a review or audit required for modifying Director/CoS? Should a role registry be structured/native or Markdown? Recommend a lightweight registry by default.

# Implementation

CoS owns lifecycle updates; use native agent registries where appropriate. Distinguish roles from agent instances and tasks using the [identity concept](../concepts/role-capability-instance.md). Provide a reconfiguration path that does not depend on the temporary installer.

# Verification

Demonstrate a safe nonmandatory role amendment or a controlled simulated lifecycle event, including discovery update and handling of active work.

## Graph relationships

- Requires [Capability Routing](capability-routing.md)
