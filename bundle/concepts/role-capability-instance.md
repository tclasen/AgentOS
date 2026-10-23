---
type: AgentOS Concept
title: Roles, capabilities, instances, tasks and runs
description: Five distinct identities that should not collapse during orchestration.
tags:
- agentos
- model
- identity
status: stable
---

# Model

- **Role:** persistent organizational responsibility with its own authority and expected outputs.
- **Capability:** ability available through knowledge, tools, or a runtime facility; roles may share a capability.
- **Agent instance:** actual working context assigned a role; several agents may fulfill one role concurrently.
- **Task:** continuing intended outcome, possibly requiring several attempts and agents.
- **Run:** a particular execution attempt with concrete identity, context, resources and observed effects.

The Director allocates work based on capability and authority, not solely role names. The CoS can change roles and capabilities without rewriting task history. Native agent IDs, filesystem claims and user-facing names are not interchangeable. An instruction file for a role is not proof that a separate running agent exists.

# Related

See [capability routing](../components/capability-routing.md), [role lifecycle](../components/role-lifecycle.md) and [work ledger](../components/work-ledger.md) when designing those mechanisms.
