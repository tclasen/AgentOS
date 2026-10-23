---
type: AgentOS Component
title: Git and pull-request delivery qualification
description: Verify remote delivery against actual repository rules when the desired outcome includes a Git publish/merge.
tags:
- agentos
- component
- git-publication
- verified-remote-delivery
status: stable
agentos:
  selection: conditional
  when_any:
  - remote_git_delivery
  requires:
  - /components/delivery-acceptance.md
  - /components/effect-reconciliation.md
  provides:
  - git-publication
  - verified-remote-delivery
---

# Trigger

The user defines completion through commits, PRs, branch checks, remote main or another Git delivery destination.

# Follow-up interview

What repository and branch/remote are authoritative? Which PR/CI/review rules already exist? Does the user permit autonomous commit/push/merge, or only local edits? Does any existing workflow need preservation?

# Implementation

Preserve unrelated changes and protections. Treat local edits, commit, push, open PR, successful CI, merge and verified destination content as **different states**. Only require the terminal state the user actually approved. Record remote/revision/PR evidence when necessary. Reconcile lost API responses before reissuing operations; keep separate authorities for multiple repositories.

# Verification

Report a local-only change as local-only when remote delivery is required. Verify final destination state with a reliable Git/host observation if authorized; simulated merges are not live acceptance.

## Graph relationships

- Requires [Delivery Acceptance](../components/delivery-acceptance.md)
- Requires [Effect Reconciliation](../components/effect-reconciliation.md)
