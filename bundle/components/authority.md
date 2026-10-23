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

# Verification

Verify an authorized action is possible and an out-of-scope mutation is refused or escalated. Distinguish procedural instruction from technical enforcement.

## Graph relationships

None beyond the universal installer and constitutional rules.
