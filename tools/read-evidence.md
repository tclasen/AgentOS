# Reviewing full-source delivery evidence

This is an optional manual protocol for **prospective** qualification trials. It assesses whether a complete, approved source body reached the assigned model context at the required time. It does not infer comprehension, successful installation, an individual command's exit status, or permission to act.

The source obligation remains the [graph-routing checklist](../bundle/core/graph-routing.md): read every selected contract and prerequisite in full before proposing an installation, and load the applicable current context before writes. A hash, path list, proposed capability or batch command's intent does not satisfy it. Bind the actual proposal and selected closure first; the [selection verifier](README.md) checks structural completeness but cannot authenticate a list or resolve semantic gaps.

## Keep measurements and decisions distinct

`full_component_reads_observed` keeps its existing successful-command-only definition. `source_content_exposures` locates exact complete text in a completed command output, including failed aggregates. Neither field automatically approves a read, proposal or installation. Preserve both original measurements, raw failures and all historical verdicts.

A new trial may preregister this protocol only after its evaluator change has received independent review against the original source requirement and adversarial cases. Record the protocol revision and source/evaluator identities before results. Do not switch rules during a frozen trial, rewrite an older failure, or use a candidate's improved score to approve its own evaluator. Missing evidence stays unestablished; acquire a fresh complete read under the authorized trial rules instead of reconstructing one from claims.

## Required evidence for each source

The responsible reviewer checks all of the following against retained primary evidence, not an agent's summary. Record the result and the evidence location for each condition.

1. **Approved source identity.** Bind the exact bundle-relative path and full nonempty canonical UTF-8 body to the approved whole-source identity, including SHA-256 and byte length. The source actually read must be that approved source. Another unbound location containing the same text is insufficient. An explicitly approved relocation with verified identity can establish a new binding before use; do not invent it afterward.
2. **Source stability and read provenance.** Establish that the bound source remained the applicable bytes during execution, for example through a controlled read-only mount and retained identity checks. Inspect the actual command and environment evidence to identify a real read of that source. This protocol's narrow compound-command allowance covers a plain identifiable read such as `cat` followed by known unrelated read-only probes. A dynamic path with unresolved expansion, substituted executable/function, reconstructed literal, uncertain environment, or unknown stability is insufficient. Before/after hashes alone are not a continuous race monitor.
3. **Trusted completed output.** Correlate the primary tool record with the assigned native session, item and current context. Require a completed command-execution event, its actual command and output, and the **entire exact canonical body in one untruncated output**. Do not join fragments, discard missing suffixes, infer completion from a started event, or accept an agent message as a tool read. An explicit transport truncation/ambiguity flag makes this bounded protocol inconclusive even if a body appears complete. Preserve command/output hashes, item ID and event position; a containment locator is only an aid.
4. **Correct ordering and context.** Establish that the completed output was available before the proposal that relies on it and before the first actual mutation requiring it, including shell writes and transient effects. Another session's read is not automatically this session's context. An admitted context transfer needs its own identity, completeness and ordering evidence; otherwise load the source again. A late read cannot repair an earlier proposal/write retrospectively.
5. **Separate statuses and obligations.** Retain the aggregate status/exit code, any independently observed source-command status, and any unknown individual status separately. Review every actual selected source and its duties, source-identity continuity, authority, effects, limitations and qualification independently. Per-source delivery is only one prerequisite; it grants no approval or automatic admission.

If all five conditions are established, record **full-source delivery established**, with the narrow scope and remaining gates. If any condition is missing, contradicted or ambiguous, record **not established**, identify why, and keep dependent admission closed. This is an evidence finding, not an assertion that the model did or did not understand the text.

## A failed later probe does not erase returned text

For a controlled read of a pinned source, a completed command such as:

```sh
cat /approved/bundle/phases/design.md; ls /approved/bundle/optional-missing-directory
```

can return the complete canonical design body and then fail on the unrelated missing directory. With all required identity, provenance, completeness, stability, context and ordering evidence above, full-source delivery can be established. The aggregate failure remains a failure. The earlier `cat` exit remains **unknown** unless separately observed; semicolon continuation does not prove exit zero. Record the individual code as unknown rather than calling the whole command successful.

This differs from `printf` printing a copied body, a read of an unapproved copy, or a command whose source path/provenance is unresolved. Exact text containment alone does not establish the required read operation. Conversely, a zero aggregate exit is not sufficient: it can conceal failed earlier commands or contain literal text instead of a source read. Unknown side effects or unresolved semantic duties continue to block admission even when per-source delivery is established.

## Retained decision record

Keep the protocol version, trial/phase and assigned session; actual proposal/selection and approved source identity; each source path/hash/length; primary event/item and command/output hashes; provenance/stability observations; before-proposal/before-write ordering; aggregate exit and source-specific exit or `unknown`; the five condition findings; reviewer identity; and remaining semantic/effect/approval gates. Retain failed commands and both original helper measurements beside the manual finding.

Controlled evidence fixtures can test these distinctions, but label them as simulations. Their supplied premises do not prove a real onboarding read. Fresh native evidence is required for real trial admission. This procedure supplies no automatic shell parser, log authentication or enforcement mechanism; its limitations must remain explicit in the trial plan and final report.
