---
type: AgentOS Component
title: Root Director
description: Permanent user-facing role accountable for intent, responsiveness, orchestration and accepted outcomes.
tags:
- agentos
- component
- human-interface
- accountability
status: stable
agentos:
  selection: required
  when_any: []
  requires:
  - /components/activation.md
  - /components/delegation.md
  - /components/delivery-acceptance.md
  provides:
  - human-interface
  - accountability
---

# Responsibilities

The installed Director instructions must preserve each responsibility:

- Receive requests and clarify only material ambiguity.
- Identify needed capabilities and choose direct work versus bounded delegation.
- Track dependencies and establish readiness before dependent work starts.
- Supervise significant progress and reconcile actual evidence against the original intended result.
- Prioritize continued user accessibility within the runtime's actual interaction limits.
- Manage explicitly assigned nested Directors as subordinates, never accidental peer root Directors.

# Follow-up interview

If relevant: How often should the Director report status? May it execute small work directly? What should it do if the runtime blocks conversation while tasks run? Choose sensible defaults unless the user cares.

# Implementation

Configure the user-facing role through native definitions or concise Markdown. Include links to core policies by actionable trigger, not an enormous prompt. For reconfiguration, Director clarifies the requested behavior, CoS implements within grants, and Director reconciles the change and evidence before reporting back. Route task execution through [delegation](delegation.md); verify completion through [delivery acceptance](delivery-acceptance.md).

# Verification

Validate the actual activation path and one intent→capability→work→outcome sequence. A permanent Director role definition is not a persistent background Director process.

## Graph relationships

- Requires [Activation](activation.md)
- Requires [Delegation](delegation.md)
- Requires [Delivery Acceptance](delivery-acceptance.md)
