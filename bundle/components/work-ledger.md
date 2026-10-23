---
type: AgentOS Component
title: Durable work lifecycle and claim ledger
description: Track task ownership, dependencies, attempts and nonterminal work when transient conversational memory is insufficient.
tags:
- agentos
- component
- durable-task-state
- ownership-tracking
status: stable
agentos:
  selection: conditional
  when_any:
  - long_running_work
  - parallel_workers
  - complex_dependencies
  requires:
  - /components/delegation.md
  - /components/delivery-acceptance.md
  provides:
  - durable-task-state
  - ownership-tracking
---

# Trigger

Long-running work, parallel workers, nested dependencies or serious interruption risks require durable ownership and state.

# Follow-up interview

What existing task tracker or runtime state is authoritative? How many simultaneous tasks and owners are expected? Should project tasks remain in their own system? Are read-only status views sufficient?

# Implementation

Use native task services, existing issues, a compact structured state file or Markdown when suitable. Distinguish task, run and actual worker identity, single accountable owner, blocking dependencies, status transitions and active conflicting resource claims. Do not pretend shared Markdown is a distributed lock. Preserve failed attempts and record current vs historical state.

# Verification

Test dependencies, conflicting claims, cancellation and stale task status; check current destination state before retrying external operations. Separate a reported done worker from task acceptance.

## Graph relationships

- Requires [Delegation](delegation.md)
- Requires [Delivery Acceptance](delivery-acceptance.md)
- Consider [Durable Handoff](durable-handoff.md) when applicable.
