# Source Context Reference Template

A Source Context Reference (SCR) is a companion document, not a CRD and not a capability. It exists because a Capability Inventory and its CRDs deliberately hold only capability-scoped meaning — purpose, boundaries, contracts, rules for one ability at a time. Real source material (a PRD, a plan, a spec) usually also contains product-wide or cross-cutting content that no single capability owns: why the product exists at all, constraints that apply across many capabilities, how different clients expose different subsets, and the order work is meant to happen in. Without a dedicated place for that content, it gets silently dropped, flattened into one capability's notes where it doesn't really belong, or left for a reader to reconstruct from 13 different files.

An SCR is produced once per source (or per closely related set of sources) that a Capability Inventory was derived from — not once per capability.

**An SCR carries no binding requirements of its own beyond what the CRDs it accompanies already state.** It is a reference, not a source of new rules. If a cross-cutting constraint listed here should be binding on a capability, that capability's own CRD must carry it as a rule/invariant, implementation requirement, or recommended default — the SCR only prevents that constraint from being lost or forgotten, it doesn't substitute for stating it where it governs.

## Template

### Source(s)

For each source document: title, path/URL, version or date if known, stated target audience, and stated purpose (quote or closely paraphrase — don't invent one if the source doesn't say).

### Product/system intent

Why this exists, in the source's own terms (business rationale, problem being solved). Mark as `rationale/intent`, not `capability purpose` — this is about the whole product/system, not one ability.

### Scope

What the source includes in the version/release being described, and what it explicitly excludes (non-goals). This is evidence for the Capability Inventory's own boundaries, not a capability itself.

### Cross-cutting constraints

A table of constraints that apply across multiple capabilities, each with which capabilities it constrains and its semantic class:

| Constraint | Applies to (capability IDs) | Semantic class | Source |
|---|---|---|---|
|  |  | rule/invariant \| recommended default \| operational constraint |  |

Typical entries: localization/language requirements, performance/scalability/reliability targets, forward-compatibility promises ("don't build X now, but don't preclude it later"), security/privacy defaults that aren't owned by one capability, accessibility requirements that span multiple capabilities' presentation.

**If a constraint here is a rule/invariant or implementation requirement**, verify it is also stated inside every capability's CRD that it actually constrains — don't let it live only in this table. If it isn't yet reflected in the relevant CRDs, say so explicitly as a gap, don't silently drop it.

### Platform/client exposure matrix

When the source describes more than one client/platform with different capability scope, a table making that explicit:

| Capability | Client A | Client B | Client C |
|---|---|---|---|
|  | full \| partial \| none |  |  |

### Delivery/build sequencing

The source's own stated build order, phases, or rollout plan, if any — explicitly non-normative to any capability. This section exists so a reader doesn't lose *when* the source wanted things built, while making unambiguous that CRDs describe *what*, not *when*. A Capability Inventory's `realization status` field is the right place to summarize where a specific product currently stands, if known; this section is the fuller narrative context behind it.

### Test/verification material

Any source-provided test data, acceptance criteria, or success-criteria narrative that spans multiple capabilities (a single end-to-end scenario, for example) and would otherwise have to be split across several CRDs' individual "Tests / verification" fields, losing the narrative that ties them together.

### Unmapped or deferred source material

A short list of anything substantive in the source that didn't become a capability, a cross-cutting constraint, or part of this document, with a one-line reason. This overlaps with a decision log if one exists — cross-reference it rather than duplicating its reasoning here.
