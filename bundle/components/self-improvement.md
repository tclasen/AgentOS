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

CoS follows this complete loop during available runtime sessions; no background process is required:

1. Identify an observed issue from tasks, user feedback, tests or measured overhead; distinguish evidence from conjecture.
2. **Before changing the candidate**, record hypothesis, scope, expected benefit, evidence/acceptance standard, guardrails and a scoped rollback plan with the prior content or a usable recovery pointer.
3. Check authority and implement only the authorized modification, preserving unrelated work and active assignments.
4. Execute the evaluation against the prior criteria. The candidate **must not weaken its evaluator, acceptance criteria or evidence standard to pass**; proposed evaluator changes are assessed under the previous approved rules.
5. Decide retain, revise or scoped rollback from the observed result. Insufficient evidence stays inconclusive, and a narrow deterministic correction is not broad organizational benefit.
6. Retain the source evidence, hypothesis, candidate/check, result and rollback/disposition for **accepted, rejected and inconclusive** outcomes. Report the result through Director.

These steps can share a short section in an existing file. They do not require a separate queue, experiment framework or independent-evaluation infrastructure unless those components are selected.

# Follow-up interview

Ask only when consequential: Should CoS improve after tasks, on meaningful incidents, by schedule, or another event? How much autonomy and review? What costs or evidence standard justify a change? Do not hardcode any experimental sample size or statistical threshold.

# Implementation

A lightweight installation can use a task-completion or session-start improvement trigger and short lessons file. Higher assurance can select [independent evaluation](independent-evaluation.md), [learning queue](learning-queue.md) and [telemetry](telemetry.md). CoS can modify itself and Director, but not discard constitutional obligations.

# Verification

Demonstrate a plausible trigger and an authorized small improvement path, and distinguish a narrow deterministic correction from measured organization-wide benefit.

## Graph relationships

- Requires [Authority](authority.md)
- Requires [Delivery Acceptance](delivery-acceptance.md)
- Consider [Independent Evaluation](independent-evaluation.md) when applicable.
- Consider [Learning Queue](learning-queue.md) when applicable.
- Consider [Telemetry](telemetry.md) when applicable.
