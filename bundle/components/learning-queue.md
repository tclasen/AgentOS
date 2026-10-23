---
type: AgentOS Component
title: Curated organizational correction queue
description: Convert recurring incidents into bounded improvement hypotheses with durable lineage and counterexamples.
tags:
- agentos
- component
- learning-candidates
- incident-to-improvement
status: stable
agentos:
  selection: conditional
  when_any:
  - repeatable_improvement
  - recurring_failures
  - high_assurance
  requires:
  - /components/self-improvement.md
  provides:
  - learning-candidates
  - incident-to-improvement
---

# Trigger

Frequent repeated work, observed corrections, specialized quality requirements or desire to compound improvements across tasks.

# Follow-up interview

Which sources of corrections are available (reviews, tickets, runs, user feedback)? How often should CoS inspect them? What can be stored, shared or retained safely?

# Implementation

Track source incident, causal hypothesis, scope, proposed fix, contradictory example, evaluation exposure, result and recurrence. A lesson observed once stays a hypothesis until generalized. Keep rejected and inconclusive candidates appropriately; prevent repeated final-test exposure from masquerading as independent validation.

# Verification

Trace one genuine or fixture correction from evidence through a candidate and its disposition; do not treat an empty queue as proof that no improvements are needed.

## Graph relationships

- Requires [Self Improvement](self-improvement.md)
- Consider [Independent Evaluation](independent-evaluation.md) when applicable.
