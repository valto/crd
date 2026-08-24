# Changelog

## Unreleased

- Hardened `agent-transformation-instructions.md` and the CRD Author skill against four failure modes found by a second, independently-run extraction test (a real codebase, not a PRD) and a fresh blind audit of its output: cross-session/cross-source terminology leakage (don't carry over facts or terms from other work handled earlier in the same session; prefer isolated subagents over forks for extraction); unverified machine-checkable claims (don't assert build-membership or similar facts without citing the exact file/line traced); a disclosed-but-not-resolved rule violation (recording that a combine decision breaks the individual-MLE-test rule doesn't satisfy the rule); and declared-but-unreached values presented as live outcomes.

- Added a Source Context Reference template (`source-context-template.md`) for product-wide/cross-cutting content (intent, cross-cutting constraints, platform exposure, build sequencing) that no single CRD should own but that shouldn't be lost between capability-scoped documents either.
- Added `known realizations` to the Capability Inventory format (`capability-inventory.md`), so a generic capability's reusability is a checkable fact (which products/services realize it) rather than an assertion.
- Hardened the CRD Author skill against issues found by two independent blind audits of a real extraction run: don't infer a priority ordering between independently stated facts; preserve source hedge language instead of silently strengthening it into a binding rule; run the MLE test on each element individually before combining, not just on the merged result; treat generalizing phrases in a generic projection as a checkpoint against the source, not a free pass; don't route a persisting/retained state into a Mermaid `[*]` exit; default Extract mode to the specific/operational set only, producing a generic projection only on request or demonstrated reuse.
- Added optional Mermaid diagram guidance to the CRD Author skill (`skills/crd-author/SKILL.md`): illustrative, non-normative renderings of Interaction Contract state flow and shared-element/skill/tool relationships, always traceable to text already stated in the CRD.
- Added an illustrative Mermaid state-flow diagram to the `Reconcile payments` example.

## 0.5.0 — 2026-08-20

- Added the CRD Author agent skill (`skills/crd-author/SKILL.md`): Define mode for new reusable CRDs, Extract mode for deriving CRDs from existing material, and a shared Capability Inventory registration step.

## 0.4.0 — 2026-08-20

- Added explicit realization execution modes, including the distinction between agent-primary and software-primary control.
- Added the standard decision-precedence order for CRD consumers and agents.
- Added optional shared-element provenance and approved-reuse declarations.
- Added skill/tool relationship guidance and optional agentic mappings.
- Added audience-projection guidance for business, UX, frontend, backend, API/MCP/tools, agents, and operations.
- Added an internal `Reconcile payments` CRD example.
- Added the Working with CRDs guide explaining why CRD is not merely a feature, PRD, API document, skill, or MCP tool.

## 0.3.0 — 2026-08-20

- Refined the vocabulary: **Capability Documentation** is the framework; **Capability Requirements Document (CRD)** is the canonical artifact for one Capability MLE.
- Added Capability Inventory and Operational Capability Documentation as distinct concepts.
- Clarified that a CRD can exist independently of a PRD in a reusable or open inventory.

## 0.2.0 — 2026-08-20

- Renamed the project from the working name “Capability Documentation” to **Capability Requirements Documentation (CRD)**.
- Defined the reusable artifact as a **Capability Requirements Document (CRD)**, aligned with the familiar PRD naming pattern at capability scope.
- Added the CRD cube mark as the public site logo, favicon, and touch icon.

## 0.1.0 — 2026-08-18

- Established the initial Capability Documentation draft.
- Defined Capability MLE, Interaction Contract MLE, and Realization.
- Added the required semantic core and optional realization extensions.
- Added human template, agent transformation instructions, JSON Schema, and illustrative quote-request examples.
- Licensed the documentation under CC BY 4.0 with attribution to Valto Loikkanen.
