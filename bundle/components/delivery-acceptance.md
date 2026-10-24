---
type: AgentOS Component
title: Outcome verification and user delivery
description: Distinguish worker completion, verified outputs, actual delivery, and user satisfaction.
tags:
- agentos
- component
- outcome-accountability
- verification
status: stable
agentos:
  selection: required
  when_any: []
  requires:
  - /components/authority.md
  provides:
  - outcome-accountability
  - verification
---

# Operational contract

The Director reconciles the original user intent with actual outputs and available evidence. Separate attempted, produced, reviewed, delivered and accepted work as needed. A local artifact, passing test, agent statement or open pull request must not silently substitute for the user's actual required outcome.

Preserve explicit execution requirements as well as output requirements. When the user requires an existing tool, function, input source or transformation, use it to produce the requested result and verify that the delivered artifact derives from that execution. A hand-constructed expected answer can have correct bytes while bypassing the requested method; running the method separately in a test does not establish the artifact's derivation. Suppress incidental writes on the actual invocation while preserving its required work. If the method cannot run within the grant or runtime, report that specific gap rather than silently replacing it. When only the outcome is specified, choose a suitable implementation without inventing extra method constraints.

# Follow-up interview

What does delivery mean for this repository—usable local edits, a published report, a merged remote change, a completed external action or user sign-off? What level of independent review is appropriate? Adapt the answer to the domain and risk.

# Implementation

Establish proportionate acceptance criteria, final-response reconciliation and truthful blocked/unverified reporting. Use [Git delivery](git-delivery.md) only if remote Git delivery is needed and [independent evaluation](independent-evaluation.md) only when it improves assurance.

# Verification

Test both a genuinely completed outcome and an apparently completed but undelivered/invalid outcome; the latter must not be falsely accepted.

Include a case where correct artifact bytes were supplied without the explicitly requested method. Inspect the actual invocation, input and result-to-artifact path before accepting that requirement; distinguish it from independent tests of the method.

## Graph relationships

- Requires [Authority](authority.md)
- Consider [Git Delivery](git-delivery.md) when applicable.
- Consider [Independent Evaluation](independent-evaluation.md) when applicable.
