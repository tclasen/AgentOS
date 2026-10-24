---
type: AgentOS Component
title: Cumulative resource and complexity budgeting
description: Bound nested delegation, retries, context, monetary costs and evaluation overhead.
tags:
- agentos
- component
- budgeting
- resource-optimization
status: stable
agentos:
  selection: conditional
  when_any:
  - time_limits
  - retry_limits
  - agent_slot_limits
  - cost_constraints
  - parallel_workers
  - expensive_tools
  requires:
  - /components/delegation.md
  provides:
  - budgeting
  - resource-optimization
---

# Trigger

Explicit time or retry limits, limited agent slots, meaningful cost constraints, expensive tool use, deep delegation, quotas, or active optimization campaigns. These limits can apply to one sequential session; a dollar cap or parallel workers are not prerequisites. Reconcile the stated constraints with this contract before deferring it.

# Follow-up interview

What limits matter (time, tokens, concurrency, dollars, retries, storage or attention)? Which are measurable versus advisory? When should the Director ask to replan or stop?

# Implementation

Preserve each of these duties in the installed instructions:

- Track observable costs at task and child-run levels; retries and nested delegation do not reset totals.
- Use task-appropriate model and reasoning choices rather than fixed job-title assignments.
- Unknown usage stays unknown; don't substitute an imaginary dollar counter.
- Limit runaway coordination without reducing correctness/safety goals.

# Verification

Test at least a nested or retried work scenario demonstrating cumulative accounting, bounded status and escalation where supported.

## Graph relationships

- Requires [Delegation](delegation.md)
