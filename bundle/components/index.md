# AgentOS components — progressive discovery catalog

This is a **routing catalog**, not a mandatory reading list. Start with the required components, then choose conditional components based on the user's answers and repository/runtime observations. The `agentos:` extension in each node expresses `selection`, `when_any`, `requires`, and `provides`; the standard Markdown links form the OKF graph. Resolve hard dependencies **only for selected components**.

## Required responsibilities in every installation

- [Director](director.md) — human interface and delivery ownership.
- [Chief of Staff](chief-of-staff.md) — organizational evolution and recursive improvement.
- [Activation](activation.md) — role-aware user/director startup.
- [Authority](authority.md) — actual grants, permissions and scope.
- [Capability routing](capability-routing.md) — select and evolve needed capabilities.
- [Delegation](delegation.md) — assigned outcomes and subordinate collaboration.
- [Delivery acceptance](delivery-acceptance.md) — verify user intent and real outcomes.
- [Core context](context-core.md) — progressive, relevant instruction loading.
- [Self-improvement](self-improvement.md) — observable, bounded learning loop.
- [Role lifecycle](role-lifecycle.md) — safe create/modify/retire procedure.

These are **required operating responsibilities**, not necessarily ten installed files or ten processes.

## Conditional components and discovery signals

- [Runtime-native integration](runtime-native.md) — `native_agents`, `runtime_specific_integration`; native structured agent/hook configuration.
- [Durable work ledger](work-ledger.md) — `long_running_work`, `parallel_workers`, `complex_dependencies`; task/run/dependency state.
- [Parallel coordination](parallel-coordination.md) — `parallel_workers`, `nonblocking_director`; actual concurrent agents.
- [Durable handoff](durable-handoff.md) — `long_running_work`, `cross_session_continuity`, `interrupted_work`, `external_effects`.
- [Effect reconciliation](effect-reconciliation.md) — `external_effects`, `remote_git_delivery`, `business_automation`; safe external retries.
- [Independent evaluation](independent-evaluation.md) — `high_assurance`, `repeatable_improvement`, `strict_review`.
- [Learning queue](learning-queue.md) — `repeatable_improvement`, `recurring_failures`, `high_assurance`.
- [Telemetry](telemetry.md) — `rich_telemetry`, `optimization_metrics`.
- [Resource budgets](resource-budgets.md) — `cost_constraints`, `parallel_workers`, `expensive_tools`.
- [Git delivery](git-delivery.md) — `remote_git_delivery`.
- [Information boundaries](information-boundaries.md) — `sensitive_data`, `multiple_repositories`, `public_repository`.
- [Multi-repository operation](multi-repo.md) — `multiple_repositories`, `portfolio_management`.
- [Scheduling](scheduling.md) — `recurring_triggers`, `always_on_automation`.
- [Brownfield migration](brownfield-migration.md) — `existing_agent_system`, `brownfield_conflicts`.
- [Advanced qualification](advanced-validation.md) — `high_assurance`, `compliance`, `complex_dependencies`.

A signal suggests *investigation*, not automatic installation. Components may become relevant for unlisted reasons. Individual nodes ask local follow-up questions. Do not open every conditional file just because it is listed here.
