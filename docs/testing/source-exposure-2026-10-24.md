# Separate source content exposure from command success

The qualification helper now records complete canonical Markdown content appearing in completed command output as `source_content_exposures`. Each source carries its SHA256/byte count and observations with parsed-event index, item ID, command/output hashes and aggregate exit/status. This fixes an evidence gap exposed in PR18: a later command can fail after a complete source body has already reached the output.

**Proposed helper disposition: accept, subject to independent review.** Existing `full_component_reads_observed`, `failed_commands` and every other prior summary field retain their original behavior. The new field is evidence for human inspection, not automatic approval. Complete text does not prove a file-read operation, its own exit status, comprehension, semantic correctness or read-before-write ordering. Raw provenance, approved source identity, original duties, scope and actual behavior still require review. Agent claims, started-only events, partial/wrong bodies, empty sources and links receive no new credit; partial fragments are not joined.

**Operative onboarding disposition: reject promotion as unqualified.** The seven restored bundle edits are withdrawn. This round never reached installation or first use; it does not establish whether the cache guidance works in an installed organization.

Base `9fec32e2f944f70a777cfa142ccc534aeeb0350e`; tested combined candidate `c12f9bf1e16339d93fcca394101db7577c426579`. Final product changes are only `tools/qualification.py`, `tools/README.md` and `tests/test_qualification.py`; final bundle equals base. [Task](../agent-records/tasks/project/TASK-000192.md), [run](../agent-records/runs/RUN-000187.md), [detailed findings](source-exposure-2026-10-24.json).

## Validation

44 regressions passed in12.053seconds:41original tests plus3new tests covering failed compound commands with preserved failure/strict metric and exact provenance; partial/wrong/agent-claim/started-only/fragmented evidence; successful output; and empty/linked-source refusal with input preservation. These test assertions establish helper behavior, not model comprehension.

Replayed all four PR18 native logs against their archived original source. Every original summary field remained identical. The checkout Sol design body appears in the new field at item_6 with outer exit2 retained; its historical unqualified verdict is unchanged. Also compared the three fresh logs below against the baseline helper: all original summary fields remain identical. No retrospective replay is counted as a fresh model trial.

Graph closures remain portable10/engineering22/portfolio18, with23 unchanged component bodies, four preserved budget duties and23 relevant links. The seven operative source files were identical to the prior tested implicit-write candidate3facc2433007827e2dd9e58934a9bff774194a0b throughout the fresh trials. Four correction-fixture cases and four owned local-import cache probes passed. Normal correction retained actual accepted/rejected/inconclusive results and scoped recovery preserving later_note; refusal cases preserved preexisting data. Cache guards suppressed bytecode while producing the same14 output bytes. These are parent local checks only.

## Fresh native trials

Codex updated0.149.1→0.164.0 before trials; native catalog advertised high for both requested models. Actual session metadata confirms each configuration. Peak two roots, zero children/model retries. All3returned; all existing target/source/Git/cache bytes preserved by full inventories and actual command-effect inspection.

| Trial | Actual model/effort | Seconds | Gate/result |
| --- | --- | ---: | --- |
| Checkout Luna | gpt-6-luna/high | 50.902 |11selected sources and startup content, exact47file identity; pass D |
| Checkout Sol | gpt-6.1-sol/high |189.984 |11selected sources and startup content, exact47file identity; pass D |
| Bundle-only Luna | gpt-6-luna/high |74.891 |11selected sources and startup content;47correct paths/hashes, missing byte counts; reject under frozen manifest-format gate |

Bundle Luna item_2 displays complete constitution, installer policy, graph routing, bootstrap and discovery bodies before the optional-tools search exits2. The new field retains those exact bodies with failed status; the old successful-only measure and raw failure remain unchanged. Parent inspected command ordering/provenance rather than treating containment as automatic semantic acceptance. This is a fresh native example of the intended helper distinction.

Bundle Luna item_7 emits all47correct path/SHA256 pairs but no byte lengths, and its final proposal retains that actual output. The preregistered trial gate requires path/hash/length equivalence, so no installation handoff was approved for that cell and no parent filled missing fields. The portable source itself asks for an equivalent verifiable byte manifest; a complete correct cryptographic hash list is substantive identity evidence. This is therefore a trial/schema completeness constraint, not proof of substituted source, missing source content or ineffective cache guidance. A concrete portable manifest recipe or a separately assessed identity-evidence rule could address the mismatch in a future experiment; neither is implemented by this PR.

No bundle Sol discovery or any I/U was admitted after that failure was diagnosed; already-admitted checkout Sol finished and its design evidence was retained. No source/evaluator revision or native rerun repaired the outcome. The separate helper-versus-operative dispositions were declared before trials. No incomplete path receives a pass or claim of broad onboarding qualification.

## Evidence and remaining work

Verified trial archive `/private/tmp/agentos-exposure-20261024-trials.tar.gz`: SHA256 `6a6a3fa12ed7a7e2b3579d16f505563188f918f98912afe1ca3d33b463458b12`,4,073,691bytes,1193indexed payloads. Includes frozen sources/criteria/controls, prior archive, original and new observations, actual3native logs, failed identity evidence, local validations and protected inventories. The old archive has its own recorded SHA and original verdicts; no historical evidence was overwritten.

Fresh APP-000020 review, protected PR/main verification, acceptance export and exact owned sandbox/raw-fixture cleanup remain pending at this reviewed revision. Preserve all63preexisting sandbox identities; no global prune. No dollar/token usage is invented. Full both-model/all-designed-path onboarding and fresh use remain active requirements.
