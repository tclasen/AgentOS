# Native trial deadlines

The corrected runner is recommended for promotion only after fresh independent APP-000035 and normal protected delivery. It addresses the observed TASK204 failure in which parent compaction left a600second trial running to699seconds. Enforcing deadlines inside the sandbox removes dependence on interactive polling. The previous onboarding failure remains rejected.

Native trials default to600seconds; --timeout-seconds accepts integers1..86400 within the existing grant. The independent Python supervisor preserves argv/stdin, launches a POSIX process group, measures monotonic elapsed time, interrupts at the deadline, and escalates after at most5seconds. Remaining same-group processes are killed on timeout; unrelated groups are not targeted. Partial native output and typed start/finish controls are retained. Timeouts never become successful runs, even after a completed-turn event; native exit124 remains distinct. The host transport is bounded at N+30seconds, with partial evidence and unknown remote termination retained on expiry.

## Independent rejection and correction

APP-000034 rejected first candidate6eda9b5c2d793036f97f216591476fca9606fb33 (operative4d6996253610ee9b94a7b9b377a35744c664dd99). Its60 passing tests and four native cases did not prove the full malformed-control criterion. Three independent probes showed Boolean version/timeout/exit fields were accepted because Python equates booleans and integers. The default supervisor emitted correct values; this was an evidence-validation defect, not a demonstrated bypass of its process deadline.

Plan2 prospectively admitted a new pinned repair under the continuing user grant and unchanged criteria. All first-revision code, results and APP34's880 indexed files remain preserved. A new24case regression first failed15 cases against rejected code; after explicit primitive-integer validation for version,limit,grace,PID,process-group andexit fields, all24 refuse correctly. The replacement operative is af4c13cb2612b40105e8bd138fc66dbe3f1ea7d2, treed712f3454d63d4e304ea298b46effc3d932dc2e7. No edits after its freeze; no original native result regrade. Bundle, source-read protocol, qualification matrix and original51 test criteria remain unchanged.

## Replacement validation

All61 tests pass on macOS29.070seconds and Linux15.729seconds. They include actual argv/stdin/native124, partial output, completed-turn-before-timeout, graceful interrupt, forcedkill when SIGINT is ignored, same-group descendant cleanup, unrelated-process preservation, closed-output cleanup, invalid limits/control records, and transport evidence retention. Existing isolated runner mocks only gained supervisor receipts and the timeout keyword. Original assertion criteria remain intact.

| Fresh revision2 root | Native seconds | Result |
| --- | ---: | --- |
| Sol normal |5.393219|README command exits0, exact TRIAL_OK;returned |
| Luna normal |3.323732|README command exits0, exact TRIAL_OK;returned |
| Sol deliberate15second deadline |15.016042|SIGINT,childexit1,wrapper124;failed as required |
| Luna deliberate15second deadline |15.016079|SIGINT,childexit1,wrapper124;failed as required |

Both interrupted roots started the requested60second sleep. Sol polled the same native tool session; it did not rerun the command. No completed-sleep/final-result credit is assigned. Native metadata confirms Sol/high and Luna/high with Codex0.164.0, updated from0.149.1 before any root. Source-v1's542 and source-v2's546 regulars,23 original frozen controls,8 revision2 control bindings, and all27 original regulars in each of eight targets remain unchanged. No additions/cache; a subsequent process inspection found no active trial-target processes. Endpoint equality is not proof against every transient effect.

The first four native roots remain revision1 evidence: both normal cases returned TRIAL_OK; both deliberate15second cases correctly failed at15.068seconds. APP34 independently reran all60 original-revision tests and the real fake-transport integration. The latter stopped at31.184seconds for N=1, retaining partial thread evidence and unknown remote termination. It invokes no model or real sandbox connection. It validates the unchanged host transport path; fresh revision2 model roots validate the repaired control receipt path. These are runner smoke/deadline tests, not AgentOS design, installation, first-use or comprehension qualifications.

## Evidence and limits

Retained attempts include the restricted host socket-bind failure and authorized retry, an initial NaN equality assertion error on both platforms (the runner already refused correctly), prefreeze closed-output hardening, absent cached catalog followed by a successful short-lived native model/list query, a disappearing Git maintenance lock during initial pre-admission inventory, and sbx help preferences warnings. APP34 retains one diagnosed criterion-log parser retry for the unchanged Linux socket fallback. The15 red regression failures are deliberate pre-fix evidence, not successful refusals. None is erased or used to repair participant output.

Escaped process groups, suspension and uninterruptible kernel work are outside guarantees. Snapshot preparation/evidence processing are outside command deadlines. Transport expiry does not prove remote termination; inspect exact owned processes before retry. This is not hostile-process containment or transient-write monitoring. An elapsed>N synthetic diagnostic did not drive APP34's rejection and grants no stronger scheduling guarantee. Overrides remain limited by caller authority; billing is unknown.

The original60minute budget remains cumulative; Plan2 prospectively allocates up to11 roots (9 completed before freshAPP35), peak2 andchildren0. APP35 is narrowed to1200seconds so review and delivery fit the remaining task budget. It must independently assess the exact replacement, the original rejection, meaningful adversarial tests and both native result sets. Only an approved candidate proceeds through protected PR32, expected-head merge and fetched-main verification. Both reviewers' complete indexed files, exact receipts/indexes/native metadata and recoverable filesystem metadata must appear directly in each of two verified final external archives before deleting the exact owned sandbox/rawroot. Preserve all63 original sandbox pairs. The broader onboarding goal remains active.
