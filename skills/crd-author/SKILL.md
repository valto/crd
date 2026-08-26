---
name: crd-author
description: "Write Capability Requirements Documents (CRDs) and maintain a Capability Inventory using the CRD framework (github.com/valto/crd, Draft 0.4). Two modes: Define — write a new, reusable, technology-agnostic CRD for a capability that doesn't exist yet or is being specified independent of any particular implementation; Extract — decompose or combine existing material (PRD, codebase, API/OpenAPI spec, MCP server, database schema, user stories, existing application) into one or more CRDs plus Operational Capability Documentation, without inventing facts. Both modes register the result in a Capability Inventory (including known realizations, so reusability claims are checkable rather than asserted) and can optionally render an illustrative Mermaid diagram of interaction-contract state flow or shared-element/skill/tool relationships. Extract mode defaults to producing only the specific/operational set, and produces a Source Context Reference alongside the CRDs for product-wide/cross-cutting context that no single CRD should own. Use whenever asked to: 'write/create/draft a CRD', 'document this as a capability', 'define a Capability MLE', 'build/update a capability inventory', 'extract capabilities from this PRD/codebase/API/MCP server', 'turn this into capability documentation', 'diagram this capability/state flow', or any request framed in CRD / Capability MLE / Interaction Contract MLE terms."
---

# CRD Author

Implements the Capability Documentation model (Draft 0.4): Capability MLE → Interaction Contract MLE → Realization, documented as a Capability Requirements Document (CRD) and catalogued in a Capability Inventory.

This file is the workflow. The semantic model itself lives in the referenced files — read `../../crd-specification.md` and `../../working-with-crds.md` before drafting anything non-trivial.

## Step 0 — Determine mode

Ask, unless it's already obvious from what the user handed you:

- **Define** — the capability doesn't exist yet, or is being specified independent of any particular implementation (e.g. "I want a CRD for X").
- **Extract** — the user has handed you existing material (a PRD, a codebase, an API/OpenAPI spec, an Arazzo workflow document, an MCP server, a database schema, user stories, a running application) and wants it decomposed or combined into CRDs.

If existing material is provided without a stated mode, default to Extract but confirm scope before finalizing. If a capability is described abstractly with no existing system behind it, default to Define.

## Step 1 — Locate or create the workspace

You're inside the `valto/crd` repository. Worked/illustrative examples belong in `examples/<slug>.md` (+ optional `examples/<slug>.json`), matching `request-moving-quote` and `reconcile-payments`. Register every example in `capability-inventory.md`. If the user is documenting a *different* project's capabilities while working in this repo, ask where that project's own `capability-inventory.md` and `crds/` directory should live instead — don't mix another product's capabilities into this repo's inventory.

## Step 2 — Define mode

1. State the candidate capability name and run the MLE test from `../../minimum-logical-element.md` and `../../crd-specification.md` §3.1 before writing anything:
   - Is it understandable independently?
   - Can it be invoked or used meaningfully?
   - Can success or failure be determined?
   - Would splitting it further cause the pieces to lose their purpose context?
   - Would enlarging it fold in other independently meaningful abilities?
   - Is the candidate's actor really just "a developer manually running this for pre-release verification," with no recurring operational role and no exposure beyond that developer? If so, it's presumptively a tool or test scaffolding (`../../crd-specification.md` §3.6), not a capability, even if it passes every question above and has its own doc, test, and CLI target. Good documentation and test coverage make it good engineering, not a capability.
2. If the candidate fails the test, propose a split (multiple CRDs) or a merge (one CRD) and say why, before drafting.
3. Fill `../../crd-template.md` for the capability. Required core: name, definition, capability purpose, boundaries (includes/excludes), meaningful outcome, at least one Interaction Contract MLE (or an explicit unknown explaining why none exists yet), rules/invariants (or "none known"), recommended defaults (or "none known"), unknowns.
   - **Terms and concepts:** for a reusable/generic CRD, ground terms in an applicable open standard vocabulary (schema.org first choice; Dublin Core, ActivityStreams, or another IANA/W3C vocabulary where a better fit exists) instead of inventing bespoke terminology, unless the source material specifies a concrete term that should be preserved as-is. Cite the standard type/property alongside the plain-language term (e.g. `participant (schema.org/Person)`, `comment (schema.org/Comment)`, `rating/confidence (schema.org/Rating.ratingValue)`). This is guidance for the reusable CRD's terms only — an Operational Capability Documentation extension should use the actual system's own terminology, not the standard vocabulary.
4. Tag every substantive statement with a semantic class from `../../crd-specification.md` §6 (capability purpose, rationale/intent, rule/invariant, implementation-requirement, recommended default, example, implementation choice, operational constraint, unknown/unresolved) — never let an example or implementation choice read as a binding rule.
5. Add optional sections (operational realization, shared elements/approved reuse, agentic mappings, audience projections) only where you have real content — an empty optional section is worse than an omitted one.
6. When declaring a realization, state its execution mode explicitly: `software-primary`, `agent-primary-using-software`, `software-primary-calling-agents`, or `unknown`. Don't conflate this with `agent-built-software`, which is provenance (how it was built), not runtime control.
7. Optional: add a Mermaid diagram (see "Optional: Mermaid diagrams" below) when a visual rendering of the states/transitions or the shared-element/skill/tool relationships would help a reader, without introducing anything not already stated in the CRD's text.
8. Optional: add universal tags (`../../crd-specification.md` §7.3) only for a dimension not already derivable from another field — e.g. `network-touching`/`local-only`, `data-sensitive`, `identity-related`, `notification-triggering`. Don't tag `read-only` when a contract's `transition` already says none, and don't tag `internal`/`user-facing` when `exposure` already says so. Keep implementation-specific groupings (a module/domain name) in the realization's implementation tags instead, prefixed (e.g. `impl:inbox`) so they're never mistaken for universal ones. In an HTML showcase, the visual tag/badge convention is reserved for implementation tags — a universal tag becomes a grouping/section key (its own tab) or plain text, never the same badge.

## Step 3 — Extract mode

Follow `../../agent-transformation-instructions.md` exactly; it is the canonical procedure. Non-negotiables:

- Never invent product facts, policies, ownership, outcomes, or implementation details.
- Mark uncertainty `unknown/unresolved` rather than filling it with a plausible answer.
- Distinguish explicit fact / reasonable inference / recommended default / example / implementation choice / operational constraint at every statement.
- Do not derive a reusable CRD solely from one operational realization without flagging realization-specific facts as such.
- Resolve competing guidance in precedence order: rule/invariant → explicit implementation requirement → explicit owner/user choice → recommended default → agent judgment. Same-level conflicts become `unknown/unresolved`, not a silent choice.
- Do not infer a priority or ordering relationship between independently stated facts unless the source states that ordering directly. If a source states several related settings/rules but never says which wins when they conflict, that ordering is `unknown/unresolved` — not a rule, and not even an "example" default, however sensible it looks.
- Preserve the source's own hedge language. A statement phrased as "preferably," "should," "recommended," or an equivalent hedge in the source language classifies as `recommended default` or `implementation choice`, never `rule/invariant` — regardless of how operationally important it seems. Strengthening a hedge into a binding rule is inventing a fact.
- Do not carry over terminology, facts, or conclusions from any other source, project, or prior work not included in the material assigned for this extraction — including other material handled earlier in the same session. If a term seems relevant but you cannot point to where in the assigned source it appears, omit it; do not include it hedged as "possibly used elsewhere." If you are the orchestrator delegating this to a subagent, prefer a fresh subagent with no inherited context over a fork that shares session history with other extraction work — shared context is the most common way this rule gets violated even when the executing agent's instructions are otherwise correct.
- When extracting from a codebase or structured configuration (build/target definitions, schemas, manifests), do not assert a machine-checkable fact — such as which build target includes a file, or which route a client calls — as confirmed unless you have traced it directly in the specific file and line that governs it. If you have not traced it, mark it `unknown/unresolved` rather than stating it with confidence.
- A declared type, enum case, schema field, or similar construct that you cannot find an actual code path constructing, assigning, or reaching must not be presented as a live, reachable, user-visible outcome. Either omit it, or explicitly mark it "declared but reachability not confirmed."

Procedure: inventory and classify sources → extract candidate statements → identify candidate capabilities (apply the MLE test from Step 2.1) → combine/decompose → define interaction contracts → separate reusable definition from realization (including execution mode and shared-element/approved-reuse notes, §6.1) → produce and validate.

When deciding to combine several elements into one capability, don't just test the merged result — run the MLE test from Step 2.1 on each element being combined, individually, first. Combine only when every element fails the test alone (none is independently meaningful). If one element you're about to fold in actually passes the test by itself — it has its own actor, command, state, and result — it is very likely its own Capability MLE, not a contract inside a bigger one. Record this check in the decision log, not just its conclusion. This is not discretionary once an element passes alone: split it out. Writing down that an element passed the test alone and combining it anyway does not satisfy this rule — disclosure is not compliance.

When the source includes an Arazzo workflow document alongside an OpenAPI (or other API) description, treat each declared workflow as a candidate-capability hypothesis and each of its steps as candidate Interaction Contract evidence — not as an automatic capability boundary. Still run the MLE test on the workflow as a whole: a vendor-declared workflow may bundle several independently meaningful capabilities, or be too narrow to be one on its own. A step's referenced operation is evidence for a tool, not a capability by itself. Most API sources won't have an Arazzo document — a raw OpenAPI spec alone needs the same combine/decompose work, with less structural evidence to work from.

**Default to the specific/operational CRD set only.** Produce an additional generic/reusable projection only when the user asks for one, or when reuse by a second real consumer is already established or clearly imminent — not by default, and not just because generalization is possible. A generic CRD produced with no known consumer is a hypothesis, not a demonstrated reusable capability; say so in the inventory (see Step 5) rather than implying otherwise. When you do produce a generic projection, treat every generalizing phrase ("or otherwise," "or similar," "any," "etc.") as a checkpoint: verify it's directly supported by the source, not merely a plausible-sounding broadening. Generalizing vocabulary (Step 2's "Terms and concepts" guidance) is never license to generalize requirements.

When extracting multiple capabilities from one substantial source (a PRD, a plan, a spec), also produce a Source Context Reference — see `../../source-context-template.md` — capturing the source(s) used and the product-wide/cross-cutting content that no single capability should own but that shouldn't be lost either: overall intent, cross-cutting constraints (localization, non-functional requirements, forward-compatibility promises), a platform/client exposure matrix if the source describes more than one client, and the source's own build/delivery sequencing (explicitly marked non-normative to any CRD). Skip it for a small or single-capability extraction where there's no real cross-cutting content to lose.

Required output for Extract mode, every time:
1. One CRD per identified Capability MLE.
2. A statement-provenance table.
3. A short decision log explaining each combine/decompose choice, including the symmetric MLE check above.
4. An unresolved-questions list.
5. A shared-element/reuse table and agentic mapping when a component, schema, prompt, tool, or skill supports more than one capability.
6. A Source Context Reference when extracting from one substantial source (see above).

## Optional: Mermaid diagrams

A CRD MAY include one or more Mermaid diagrams as an illustrative, non-normative rendering of content that is already stated in the CRD's text. Mermaid is preferred over other diagram formats here because it is plain text, renders natively on GitHub, and stays diffable — consistent with the CRD framework's text-first, agent-readable approach.

Two renderings are useful:

1. **Interaction Contract state flow** — a `stateDiagram-v2` or `flowchart` showing the states and transitions across a capability's Interaction Contract MLEs (current state → transition → new state, per contract).
2. **Shared-element / skill / tool relationship** — a `graph`/`flowchart` showing the many-to-many relationship between the Capability MLE, any skills that realize or bundle it, any tools it depends on, and any shared elements it declares (`createdFor`/`approvedReuse`).

Rules for using them:

- A diagram is a projection of the CRD, exactly like an audience projection (§7.2 of `../../crd-specification.md`): it MUST trace back to states, transitions, rules, or relationships already declared in the document's text, and MUST NOT introduce a state, transition, edge, or relationship that isn't already stated there.
- Label the diagram clearly as illustrative (e.g. a heading like "Illustrative state flow (Mermaid)") so it is never mistaken for an additional normative section.
- Do not add a diagram merely to make a CRD look more complete — omit it if it wouldn't help a reader understand something the prose doesn't already make clear.
- Place it near the section it illustrates (Interaction Contract MLEs, or the shared elements/agentic mappings section), not as a required standalone section.
- In a `stateDiagram-v2`, do not route a state into the `[*]` exit pseudostate unless the prose explicitly describes that state as terminal/final. A state the prose describes as "retained," "persists," or "stays in history" is not terminal — model it as a state, not an exit, even if nothing further happens to it in this CRD's contracts.

## Step 4 — Validate

Before presenting output:
- Every CRD has all required-core fields present or explicitly marked unknown.
- No example, implementation choice, or operational constraint is stated as if it were a rule/invariant.
- No API endpoint, UI component, database table, skill, or tool name is treated as a capability without independent purpose context (see the skill/tool/capability distinction in `../../working-with-crds.md`).
- No capability has silently grown into a vague feature bucket — check boundaries excludes at least as carefully as includes.
- If a Mermaid diagram is included, every state/transition/edge in it matches something explicitly stated in the CRD's own text — no diagram-only facts.
- If producing a JSON example in this repository, run `python3 scripts/validate.py` from the repository root. The bundled validator checks the repository's JSON examples against `schema/crd.schema.json`; validate external CRD files with an equivalent schema-aware check.

## Step 5 — Register in the Capability Inventory

Add or update one row per capability in `capability-inventory.md` using the format it already defines: `id`, `name`, `status`, `purpose`, link to the CRD, `realization status`, `known realizations`, `tags`, `notes`. Never let the inventory drift from the CRDs it links to — if a CRD's status or realization status changes, update the row in the same pass. `tags` combines the CRD's own universal tags with this row's implementation tags (each prefixed, e.g. `impl:inbox`) — omit the column entirely if it adds nothing beyond `purpose`.

For a generic/reusable inventory, populate `known realizations` honestly: list every product/service/app already known to realize the capability, linked to that realization's own CRD or Operational Capability Documentation if one exists. If the generic capability was itself generalized from one specific product's capability (the common case when you produced both sets from one Extract-mode run), that product is realization #1 — list it, don't leave the column empty just because it feels like the "obvious" source. A capability with zero known realizations is an unproven hypothesis about reusability, not a demonstrated one; the inventory should make that visible rather than implying otherwise through silence.

## Optional: showcase the inventory as HTML

A Capability Inventory and its CRDs are markdown by default — good for agents, not always pleasant for a human browsing their own product's capabilities. When the user wants to browse or publish an inventory, the showcase must be **entirely HTML** — a human should never click through from it and land on a raw `.md` file. That means three template files, all used together, not just the index:

- `../../inventory-html-template.html` — the index page. Copy it next to `capability-inventory.md`, fill in the title/subtitle from the inventory's own intro, and generate the CSS-only two-tab structure the template documents — one tab segmented by universal tag, one by implementation tag/domain — from your `capability-inventory.md`/CRD data, in the same order, with no additions or omissions (this page is a projection, like any audience projection, not a new source of truth). Only build a tab your data actually supports; if neither kind of tag exists anywhere in the inventory, skip the tabs and render one flat table instead.
- `../../crd-html-template.html` — render **one of these per capability**, from its CRD's own fields (Identity, Core meaning, every Interaction Contract MLE, Rules and defaults, Unknown/unresolved, and any Optional sections the CRD actually has). Link the index's rows to these pages, not to the `.md` files. Universal tags render as plain text; the `<span class="tag">` badge is reserved for implementation tags.
- `../../doc-html-template.html` — render one of these for each supporting doc that exists (source context, decision log, unresolved questions, provenance), converting the markdown structure directly (headings, bold, lists, tables, code blocks, links) without summarizing or reorganizing it.

Do not add a build pipeline, JS framework, or external dependency; every page should open directly from disk or host as a static file with zero configuration — the two-tab UI uses only a radio-input/label/`:checked`-sibling CSS technique, no `<script>`. Produce this only when asked or when publishing — not by default alongside every extraction.

## What not to do

- Do not treat a component, endpoint, screen, or database table as a capability merely because it is callable or reusable.
- Do not expand a capability into a broad product area to avoid writing several CRDs.
- Do not let a recommended default or your own judgment override a rule/invariant or an explicit requirement.
- Do not assume a skill equals one capability, or that a tool equals a skill — map them explicitly (`../../working-with-crds.md`).
- Do not hide unknowns behind confident-sounding generic language.
- Do not invent a priority ordering between facts the source states independently, and do not strengthen a source's hedge language ("preferably," "should") into a binding rule.
- Do not let a Mermaid diagram assert a state, transition, or relationship that the CRD's own text doesn't already establish.
- Do not produce a generic/reusable CRD set by default — only when asked, or when a second real consumer already exists or is imminent — and do not claim a generic capability is reusable without listing its known realizations.
- Do not document in your own decision log that an element passes the MLE test alone and then combine it anyway — that is a rule violation, not a disclosed judgment call.
- Do not treat a manually-run developer verification tool as a capability just because it has its own doc, test, or CLI target — check for a recurring operational role or third-party/agent exposure first.
- Do not assert a build-membership or other machine-checkable fact without citing the exact file/line you traced to confirm it.
- Do not present a declared type, enum case, or schema value as a live, reachable outcome without confirming a real code path constructs or reaches it.
- Do not tag a dimension another field already settles, and do not leave an implementation tag unprefixed so it could be mistaken for a universal one.
- Do not render a universal tag as a `<span class="tag">` badge in an HTML showcase — that badge convention is reserved for implementation tags; a universal tag becomes a grouping/section key or plain text instead.
- Do not modify, operate, or publish changes to a live service, repository, or external system as a side effect of documenting it, unless explicitly authorized.

## Reference material

- `../../crd-specification.md` — normative model and required core.
- `../../crd-template.md` — the document to fill in.
- `../../minimum-logical-element.md` — Minimum Logical Element origin and the MLE test.
- `../../working-with-crds.md` — decision precedence, shared-element reuse, skill/tool mapping, audience projections, why a CRD isn't a feature/PRD/API doc.
- `../../agent-transformation-instructions.md` — canonical Extract-mode procedure.
- `../../capability-inventory.md` — Capability Inventory entry format, including known realizations.
- `../../source-context-template.md` — companion document for product-wide/cross-cutting context that no single CRD should own.
- `../../inventory-html-template.html` — dependency-free static-page template for a capability inventory's HTML index.
- `../../crd-html-template.html` — HTML page template for a single CRD, used by the inventory showcase.
- `../../doc-html-template.html` — HTML page template for a supporting doc (source context, decision log, unresolved, provenance), used by the inventory showcase.
- `../../schema/crd.schema.json` — machine-readable schema for JSON instances.
- `../../scripts/validate.py` — schema validator.
- `../../examples/` — worked examples (external-facing and internal capabilities).
