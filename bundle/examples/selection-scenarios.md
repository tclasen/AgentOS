---
type: AgentOS Example
title: Illustrative OKF component selection scenarios
description: Example signals and recursive dependencies to explain navigation without imposing a fixed installation.
tags:
- agentos
- examples
- routing
status: stable
---

# Scenario A: Small research/document repository

Read-only inspection finds a simple non-code repository and no actual native agents. User wants conversational Director, CoS-driven improvement and low overhead, with no long-running or external effects. Select only required responsibilities, synthesized as a small set of Markdown policies and role instructions. No automatic scheduler, durable task database or fake concurrent workers.

# Scenario B: Codex with concurrent software tasks

Runtime inspection confirms supported agent spawning; user wants actual parallel workers, nested tasks and Git PR delivery. Signals: `native_agents`, `parallel_workers`, `remote_git_delivery`, `long_running_work`. Examine [native runtime](../components/runtime-native.md), [parallel coordination](../components/parallel-coordination.md), [work ledger](../components/work-ledger.md), and [Git delivery](../components/git-delivery.md). Git delivery requires [external effect reconciliation](../components/effect-reconciliation.md), and may benefit from [durable handoff](../components/durable-handoff.md) if tasks span sessions. Ask only targeted unresolved follow-ups, approve any extra native configuration paths, then validate actual behavior.

# Scenario C: Existing sensitive multi-project organization

An existing agent system, multiple project repositories and private records imply `existing_agent_system`, `multiple_repositories`, `sensitive_data`. Investigate [brownfield migration](../components/brownfield-migration.md), [multi-repository management](../components/multi-repo.md) and [information boundaries](../components/information-boundaries.md). Ask ownership and migration questions before any edits; do not inherit old grants as if they were current.

# Graph semantics

These scenarios demonstrate trigger → candidate → local questions → hard dependencies → approved installation. They are not code to run, not a fixed questionnaire and not proof that the runtime offers these features.
