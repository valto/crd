# Capability Documentation: CRD Specification

Status: Draft 0.4

## 1. Purpose

**Capability Documentation** is the common, implementation- and technology-agnostic framework through which humans, agents, applications, and developers can understand, use, build, compose, and operate capabilities.

Its canonical per-capability artifact is a **Capability Requirements Document (CRD)**: the requirement document for one Capability MLE. A CRD defines what must remain meaningful and true regardless of whether the capability is realized through software, an agent, MCP, an API, UI, or a future mechanism.

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

Every realization MUST declare its **execution mode**:

| Execution mode | Meaning |
|---|---|
| `software-primary` | Software or a deterministic workflow controls the capability flow. |
| `agent-primary-using-software` | An agent controls the capability flow and invokes software, tools, or services as needed. |
| `software-primary-calling-agents` | Software or a deterministic workflow controls the flow and calls an agent only at defined steps. |
| `unknown` | The runtime control relationship is not yet established. |

`agent-built-software` is implementation provenance, not an execution mode: it says how a realization was constructed, not what controls it at runtime. The distinction between `agent-primary-using-software` and `software-primary-calling-agents` is material because it determines authority, fallback, observability, and failure handling.

**Operational Capability Documentation** describes the current realization of a CRD in a particular service or system. It records realization-specific rationale, constraints, exposures, dependencies, evidence, and operating context without changing the reusable CRD itself.

### 3.4 Capability Inventory

A Capability Inventory is a catalogue of available or planned Capability MLEs. Each entry SHOULD link to a CRD when one exists. A CRD MAY exist independently in a reusable or open inventory; it does not require a Product Requirements Document (PRD) above it.

### 3.5 Cardinality

A capability MAY have one or many interaction contracts. A contract MAY have one or many realizations. The same component, endpoint, function, or tool MAY support multiple capabilities. No one-to-one mapping is implied.

### 3.6 Skill and tool relationship

A **tool** is an executable primitive, such as a function, API operation, MCP tool, command, or workflow step. A tool is not automatically a capability: it may be too small to retain complete purpose context.

A **skill** is an agentic realization package that guides an agent in performing work. A skill MAY realize one Capability MLE, bundle several Capability MLEs, or use tools that support many capabilities.

The relationship is therefore many-to-many:

```text
Capability MLE ↔ Skill ↔ Tool
```

A capability MAY be the MLE of a skill when the skill has one complete contextual purpose. A skill MUST NOT be assumed to equal one capability merely because it has a name or a tool interface.

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
| `implementation-requirement` | Explicit requirement of a particular realization. |
| `recommended default` | Normal behaviour unless deliberately overridden. |
| `example` | Illustrative and non-binding unless explicitly promoted to a rule. |
| `implementation choice` | Current, replaceable realization. |
| `operational constraint` | Restriction of one realization, not the reusable capability. |
| `unknown/unresolved` | Intentionally unspecified, uncertain, or awaiting decision. |
| `explicit fact` | Directly supported by a source. |
| `reasonable inference` | Supported interpretation that is not directly stated. |

`capability purpose` MUST remain distinct from `rationale/intent`. For example, the general purpose of `Convert currency` is enabling conversion of monetary values; a business rationale might be that a particular service has international customers.

### 6.1 Decision precedence

When a consumer, implementation, or agent encounters competing applicable guidance, it MUST resolve it in this order:

```text
1. Rule / invariant
2. Explicit implementation requirement
3. Explicit owner or user choice
4. Recommended default
5. Agent judgment
```

A lower-precedence item MUST NOT override a higher-precedence item. If two items at the same precedence level conflict or their scope is unclear, the consumer MUST surface the conflict as `unknown/unresolved` or request a decision rather than silently choosing.

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
- execution mode and agentic mappings
- shared-element reuse approvals
- audience projections

These become important when documenting a particular operational realization.

### 7.1 Shared elements and approved reuse

When a lower-level element is shared across capabilities, a CRD MAY declare its provenance and approved reuse:

```text
shared element: customer-identity-validation
created for: customer-onboarding
approved reuse: [request-moving-quote, submit-insurance-claim]
```

This does not imply exclusive ownership. It records the capability context in which an element originated and the capability contexts in which reuse has been explicitly accepted. Reuse approval is especially useful when shared tools, components, prompts, schemas, or workflows carry domain assumptions that should not be silently generalized.

### 7.2 Audience projections

One canonical CRD MAY be projected into audience-specific views without creating divergent requirements. Typical projections answer:

| Audience | Primary questions |
|---|---|
| Business / domain | Why does this capability exist, what outcome and rules matter? |
| UX | Who acts, what states and choices exist, and what outcomes must be intelligible? |
| Frontend | What representations and interaction constraints are required? |
| Backend | What transitions, invariants, effects, and integrations must hold? |
| API / MCP / tools | What commands, contracts, inputs, outputs, and authority boundaries exist? |
| Agent | What authority, grounding, precedence, approval, and escalation rules apply? |
| Operations | Which realization is active, how is it observed, and what constraints or fallback paths exist? |

Projections SHOULD be traceable to the canonical CRD. They MUST NOT silently introduce requirements that are absent from it.

## 8. Boundary rules

Boundaries MUST identify included and excluded concerns. They SHOULD distinguish a capability from adjacent capabilities, reusable primitives, and implementation detail. Boundaries are the primary protection against a capability expanding into a vague feature bucket.

## 9. Conformance

A document conforms as a **Capability Requirements Document (CRD)** when it satisfies section 4 and all defined contracts satisfy section 5. It conforms as an **Operational Capability Realization** when it additionally documents the realization-specific constraints, references, and evidence it chooses to expose.
