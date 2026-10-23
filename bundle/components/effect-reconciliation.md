---
type: AgentOS Component
title: External side-effect reconciliation
description: Prevent blind retries of ambiguous consequential operations and bind actions to actual destination state.
tags:
- agentos
- component
- effect-reconciliation
- safe-retry
status: stable
agentos:
  selection: conditional
  when_any:
  - external_effects
  - remote_git_delivery
  - business_automation
  requires:
  - /components/authority.md
  provides:
  - effect-reconciliation
  - safe-retry
---

# Trigger

External messaging, APIs, pull requests, publication, deployment, transactions or any action where a lost response can hide a completed side effect.

# Follow-up interview

Which external destinations are used? Do they support idempotency keys or reliable lookup? What operations require a preflight record or explicit approval? How severe is duplication?

# Implementation

Select the smallest sufficient intent–attempt–observation pattern. Track target, candidate, authority, stable correlation identity, attempt and observed receipt where relevant. Do not issue a duplicate after a lost acknowledgment until destination state is reconciled. A local journal does not authenticate remote success and does not make the provider idempotent. Preserve unknown outcomes.

# Verification

Inject an interrupted response after a simulated/authorized effect and show no duplicate action; independently check actual destinations where scope permits. Distinguish simulated tests from live external verification.

## Graph relationships

- Requires [Authority](../components/authority.md)
- Consider [Durable Handoff](../components/durable-handoff.md) when applicable.
