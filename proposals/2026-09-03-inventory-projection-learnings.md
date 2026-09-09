# Proposal: Inventory projection and cross-source extraction learnings

**Status:** reviewed and resolved, 2026-09-09.  
**Date:** September 3, 2026.  
**Evidence base:** a Prifina Individuals pilot comprising three initially validated AI Twin CRDs, seven further cross-source Knowledge CRDs, a canonical ten-node relationship dataset, and an authenticated human-facing inventory projection.

## Review outcome (2026-09-09)

Independently reviewed via a 3-lens audit (factual accuracy, evidence-base verification, design-quality/redundancy), each a fresh non-fork agent, per [[audit-principles]]. The evidence base was independently verified against real local artifacts (`~/Code/crds-for-individuals`, `~/Code/prifina-capability-hub`) and checks out in exact detail — this is not an unsubstantiated claim. The proposal's factual claims about repo state (§Purpose's "already incorporated separately," §1's "no core change") were all confirmed accurate. Two issues were found and are fixed below; one issue is a resolution/deferral, not an implementation.

| Recommendation | Outcome |
|---|---|
| 1. Capability statement projection | **Adopted with a fix.** The original guardrail gated on field *presence* ("established" vs. "unknown"), which would let a sentence assembled entirely from `reasonable inference` or hedged fields render with the same confident fluency as one built from `explicit fact` — a false-completeness risk. Fixed to gate on *semantic class*: render only when actor, intent, and outcome are each `explicit fact`; otherwise fall back to the canonical purpose. Shipped in `crd-specification.md` §7.2, `working-with-crds.md`, and the CRD Author skill. |
| 2. Full-detail applicability pass | **Adopted by merging**, not as a new mechanism. It substantially restated rules already in `agent-transformation-instructions.md` (provenance, §6.1 shared-element handling, execution mode "when known," rules 10-11 on unresolved API/production claims). Its one real contribution — naming this a discrete, required per-CRD pass — is now a named step inside the existing step 7 ("Produce and validate the document"), not a separate section. |
| 3. Source-role/limitation matrix | **Adopted, expanded.** The original 5-row table omitted source types the framework already names as canonical (`agent-transformation-instructions.md`'s source list): database schemas, tests/operational runbooks, user stories/interviews, and live running service responses. Added those four rows before shipping into `agent-transformation-instructions.md` step 1 and `source-context-template.md`. |
| 4. Capability Relationship Dataset | **Deferred and reframed — not implemented as proposed.** Every edge in the proposed dataset already has to trace to an existing per-CRD "Related MLEs by Dimension" relation, making this a *generated aggregation* of data that already exists, not new source data needing its own hand-authored format. Its JSON example also used field names inconsistent with existing schema conventions (`type` instead of the schema's `relationship`, a flat `evidence` string instead of the schema's structured `statement` object, `CAP-01`-style ids with no precedent anywhere in this repo). Recorded as a deferred resolution in `working-with-crds.md` ("Deferred: an inventory-level relationship view") — build a generator from existing links when actually needed, don't hand-author a second dataset. |
| 5. Responsive human-facing projection guidance | **Adopted as-is.** No conflict with existing HTML template guidance. Added to `working-with-crds.md`. |
| 6. Mermaid — no change | **Confirmed, no action.** Reviewed; the existing rule already covers this correctly. |

**One correction to this proposal's own text:** §"Suggested adoption sequence" step 4 (below) implied that gating schema changes behind "at least two independent inventories" continues established practice. It does not — the framework's most recent prior schema change (Related MLEs by Dimension, commit `e89867f`, 2026-09-01) landed in the *same commit* as its *first* single-example trial, with blind-auditing done afterward, not before. This proposal's threshold is a **new, stricter** bar being adopted going forward for schema changes specifically — Recommendation 4's deferral is its first application — not a continuation of precedent. Treat it as such rather than as a description of how this framework has actually operated.

**Answers to this proposal's four review questions**, based on what shipped:

1. *Specification's audience-projection section, or only `working-with-crds.md` and the skill?* Both — a short normative mention in `crd-specification.md` §7.2 (so it's discoverable from the spec itself), full guidance and the worked example in `working-with-crds.md` and the skill (so the detail doesn't bloat the normative spec). Matches how Tags (§7.3) and Related MLEs by Dimension (§7.4) are already split between spec and guide.
2. *Should the source-role/limitation matrix become part of `source-context-template.md` now?* Yes — done, expanded to include the four missing source types.
3. *Minimum evidence threshold for the relationship dataset: a second inventory, or one independent blind audit of the first?* Neither yet — reframed as a generator over existing data rather than a new format, so the threshold question is deferred until that generator is actually designed, not just until an inventory count is reached.
4. *Should responsive projection guidance be a mandatory skill checklist, or stay in HTML templates only?* Stays in template/guide reference only, as originally proposed — no mandatory checklist added; nothing in the audit found a reason to escalate it.

## Purpose

Record practical framework improvements observed while applying Draft 0.4 to a real, growing capability inventory. This proposal does **not** change the required CRD core yet. It distinguishes:

1. small guidance additions that can safely enter the CRD Author skill and working guide;
2. optional inventory/projection conventions that need another application before becoming normative; and
3. visual implementation choices that should remain outside the semantic CRD specification.

The existing Communication MLE representative-text rule is already incorporated separately; it is not re-proposed here.

## Summary of recommendations

| Priority | Recommendation | Proposed home | Core change? |
|---|---|---|---|
| High | Add a non-normative **capability statement** projection convention. | `working-with-crds.md`, CRD Author skill | No |
| High | Add a **full-detail applicability pass** to Extract-mode validation. | CRD Author skill | No |
| High | Require explicit source-role and source-limit statements in cross-source extraction context. | `agent-transformation-instructions.md`, Source Context template, skill | No |
| Medium | Define an optional, canonical **Capability Relationship Dataset** and inventory graph projection. | `working-with-crds.md`, new template/example, skill | No |
| Medium | Add responsive human-projection guidance for labelled fields and evidence tables. | HTML template guidance and skill | No |
| Keep as-is | Keep Mermaid optional and capability-local. | Existing specification/skill | No |

## 1. Optional capability statement projection

### Recommendation

Allow a human-facing inventory to render a concise, source-derived statement in this form:

> `[actor] can [intent] so that [meaningful outcome].`

It is an **audience projection**, not a new CRD field and not a replacement for `capability purpose`, `meaningful outcome`, or the Interaction Contract MLE.

### Example

Canonical CRD fields:

```text
Actor: AI Twin owner
Command / intent: Submit a public article URL and approve its draft
Meaningful outcome: A reviewed web-page draft is approved as AI Twin Knowledge.
```

Human projection:

> An AI Twin owner can submit a public article URL and approve its draft **so that a reviewed web-page draft is approved as AI Twin Knowledge.**

### Rules

- Generate it only when actor, intent, and meaningful outcome are all established by canonical content.
- If any component is unknown, render the canonical purpose instead; do not invent a grammatical sentence.
- The outcome clause may be visually emphasized in a projection, but that styling is not semantic priority and does not make the projection normative.
- The canonical CRD remains the authority if the sentence is abbreviated or awkward.

### Why this is worth adding

Capability purpose alone often answers *why* but not clearly *who does what and to what end*. The statement makes large inventories more scannable without duplicating requirements.

## 2. Full-detail applicability pass

### Recommendation

Add a required validation pass for a bounded “complete baseline” extraction set. The pass does not require every optional extension; it requires assessing each relevant extension deliberately.

For each CRD, verify:

- operational realization and execution mode are documented where evidence supports them, otherwise explicitly unknown;
- shared elements/approved reuse are documented where a shared component, collection, prompt, schema, or workflow is genuinely evidenced;
- Related MLEs by Dimension are included only for real traceability;
- Communication MLEs exist only when the capability actually triggers a meaningful communication, with representative example text under the existing rule;
- direct production/API/runtime claims remain unresolved unless traced to their governing source.

### Example outcome

For a Knowledge-input capability, a `Data/Information → supports → Answer grounded in Knowledge` relation can be recorded when both CRDs establish the common collection and answer role. A current API edge must remain absent if no source traces that application behavior to a concrete current API contract.

### Rule

“Full detail” means *applicable details are assessed and evidence-backed*, not *every optional section is filled*.

## 3. Source role and limitation matrix

### Recommendation

Extend cross-source extraction context so every source records both its authority role and its limit.

| Source role | Can establish | Cannot establish alone |
|---|---|---|
| Product-facing guide / help content | Documented user intent and described behavior | Current implementation, API shape, storage, or deployment state |
| Current application code | A traced implementation path | Product intent, policy, or general reusable meaning by itself |
| API specification | Published interface contract | User-facing capability purpose or actual caller/consumer by itself |
| Shared-core implementation | Generic primitives and current code paths | That a particular product capability uses them without a traced connection |
| Test fork / historical implementation | Comparison patterns and historical implementation choices | Current production behavior or authority |

### Required extraction rule

Do not upgrade generic shared-Core/API evidence into a product-specific realization claim without a traceable connection between the product and that implementation surface.

### Suggested source-context additions

- revision, version, date, or content hash when reasonably available;
- source role;
- what the source can establish;
- what it cannot establish alone;
- currentness / production status where relevant.

## 4. Optional Capability Relationship Dataset and graph

### Recommendation

Define an optional inventory-level canonical dataset for relationships across CRDs. A relationship graph is a projection of that dataset, not a separately authored map.

Minimal illustrative shape:

```json
{
  "id": "example-capability-relationships",
  "clusters": [
    {"id": "input", "label": "Input", "capabilityIds": ["CAP-01", "CAP-02"]},
    {"id": "outcome", "label": "Outcome", "capabilityIds": ["CAP-03"]}
  ],
  "relationships": [
    {
      "from": "CAP-01",
      "to": "CAP-03",
      "type": "supports",
      "label": "shared information context",
      "evidence": "crds/cap-01.md — Data/Information related MLE"
    }
  ],
  "unresolved": [
    "This graph does not establish runtime sequencing or implementation topology."
  ]
}
```

### Dataset rules

- Every edge must map to an explicit canonical CRD relation, shared-element/reuse declaration, or other named canonical evidence record.
- Use existing relationship vocabulary where applicable: `defines`, `implements`, `supports`, `constrains`, `verifies`, `exposes`, `reused_by`.
- Do not infer edges from common terms, names, inventory ordering, a shared source page, or an `Includes`/`Excludes` mention alone.
- Clusters aid reading only; they do not imply hierarchy, execution order, or ownership.
- Mark unresolved context explicitly. Do not draw a speculative edge merely to make a graph connected.

### Graph rules

- Make nodes link to canonical CRDs.
- Make edge type and evidence state legible.
- State that the graph is neither a runtime sequence nor an architecture diagram.
- Introduce the graph only when enough explicit relations exist to reveal a real cluster; do not add one merely because an inventory has more rows.

### Why this is different from Mermaid

Mermaid remains optional and capability-local: it explains a particular CRD’s state flow or declared shared-element relation. The relationship dataset/graph is inventory-level: it helps a reader navigate many CRDs without creating a second source of truth.

## 5. Human-facing projection guidance

### Recommendation

Add projection guidance, not specification requirements, for readable CRD inventories and details.

#### Detail views

- Put identity/status/evidence metadata in a compact header; do not repeat it unchanged in the body.
- Render Markdown labelled fields as label/value rows or cards, not long undifferentiated bullet lists.
- Use selective emphasis for `capability purpose`, `meaningful outcome`, `result`, `rules/invariants`, and `required meaning`; do not bold every value.
- Preserve semantic classes visibly, especially for examples, recommendations, implementation choices, and unknowns.

#### Evidence/provenance tables

- Desktop may use tables with readable Statement, Class, and Source columns.
- Narrow screens must convert each row into a labelled card or equivalent stacked representation; they must not require horizontal scrolling or clip text.
- Do not remove Class or Source on mobile: provenance is part of the meaning.

#### Inventory rows

- Use a compact table on wide screens.
- On narrow screens, use one capability card per row and suppress redundant labels only when the visual structure already makes their meaning clear.
- Avoid using color or typography alone to distinguish evidence maturity or status.

These are useful defaults for template authors, but individual products may use their own visual system.

## 6. Mermaid conclusion

No semantic change is recommended.

The pilot confirms the existing rule:

- a Mermaid diagram is optional, illustrative, and traceable to canonical CRD text;
- use it for a complex state/decision flow or shared-element relation that prose does not make easy to scan;
- do not add it to every CRD; and
- do not use it as a substitute for an inventory-level relationship dataset.

## Suggested adoption sequence

1. Add Sections 1–3 to the CRD Author skill and working/extraction guidance.
2. Add the relationship-dataset convention as an experimental optional extension, with one worked example and validator only after a second independent inventory validates it.
3. Add responsive projection rules to the HTML-template guidance, not the semantic specification.
4. Revisit whether any convention belongs in the JSON schema only after at least two independent inventories demonstrate stable needs.

## Non-recommendations

- Do not add the capability statement to the required CRD core.
- Do not require a Mermaid diagram, relationship graph, or every Related-MLE dimension.
- Do not make UI styling normative CRD semantics.
- Do not treat a graph edge as proof of API/runtime dependency or execution order.
- Do not generalize a single product’s fields or UI terminology into a reusable requirement without a second consumer.

## Review questions

1. Should the capability-statement projection be described in the specification’s audience-projection section, or only in `working-with-crds.md` and the skill?
2. Should the source-role/limitation matrix become part of `source-context-template.md` now?
3. What is the minimum evidence threshold for introducing the optional relationship dataset: one second inventory, or one independent blind audit of the first?
4. Should responsive projection guidance remain solely in HTML templates, or also appear as a mandatory checklist in the skill when an HTML showcase is requested?
