# Working with CRDs

This guide explains four practical parts of CRD use that should remain visible without enlarging the required core: decision precedence, shared-element reuse, audience projections, and why a CRD is not simply a feature specification, PRD, API document, or skill.

## Decision precedence

When guidance conflicts, resolve it in this order:

```text
1. Rule / invariant
2. Explicit implementation requirement
3. Explicit owner or user choice
4. Recommended default
5. Agent judgment
```

For example, an agent may use judgment to choose how to summarize a discrepancy, but it cannot use judgment to bypass a reconciliation invariant. If two same-level requirements conflict, preserve the conflict as `unknown/unresolved` and ask for a decision.

## Shared elements and approved reuse

Reusable code and tools are not automatically reusable capability meaning. A shared element can retain assumptions from the capability it was first created for. Record that relationship where it matters:

```text
shared element: customer-identity-validation
created for: customer-onboarding
approved reuse: [request-moving-quote, submit-insurance-claim]
```

This enables safe reuse without claiming exclusive ownership. It is useful for tools, prompts, components, schemas, workflows, and tests that are reused across capability boundaries.

## Capability, skill, and tool

| Concept | Meaning | Typical relationship |
|---|---|---|
| Capability MLE | Complete contextual ability that produces an outcome. | Defined by one CRD. |
| Skill | Agentic realization package: instructions, context, tools, and workflow. | May realize one Capability MLE or bundle several. |
| Tool | Executable primitive: API operation, MCP tool, function, command, or workflow step. | May support many skills and capabilities. |

The relationship is many-to-many. A skill is not automatically a capability, and a tool is not automatically a skill. A capability can be the MLE of a skill when the skill has one coherent outcome; otherwise the skill should map to several CRDs.

## Related MLEs by Dimension

A CRD may optionally trace itself to lower-level, discipline-specific MLEs — Business/Domain, UX/Experience, Communication, Interaction/Behaviour, Frontend/Interface, Backend/Execution, Data/Information, API/Interoperability, Agentic, Verification, Operations — using relationship types `defines`, `implements`, `supports`, `constrains`, `verifies`, `exposes`, or `reused_by` (full model: `crd-specification.md` §7.4). This is traceability, not coverage: never fill a dimension that has no genuine content just to appear complete, exactly as with every other optional CRD section.

**Communication** is deliberately first-class here rather than filed under UX, because a message's meaning is usually shaped by business rules, rendered by frontend or delivery infrastructure, and localized independently — no single discipline owns it. A Communication MLE separates canonical meaning from its channel realization and its language realization, so the same intended meaning stays consistent across a toast, an email, a push notification, and a translation of any of those. Every Communication MLE includes representative example text so readers can test whether the canonical meaning is concrete; it is always classed as an `example`, using sourced wording when available or clearly labelled illustrative wording when it is not.

One capability-owned Communication MLE and one product-wide Source Context Reference are complementary, not competing: the message itself (its trigger, audience, and required meaning) belongs to the capability that produces it, while a cross-cutting terminology or tone convention that many messages should follow belongs in SCR if the product already has one. See the worked trial in [Reconcile payments](examples/reconcile-payments.md), which resolves this exact question with a concrete example.

## Why a CRD is not merely a feature or existing artifact

Existing artifacts remain useful, but each answers only part of the capability question:

| Artifact | Useful for | What it does not establish alone |
|---|---|---|
| PRD | Product/application rationale and scope. | A reusable, independently bounded capability. |
| User story | A human actor's desired outcome. | Domain rules, state transitions, machine contracts, and realization independence. |
| UI screen or Storybook component | An interface representation. | The complete capability purpose, policies, effects, and non-UI use. |
| API/OpenAPI/GraphQL module | Technical interface and data contract. | Whether technical operations together form one meaningful capability. |
| Skill | Agentic realization and instructions. | Whether the skill bundles one or multiple Capability MLEs. |
| MCP tool | Executable interface for an agent. | The product/domain purpose, boundaries, and approved use context. |

“Feature” is often a useful informal word, but its boundary is typically negotiated case by case. A CRD makes the boundary explicit through purpose, meaningful outcome, included/excluded concerns, interaction contracts, rules, defaults, and unknowns.

## Audience projections

One canonical CRD can be projected for different readers without duplicating or diverging its requirements:

| Projection | Questions it should answer |
|---|---|
| Business/domain | Why does this capability exist? What outcome, rule, and rationale matter? |
| UX | Who acts? What choices, states, and outcomes must be understandable? |
| Frontend | What representations and interaction constraints are needed? |
| Backend | What state transitions, invariants, effects, and dependencies must hold? |
| API/MCP/tools | What commands, contracts, inputs, outputs, and authority bounds exist? |
| Agent | What authority, grounding, precedence, approval, and escalation rules apply? |
| Operations | Which realization is active? How is it observed, constrained, recovered, and retired? |

The projection is a view of the CRD, not a new source of truth. It must trace back to the canonical document.
