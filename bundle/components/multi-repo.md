---
type: AgentOS Component
title: Multi-repository/project enrollment
description: Coordinate projects with independent source authority, histories and acceptance criteria.
tags:
- agentos
- component
- portfolio-routing
- cross-repository-control
status: stable
agentos:
  selection: conditional
  when_any:
  - multiple_repositories
  - portfolio_management
  requires:
  - /components/information-boundaries.md
  - /components/authority.md
  provides:
  - portfolio-routing
  - cross-repository-control
---

# Trigger

AgentOS is intended to manage more than one Git repository or externally owned project system.

# Follow-up interview

Which projects are in scope and who owns them? Are all actually enrolled now or merely candidates? Can AgentOS write across repositories? What is each project's canonical task and acceptance source?

# Implementation

Use minimal project profiles/pointers and independent grants. Do not assume the organization's repo authorizes product repo changes. Decompose cross-boundary work into separately governed obligations; avoid accidentally staging nested repos or pushing private records into the wrong Git history.

# Verification

Test correct routing to distinct owners and an unauthorized-project refusal. Confirm organization changes do not silently modify project source.

## Graph relationships

- Requires [Information Boundaries](../components/information-boundaries.md)
- Requires [Authority](../components/authority.md)
