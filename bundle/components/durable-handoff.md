---
type: AgentOS Component
title: Cross-session checkpoint and handoff
description: Persist enough task-specific state for a new agent context to resume safely without predecessor conversation.
tags:
- agentos
- component
- session-recovery
- durable-handoffs
status: stable
agentos:
  selection: conditional
  when_any:
  - long_running_work
  - cross_session_continuity
  - interrupted_work
  - external_effects
  requires:
  - /components/work-ledger.md
  - /components/context-core.md
  provides:
  - session-recovery
  - durable-handoffs
---

# Trigger

Long tasks, interruption, session restarts, human pauses or operation recovery requirements.

# Follow-up interview

What can be resumed by the runtime? What operational state already persists? What sensitive data must never be recorded? How long should handoff data be retained?

# Implementation

Checkpoints identify current task/run/role, expected outcome, completed actions, artifacts/evidence, changed resources, unresolved effects, owner and exact next safe action. Link canonical state rather than copy transcripts. Read actual tool/destination state before using stale checkpoint claims.

# Verification

A genuinely fresh worker receives only the approved context/manifest and must recover or explicitly refuse unsafe continuation. A filled Markdown template by itself does not establish recovery.

## Graph relationships

- Requires [Work Ledger](../components/work-ledger.md)
- Requires [Context Core](../components/context-core.md)
