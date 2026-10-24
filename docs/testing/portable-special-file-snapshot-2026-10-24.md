# Portable special-file snapshot qualification — 2026-10-24

TASK-000201 / RUN-000196 proposes accepting the snapshot fix, subject to independent APP-000029 review and normal PR/main verification. The baseline helper blocks when it opens a FIFO retained by a completed worker; a fresh 3-second subprocess reproduction timed out and was reaped without a writer. Recording special-entry type bits with `lstat` avoids opening FIFOs, sockets or devices. Regular-file hashes/bytes, directory and symlink representations and exclusions remain unchanged.

The prior TASK-000200 result remains rejected: Luna could not finish socket/delta tests after `bind` was denied. This prospectively registered round keeps the nonblocking, exact-type, preservation and delta requirements, and adds a documented Linux fixture method: after `PermissionError`, `mknod(S_IFSOCK|0600)` creates an actual filesystem socket inode. It does not create a bound endpoint or prove socket communication. The test reports its construction method; no skip, weakened assertion, native permission change or historical regrade was used. Other setup errors still fail.

## Verified local and native evidence

The restricted macOS suite retained its setup error: 50 passed, one `socket.bind` PermissionError, 51 tests in 16.242 seconds. An authorized host rerun passed all 51 in 16.851 seconds using a real bound Unix socket. Original49 tests remain; two focused tests cover bounded actual CLI snapshots, a nonregular-read trap, type deltas and target/additional-scope run finalization.

Codex was updated from0.149.1 to0.164.0 before either native root. App-server catalog supports both requested models/high; owned-session metadata confirms actual Sol/high and Luna/high. Each received only its target, public candidate source/guidance and bounded task context, with source read-only and writes confined to its own scratch. Source/prompts/criteria were frozen before either launch.

| Observation | Sol | Luna |
| --- | --- | --- |
| Native duration | 183.285 seconds | 43.868 seconds |
| Local checks | 34 passed | 54 passed |
| Actual CLI snapshots | 3 | 26 |
| Longest snapshot (5-second limit) | 0.024101 seconds | 0.034775 seconds |
| Retained bind failures / successful inode fallbacks | 11 / 11 | 8 / 8 |
| Parent-collected special entries | 8 | 2 |
| Original regular files including Git preserved | 27 | 27 |
| New regular scratch files | 37 | 81 |

Both independently tested FIFO/socket additions, removals and both directions of transitions with regular files, directories and symlinks. Sol preregistered a17-entry baseline,22-entry forward fixture and reversed baseline; exact expected JSON,12 changed paths each way,5 additions/removals and per-call before/after inventories all matched. Luna executed26 CLI snapshots, checked independently enumerated live entries, explicit special types and known regular/link contents, and checked12 directional transitions plus FIFO/socket additions/removals. Its preservation evidence covers bytes/types/link targets rather than Sol's additional inode/time metadata.

Parent inspection independently verified actual scripts, outputs, live types, original regular-file hashes, source/control hashes, scope and both runner records. Both parent runners returned without opening or writing FIFOs, with typed `special` entries in `after`; no parent repair or semantic model retry occurred. No bytecode caches were created. CLI summaries contain10 Sol and5 Luna completed commands, all exit0; construction PermissionErrors were caught and retained in scripts/reports, not silently relabeled successful binds.

Each initial batched source read had an explicit native truncation flag (Sol line27, Luna line17); both subsequently read the relevant snapshot implementation. This experiment grants no full-source delivery, installation or onboarding credit. Its acceptance concerns demonstrated helper behavior and fixture construction under the registered contract. Native primary tool records, including these limitations, are retained for review.

## Provenance, scope and delivery

Base `dc19ed51e18177550ba8027997b029f175123504`; operative candidate `023b2d4321bb4cedfae856d85f6804d42dd7324d`, tree `3157819ab5cd41833621f752e92fd70fdfd21208`. The machine report binds exact native identities, requested/actual configuration, usage, paths, timings and evidence. `controls/frozen.json` binds223 frozen source files, original targets and control hashes. Raw evidence is under `/private/tmp/agentos-portablesnapshot-20261024`; verified compact trials/acceptance archives must precede exact-owned cleanup. Special entries are preserved as recoverable metadata, never read into an archive.

Both trial usage records total297335 input tokens,240896 cached input,13562 output and2208 reasoning-output tokens; cache writes0. These are native counters, not a billing estimate. Review usage will be separately observed. Maximum4native roots, peak2, children0,600-second trial and1200-second review limits,60-minute round and two diagnosed retries per operation remain in force.

No bundle/onboarding/source-reading/selection semantics, canonical governance, unrelated branch, original sandboxes or harness configuration changed. There is no device-content, socket-communication or race-safety claim. The user’s broader all-execution-path improvement goal remains active.

Independent Reviewer must inspect the pinned code/report/evidence, assess the portability adaptation under unchanged functional criteria, rerun full/focused tests and approve or reject. If approved, only an expressly permitted byte-identical APP29 receipt and observed-fact attestation may follow without affected rereview. Closure takes effect only after normal PR merge, fetched-main content/ancestry verification, indexed evidence retention and exact-owned sandbox/raw-fixture cleanup; those observations belong in the final delivery handoff.
