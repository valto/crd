# CRD vs PRD

A **Capability Requirements Document (CRD)** specifies one complete capability independently of its current implementation. A **Product Requirements Document (PRD)** usually coordinates a product initiative, including its goals, users, scope, priorities, delivery context, and multiple features or capabilities.

Neither replaces the other. A PRD may explain why a product change should happen and how it fits a roadmap; one or more CRDs can preserve the durable meaning of the complete capabilities involved.

## Comparison

| Question | CRD | PRD |
|---|---|---|
| Primary unit | One Capability MLE | A product, initiative, release, or problem space |
| Main purpose | Preserve what one complete capability means and must keep true | Coordinate product intent, outcomes, scope, priorities, and delivery |
| Implementation stance | Technology- and implementation-agnostic at the reusable layer | May contain product- and implementation-specific decisions |
| Typical contents | Purpose, outcome, boundaries, contracts, rules, defaults, unknowns, provenance, realizations | Goals, users, problems, requirements, priorities, milestones, metrics, dependencies |
| Useful lifetime | Can remain stable across several realizations | Often tied to a product initiative or planning cycle |
| Relationship | May be created independently or derived from a PRD | May contain or point to several capabilities and CRDs |

## CRD versus adjacent artifacts

- **Feature specification:** often describes a product-visible change. A CRD is scoped by a complete meaningful ability, whether or not it is presented as a feature.
- **User story:** expresses a user-centered need or slice of work. A CRD preserves the complete capability, including rules, contracts, evidence, and unknowns.
- **API or MCP specification:** defines an interface or protocol. It may realize part of a capability but does not necessarily preserve the capability's complete purpose context.
- **Skill:** packages agent behavior and instructions. A skill may realize one capability or bundle several capabilities.
- **Tool:** provides an executable primitive. A tool may support many skills and capabilities without being a complete capability itself.

## When to use each

Use a PRD when a team needs to align a product initiative, opportunity, audience, priority, and delivery context. Use a CRD when people, agents, and software need a durable specification of one complete capability that can survive changes in UI, code, API, agent, or operating model.

Use both when a product initiative contains capabilities whose meaning must remain traceable after the original roadmap or implementation changes.

## Authority

This comparison is guidance. The normative definition and conformance rules are in the [CRD Specification](crd-specification.md).
