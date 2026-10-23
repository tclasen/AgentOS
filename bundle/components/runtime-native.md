---
type: AgentOS Component
title: Native agent runtime integration
description: Integrate supported native role definitions, skills, hooks or structured policies when useful.
tags:
- agentos
- component
- native-runtime-adapter
status: stable
agentos:
  selection: conditional
  when_any:
  - native_agents
  - runtime_specific_integration
  requires:
  - /components/activation.md
  provides:
  - native-runtime-adapter
---

# Trigger

Native role configuration, skills, hooks, identity, sandboxing or telemetry would improve requested behavior, or the user explicitly prioritizes runtime specialization.

# Follow-up interview

Which runtime version and integration depth should be supported? Does the user want portable Markdown fallback? Which native files are permitted outside the compact AgentOS home? Do not ask about details the environment can verify.

# Implementation

Inspect current official/local runtime specifications; choose actual supported paths and structured formats, obtain permission for extra repository footprint, and avoid globally overriding existing config. Maintain one canonical source of truth or explicit sync rules. Preserve portable root entrypoint.

# Verification

Parse native configuration and exercise representative activation/delegation in the actual installed runtime where available. Advertising a feature is not exercise evidence.

## Graph relationships

- Requires [Activation](../components/activation.md)
