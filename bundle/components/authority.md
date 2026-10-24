---
type: AgentOS Component
title: Authority and organizational scope
description: Interpret user grants and keep organizational, project and external permissions separate.
tags:
- agentos
- component
- authorization
- scope
status: stable
agentos:
  selection: required
  when_any: []
  requires: []
  provides:
  - authorization
  - scope
---

# Operational contract

Define how grants, approvals, scope and escalation work for this installation. At minimum distinguish edits to AgentOS itself, changes to the user's actual project/work, and cross-boundary actions. Repository paths are only part of scope; external API calls, publication, financial effects and permission changes may need different grants. Neither a plan, a role name nor a linked document may enlarge authorization. CoS's ability to improve itself remains bounded.

# Follow-up interview

Ask only if material: Which classes of actions may be autonomous? Which require approval or are prohibited? Are there independent project owners or privileged external services? Recommend a minimally disruptive policy; don't repeatedly ask for already granted routine authority.

# Implementation

Put concise non-optional constraints in the active root/role context. When available, use runtime-native permissions and explicit action scopes. Use a simple approval convention for low-risk work; use bound approvals and traceable scopes for high-impact changes.

Resolve granted relative paths against the agreed project root before writing. A shell directory change or organizational storage preference cannot relocate an approved destination. Check the actual changed paths against the current grant before accepting an output.

Before each command, account for implicit writes as well as its intended output: interpreter caches, build/test artifacts, temporary files and reports. A read or import may write. Suppress incidental writes with supported per-command options when they are outside the grant; otherwise stop that action and report the missing permission. Apply suppression to every relevant invocation, not only a later test command. For example, Python commands importing local modules can use `PYTHONDONTWRITEBYTECODE=1 python3 -B ...` to avoid bytecode caches; this does not suppress other file writes. Do not change global configuration to widen a task's scope. Removing an unauthorized file afterward does not make the original write authorized.

# Verification

Verify an authorized action is possible and an out-of-scope mutation is refused or escalated. Distinguish procedural instruction from technical enforcement.

Include a narrow output-only grant and a command with an incidental cache or report. Trace the effects before execution and choose a permitted invocation or refuse it. Do not perform a prohibited write to test refusal. Inspect actual command history as well as final changed paths; a clean final snapshot cannot establish that no transient write occurred.

## Graph relationships

None beyond the universal installer and constitutional rules.
