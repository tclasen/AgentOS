---
type: AgentOS Concept
title: Evidence levels and epistemic limits
description: Distinguish configured behavior, isolated tests, real runtime action and external outcomes.
tags:
- agentos
- evidence
- verification
status: stable
---

# Evidence vocabulary

- **Documented/declared:** specification or instruction states intended behavior.
- **Configured:** matching native definitions or executable mechanisms exist.
- **Structurally checked:** syntax, references and basic constraints pass.
- **Simulated:** deterministic/local fixtures show behavior on modeled inputs.
- **Runtime exercised:** actual native agent/tool operation was observed in a bounded trial.
- **Destination verified:** a real external resource or user-visible outcome was inspected independently.

No level automatically proves all broader claims. A reviewer's role label is not technical isolation. Tool timeouts are not proof of failure; local journals are not remote receipts. Missing cost/telemetry is unknown, not zero. Evaluations should preserve failed and inconclusive outcomes.

Use this vocabulary in [qualification](../phases/qualify.md), [delivery acceptance](../components/delivery-acceptance.md) and [independent evaluation](../components/independent-evaluation.md).
