---
type: AgentOS Component
title: Canonical record and sensitive data ownership
description: Keep organizational governance, project products, telemetry and private data under their proper owners.
tags:
- agentos
- component
- data-ownership
- privacy-boundaries
status: stable
agentos:
  selection: conditional
  when_any:
  - sensitive_data
  - multiple_repositories
  - public_repository
  requires:
  - /components/authority.md
  provides:
  - data-ownership
  - privacy-boundaries
---

# Trigger

Sensitive information, multi-project scope, separate authorities, cross-repository records, or installation privacy requirements.

# Follow-up interview

Which records may live in the organization's repository? Which belong to other projects or external systems? Are any outputs public? What historical data/credentials require retention limits or exclusion?

# Implementation

Do not centralize private project evidence in a public organizational repository. Preserve authoritative project-specific records with their owners and use minimal organizational pointers. Consider that removing files from a Git tree does not remove published history. Define consistent access/retention and sensitive redaction policies.

# Verification

Inspect a sample cross-boundary record flow; no unintended private content should enter organizational or published artifacts.

## Graph relationships

- Requires [Authority](authority.md)
