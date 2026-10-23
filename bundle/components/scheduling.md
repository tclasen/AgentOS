---
type: AgentOS Component
title: Autonomous recurring and event-driven triggers
description: Support approved periodic, session-start or event-driven organizational actions using real available mechanisms.
tags:
- agentos
- component
- scheduled-triggers
- event-driven-autonomy
status: stable
agentos:
  selection: conditional
  when_any:
  - recurring_triggers
  - always_on_automation
  requires:
  - /components/authority.md
  - /components/self-improvement.md
  provides:
  - scheduled-triggers
  - event-driven-autonomy
---

# Trigger

The user wants automatic periodic reviews, event-driven work, uninterrupted service or proactive AgentOS behavior.

# Follow-up interview

Is actual off-session execution required? What scheduler/hook runtime exists? Which events, budgets and external side effects are permitted? Would on-session or task-completion triggers satisfy the need?

# Implementation

Prefer native runtime hooks/events or an existing scheduler. Avoid daemon/service installation unless authorized and justified. Trigger identity, idempotence, failures, limits and ownership must be clear. A Markdown declaration of a schedule does **not** make an active job.

# Verification

Where real scheduling is selected, inspect its registration and exercise an authorized trigger. Otherwise qualify the event/session-based fallback and disclose the absence of background execution.

## Graph relationships

- Requires [Authority](authority.md)
- Requires [Self Improvement](self-improvement.md)
