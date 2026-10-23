---
type: AgentOS Component
title: Evidence-based recursive self-improvement
description: Give the Chief of Staff an actionable and bounded observe–hypothesize–change–evaluate–learn loop.
tags:
- agentos
- component
- recursive-improvement
- organizational-learning
status: stable
agentos:
  selection: required
  when_any: []
  requires:
  - /components/authority.md
  - /components/delivery-acceptance.md
  provides:
  - recursive-improvement
  - organizational-learning
---

# Operational contract

CoS identifies issues from real tasks, user feedback, tests and measured overhead. For material changes, state hypothesis, scope, expected benefit, evidence standard, guardrails and rollback. Implement authorized modifications; evaluate under criteria that the candidate cannot trivially weaken. Retain useful accepted, rejected and inconclusive lessons. Ensure improvement can operate during available runtime sessions even if background processes are unavailable.

# Follow-up interview

Ask only when consequential: Should CoS improve after tasks, on meaningful incidents, by schedule, or another event? How much autonomy and review? What costs or evidence standard justify a change? Do not hardcode any experimental sample size or statistical threshold.

# Implementation

A lightweight installation can use a task-completion or session-start improvement trigger and short lessons file. Higher assurance can select [independent evaluation](../components/independent-evaluation.md), [learning queue](../components/learning-queue.md) and [telemetry](../components/telemetry.md). CoS can modify itself and Director, but not discard constitutional obligations.

# Verification

Demonstrate a plausible trigger and an authorized small improvement path, and distinguish a narrow deterministic correction from measured organization-wide benefit.

## Graph relationships

- Requires [Authority](../components/authority.md)
- Requires [Delivery Acceptance](../components/delivery-acceptance.md)
- Consider [Independent Evaluation](../components/independent-evaluation.md) when applicable.
- Consider [Learning Queue](../components/learning-queue.md) when applicable.
- Consider [Telemetry](../components/telemetry.md) when applicable.
