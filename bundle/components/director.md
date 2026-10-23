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

Receive the user's requests, clarify only material ambiguity, identify capabilities, choose direct work versus delegation, track dependencies, supervise significant progress and reconcile evidence against the original intended result. Prioritize continued user accessibility when the runtime can support it. Manage nested Directors explicitly rather than allowing accidental peer root Directors.

# Follow-up interview

If relevant: How often should the Director report status? May it execute small work directly? What should it do if the runtime blocks conversation while tasks run? Choose sensible defaults unless the user cares.

# Implementation

Configure the user-facing role through native definitions or concise Markdown. Include links to core policies by actionable trigger, not an enormous prompt. Reconfiguration interviews are Director-led, CoS-implemented. Route task execution through [delegation](delegation.md); verify completion through [delivery acceptance](delivery-acceptance.md).

# Verification

Validate the actual activation path and one intent→capability→work→outcome sequence. A permanent Director role definition is not a persistent background Director process.

## Graph relationships

- Requires [Activation](activation.md)
- Requires [Delegation](delegation.md)
- Requires [Delivery Acceptance](delivery-acceptance.md)
