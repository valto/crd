# Changelog

## Unreleased

- Made representative example text a required part of every documented Communication MLE. The text is always semantically an `example`: actual source wording is preserved when available; otherwise the example must be explicitly illustrative and must not be presented as shipped or binding copy. Updated the specification, template, JSON Schema, validator, CRD Author skill, and guidance accordingly.

## 0.7.0 — 2026-09-01

- Added complete technical SEO metadata across the documentation site: canonical URLs, unique search-focused titles and descriptions, Open Graph and social-card metadata, structured data, breadcrumbs, visible provenance, a complete sitemap, and `noindex` handling for the 404 page.
- Added agent-facing publication assets: `llms.txt`, generated `llms-full.txt`, direct Markdown copies, the published JSON Schema, JSON/Markdown examples, and the CRD Author `SKILL.md` endpoint.
- Added dedicated CRD-vs-PRD, glossary, and AI-agent prompt resources; reduced homepage prompt duplication while preserving direct prompt and skill access.
- Added deterministic build and validation scripts plus CI gates for metadata, links, sitemap parity, generated-source consistency, and machine-readable endpoints.
- Fixed the homepage agent-resource link contrast and prevented large media and PDF resources from loading eagerly.
- Sharpened the "zero known realizations" wording (`agent-transformation-instructions.md`, `capability-inventory.md`, and the corresponding site pages) after an external review noted the original phrasing conflated two different claims: a capability with no realization can still be a valid *planned* requirement; what's unproven is a claim that it's *generalized/reusable*, and cross-context reuse specifically remains unproven until a second real consumer exists or is imminent. Mirrored into the CRD Author skill's bundled copies. Added the rationale for the rule to `docs/inventory.html`, which previously only asserted it.
- Added **Related MLEs by Dimension** (`crd-specification.md` §7.4, `crd-template.md`, `schema/crd.schema.json`, `scripts/validate.py`): an optional traceability section linking a Capability MLE to lower-level discipline-specific MLEs across eleven dimensions, with explicit relationship types (`defines`, `implements`, `supports`, `constrains`, `verifies`, `exposes`, `reused_by`). Traceability only — a capability must not be required to have an entry in every dimension, and an empty dimension must be omitted, not filled.
- Added **Communication** as a first-class dimension and **Communication MLE** as a documented concept, rather than a UX subcategory: the smallest contextually meaningful communication unit whose intended meaning should stay consistent across channels, interfaces, actors, and languages, with a canonical-meaning → channel-realization → language-realization chain. Resolved the open design question (is Communication always capability-owned, or does some of it belong in Source Context Reference?) with a trial decomposition of `examples/reconcile-payments.md`/`.json`/`.html`: the message itself is capability-owned, while cross-cutting tone/terminology conventions may optionally live in and be referenced from a product's SCR — the two are complementary, not competing. This extension is specified and trial-validated on one example, not yet independently blind-audited the way the core Extract-mode model has been — see the README's evidence-level note.
- Added the framework's fifth worked example, **Schedule a meeting** (`examples/schedule-a-meeting.md`/`.json`, `docs/examples/schedule-a-meeting.html`): one illustrative capability with two realizations — `agent-primary-using-software` and `software-primary` — sharing the same Interaction Contract MLEs, with an explicit implementation requirement gating any calendar write behind requester/participant confirmation. Makes the framework's agentic thesis concrete rather than conceptual.
- Restructured `docs/examples.html` into three categories (Learn the boundary; See CRD extracted from real software; Agentic realizations) and added an explicit learning-objective note (why is this a Capability MLE, what does it teach, what's its evidence status) to the top of all five example pages. Added a "too broad vs. correct MLEs" demonstration block using Open/Merge pull request to show why `Manage pull requests` would be one capability too many. Made **Merge a pull request** the flagship real-world example, calling out explicitly that capability meaning stays simple and stable while realization complexity (draft gating, required reviews, status checks, five merge methods, five distinct realizations) grows underneath it.
- Reordered the homepage's "Start here" resource grid into an enforced dominant path (Learn → Specification → Template → Examples) followed by a separate "Advanced material" section (Inventory, Source Context, Agent instructions, Working with CRDs, Media, CRD Author skill), added a compact end-to-end visual (`Product/Service/Agent → Capability Inventory → CRD per Capability MLE → Interaction Contracts → Realizations → UI/API/MCP/Skill/Code`) near the top of the page, and collapsed the full copyable agent prompt behind a closed-by-default `<details>` disclosure instead of showing it inline in full.
- Source for the non-SEO changes above: an external ChatGPT review of the site's evolution, captured and planned in `My-world-wiki/crd-framework.md` before implementation.

## 0.6.0 — 2026-08-26

- Sharpened tag-selection guidance (`crd-specification.md` §7.3) with a disambiguation table after a real extraction reached for `network-touching` when the actual dimension was `notification-triggering`: `network-touching`/`local-only` is only meaningful for a local-first/hybrid system where capabilities genuinely differ on this, not for a capability inside a uniformly hosted service (where it would only restate `exposure`). Mirrored into `crd-template.md`, `agent-transformation-instructions.md`, the CRD Author skill (both copies), and the corresponding site pages, plus a new "what not to do" bullet warning against defaulting to `network-touching`.
- Added the CRD framework's third and fourth worked examples — `examples/open-pull-request.md`/`.json` and `examples/merge-pull-request.md`/`.json`, plus `docs/examples/open-pull-request.html` and `docs/examples/merge-pull-request.html` — a real, publicly-sourced pair (GitHub's own "Open/Merge a pull request," extracted via Extract mode against GitHub's real public REST API, webhook, and branch-protection docs) alongside the two existing synthetic examples. Independently blind-audited for framework conformance and factual accuracy against GitHub's live docs: one real defect found and fixed (GitHub's merge queue is a confirmed automated realization of the merge capability, not merely unresolved) plus three provenance/tag cleanups, which also prompted the tag-selection disambiguation guidance described below. Supporting `github-pull-request-provenance.md`, `-decision-log.md`, and `-unresolved.md` carry the full statement-provenance table, combine/decompose reasoning, and open questions. Added two new cards to `docs/examples.html`.
- Reworked the HTML inventory showcase (`inventory-html-template.html`) into a CSS-only, zero-JavaScript two-tab layout (radio input + label + `:checked` sibling selector): one tab segmented by universal tag, one by implementation tag/domain. Reserved the visual tag/badge convention (`<span class="tag">`) exclusively for implementation tags — a universal tag now drives structure (a tab/section key) or renders as plain text, never a badge, so "tag" reads unambiguously in every rendered projection. Updated `crd-specification.md` §7.3, `crd-template.md`, `capability-inventory.md`, `schema/crd.schema.json` descriptions, `agent-transformation-instructions.md`, the CRD Author skill, `crd-html-template.html`, and the corresponding site pages to match. Also fixed `crd-html-template.html`'s footer, which linked to the raw `.md` source — every other template already avoided that.
- Added a rule (`crd-specification.md` §3.6) distinguishing a capability from a tool/test scaffolding: a candidate whose actor is only "a developer manually running this for pre-release verification," with no recurring operational role and no exposure beyond that developer, is presumptively a tool, however well-documented and well-tested it is. Added to the specification, the agent transformation instructions, the CRD Author skill, and the corresponding site pages.
- Added `inventory-html-template.html`, `crd-html-template.html`, and `doc-html-template.html` — a user-facing inventory showcase must be entirely HTML; the first attempt only rendered the index and linked out to raw `.md` files, which isn't user-facing at all. The three templates together render the index, one page per CRD, and one page per supporting doc, all dependency-free and produced only on request.
- Added optional `tags` (`crd-specification.md` §7.3): universal tags for dimensions not already derivable from another required field (e.g. `network-touching`/`local-only`, `data-sensitive`), plus realization-level implementation tags for product-specific groupings, always distinguishable from universal tags (a consistent prefix such as `impl:`). Added to the specification, template, schema, capability inventory format, agent transformation instructions, the CRD Author skill, and the HTML templates (as a Tags column/badge, plus optional static grouping by domain).
- Added Arazzo workflow documents to the recognized Extract-mode source material, with guidance to treat a declared workflow as a candidate-capability hypothesis and each step as candidate-contract evidence — still subject to the MLE test, not an automatic boundary.

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
