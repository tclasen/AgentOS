---
type: AgentOS Component
title: Protected independent evaluation and improvement gates
description: Prevent organizational improvements from promoting themselves by weakening their own evaluator.
tags:
- agentos
- component
- evaluation-independence
- quality-gates
status: stable
agentos:
  selection: conditional
  when_any:
  - high_assurance
  - repeatable_improvement
  - strict_review
  requires:
  - /components/self-improvement.md
  - /components/delivery-acceptance.md
  provides:
  - evaluation-independence
  - quality-gates
---

# Trigger

High-assurance tasks, consequential self-improvement, repeatable experiments or independent review requirements.

# Follow-up interview

Which outputs need independent review? Which benchmarks and representative workloads exist? How should evaluator changes be approved? Is technical separation possible or only fresh independent contexts?

# Implementation

Establish preregistered hypotheses/criteria for material comparisons, pinned baseline/candidate and known-good recovery. Reviewer examines accepted criteria and actual outputs, not merely builder self-reports. Candidate modifications to grading criteria must be tested under prior approved rules where possible. Record all attempts, failures, inconclusive results, and actual resource costs. Choose statistics suited to the claim; no universal numeric threshold.

# Verification

Show a defective candidate cannot pass merely by changing evaluator rules. Verify independence claims honestly when resources are shared; a fresh role label alone is not trusted isolation.

## Graph relationships

- Requires [Self Improvement](self-improvement.md)
- Requires [Delivery Acceptance](delivery-acceptance.md)
