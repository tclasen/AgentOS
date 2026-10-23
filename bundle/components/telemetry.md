---
type: AgentOS Component
title: Organizational observability and scorecards
description: Measure accepted task outcomes, organization overhead and measurement coverage without inventing data.
tags:
- agentos
- component
- observability
- measurement-health
status: stable
agentos:
  selection: conditional
  when_any:
  - rich_telemetry
  - optimization_metrics
  requires:
  - /components/self-improvement.md
  provides:
  - observability
  - measurement-health
---

# Trigger

User requires operational visibility, cost/performance optimization or evidence-based comparisons supported by actual telemetry sources.

# Follow-up interview

Which runtime measurements are actually available and authorized? Are there existing dashboards or logs? Which task outcomes matter most? What data cannot be retained?

# Implementation

Separate organizational performance, work-product quality and **measurement health**. Include failures/retries and disclosed sample denominators. Record missing model, token or dollar usage as unknown. Distinguish elapsed duration from parallel effort; track review/rework overhead where measurable. Prefer existing native reports to new instrumentation services; state unobserved tool paths.

# Verification

Verify a sample scorecard preserves unknowns and failed attempts; synthetic data are labeled. A wrapper observing some commands must not claim universal interception.

## Graph relationships

- Requires [Self Improvement](self-improvement.md)
