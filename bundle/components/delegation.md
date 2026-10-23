---
type: AgentOS Component
title: Delegation and subordinate coordination
description: Describe and exercise how the Director distributes work and receives reliable results.
tags:
- agentos
- component
- delegation
- coordination
status: stable
agentos:
  selection: required
  when_any: []
  requires:
  - /components/authority.md
  - /components/capability-routing.md
  provides:
  - delegation
  - coordination
---

# Operational contract

A substantive delegated assignment should establish intent, accountable owner, authorized scope, necessary context, expected deliverable, acceptance criteria and reporting expectations. The Director should not mistake issuing a delegate call for spawning a concurrent persistent worker. Nested delegation inherits limitations and should not silently reset budgets.

# Follow-up interview

If material: Does work require real parallelism or just specialization? Should the Director remain conversationally responsive while workers run? How should interruptions or dependencies be handled? Ground any recommendation in runtime capabilities.

# Implementation

Choose native task/agent mechanisms when suitable, otherwise lightweight sequential role execution with an honest disclosure of its limits. Adopt [work ledger](../components/work-ledger.md), [parallel coordination](../components/parallel-coordination.md), or [durable handoffs](../components/durable-handoff.md) only when indicated.

# Verification

Test one meaningful delegate-and-return path where supported. Confirm the worker did not silently exceed the delegated task or permissions.

## Graph relationships

- Requires [Authority](../components/authority.md)
- Requires [Capability Routing](../components/capability-routing.md)
- Consider [Work Ledger](../components/work-ledger.md) when applicable.
- Consider [Parallel Coordination](../components/parallel-coordination.md) when applicable.
- Consider [Durable Handoff](../components/durable-handoff.md) when applicable.
