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

# Completion

Do not claim that untested features work. Do not promise ongoing background execution unless an actual authorized scheduler exists. Installed AgentOS should support future Director-led user reconfiguration and CoS-led organizational improvement without needing this installer again.
