---
name: crd-author
description: "Write Capability Requirements Documents (CRDs) and maintain a Capability Inventory using the CRD framework (github.com/valto/crd, Draft 0.4). Two modes: Define — write a new, reusable, technology-agnostic CRD for a capability that doesn't exist yet or is being specified independent of any particular implementation; Extract — decompose or combine existing material (PRD, codebase, API/OpenAPI spec, MCP server, database schema, user stories, existing application) into one or more CRDs plus Operational Capability Documentation, without inventing facts. Both modes register the result in a Capability Inventory. Use whenever asked to: 'write/create/draft a CRD', 'document this as a capability', 'define a Capability MLE', 'build/update a capability inventory', 'extract capabilities from this PRD/codebase/API/MCP server', 'turn this into capability documentation', or any request framed in CRD / Capability MLE / Interaction Contract MLE terms."
---

# CRD Author

Implements the Capability Documentation model (Draft 0.4): Capability MLE → Interaction Contract MLE → Realization, documented as a Capability Requirements Document (CRD) and catalogued in a Capability Inventory.

This file is the workflow. The semantic model itself lives in the referenced files — read `../../crd-specification.md` and `../../working-with-crds.md` before drafting anything non-trivial.

## Step 0 — Determine mode

Ask, unless it's already obvious from what the user handed you:

- **Define** — the capability doesn't exist yet, or is being specified independent of any particular implementation (e.g. "I want a CRD for X").
- **Extract** — the user has handed you existing material (a PRD, a codebase, an API/OpenAPI spec, an MCP server, a database schema, user stories, a running application) and wants it decomposed or combined into CRDs.

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
2. If the candidate fails the test, propose a split (multiple CRDs) or a merge (one CRD) and say why, before drafting.
3. Fill `../../crd-template.md` for the capability. Required core: name, definition, capability purpose, boundaries (includes/excludes), meaningful outcome, at least one Interaction Contract MLE (or an explicit unknown explaining why none exists yet), rules/invariants (or "none known"), recommended defaults (or "none known"), unknowns.
4. Tag every substantive statement with a semantic class from `../../crd-specification.md` §6 (capability purpose, rationale/intent, rule/invariant, implementation-requirement, recommended default, example, implementation choice, operational constraint, unknown/unresolved) — never let an example or implementation choice read as a binding rule.
5. Add optional sections (operational realization, shared elements/approved reuse, agentic mappings, audience projections) only where you have real content — an empty optional section is worse than an omitted one.
6. When declaring a realization, state its execution mode explicitly: `software-primary`, `agent-primary-using-software`, `software-primary-calling-agents`, or `unknown`. Don't conflate this with `agent-built-software`, which is provenance (how it was built), not runtime control.

## Step 3 — Extract mode

Follow `../../agent-transformation-instructions.md` exactly; it is the canonical procedure. Non-negotiables:

- Never invent product facts, policies, ownership, outcomes, or implementation details.
- Mark uncertainty `unknown/unresolved` rather than filling it with a plausible answer.
- Distinguish explicit fact / reasonable inference / recommended default / example / implementation choice / operational constraint at every statement.
- Do not derive a reusable CRD solely from one operational realization without flagging realization-specific facts as such.
- Resolve competing guidance in precedence order: rule/invariant → explicit implementation requirement → explicit owner/user choice → recommended default → agent judgment. Same-level conflicts become `unknown/unresolved`, not a silent choice.

Procedure: inventory and classify sources → extract candidate statements → identify candidate capabilities (apply the MLE test from Step 2.1) → combine/decompose → define interaction contracts → separate reusable definition from realization (including execution mode and shared-element/approved-reuse notes, §6.1) → produce and validate.

Required output for Extract mode, every time:
1. One CRD per identified Capability MLE.
2. A statement-provenance table.
3. A short decision log explaining each combine/decompose choice.
4. An unresolved-questions list.
5. A shared-element/reuse table and agentic mapping when a component, schema, prompt, tool, or skill supports more than one capability.

## Step 4 — Validate

Before presenting output:
- Every CRD has all required-core fields present or explicitly marked unknown.
- No example, implementation choice, or operational constraint is stated as if it were a rule/invariant.
- No API endpoint, UI component, database table, skill, or tool name is treated as a capability without independent purpose context (see the skill/tool/capability distinction in `../../working-with-crds.md`).
- No capability has silently grown into a vague feature bucket — check boundaries excludes at least as carefully as includes.
- If producing a JSON example in this repository, run `python3 scripts/validate.py` from the repository root. The bundled validator checks the repository's JSON examples against `schema/crd.schema.json`; validate external CRD files with an equivalent schema-aware check.

## Step 5 — Register in the Capability Inventory

Add or update one row per capability in `capability-inventory.md` using the format it already defines: `id`, `name`, `status`, `purpose`, link to the CRD, `realization status`, `notes`. Never let the inventory drift from the CRDs it links to — if a CRD's status or realization status changes, update the row in the same pass.

## What not to do

- Do not treat a component, endpoint, screen, or database table as a capability merely because it is callable or reusable.
- Do not expand a capability into a broad product area to avoid writing several CRDs.
- Do not let a recommended default or your own judgment override a rule/invariant or an explicit requirement.
- Do not assume a skill equals one capability, or that a tool equals a skill — map them explicitly (`../../working-with-crds.md`).
- Do not hide unknowns behind confident-sounding generic language.
- Do not modify, operate, or publish changes to a live service, repository, or external system as a side effect of documenting it, unless explicitly authorized.

## Reference material

- `../../crd-specification.md` — normative model and required core.
- `../../crd-template.md` — the document to fill in.
- `../../minimum-logical-element.md` — Minimum Logical Element origin and the MLE test.
- `../../working-with-crds.md` — decision precedence, shared-element reuse, skill/tool mapping, audience projections, why a CRD isn't a feature/PRD/API doc.
- `../../agent-transformation-instructions.md` — canonical Extract-mode procedure.
- `../../capability-inventory.md` — Capability Inventory entry format.
- `../../schema/crd.schema.json` — machine-readable schema for JSON instances.
- `../../scripts/validate.py` — schema validator.
- `../../examples/` — worked examples (external-facing and internal capabilities).
