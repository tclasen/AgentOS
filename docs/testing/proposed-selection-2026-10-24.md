# Verify the actual proposed selection

The recommended change adds `verify-selection` to the optional local qualification helper. A previous native trial exposed an approval helper that assumed 11 components even though Luna proposed 12. Planning a closure and verifying an existing proposal are different operations: filling omissions can conceal a defective proposal, and a preset cannot stand in for the actual selected set.

The new command reads a JSON list from file or stdin, preserves the declared set, and reports required/dependency omissions without repairing it. Exit 0 means structural completeness; 1 means omissions; 2 means invalid input or selected graph. The README requires correlation with the actual proposal and review of every selected duty, contradictory deferral, requirement and applicable approval. Both valid 11- and 12-component proposals may pass. A complete preset does not authenticate a different proposal.

Candidate `1d7e19de95ab4e98aaa20f6a78d1c5ba8221df37` changes only the helper, its documentation and tests, plus project records. All bundle bytes and existing successful-read/exposure functions remain unchanged. All prior 44 regression tests remain intact; five new tests bring the suite to 49 passing in 13.944 seconds. They cover exact 12-versus-11 selection, omissions and transitive prerequisites, malformed/duplicate/noncanonical inputs, selected/deprecated/cyclic/broken graphs, unrelated optional branches, file/stdin exits and read-only preservation. Graph profiles remain 10/22/18 across 25 components.

## Native evaluator-use results

Codex was updated from 0.149.1 to 0.164.0 inside one owned Docker sandbox before either trial. Native metadata independently confirms Luna/high and Sol/high. These are six-case evaluator-use trials, not onboarding or installation trials.

| Case | Actual result on both models | Semantic assessment |
| --- | --- | --- |
| A: complete 12, supplied preset 11 | 0 / complete | Both reject substituting the preset and identify independence limitations in the selected extra contract. Sol additionally executes the preset and observes that it also passes structurally. |
| B: missing Director | 1 / incomplete | Both identify the required component omission. |
| C: parallel coordination without Work Ledger | 1 / incomplete | Both identify the missing prerequisite and discuss its operating duties. |
| D: complete 11 | 0 / complete | Both preserve structural success without granting installation/read/authority credit. |
| E: duplicated Activation | 2 / invalid | Both retain the rejection without deduplicating or retrying. |
| F: Independent Evaluation selected and deferred | 0 / complete | Both flag the contradiction and withhold acceptance despite structural completeness. |

Luna finished in 41.715180 seconds; Sol in 80.284408. Parent inspected all eight Luna and nineteen Sol command bodies and parsed actual CLI outputs against the fixed expected cases. Both read the helper documentation and full relevant component contracts. Source/control and target/Git inventories remain unchanged. Python execution suppresses bytecode. There were no target imports/tests/writes, child contexts, external actions or semantic retries. Luna's aggregate command returns zero while retaining all individual exits and stderr; Sol has three expected nonzero outer commands. These observations do not erase failed commands or infer unknown earlier exits.

A's supplied mechanism does not establish protected evaluation duties or independence sufficient for acceptance. The observed withholding of approval is not a general finding that every disclosed same-context limitation is forbidden. This task neither implements nor evaluates an installed Independent Evaluation mechanism. Prior approval and author-source-read evidence were absent for all fictional proposals; evaluator reads do not retroactively supply either.

Known raw two-root usage totals: input 257779, cached input 202496, output 6271, reasoning output 2685, cache-write input 0. These are raw counters, not full-task billing or monetary cost. Peak native trial roots was two, children zero. Independent review is separately accounted.

One pre-freeze fixture-preparation assertion caught a guessed Director path before writing case files; it was corrected from the actual graph and all six expected exits verified before freeze. Restricted sandbox help emitted harmless macOS preference access diagnostics. Both are retained in evidence; no frozen candidate or native case was repaired.

## Disposition and limits

Recommend accepting the bounded verifier after fresh independent APP-000023 review and normal protected delivery. It is not an automatic approval engine and cannot detect a deliberately substituted input without proposal correlation. Existing `select` planning remains available. No bundle instructions, source-success rule or historical verdict changes. A separate prospective assessment is still needed for the compound-command source-read evidence issue; this helper does not resolve it. Both-model/all-designed-path onboarding remains an active goal.

Raw native outputs, frozen candidate/inputs, local results, metadata and inventories are retained in indexed archives outside the owned sandbox before exact cleanup. Archive identities, independent review, remote delivery and cleanup are subsequent observations; they are not claimed completed here.
