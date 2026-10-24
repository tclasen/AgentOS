---
type: AgentOS Procedure
title: Qualify actual operational contracts
description: Verify structural integrity and selected functional behavior, not just documents.
tags:
- agentos
- phase
- verification
status: stable
---

# Minimum checks

- Reconcile the selection/read checklist against all required catalog entries and the selected hard-dependency closure. Verify that each full selected source was actually read; load any omission before continuing.
- For **each selected component**, compare its individual source Responsibilities or Operational contract, Implementation and Verification obligations with the installed artifacts. Record a compact mapping of obligation → implementation location/mechanism → check and outcome, grouped by source component. This mapping may live in the installation report or another approved existing file; it is not a requirement to create one file per component. A component-level row saying its role or file exists does not establish coverage of its distinct operating steps.
- Root `AGENTS.md` exists, role-aware routing is coherent and referenced files resolve.
- Director and Chief of Staff remain permanent with all constitutional guarantees.
- Installed optional components have an actual implementation pathway; no unsupported feature is represented as enforced.
- Native structured configuration parses and uses supported conventions where applicable.
- Reconcile changed paths against approved scope; preserve existing user data and instructions. Inspect actual commands and their implicit effects, including interpreter caches, temporary files and test/build reports; final snapshots can miss a transient unauthorized write. Exercise a narrow output-only grant by deciding how to suppress or refuse incidental writes on every relevant command. Do not perform prohibited writes to test refusal or treat later cleanup as authorization. Where startup/readiness helpers persist state, exercise a narrow task grant excluding that state: manual helper writes must be skipped or blocked, including writes that merely record "skipped". Do not confuse an explicitly approved native hook's separate effects with the task's manual-write scope.
- Verify self-improvement can be triggered and has an execution/evaluation/retention path appropriate to runtime availability. Check for evidence and hypothesis, authorized scope, criteria fixed before the candidate change, an actual evaluation step, a scoped rollback decision and retention of accepted, rejected and inconclusive outcomes. A lightweight lessons entry in an existing file is sufficient; optional independent-evaluation or learning-queue infrastructure is not required. Merely saying how an edit *could* be checked does not implement this loop. Exercise a bounded correction or controlled local scenario and label its evidence honestly.

Missing required operating steps are installation defects even when the corresponding role/file exists. Correct them within the approved paths and authority, or report the installation incomplete with the exact gap. Do not label it qualified or complete on structural checks alone. Fresh-runtime tests may remain explicitly unverified where unavailable; that limitation does not excuse missing operational instructions.

For the minimal portable profile described in [implementation](implement.md), use the [concrete reference and correction exercise](../examples/portable-implementation.md) to check synthesis and evidence quality. The example is not a passing result: inspect the actual installed duties and evaluate concrete prior/candidate values against criteria fixed before the change. Retain usable recovery content and the real result; copying an illustrative outcome or saying how an edit could be checked is insufficient. Equivalent scoped exercises are allowed, and richer selected profiles retain all their own obligations.

# Required operating checks

Use these checks to catch frequently lost obligations in a compact installation. The component sources remain authoritative; this is a qualification aid, not a replacement for reading them. A controlled scenario can be carried out locally or reasoned through with an honest simulation label when native execution is unavailable.

| Contract | Inspect the installed pathway and exercise a bounded scenario |
| --- | --- |
| Director and reconfiguration | Trace intent → capability → execution/delegation → verification → outcome report. Also trace a user reconfiguration request through Director clarification, CoS implementation within grants, evaluation and return to Director; the temporary installer must not be required. |
| Capability routing | Match needed capabilities against actual availability, permissions and budget. For a missing capability, consider reuse, learning/training, an authorized tool integration or justified new role before escalation. Unknown resources stay unknown. Probe an available capability and a missing one; a dedicated budget system is unnecessary. |
| Delegation | Ensure the assignee receives intent, accountable owner, authorized scope, necessary context, deliverable, **acceptance criteria** and reporting expectations. Nested assignments inherit limits and cumulative budgets. Exercise assignment → scoped work → evidence return → Director reconciliation; sequential specialization must be labelled honestly. |
| Authority and delivery | Exercise an allowed local action and refusal/escalation of an action outside the grant. Compare a successful local outcome with a misleading worker-completion claim; verify the Director checks original intent and required delivery before acceptance. No real prohibited action is needed. |
| Role lifecycle | Check active work, pinned instruction versions, historical role identity, routing and dependent capabilities before changing or retiring a role. Simulate an optional-role amendment/retirement with an active assignment: preserve its old contract/history, transfer responsibility explicitly and update discovery before retirement. Keep Director and CoS permanent. A brief record in an existing file is sufficient. |

Apply the same obligation-level check to CoS, activation, core context and self-improvement, and to every selected conditional component. Preserve failed attempts and unresolved checks; do not silently replace an unmet criterion with an easier assertion. Report contract completeness separately from the evidence level of each scenario.

## Check the scenario evidence before claiming completion

For each required operating check, retain a short concrete record in an already approved evidence location: **input or prior state; fixed expected checks; observed decisions and result; installed instruction location used; evidence level; verdict and remaining gaps**. One scenario can cover several obligations when its actual trace demonstrates them. A simulation must still apply the installed instructions to particular inputs and record the resulting decisions; repeating the procedure or writing “scenario reasoned through” supplies no trace. A successful correction fixture does not establish delegation, reconfiguration, lifecycle or budgeting by itself.

For the minimal portable profile, the [operating-scenario worksheet](../examples/portable-implementation.md#concrete-operating-scenario-worksheet) supplies concrete inputs you can adapt. Work through every applicable case using the installed files; do not copy its expected checks as observed results. Richer profiles need the corresponding selected-component checks as well.

Before handoff, follow every evidence reference in the coverage mapping to its actual record. Check that the record contains the promised input, trace and result, and that the result satisfies the original checks. If a row promises a trace “below” but none exists, that check is incomplete. Perform the missing check within the grant or report the exact gap; do not label the installation qualified. Update current status after corrections while retaining failed attempts. Fresh-runtime activation and independent review retain their separate evidence limits.

# Risk-based behavioral qualification

When a fresh reviewer is available through the actual runtime and within the user's delegation/resource grants, use it before claiming installation qualification. Give it the selected original component sources, approved design/paths, pinned artifact identities and actual evidence. It must inspect installed content itself rather than trust the installer's mapping. Reconcile missing obligations, make scoped corrections within existing approval, and recheck the changed candidate. This is installation quality control, not automatic selection of permanent independent-evaluation infrastructure. Do not invent a reviewer when spawning is unavailable; disclose solo qualification and its limits instead. A reviewer label in the same context is not fresh review.

Choose scenarios appropriate to the approved design, using [evidence levels](../concepts/evidence-levels.md): unassigned session → Director, delegated identity preserved, task/result handoff, refusal of unauthorized action, correct delivery status, interrupted-session recovery, duplicate external effect prevention and evaluation independence. Higher-risk installations warrant independent tests and actual native runtime trials where supported.

Do not infer correctness merely from self-report, passing metadata validation, or simulated API effects. Document tested, untested, unsupported and blocked requirements separately. Incomplete required capabilities prevent a claim of full completion; accept bounded exceptions only with explicit user consent.

# Transition

Proceed to [handoff](handoff.md) with an accurate report.
