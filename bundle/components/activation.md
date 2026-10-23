---
type: AgentOS Component
title: Role-aware root activation
description: Activate the root Director for unassigned user sessions while preserving delegated worker identities.
tags:
- agentos
- component
- director-activation
- role-identity
status: stable
agentos:
  selection: required
  when_any: []
  requires:
  - /components/authority.md
  - /components/context-core.md
  provides:
  - director-activation
  - role-identity
---

# Operational contract

The repository-root `AGENTS.md` is a thin portable bridge to the installed organization. An unassigned interactive session activates the root Director; a delegated worker retains its assigned identity/context/task even if the root file is loaded. The temporary installer ceases to be active after handoff. Nested Directors are only explicit child assignments.

# Follow-up interview

If not discovered: Does the chosen runtime automatically read root `AGENTS.md`? Which native role definitions or instruction paths are supported? Is portability or deep native integration preferred?

# Implementation

Keep `AGENTS.md` short and merge with existing content. Prefer runtime-native role configuration when possible. Avoid global instruction overrides that unexpectedly replace existing rules. If the runtime cannot enforce exclusive user-facing communication, disclose the actual behavior and configure the user's chosen fallback.

# Verification

When supported, test both fresh unassigned user session and fresh explicitly delegated worker. A successful root read alone does not prove correct role identity.

## Graph relationships

- Requires [Authority](authority.md)
- Requires [Context Core](context-core.md)
- Consider [Runtime Native](runtime-native.md) when applicable.
- Consider [Brownfield Migration](brownfield-migration.md) when applicable.
