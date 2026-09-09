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

**Deferred: an inventory-level relationship view.** A capability's Related MLEs by Dimension links, aggregated across a whole inventory, would let a reader navigate many CRDs' relationships at once instead of one CRD at a time. This should be a **generated aggregation** of links that already exist in each CRD, produced by tooling from the canonical sources (the same pattern the site's own build script uses for its other derived artifacts), not a new hand-authored dataset format — every edge in such a view already has to trace to an existing per-CRD relation, so hand-authoring a second file with its own field names and evidence shape would just create a second, driftable source of truth for the same facts. Deferred until that generator is actually designed and validated against a real multi-CRD inventory; see `proposals/2026-09-03-inventory-projection-learnings.md` for the fuller reasoning.

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

### Capability statement

A human-facing inventory MAY render a concise, source-derived sentence for each capability:

> `[actor] can [intent] so that [meaningful outcome].`

For example, canonical fields:

```text
Actor: AI Twin owner
Command / intent: Submit a public article URL and approve its draft
Meaningful outcome: A reviewed web-page draft is approved as AI Twin Knowledge.
```

project to:

> An AI Twin owner can submit a public article URL and approve its draft **so that a reviewed web-page draft is approved as AI Twin Knowledge.**

This is an audience projection (§7.2), not a new CRD field and not a replacement for `capability purpose`, `meaningful outcome`, or the Interaction Contract MLE. Capability purpose alone often answers *why* but not clearly *who does what and to what end*; the statement makes a large inventory more scannable without duplicating requirements.

**The guardrail gates on semantic class, not on presence.** Generate the sentence only when actor, intent, and meaningful outcome are each stated as `explicit fact` — not merely "known." A `reasonable inference`, a hedged statement ("preferably," "should"), or `unknown/unresolved` component must fall back to rendering the canonical `capability purpose`, exactly the same as a genuinely missing one. A sentence assembled from inferred or hedged fields reads with the same confident, quotable fluency as one assembled from fact — an inventory reader has no way to tell the difference from the sentence alone, so the check has to happen before rendering, not after. The outcome clause may be visually emphasized in a projection; that styling is not semantic priority and does not make the projection normative. The canonical CRD remains the authority if the sentence is abbreviated or awkward.

### Responsive human-facing projection guidance

These are useful defaults for HTML/showcase template authors, not specification requirements — individual products may use their own visual system:

- Put identity/status/evidence metadata in a compact header; don't repeat it unchanged in the body.
- Render labelled fields as label/value rows or cards, not long undifferentiated bullet lists.
- Use selective emphasis for `capability purpose`, `meaningful outcome`, `result`, `rules/invariants`, and `required meaning`; don't bold every value.
- Preserve semantic classes visibly, especially for examples, recommendations, implementation choices, and unknowns.
- An evidence/provenance table may use Statement/Class/Source columns on wide screens; on narrow screens, convert each row into a labelled card or equivalent stacked representation rather than requiring horizontal scroll or clipping text — don't remove `Class` or `Source` on mobile, provenance is part of the meaning, not decoration.
- An inventory may use a compact table on wide screens and one capability card per row on narrow screens; avoid using color or typography alone to distinguish evidence maturity or status.

See `~/.claude/skills/crd-author/reference/inventory-html-template.html` and `crd-html-template.html` for where these apply in the bundled templates.
