# Capability Documentation

Draft 0.4 (package release 0.6.0) — an open, technology- and implementation-agnostic framework for defining, cataloguing, and operating complete capabilities.

The canonical artifact is a **Capability Requirements Document (CRD)**: the requirement document for one Capability MLE. A capability may belong to a product, service, system, agent, or reusable open inventory; a CRD can be created before implementation or derived from existing systems, and it remains independent of any one realization mechanism.

The core model and Extract-mode workflow are stable and validated: the required-core fields haven't changed since Draft 0.4, and the [CRD Author skill](skills/crd-author/SKILL.md)'s Extract mode has been run against four independent real sources (a PRD, a real codebase, a real API/webhook documentation set) and each result independently blind-audited for both framework conformance and factual accuracy — see [CHANGELOG.md](CHANGELOG.md) for what each audit found and fixed. Define mode and some optional extensions (Arazzo/OpenAPI structured extraction, audience projections, Mermaid diagrams beyond one worked example) are specified but have not yet been exercised and audited the same way — treat those as reasonable but less-proven guidance. It is not a software runtime, a required product-management process, or an attempt to replace domain-specific documentation.

## Start here

> **A CRD is like a feature specification for the agentic era.**

It is smaller than a PRD and more rigorous than a typical feature definition. A CRD specifies one complete capability’s purpose, boundaries, requirements, interaction contracts, realizations, evidence, and unknowns—so people, agents, and software can work from the same durable meaning.

| Question | Short answer |
|---|---|
| **What?** | A CRD is the requirement document for one complete Capability MLE, not merely a feature, endpoint, component, or function. |
| **For whom?** | Product, domain, UX, and engineering people; AI agents; applications; and other software. |
| **Why?** | To prevent purpose, requirements, defaults, examples, implementation choices, operational constraints, and unknowns from being confused or lost between systems. |
| **How?** | Define a Capability MLE, its Interaction Contract MLEs, and one or more realizations; then trace the CRD to relevant UX, APIs, tools, code, tests, and operations. |

Read the public introduction at [valto.github.io/crd](https://valto.github.io/crd/).

## Core model

```text
Capability Documentation
  ├─ Capability Inventory
  │    └─ Capability MLE
  │         └─ Capability Requirements Document (CRD)
  │              ├─ one or more Interaction Contract MLEs
  │              └─ Operational Capability Documentation
  │                   └─ one or more Realizations
```

- **Capability Documentation**: the overall methodology, open standard, and resource.
- **Capability Inventory**: a catalogue of available or planned Capability MLEs and their CRDs.
- **Capability MLE**: the smallest complete, contextually meaningful ability that produces a meaningful outcome.
- **Capability Requirements Document (CRD)**: the canonical technology- and implementation-agnostic specification of one Capability MLE.
- **Interaction Contract MLE**: the smallest contextually meaningful executable behaviour.
- **Operational Capability Documentation**: documentation of a CRD’s current realization in a particular service or system.
- **Realization**: a software, agent, or combined implementation of a capability or interaction contract.

## Package

- [CRD Specification](crd-specification.md) — semantic model and conformance rules.
- [CRD template](crd-template.md) — minimal document form with optional extensions.
- [Minimum Logical Element (MLE)](minimum-logical-element.md) — origin, rationale, and the conceptual path to CRDs.
- [Working with CRDs](working-with-crds.md) — precedence, shared-element reuse, skill/tool mapping, audience projections, and why CRD is not merely a feature.
- [CRD vs PRD](crd-vs-prd.md) — concise boundaries between capability requirements, product requirements, feature specifications, user stories, APIs, skills, and tools.
- [CRD glossary](glossary.md) — canonical short definitions for the framework vocabulary.
- [CRD prompt for AI agents](agent-prompt.md) — a portable prompt for agents that cannot install the CRD Author skill.
- [Capability Inventory](capability-inventory.md) — a lightweight catalogue form for available or planned Capability MLEs, including known realizations.
- [Source Context Reference template](source-context-template.md) — a companion document for product-wide/cross-cutting context (why it exists, cross-cutting constraints, platform exposure, build sequencing) that no single CRD should own, but that shouldn't be lost either.
- [Agent transformation instructions](agent-transformation-instructions.md) — derive documentation from existing material without inventing facts.
- [Worked example](examples/request-moving-quote.md) — an illustrative CRD and realization.
- [Internal-capability example](examples/reconcile-payments.md) — an illustrative internal CRD with a software-primary realization.
- [Real-world example: Open a pull request](examples/open-pull-request.md) / [Merge a pull request](examples/merge-pull-request.md) — extracted from GitHub's own public REST API and webhook documentation (not synthetic), independently blind-audited for framework conformance and factual accuracy; see the accompanying [provenance table](examples/github-pull-request-provenance.md) and [decision log](examples/github-pull-request-decision-log.md).
- [JSON Schema](schema/crd.schema.json) — portable machine-readable representation of the required core.
- [JSON example](examples/request-moving-quote.json) — schema-conforming illustrative instance.
- [CRD Author skill](skills/crd-author/SKILL.md) — a packaged agent skill that writes CRDs (Define mode) or extracts them from existing material (Extract mode) and maintains a Capability Inventory.
- [Inventory HTML template](inventory-html-template.html) — a dependency-free static index page for browsing a Capability Inventory, produced only on request. Used together with [crd-html-template.html](crd-html-template.html) (one per capability) and [doc-html-template.html](doc-html-template.html) (one per supporting doc), so the whole showcase is HTML — no link in it lands on a raw `.md` file.

The published documentation also exposes an [LLM resource map](https://valto.github.io/crd/llms.txt), generated Markdown views, the JSON Schema, examples, and the CRD Author skill directly from the documentation host.

## Quick start

1. Read the [CRD Specification](crd-specification.md).
2. Copy the [CRD template](crd-template.md) for a reusable capability.
3. Use the [Agent transformation instructions](agent-transformation-instructions.md) to derive documentation from existing material without inventing facts, producing a [Source Context Reference](source-context-template.md) alongside the CRDs when extracting from one substantial source. An agent can also run this end to end via the [CRD Author skill](skills/crd-author/SKILL.md).
4. Validate a structured representation against the JSON Schema where machine interchange is useful.

## License and attribution

This repository is licensed under [Creative Commons Attribution 4.0 International](LICENSE). Reuse and adaptation are welcome, including commercially, provided appropriate attribution is given to **Valto Loikkanen**. See [NOTICE](NOTICE) for the requested attribution form.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). This first draft intentionally keeps the required core small; proposed additions should demonstrate why they preserve contextual logical meaning rather than turn a CRD into a mini-PRD.

The initial draft deliberately does not prescribe a single serialization format, repository layout, or runtime. Markdown is the human form and JSON Schema is the initial portable machine-interchange form.

## Compatibility note

The project was briefly published under the name **Capability Requirements Documentation (CRD)**. The refined vocabulary restores **Capability Documentation** as the overall framework and reserves **CRD** for the canonical per-capability artifact.
