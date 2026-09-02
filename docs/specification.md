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

A candidate that passes the MLE test's five questions (§3.1) on a literal reading — it has an actor, a command, a determinable result — is not automatically a capability if that actor is only "a developer manually running this for pre-release verification" and the candidate has no recurring operational role in the running system and is not itself exposed for a third party or agent to invoke. Such a candidate is presumptively a **tool** or **implementation/test scaffolding**, not a capability, regardless of how well-documented or well-tested it is. Documentation quality and test coverage establish that a tool is good engineering; they do not establish that it is a capability. Promote it to a capability only when it serves a recurring operational purpose within the product (compare the internal `Reconcile payments` example, which runs repeatedly as real business operation, not a one-time developer check) or when it is exposed for someone other than the building developer to invoke.

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
- tags
- related MLEs by dimension, including Communication MLEs (§7.4)

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

### 7.3 Tags

A CRD MAY declare a small set of universal tags for dimensions that are not already derivable from its required fields (§4) and that stay meaningful regardless of which product realizes the capability. Reserve a tag for what isn't already implied elsewhere: do not tag `read-only` when every Interaction Contract's `transition` already states none; do not tag `internal`/`user-facing` when `exposure` (§7) already says so. A hand-authored tag that duplicates a derivable fact tends to drift from that fact over time — prefer deriving over tagging whenever a field already settles the question.

Choose the tag whose dimension a statement is actually about, not the nearest-sounding one. A common mistake is reaching for `network-touching` whenever a source mentions an API call or a network-triggered side effect, when the statement's actual point is a different dimension:

| Tag | Use it for | Do not use it for |
|---|---|---|
| `network-touching` / `local-only` | Whether reaching this capability's outcome requires leaving the local device or process — meaningful for a local-first, hybrid, or offline-capable system where some capabilities complete entirely on-device and others don't. | A capability inside a product that is uniformly a hosted network service, where every capability is network-touching by construction and the tag would only restate what `exposure` (§7) already implies. |
| `notification-triggering` | Invoking this capability causes a notification, alert, or message to be sent to a person, as a side effect distinct from any network activity. | A side effect that is really about the network round-trip itself, not about a person being notified. |
| `data-sensitive` | This capability reads, writes, or otherwise handles sensitive or private data as part of its core operation. | Data sensitivity that a boundary or a contract's `policies/invariants` already states explicitly. |
| `identity-related` | This capability's core operation is about establishing, verifying, or managing who someone is. | A capability merely invoked by an already-authenticated actor — that's the contract's `actor` field, not a tag. |

An Operational Capability Documentation extension MAY separately declare **implementation tags** — product-specific groupings (a module, domain, or internal team name) meaningful only within that realization. Implementation tags MUST be clearly distinguished from the CRD's own universal tags and MUST NOT be presented as if they describe the reusable capability generally (a common convention is prefixing each one, e.g. `impl:inbox`).

A rendered projection (e.g. an HTML showcase) SHOULD keep the visual "tag" badge convention exclusive to implementation tags. A universal tag conventionally drives structure instead — a grouping or section key (e.g. one tab segmented by universal tag, another by implementation tag) — or appears as plain text where structure isn't practical, rather than as an inline badge indistinguishable from an implementation tag's.

### 7.4 Related MLEs by Dimension

A CRD MAY declare traceability links from its Capability MLE to lower-level, discipline-specific MLEs across these dimensions: Business/Domain, UX/Experience, Communication, Interaction/Behaviour, Frontend/Interface, Backend/Execution, Data/Information, API/Interoperability, Agentic, Verification, Operations. Each link states a `dimension`, a `relationship` (`defines`, `implements`, `supports`, `constrains`, `verifies`, `exposes`, or `reused_by`), and a reference to the related MLE — by name, or by link when the related MLE is documented elsewhere.

This section is traceability, not required coverage. A capability MUST NOT be required to have an entry in every dimension, and a dimension with no genuine content MUST be omitted rather than filled to appear complete — the same principle that governs every other optional CRD section (§7). A link records provenance and impact visibility (which capabilities does this lower-level MLE support; which lower-level MLEs does this capability depend on) without duplicating the linked MLE's own content into the CRD.

**Communication is a first-class dimension**, not a subcategory of UX. A message's intended meaning is frequently shaped by business rules, rendered by frontend or delivery infrastructure, and localized independently — no single discipline owns it, which is exactly why it needs its own dimension rather than being buried in UX or treated as a frontend string.

A **Communication MLE** is the smallest contextually meaningful communication unit whose intended meaning should remain consistent across channels, interfaces, actors, and languages. Its required core:

| Field | Meaning |
|---|---|
| `name` | Concise identifier for the communication. |
| `purpose` | What understanding or commitment this communication establishes. |
| `trigger` | The event or state that causes this communication. |
| `audience` | Who receives it. |
| `required meaning` | The meaning that MUST survive regardless of channel or language — not the wording. |
| `representative example text` | A concrete rendering of the required meaning, explicitly classified as an `example`; use sourced wording where available, otherwise label it illustrative. |
| `possible realizations` | Known or anticipated channels (inline UI, toast, email, push, SMS, agent response, etc.). |

The representative example text makes the canonical meaning concrete; it does **not** make its wording a requirement. It MUST be semantically classified as an `example`. When an authoritative source supplies the actual communication, preserve that wording and its source. When no authoritative wording exists, provide a clearly labelled illustrative rendering and never imply it is shipped or production copy.

Optional fields (terminology, tone/style, rules, recommended defaults) follow the same semantic classes as §6 — a commitment like a response-time promise is a `rule/invariant` only if the realization actually guarantees it, otherwise it is at most a `recommended default`.

A Communication MLE's realization chain is: **canonical meaning → channel realization → language realization**. This is stronger than a typical string-key → translation localization model because it separates meaning from both channel and language, not just from source code — a channel realization (e.g. "toast") and a language realization (e.g. a Finnish translation of that toast) are both downstream of one canonical meaning, not siblings of it.

Not every communication needs the full template — a one-line internal toast may need only the required core and its representative example text. Omit optional fields that add nothing, per §7's general rule for optional sections.

**Relationship to Source Context Reference:** an individual Communication MLE is owned by the capability whose trigger produces it, the same as any other dimension link — it is not, by itself, product-wide context. But the *tone and terminology conventions* multiple Communication MLEs should follow (e.g. "call it a `quote request`, never an `application`, anywhere in the product") often are product-wide and cross-cutting. When a Source Context Reference already exists for a product, a Communication MLE MAY reference it for those shared conventions rather than restating them; this does not change SCR's own scope (§ Source Context Reference — it still preserves context, not capability requirements) and does not make Communication itself an SCR-owned dimension.

## 8. Boundary rules

Boundaries MUST identify included and excluded concerns. They SHOULD distinguish a capability from adjacent capabilities, reusable primitives, and implementation detail. Boundaries are the primary protection against a capability expanding into a vague feature bucket.

## 9. Conformance

A document conforms as a **Capability Requirements Document (CRD)** when it satisfies section 4 and all defined contracts satisfy section 5. It conforms as an **Operational Capability Realization** when it additionally documents the realization-specific constraints, references, and evidence it chooses to expose.
