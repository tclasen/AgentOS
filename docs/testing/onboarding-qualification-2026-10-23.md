# Onboarding qualification — 2026-10-23

AgentOS was exercised in native Codex sessions with both `gpt-6.1-sol` and the explicitly requested weaker model, `gpt-6-luna`. Discovery, approval boundaries, preservation and fresh Director activation worked in the bounded trials. **Weaker-model self-qualification was not reliable:** independent review found incomplete operating contracts even after the installer produced a plausible qualification manifest. Review and correction remain necessary; these trials do not establish unattended or universal installation reliability.

## Environment and scope

The baseline was remote `main` commit `76b2dd57672202175f01c6ba4e1ddb9ffedef4e0`, verified against GitHub before testing. One local Docker Sandboxes instance (`agentos-onboarding-20261023`, 2 CPUs, 4 GiB) hosted separate disposable Git fixtures. Codex was updated **before the first trial**, from `0.149.1` to the npm registry's then-current `0.164.0`. Normal trials explicitly used `--sandbox workspace-write`; independent reviewers used `--sandbox read-only`. The default model was observed as `gpt-6.1-sol`; weaker-model commands explicitly passed `-m gpt-6-luna`. Monetary cost and reasoning configuration were not measured.

The user-facing README installation prompt was exercised with a supplied read-only, revision-pinned source checkout. Small Python notes and reporting projects were synthetic. The reporting fixture included existing `AGENTS.md` instructions, a preservation marker, dirty application code and an untracked note. No live project was enrolled or installed, and no application work, fixture publication, deployment, provider integration or background service was authorized. Existing unrelated sandboxes were inventoried and excluded from cleanup.

## Observations and changes

| Trial | Observed result |
| --- | --- |
| Baseline structural graph | All 46 bundle documents' local links resolved; 25 components and 38 hard-dependency edges had no missing target or cycle. YAML frontmatter parsed in 40 documents. The ten required metadata selections matched the catalog. |
| Default-model new project | Read all ten required components, asked a short interview and waited for approval. Interview answers explicitly withholding approval still produced no writes. Approved installation created exactly seven files, preserved README bytes and resolved all 16 installed links. |
| Default-model existing project | Read all ten required and six relevant conditional components. Preserved original instruction bytes, dirty code, untracked notes, HEAD and the staged tree. Added only the six approved organizational files and the approved root append. Fresh read-only review passed its structural/procedural criteria; this was not proof of every runtime behavior. |
| Fresh sessions and task paths | Unassigned sessions adopted Director and rejected misleading claims that local output and passing tests prove delivery/acceptance. A fresh delegated CoS retained its identity, repaired a controlled typo and returned evidence; parent byte comparison confirmed exact restoration and a retained lesson. |
| Recovery | Fresh Director resumed a saved checkpoint, inspected a correlated **local simulated receipt**, recorded a simulated result and did not retry. Prior state and all unrelated content were preserved; receipt delivery count remained one. No real external destination was tested. |
| Baseline weaker model | Lightweight discovery read all ten required sources and respected both approval pauses. Its seven-file installation preserved scope and links, but independent review failed its improvement loop: prospective checking was substituted for evaluation, rollback and retention of rejected/inconclusive lessons. |
| Baseline weaker conditional navigation | Read only nine of ten required sources: `components/capability-routing.md` was omitted despite selected dependencies requiring it. Project files remained unchanged. |
| First candidate correction | Explicit selection/read reconciliation repaired navigation: both weaker-model scenarios read all ten required sources. The generated improvement loop gained evaluation, rollback and three outcome labels. Independent review still found partial delegation, capability routing, Director reconfiguration and lifecycle contracts. The eleven-file layout did not itself establish completeness. |
| Second candidate correction | Obligation-level qualification and concrete scenario checks preserved compactness: the weaker model chose seven files. Both clean navigation scenarios read all ten required sources; the conditional scenario read six additional relevant components. Scope, links, approval and fresh Director activation passed. Independent review still found a missing initial budget check, insufficient Director dependency/progress detail, and only a generic improvement walkthrough. **Full first-pass qualification failed.** |

Four installer files now make the checks more explicit:

- [Graph routing](../../bundle/core/graph-routing.md) and [design](../../bundle/phases/design.md) require reconciling actual completed reads with every required component and the selected hard-dependency closure before approval.
- [Implementation](../../bundle/phases/implement.md) requires preserving individual operating obligations when consolidating files.
- [Qualification](../../bundle/phases/qualify.md) checks obligations and actual pathways rather than component names. Its bounded scenarios cover reconfiguration, capability availability/authority/budget, inherited delegation limits, delivery claims, role history, improvement evaluation and retention. Missing contracts must be corrected or reported incomplete.

The original constitution and component contracts were unchanged. No optional framework, runtime, ledger, fixed installed file count or recurring independent-review infrastructure was added.

## Review and correction trial

The remaining observed budget and Director omissions were assigned to a fresh `gpt-6-luna` CoS context as a bounded correction to the already-approved design. Its acceptance criteria were fixed before editing: match availability, permission and budget; preserve unknowns as unknowns; track dependencies and significant progress; preserve all existing grants and unrelated content; evaluate the actual change, retain its outcome and return evidence to Director. Independent acceptance is separate from the CoS's own checks.

The weaker CoS completed the correction and retained its predeclared criterion, actual text evaluation, accepted outcome and scoped rollback decision. Parent byte comparisons confirmed exactly the four authorized paths changed; no files were added and all protected files were unchanged. A fresh independent review (`01a16aa3-44dc-7340-8be8-3dc3e58c3385`) **passed repaired operating-contract completeness** against all ten original required components. It also identified two stale installation-time statements in the qualification record; those were qualified as historical without changing operating contracts.

Fresh `gpt-6-luna` activation and delegated CoS behavior were observed in separate processes. This establishes a bounded **review → correction → re-review** pathway, not reliable first-pass self-qualification. The actual available budget, runtime permission enforcement, concurrency, live role retirement and broad organizational benefit remain unverified. A fresh reviewer should check weaker-model installations before they are accepted; a plausible installer manifest alone is insufficient.

## Evidence and reproduction

Local raw JSONL transcripts, fixture baselines, installed snapshots, SHA-256 manifests, structural check scripts, failed attempts and parent inspections are retained under `/private/tmp/agentos-onboarding-20261023/`. They are not published with this report. Useful native thread identities include:

- Baseline lightweight weaker installer: `01a16a96-34aa-7a73-87b9-2712cdf1954d`; failing independent review: `01a16a98-e03d-71f3-9e2c-57bb63742057`.
- Baseline conditional weaker installer: `01a16a98-5d4f-7c20-96f0-435932022c8c`.
- First corrected weaker installer: `01a16a9a-d019-7ae2-a24a-d0805544a3b1`; failing review: `01a16a9c-f5d3-78d3-9900-3878a849e6b4`.
- Second corrected weaker installer: `01a16a9e-d7ba-79d0-93c9-1061e92c6017`; pre-rework review: `01a16aa0-8406-76d2-882e-2611b0737f09`.

To reproduce, create a clean disposable Git project, use the README prompt with the tested source revision and capture `codex exec --json` events. Separate discovery, answers that withhold approval, explicit path approval and installation. Independently compare baseline hashes, approved paths, HEAD and index. Inspect actual completed source reads, expanding shell loops/brace lists; do not count a directory listing as a read. Start fresh unassigned and delegated sessions, and review generated contracts against the original selected component sources. Preserve failed trials rather than reporting only the successful retry. All model trials are single observations, not a statistical benchmark; interview answers were supplied up front in corrected cold trials, unlike the initial lightweight interview.

Final candidate source SHA-256 values:

```text
bundle/core/graph-routing.md   2e53804476b9c3960c0893bff2f83db5d57e5bb21d40cdea0f1a16fd9db93977
bundle/phases/design.md        feddbeca4d74938a322e51108695febf150d01fd7e61d049d0adaae726d20974
bundle/phases/implement.md     7681fa4b99d2b43dcc89cd02e2bd150a58482f1c694db3b7a2cb409ac71dfd1d
bundle/phases/qualify.md       17a8782f7a090492c9cbedd537c35857f05a2789dca5c813a3d4e076d83557a7
```

## Limits and cleanup

No live remote publication, scheduler, concurrency, provider idempotence, real external-effect recovery or cross-runtime compatibility was qualified. Fresh CLI processes demonstrate bounded role behavior, not persistent workers, technical separation or independent permission enforcement. The cached-source trials do not qualify first-time source download/authentication. Rejected host-sandbox commands and a missing `python` alias were harness/tooling events; trials recovered with normal Codex workspace restrictions and `python3`, and their failures remain in local evidence.

Only the named test sandbox is owned by this task. Teardown follows evidence export and native reviews; the final session handoff must verify its absence and preserve unrelated instances. No broad prune, reset or removal of unrelated images/volumes is authorized.
