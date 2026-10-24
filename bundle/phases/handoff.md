---
type: AgentOS Procedure
title: Installer-to-Director handoff
description: Conclude the temporary installer role with a usable root Director activation path.
tags:
- agentos
- phase
- handoff
status: stable
---

# Installation report

Report installed organizational home and root entrypoint, runtime integrations, permanent/initial roles, capabilities activated, user-governance boundaries, improvement/recovery mechanisms, structural and behavioral evidence, known exclusions and exact first-use instructions.

# Activation

If the runtime genuinely supports immediate transition and the user prefers it, hand off to the new root Director. Otherwise provide clear instructions to start a fresh agent session so the root `AGENTS.md` activates it. A new startup must not reactivate the temporary installer.

Keep frozen installation qualification separate from ongoing startup/readiness checks. A later explicitly authorized task may add files or advance Git state; its outputs must be checked against that task's grant, not rejected merely for differing from the original installation-only allowlist. Retain the original installation evidence and continue enforcing current scope and protected configuration.

Document the persistent side effects of manual startup, readiness and completion helpers. Before invoking one, compare its writes with the current task grant; a startup instruction, writable path or approval of a different command cannot enlarge that grant. If a helper would write outside scope, skip it and use authorized checks or report the gap. Recording a helper as "skipped" may itself write, so do not invoke it merely to record that disposition outside scope. Treat separately reviewed native-hook effects as their own explicit standing grant, not permission for other helper writes.

# Completion

Do not claim that untested features work. Do not promise ongoing background execution unless an actual authorized scheduler exists. Installed AgentOS should support future Director-led user reconfiguration and CoS-led organizational improvement without needing this installer again.
