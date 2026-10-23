---
type: AgentOS Interview
title: Minimum adaptive opening interview
description: Short initial user conversation that seeds graph traversal without a rigid form.
tags:
- agentos
- interview
- bootstrap
status: stable
---

# Before questioning

Run [read-only discovery](../phases/discover.md). Extract credible facts from the repository and runtime first. Do not ask what you can reliably determine. Explain relevant observations briefly.

# Opening conversation

Ask a **small, conversational** set of questions, ideally covering these independent uncertainties when they remain unresolved:

1. **Mission:** What should this organization accomplish in this repository, and what would a successful first outcome look like?
2. **Runtime:** Which agent runtime(s) should it serve? Prefer native integration or portability? Suggest detected runtime when credible.
3. **Decision authority:** What kinds of actions can it take without checking with you, and what actions require approval? Recommend safe scope defaults.
4. **Operating expectations:** Do you want long-running/parallel work, cross-session continuity, observability, or routine task-level use? Infer likely needs and offer a concise recommendation rather than an exhaustive menu.

You may combine, shorten, or reorder questions. Ask fewer when the user already supplied answers. Do not ask the user to define technical state machines, JSON schemas, metrics, or mechanisms unnecessarily.

# Seed discovery signals

Use factual shorthand signals (examples, not a closed schema): `native_agents`, `parallel_workers`, `long_running_work`, `external_effects`, `existing_agent_system`, `sensitive_data`, `multiple_repositories`, `high_assurance`, `cost_constraints`, `remote_git_delivery`, `recurring_triggers`, `repeatable_improvement`, `rich_telemetry`, `business_automation`, `runtime_specific_integration`.

Observe which are **requested**, **present**, **absent**, or **unknown**. Do not infer an unavailable capability just because the user wants it.

# Next step

Consult the [component catalog](../components/index.md). Activate relevant nodes and ask their **own** targeted follow-up questions. Repeat until the graph selection and design decisions stabilize. Then [propose the architecture](../phases/design.md).
