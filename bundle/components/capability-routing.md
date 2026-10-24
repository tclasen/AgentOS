---
type: AgentOS Component
title: Capability-based work routing
description: Route tasks to available capabilities without a fixed catalog of specialist roles.
tags:
- agentos
- component
- capability-selection
- role-routing
status: stable
agentos:
  selection: required
  when_any: []
  requires: []
  provides:
  - capability-selection
  - role-routing
---

# Operational contract

Before work or delegation, the Director identifies needed capabilities and checks **all** of:

- Known role/tool abilities and actual availability.
- Permission for the particular paths, actions and effects.
- Available budget/resource limits, including cumulative usage already incurred. Unknown cost or limits remain unknown, never invented.

Multiple instances may represent one role. For a missing capability, consider reuse, learning/training, an authorized tool integration or a justified new role before explicit escalation. Do not proliferate roles as a substitute for missing tools. These checks are mandatory even when the optional resource-budget component is not selected; a dedicated budget system is unnecessary.

# Follow-up interview

Only if unclear: What kinds of work dominate initially? Which expertise must be separate? Which tools or external services are already approved? Recommend starting with the fewest useful roles.

# Implementation

Maintain a discoverable capability registry or native equivalent that the Chief of Staff can evolve. Distinguish capability descriptions from tested availability. See [roles, capabilities and instances](../concepts/role-capability-instance.md).

# Verification

Probe a representative task requiring an available capability and a task lacking one; show sensible routing or truthful capability-gap escalation.

## Graph relationships

None beyond the universal installer and constitutional rules.
