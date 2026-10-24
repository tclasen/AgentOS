---
type: AgentOS Procedure
title: Recursive component selection and interview routing
description: Interpret OKF concepts and AgentOS extension fields without installing the whole graph.
tags:
- agentos
- graph
- routing
- required
status: stable
---

# OKF compatibility

This bundle follows Google OKF v0.2. OKF only standardizes Markdown concept documents, YAML frontmatter, links, optional indexes, and provenance. **All `agentos:` metadata below is an AgentOS-local convention**, not part of Google OKF. Normal Markdown links are the actual graph edges; frontmatter adds structured selection semantics.

A component may declare:

- `agentos.selection`: `required` or `conditional`.
- `agentos.when_any`: advisory factual or preference signals that make a conditional component worth considering. **A signal is never sole authority to install.** Additional unlisted reasons are allowed.
- `agentos.requires`: bundle-root-relative component paths; their dependencies must be resolved before installation.
- `agentos.provides`: capability labels for matching work to solutions, not executable guarantees.

# Progressive interview and traversal algorithm

1. Read [bootstrap questions](../interviews/bootstrap.md) and inspect the repository/runtime. Capture answers and observed facts, with provenance and uncertainty. Ask at most a small cohesive set of initial questions; skip answered ones.
2. Seed the selection with all **required** components listed in [the catalog](../components/index.md). Inspect the catalog summaries for conditional candidates matching user requirements, observed signals or inferred constraints; read only candidates likely to matter.
3. Read each activated component's frontmatter and body. Recursively activate its `requires` paths; verify they exist, are in the bundle, are not deprecated, and have no unresolved conflicts or cycles. Read links marked as prerequisite or relevant implementation guidance; do **not** read every neighbor by default.
4. Each component contains `## Follow-up interview` questions. Ask only the subset whose answers materially affect implementation; recommend defaults and skip redundant questions. An answer may reveal new signals and activate additional components.
5. Iterate graph selection and questioning to a **fixed point**. Track visited paths, chosen/deferred/rejected components, reasons, relevant answers, and capabilities not supported by the selected runtime. No infinite recursive prompts.
6. For alternative implementations, explain the tradeoff, choose the smallest appropriate option, and record its reason. When a required component cannot function as requested, disclose the limitation or block, instead of writing fictitious behavior.
7. Before edits, present the selected component closure, anticipated target artifacts and paths, permissions, validation level, exclusions and constraints. Obtain approval. Do not silently install source graph nodes themselves.
8. Implement tailored instructions and native configuration synthesized from selected nodes. Verify component implementation and activation, not merely link existence. Record installer bundle commit/tag and selections in a compact installation manifest **if authorized and useful**.

# Safety and graph discipline

When a local AgentOS checkout and Python 3.9+ are available, the optional read-only command `python3 tools/qualification.py select bundle --component components/git-delivery.md` (from the AgentOS checkout root) computes required plus requested dependency closure and rejects deprecated selected nodes. Repeat `--component` for additional requested nodes; omit it for the required closure. Its hashes and path list do not establish full-source reads, requirement coverage or authority. Continue the interview/read/approval checks below. Manual traversal remains sufficient when the helper is unavailable; do not install it into the target merely to plan an organization.

Reconcile each stated requirement with a selected operating contract, an explicitly approved alternative, or an unresolved gap before deferring a candidate. **Contract selection, runtime activation and permission to execute an effect are separate decisions.** A future action grant or unavailable background runtime does not by itself remove the requested contract:

- Planned Git delivery needs the Git-delivery contract even when installation permits no commit or push.
- An approved on-session/event fallback still needs the scheduling contract; prohibiting daemons does not prohibit that fallback.
- Limited agent slots and cumulative retry/delegation accounting activate resource budgeting even without a dollar cap.
- A requested scorecard still needs the telemetry contract when measurements are unknown; unknown coverage is a measurement-health result, not a reason to omit the contract.
- Requested adversarial/refusal/recovery qualification still needs advanced validation when its scenarios are controlled locally rather than sent to a real provider.

Selection only proposes the needed responsibilities. It grants neither target mutations nor future effects; obtain the applicable approvals before either.

Do not label a component deferred while proposing to implement its contract in another file. Consolidation or declining a dedicated tool/service does not defer the responsibilities. Before the proposal, show a compact conversation-only table: **stated requirement → selected component path → proposed mechanism → activation/grant status**. Check every deferral against this table; an omitted requirement or contradictory deferral is unresolved, not a completed design.

Before proposing an installation, reconcile a compact **selection/read checklist** against the actual catalog and completed reads, rather than memory. For each selected component, track its bundle path, selection reason, hard prerequisites and whether its full source has been read. Compare the checklist with **every required catalog entry**, then follow each selected node's `agentos.requires` until every prerequisite is selected and read. A batch read covers only the files actually included and successfully returned; mentioning a capability in a proposal does not satisfy this check. Load any missing source before asking for approval. Keep this provisional checklist in conversation until persistence is authorized; it need not become another installed file.

Read each required source in a separate displayed tool result and inspect that result for truncation before marking the source read. A full command log behind a truncated response is insufficient. Reread every affected required file in full in its own response before the proposal or dependent write; excerpts, joined fragments and metadata cannot fill the gap. Output limits may apply both to a command and to the wrapper displaying it. If the complete file cannot be delivered with the available limits, keep the dependent step blocked. This also applies when loading current contracts and procedures after a context handoff.

- An OKF link states a relationship, **not necessarily a hard dependency**; only `agentos.requires` does that in this installer profile.
- `agentos.when_any` describes *discovery hints*, not an exhaustive choice ontology or a compulsory static questionnaire.
- A missing optional link is tolerated by OKF; a missing selected hard dependency is an **AgentOS installation blocker**.
- Do not interpret `verified` as permission or treat a human-review tag as a guarantee of operational success.
- Installer graph traversal does not itself confer scheduling, permissions, agent spawning or state persistence.
