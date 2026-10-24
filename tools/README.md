# Local qualification helpers

`qualification.py` records bounded Codex trials in an operator-created disposable Git workspace. It does not install Docker, authenticate Codex, create fixtures, grant external authority, or decide whether model output satisfies a contract. A returned run means the CLI completed; it is **not a passing grade**.

Use Python 3.9 or later, `sbx`, and an updated/authenticated sandbox Codex. Mount the selected AgentOS source and fixed prompts read-only, and a dedicated fixture workspace writable. Inventory existing sandboxes first. Use normal Codex sandbox restrictions and only task-owned writable directories. The caller must supply fixture-specific grants, immutable expected outcomes, before-state preservation, and independent checks.

```sh
python3 tools/qualification.py graph bundle
python3 tools/qualification.py select bundle --component components/git-delivery.md
python3 tools/qualification.py snapshot /path/to/fixture /path/to/baseline.json
python3 tools/qualification.py run \
  --target /path/to/work/fixture --workspace /path/to/work \
  --sandbox owned-sandbox --source /path/to/AgentOS \
  --output /path/to/evidence --name unique-attempt-name --task TASK-000178 \
  --prompt /path/to/read-only-prompt.txt --model gpt-6-luna --agents 0
```

`--agents` caps subordinate contexts for the trial; operators must also account for descendants and simultaneous trials. `--strict-config` exercises the actual Codex parser. `--resume` requires an observed native thread ID. `--add-dir` grants an additional existing directory inside the declared disposable workspace; keep it as narrow as the test destination. This directory's path delta is recorded separately. Existing evidence names cannot be reused. Failed or inconclusive trials need a separately named retry with a recorded diagnosis; never overwrite them.

`--task` is required: replace the example with the owning task's `TASK-NNNNNN` identifier. It is recorded verbatim after format validation, before any run starts. This fixes the earlier hard-coded task label; callers must add the flag when upgrading. The identifier attributes evidence; it does not verify that a task exists or grants authority. Historical manifests retain their original labels and need explicit external reconciliation if misattributed.

The manifest records source hashes, prompts, before and after snapshots/deltas for both target and additional scopes, CLI events, reported native thread IDs and available usage. Retained after hashes allow later artifact mutation to be detected; they do not make the files immutable. Read-credit is conservative: only complete source text in successful completed command output is credited; truncation is inconclusive. Actual child model identity and monetary cost remain unknown unless independently observed. Graph parsing supports this repository's small metadata profile, not arbitrary YAML. Snapshots omit Git internals and Python caches and record symlinks without following them; inspect Git status/index/history independently.

Snapshots include every observed regular subdirectory, even empty ones, as `{"directory": true}`. File entries retain `sha256`/`bytes`; links retain `symlink`. Consumers must distinguish these entry types. Deltas can now expose empty-directory additions/removals and changes between files, directories and links. The root itself, `.git`, `__pycache__` and `.pytest_cache` directory trees, permissions and timestamps are excluded. Earlier snapshots did not record regular directories; do not treat comparison across formats as evidence of newly created directories. These are point-in-time observations, not a race-safe filesystem monitor.

`select` is an optional read-only planning aid. With no `--component` arguments it selects all required components and their dependencies; repeat the flag to add requested optional components. It reports the selected closure and source hashes, and rejects unknown or deprecated selected components, including deprecated transitive prerequisites. An unrelated deprecated optional component is not selected. The command does not infer user requirements, prove full-source reads, validate an installed organization or grant authority. Manual traversal remains supported when Python or a local checkout is unavailable; no helper needs to be installed into the target project.

`select` checks hard-dependency existence and cycles within the required/requested closure. A well-formed optional branch with a missing or escaping dependency, or a cycle, does not block a selection that never reaches it; selecting or depending on that branch still fails. Supported structural metadata, source-file boundaries and the required catalog are checked across the bundle, so malformed metadata still blocks selection. Use `graph` for a full-bundle audit: it continues to reject broken dependency edges and cycles even in unselected branches.

`qualification-matrix.json` fixes source-derived component criteria for both model names and three installation profiles. It is a coverage plan, not a result. See the qualification reports under `docs/testing/` for observed outcomes and limitations.

Within this small profile, a top-level `status` value may be a plain, single-quoted or double-quoted word, with an optional trailing comment. Duplicate or unsupported declared status syntax is rejected; an absent status remains unspecified. This is a bounded scalar parser, not a general YAML loader.

An `agentos` block must contain exactly one two-space-indented `selection` field (plain `required` or `conditional`) and one `requires` field. Dependencies use `requires: []` or a block list with two-space-indented dashes and unquoted paths containing letters, digits, `_`, `.`, `/` or `-`. Blank lines, standalone comments and trailing whitespace in that list do not truncate it. Unsupported list forms, duplicate declarations, null/missing fields and unterminated frontmatter are refused instead of silently omitting dependencies. Fields from another top-level mapping cannot supply missing AgentOS fields. Normalize unsupported metadata to this profile or use an appropriately validated manual traversal; the helper does not implement arbitrary YAML.

`local_effect_fixture.py` is a local SQLite test destination. A dropped acknowledgment commits a receipt but returns failure; offline attempts remain unknown. All attempt calls are journaled so a duplicate retry cannot be hidden by an idempotent receipt. It establishes no third-party guarantee. Give its exact disposable directory to the worker because lookups also append their call journal.

Available `lookup` responses include `observed_payload_sha256`, the digest of the committed payload for that identity. It is `null` for absent or unavailable observations, including an offline lookup of an existing receipt. Compare it with the intended candidate before accepting delivery; `present` alone is not a match. A mismatch is a conflict to reconcile, not permission to overwrite or retry. The fixture returns no raw payload, and its local digest is not proof about any real provider.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Keep raw CLI logs and fixture data out of public commits. Export and verify a bounded evidence archive before removing only the task-owned sandbox and fixtures. Never globally prune someone else's sandboxes, images, volumes, or Docker state.
