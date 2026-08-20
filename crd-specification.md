# Capability Requirements Documentation (CRD) Specification

Status: Draft 0.2

## 1. Purpose

Capability Requirements Documentation (CRD) is the common, implementation- and technology-agnostic way to express the requirements of a complete capability. A **Capability Requirements Document (CRD)** gives humans, agents, applications, and developers a shared basis to understand, use, build, compose, and operate that capability.

This specification preserves the Minimum Logical Element (MLE) principle: the document requires only the information necessary for a capability to retain contextual logical meaning. Detail that belongs to a particular implementation is optional.

## 2. Normative terms

**MUST** means required for a conforming Capability Requirements Document (CRD). **SHOULD** means recommended unless a documented reason exists not to follow it. **MAY** means optional.

## 3. Model

### 3.1 Capability MLE

A Capability MLE is the smallest complete ability that retains sufficient contextual logical meaning and produces a meaningful outcome.

It MAY be externally visible, agent-facing, application-facing, or internal. It MUST NOT be enlarged merely because a larger grouping is possible.

### 3.2 Interaction Contract MLE

An Interaction Contract MLE is the smallest contextually meaningful executable behaviour within a capability. Its abstract kernel is:

```text
Actor + Command + Current State
  -- subject to Policies/Invariants -->
New State + Result + Events/Effects
```

An interaction contract is independent of whether it is exposed through a UI, API, MCP tool, workflow, event consumer, function, or agent.

### 3.3 Realization

A realization is a particular operational implementation of a capability or interaction contract. A capability can have zero, one, or many realizations. A realization can be software, an agent, software plus agents, or agent-built software.

### 3.4 Cardinality

A capability MAY have one or many interaction contracts. A contract MAY have one or many realizations. The same component, endpoint, function, or tool MAY support multiple capabilities. No one-to-one mapping is implied.

## 4. Capability Requirements Document (CRD): required core

A conforming CRD MUST contain:

| Field | Meaning |
|---|---|
| `name` | Stable, concise capability name. |
| `definition` | What the ability is, without implementation detail. |
| `capability purpose` | The general outcome the ability exists to enable. |
| `boundaries` | What belongs inside the capability and what explicitly does not. |
| `meaningful outcome` | The condition or result that makes the ability complete. |
| `interaction contracts` | At least one named contract, or an explicit unknown explaining why none is defined yet. |
| `rules/invariants` | Binding statements, or an explicit statement that none are known. |
| `recommended defaults` | Normal behaviour when no explicit choice overrides it, or an explicit statement that none are known. |
| `unknowns/unresolved questions` | Deliberately unspecified, uncertain, or pending information. |

The definition SHOULD be independently understandable and meaningfully invokable. It SHOULD be split when its parts retain the same purpose context independently; it SHOULD be combined when isolated parts lose that context.

## 5. Interaction Contract: required core

Each defined Interaction Contract MUST include:

| Field | Meaning |
|---|---|
| `name` | Concise behaviour name. |
| `actor` | Who or what initiates it; use `unknown` if not established. |
| `command/intent` | The requested action or intent. |
| `current state` | Required starting state or context. |
| `policies/invariants` | Conditions that govern validity. |
| `transition` | State change, or an explicit statement that no state changes. |
| `result` | Direct outcome delivered to the actor or caller. |
| `events/effects` | Material emitted events, side effects, or an explicit `none known`. |

## 6. Documentation semantics

Every substantive statement SHOULD be assigned one of these semantic classes:

| Class | Meaning |
|---|---|
| `capability purpose` | General outcome the ability exists to enable. |
| `rationale/intent` | Why a particular organization chose the capability or realization. |
| `rule/invariant` | Binding requirement. |
| `recommended default` | Normal behaviour unless deliberately overridden. |
| `example` | Illustrative and non-binding unless explicitly promoted to a rule. |
| `implementation choice` | Current, replaceable realization. |
| `operational constraint` | Restriction of one realization, not the reusable capability. |
| `unknown/unresolved` | Intentionally unspecified, uncertain, or awaiting decision. |
| `explicit fact` | Directly supported by a source. |
| `reasonable inference` | Supported interpretation that is not directly stated. |

`capability purpose` MUST remain distinct from `rationale/intent`. For example, the general purpose of `Convert currency` is enabling conversion of monetary values; a business rationale might be that a particular service has international customers.

## 7. Optional extensions

The following are optional and MUST NOT be required merely to classify something as a capability:

- operational realization and availability
- ownership, lifecycle, and implementation/business rationale
- API, MCP, tool, event, or UI exposure
- implementation and dependency references
- UX representations and user stories
- test evidence, telemetry, SLOs, or audit trail
- provenance and source links
- authorization, agent authority, grounding/context, and approval gates

These become important when documenting a particular operational realization.

## 8. Boundary rules

Boundaries MUST identify included and excluded concerns. They SHOULD distinguish a capability from adjacent capabilities, reusable primitives, and implementation detail. Boundaries are the primary protection against a capability expanding into a vague feature bucket.

## 9. Conformance

A document conforms as a **Capability Requirements Document (CRD)** when it satisfies section 4 and all defined contracts satisfy section 5. It conforms as an **Operational Capability Realization** when it additionally documents the realization-specific constraints, references, and evidence it chooses to expose.
