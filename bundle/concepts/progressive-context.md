---
type: AgentOS Concept
title: Progressive disclosure of instruction context
description: Constrain startup material and discover detailed procedures at action time.
tags:
- agentos
- context
- progressive-disclosure
status: stable
---

# Layers

1. **Core:** constitution, authority, active role identity and safe startup rules.
2. **Assignment:** task objective, relevant role, constraints, accepted criteria and needed source revisions.
3. **Action:** procedure required for the next operation, loaded on a trigger.
4. **Optional:** examples, prior incidents and historical evidence retrieved selectively.

Indexes should describe where to go and *why*, not require recursively loading linked pages. A known path can be read directly. A Markdown link is an edge, not necessarily a required read. Keep canonical rules in one place and avoid repeating large instruction blocks per role.

See [core context](../components/context-core.md) for the required minimal implementation and [durable handoff](../components/durable-handoff.md) when context needs to survive interruptions.
