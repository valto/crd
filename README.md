# Capability Documentation

Draft 0.1 — a technology- and implementation-agnostic way to document capabilities so that humans, agents, applications, and developers can understand, use, build, compose, and operate them.

This is an early, reviewable specification draft. It is not a software runtime, a required product-management process, or an attempt to replace domain-specific documentation.

## Core model

```text
Product / Service / Application
  └─ Capability MLE
       └─ one or more Interaction Contract MLEs
            └─ one or more Realizations
```

- **Capability MLE**: the smallest complete, contextually meaningful ability that produces a meaningful outcome.
- **Interaction Contract MLE**: the smallest contextually meaningful executable behaviour.
- **Realization**: a software, agent, or combined implementation of a capability or interaction contract.

## Package

- [Specification](capability-documentation-specification.md) — semantic model and conformance rules.
- [Human template](capability-document-template.md) — minimal document form with optional extensions.
- [Agent transformation instructions](agent-transformation-instructions.md) — derive documentation from existing material without inventing facts.
- [Worked example](examples/request-moving-quote.md) — an illustrative capability definition and realization.
- [JSON Schema](schema/capability-definition.schema.json) — portable machine-readable representation of the required core.
- [JSON example](examples/request-moving-quote.json) — schema-conforming illustrative instance.

## Quick start

1. Read the [Specification](capability-documentation-specification.md).
2. Copy the [Human template](capability-document-template.md) for a reusable capability.
3. Use the [Agent transformation instructions](agent-transformation-instructions.md) to derive documentation from existing material without inventing facts.
4. Validate a structured representation against the JSON Schema where machine interchange is useful.

## License and attribution

This repository is licensed under [Creative Commons Attribution 4.0 International](LICENSE). Reuse and adaptation are welcome, including commercially, provided appropriate attribution is given to **Valto Loikkanen**. See [NOTICE](NOTICE) for the requested attribution form.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). This first draft intentionally keeps the required core small; proposed additions should demonstrate why they preserve contextual logical meaning rather than turn a Capability Document into a mini-PRD.

The initial draft deliberately does not prescribe a single serialization format, repository layout, or runtime. Markdown is the human form and JSON Schema is the initial portable machine-interchange form.
