# Minimum Logical Element (MLE)

## Definition

An MLE is the smallest bundled unit that still retains logical sense and context when considered across business, design, and development perspectives.

The word **logical** matters. An MLE is not simply the smallest technical artifact, the smallest UI part, or the smallest backlog item. It is the smallest unit that can still be understood as something meaningful in its own context.

## Why MLE was needed

Software work is commonly fragmented into requirements, stories, screens, components, APIs, functions, schemas, tests, and operational processes. Each is useful, but none alone necessarily represents a complete, meaningful unit of the product.

The MLE lens asks two complementary questions:

1. What is the smallest meaningful unit within this discipline?
2. What is the smallest meaningful unit when the relevant disciplines are considered together?

It prevents two opposite failures:

- **Feature buckets** that become too broad to explain, govern, implement, or reuse coherently.
- **Fragments** such as a component, endpoint, or data field that are too small to retain the purpose they serve.

## Early cross-discipline framing

The original EcosystemOS material applied the MLE idea to several disciplines:

| Discipline | Example MLE |
|---|---|
| UX/UI | User Story |
| Data modelling | Bounded Context |
| Frontend | Element Component |
| Backend | Use Case |

These are not a claim that every discipline has a universal one-to-one unit. They demonstrate the core observation: every relevant level has its own minimum logical element.

## From MLE to Capability MLE

The next question was: what is the MLE of a complete software capability?

The answer is a **Capability MLE**:

> The smallest complete, contextually meaningful ability that produces a meaningful outcome.

For example, `Request a moving quote` can be a Capability MLE. It can be independently understood, invoked, implemented, tested, and composed. Splitting it into arbitrary implementation pieces loses its purpose context; expanding it into all quote management makes it a vague feature bucket.

## Why this leads to a CRD

A Capability MLE needs a durable, technology-agnostic requirement specification. That is the role of the **Capability Requirements Document (CRD)**.

```text
Minimum Logical Element principle
        ↓
Capability MLE
smallest complete meaningful ability
        ↓
Capability Requirements Document (CRD)
canonical requirements specification for that ability
        ↓
Interaction Contract MLEs
smallest executable behaviours
        ↓
Operational Capability Documentation
current realizations in software, agents, APIs, MCP, UI, and workflows
```

The CRD does not replace a PRD. A PRD can describe a product or application and link to several CRDs. A CRD can also exist independently in a reusable Capability Inventory.

## What MLE contributes to the CRD model

MLE is the scope discipline that keeps a CRD useful:

- The CRD is not a broad product area or undifferentiated feature request.
- It is not a documentation wrapper around one endpoint, screen, component, or function.
- It carries enough context—purpose, boundaries, requirements, contracts, and unknowns—to remain meaningful across implementations.

This is why CRD can become common ground for people, agents, applications, and developers without being tied to one technology or one current realization.

## Source and status

This background is derived from Valto Loikkanen’s original *Tools of EcosystemOS — TechStack for Ecosystem Orchestration* material and subsequent CRD development. It is a conceptual background document, not a fixed claim that the discipline examples are universal or final.
