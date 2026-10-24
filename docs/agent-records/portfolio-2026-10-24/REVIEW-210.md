# REVIEW-210 — Independent supervised preview release review

- ID: REVIEW-210
- Status: verified
- Target System: project
- Change Classification: project
- Authorized Scope: independent exact-candidate AgentOS release review; write APP-000395.md and REVIEW-210.md only, plus assigned scratch; no product mutation, merge or deletion
- Affected Paths or Resources: /Users/Shared/projects/AgentOS read-only subject; docs/agent-records/portfolio-2026-10-24/APP-000395.md and REVIEW-210.md; /private/tmp/agentos-release-review-20261024
- Owning Role: Reviewer /root/review_agentos_release, AGENT-000008
- Related Requirements: REQ-000057
- Related Tasks: TASK-000210, RUN-000205, TASK-000218, RUN-000213
- Approval Requirements: direct current user project authority and fresh Coordinator review delegation; exact candidate binding; ordinary PR protections and separate permitted promotion; no organization approval

Decision time: 2026-10-24T20:21:59.277121+00:00. This is a fresh execution without implementation authorship. Requested inherited model/effort and actual billing are not independently observed here. No subagents, native model trials, GPU, sandbox services, deployments, target installations, merge, deletion or source mutation occurred.

**PASS for shipping the documented supervised preview. No product defect blocks that supported scope.** This review does not establish reliable general onboarding, production readiness or completion of the prior both-model/all-path qualification goal. Those remain explicitly unverified. Promotion and retirement remain pending gates.

## Exact subject and authority

Repository /Users/Shared/projects/AgentOS; origin https://github.com/tclasen/AgentOS.git; owning main. PR https://github.com/tclasen/AgentOS/pull/34 is OPEN, MERGEABLE, with no reported checks, and its live head/base match:

- Baseline: e352574dc4b932ae1cdc8e5d94a98a5e86f619ae
- Reviewed head: bba2b9222288a7cadb51e723d482b5d8a59997ce
- Reviewed tree: ddb6f79087d93d77a55438e8604df1c6f9fcb850
- Branch: ship/agentos-2026-10-24

Read organization core, authority/scope, Reviewer role/context, acceptance/Git/approval/change control, assigned task/run and review task/run, README, release report, tool guide, bundle start/constitution/installer policy/routing/qualification/handoff and relevant prior findings/qualification reports. No project AGENTS.md/profile exists; direct user/task authority governs. Reviewer claim is limited to these records and scratch; Coordinator owns later Git/deletion. Review task/run copies retain historical Developer fields; their explicit Reviewer role/claim and delegation identify this execution. They are admission records outside the frozen eleven-file subject.

## Criterion results

| Criterion / expected | Observed / outcome |
| --- | --- |
| Practical supervised entry point | PASS. README explains Markdown installer versus optional helpers, separate source/target location, immutable source identity, exact-path approval, preservation, required qualification and Director handoff. Source start and operating contracts support that flow. |
| Honest supported use and limits | PASS. Prominent preview wording and release evidence distinguish historical corrected native successes, current deterministic helper checks, retained failures and absent current AI onboarding/first-use rerun. No automatic installer or enforcement guarantee is implied. |
| Prior failed experiment remains failed | PASS. Latest manifest-reference report and APP36 still reject the experimental twelve-path package. All bundle/tools/tests and prior reports/approvals are byte-identical to baseline. No failure is regraded, removed or relabelled as a model pass. The withdrawn literal-program experiment is not an active requirement to prove the current unchanged preview package usable. Its original failure remains valid. |
| Existing regressions | PASS. Independently reran unchanged suite from exact-head archive in scratch: 61 tests, 28.673 test seconds / 28.941430 wrapper seconds, exit0, no skips. |
| Real helper use without Git | PASS. Actual copied non-Git graph and identity invocations pass; alteration of start.md actually exits1 and reports only changed start.md. This tests helper behavior, not AI installation. |
| Structural profiles and release identity | PASS. Graph25; portable10/engineering22/portfolio18 closures. Manifest helper matches all46 bundle regulars. Separate reviewer stdlib path/hash/length recomputation equals the manifest exactly. Selection is structural only. |
| Local published links | PASS. 186 local file destinations resolve. URL reachability and Markdown fragment validity excluded. |
| Scope and evaluator integrity | PASS. Exact eleven-path diff contains README plus release/task evidence; product/tools/tests and prior reports unchanged. Reused evaluator bytes are pinned below and all six governance-before bindings remain equal. |
| Whitespace | Source/doc checks PASS. Full git diff --check exits2 solely for a new blank line at EOF in release-checks.log:1100 and release-checks-attempt1.log:80. These are retained raw outputs, not product whitespace defects; preserve their exact bytes and hashes. |
| Remote-main delivery | PENDING. Live main remains baseline e352574; PR34 is open. No merge or completion is attested. |
| Safe local retirement | BLOCKED pending preservation and release of users, detailed below. No deletion performed or approved here. |
| General model/runtime/production behavior | UNVERIFIED. No current model, GPU, provider, native integration, authentication/retrieval, target installation, fresh activation or real application scenario was run. Python3.9 minimum is documented, but this execution tests only Python3.15/macOS POSIX. |

## Independent execution evidence

An exact-head git archive was extracted into owned scratch, without modifying the repository or tests. Candidate JSON/log were renamed outside the copied evidence directory before execution because the script refuses overwrite. The unchanged release-checks.py ran once with Python -B and its PYTHONDONTWRITEBYTECODE environment, suite timeout600s. Ordinary approved execution escalation permitted the test's owned AF_UNIX socket fixture. No weakening, skipping or semantic retry occurred. Environment: macOS-27.0.1-arm64-arm-64bit-Mach-O; Python 3.15.0 (main, Oct  9 2026, 11:16:41) [Clang 21.0.0 (clang-2100.3.34.2)]. Start 2026-10-24T20:19:34.211778+00:00.

| Check | Actual / expected exit | Result |
| --- | --- | --- |
| existing-regressions | 0 / 0 | PASS |
| bundle-graph | 0 / 0 | PASS |
| portable-selection | 0 / 0 | PASS |
| engineering-selection | 0 / 0 | PASS |
| portfolio-selection | 0 / 0 | PASS |
| release-manifest | 0 / 0 | PASS |
| copied-source-graph | 0 / 0 | PASS |
| copied-source-identity | 0 / 0 | PASS |
| copied-source-change-refused | 1 / 1 | PASS |
| published-entrypoint-and-bundle-local-links | 186 destinations; 0 broken | PASS |

Independent scratch report SHA-256 `7e286238e9aa9d0140d37c2ea9597edcbef77348aa3a0b8094128ff580950036`; raw log SHA-256 `80a9a7e188b1a368f31341d5e89eb9b938f2226502b81ecdaa7160f5002d22b2`; unchanged script SHA-256 `f170735b5311d12921a5f3565c78813976670d51a676fe57b07c4477a0f6179d`. Audit/instruction/Git/input bindings are in scratch review-audit.json SHA-256 `2ad5b1d3737b379771d706a597224d83f799196126b04a560226258e9ac33c14`. Non-.git inventory is inventory-before-review.json SHA-256 `1df6926c72f30c1c0e9801bb77d2097a87f9248a4580e9185603a21c7eff1a83`. Retain these actual independent evidence bytes in verified durable archival storage before scratch cleanup; a temporary path is not durable preservation.

Developer attempt1 remains failed: 60 pass and one PermissionError at Unix socket bind, before its snapshot assertion. Its JSON/log persist unchanged in the candidate; subsequent successful execution does not erase it. Inspection-only diagnostics here: guessed bundle/reference/README.md absent (no read credit); one combined display truncated (no completeness inference); initial non-escalated gh API connection denied, ordinary approved read-only escalation succeeded. No content was changed to repair these probes.

## Safe deletion preconditions

Before review records were written, checkout has272 non-.git regulars:270 tracked, two untracked review admission records (TASK218/RUN213). No tracked modifications, staged changes, ignored files, symlinks, nested repositories/submodules or special files were observed. One registered worktree is the primary checkout at /Users/Shared/projects/AgentOS. No removal was attempted. Later review records and any Coordinator updates increase the preservation set; reinventory immediately before retiring it and establish no active user remains.

Live ls-remote --heads origin reports only main e352574 and ship bba2b92. Stale remote-tracking refs are not proof that corresponding objects remain remotely reachable. Three local backup refs retain four commits absent from both live remote heads:

| Local ref | Tip |
| --- | --- |
| refs/backup/pre-cleanup-main | 41e225c21a68319ec8770ba2f88815b85219d3b0 |
| refs/backup/pre-markdown-only-main | 1925c34955da27dde3bed1ecc351bbcbe41fd155 |
| refs/backup/pre-simplification-main | 055f48f2e8181d7be13a00c26f8685e167c9c819 |

The fourth retained ancestor is87775f2fde919190e8724b09cf1211086fa1aff3. Preserve a complete ref/object/reflog-aware recovery archive or equivalent verified durable destination, including these backup identities, before deletion. Do not assume GitHub main or deleted PR branches preserves them. The local fix/onboarding branch and stale historical tracking refs also require recorded disposition; retain full Git state if uncertain. No archival destination for unique Git state was independently verified by this execution.

Required sequence: publish exact approved content plus independent records, inspect current protections/threads/checks, permitted normal merge and fresh owning-main content/ancestry verification; preserve any remaining unique tracked/untracked/ignored/ref/reflog evidence with path/hash/length verification outside the retiring checkout; preserve this review scratch evidence durably; release all active claims; recheck inventories and perform only separately authorized full-checkout retirement. Factory scope removal is a separate organization change and is outside this approval. Coordinator's pending explicit promotion approval following automatic review rejection remains a gate; this review grants no bypass.

## Exact eleven-file content binding

| Candidate path | Bytes | SHA-256 |
| --- | ---: | --- |
| README.md | 2760 | 6d8b0133eb608e43cb96ce23a06c804a1e4a867482ff98f53a5d9f3293d03072 |
| docs/agent-records/portfolio-2026-10-24/RUN-000205.md | 4042 | 83f7bca5a1f2be5dea417d13812a56fe1b0f6133c84993fdc9c03d18750c8dbe |
| docs/agent-records/portfolio-2026-10-24/TASK-000210.md | 9174 | d53d0c214b51f305c08a93a2aceee1fbdb91ad205723a30ba396e877767acb10 |
| docs/agent-records/portfolio-2026-10-24/governance-before.json | 568 | b345f83118d078d0ca650f38530f4c0dc6a41d174c3ae742c67db462eda046c0 |
| docs/agent-records/portfolio-2026-10-24/release-checks-attempt1.json | 4200 | b9249884e48b8f9c4148871074e0ffffa1ae63b0db215f45d222c41321bc4c34 |
| docs/agent-records/portfolio-2026-10-24/release-checks-attempt1.log | 11294 | 9793d8991fef5709403d55a81886baccf2d79d0e60e1297c809044a8b1c8b98a |
| docs/agent-records/portfolio-2026-10-24/release-checks.json | 13741 | 9909495070867de0859e81756ca382479f9b4eb7789bc6ada07055ec2ec152c4 |
| docs/agent-records/portfolio-2026-10-24/release-checks.log | 44006 | 4fd2ae3116e1a7a99531d704ec41a5ec8727ae915cc16b58f03c438529af6a53 |
| docs/agent-records/portfolio-2026-10-24/release-checks.py | 6243 | f170735b5311d12921a5f3565c78813976670d51a676fe57b07c4477a0f6179d |
| docs/releases/2026-10-24-preview.md | 4586 | 0ca1b41e378c409bdb685d798b9d196289a65b826317a3cc0de1278f6f168c6b |
| docs/releases/2026-10-24-source.json | 6746 | 40751dd56ebfda0b1c2dafa7e4ef64ac36c71c12494eca24b2d1539b498b22c8 |

Handoff: PASS bounded preview release review to Coordinator/project authority. Permit publication of this receipt and APP395 plus factual admission/final delivery observations without rerunning unchanged product tests; compare every original eleven-path byte binding before promotion. Product/release-claim/evaluator changes invalidate affected approval. Keep TASK210/TASK218 nonterminal until required delivery and retirement obligations are reconciled. Rollback is an ordinary corrective/revert PR, preserving failures and unique data.
