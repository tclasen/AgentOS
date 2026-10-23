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

The Director identifies capabilities needed for work, then matches the organization's known role/tool abilities, availability, permissions and budget. Multiple instances may represent one role. Missing capability prompts reuse, training, tool integration, a justified new role or explicit escalation—not arbitrary role proliferation.

# Follow-up interview

Only if unclear: What kinds of work dominate initially? Which expertise must be separate? Which tools or external services are already approved? Recommend starting with the fewest useful roles.

# Implementation

Maintain a discoverable capability registry or native equivalent that the Chief of Staff can evolve. Distinguish capability descriptions from tested availability. See [roles, capabilities and instances](../concepts/role-capability-instance.md).

# Verification

Probe a representative task requiring an available capability and a task lacking one; show sensible routing or truthful capability-gap escalation.

## Graph relationships

None beyond the universal installer and constitutional rules.
