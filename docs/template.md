# Capability Requirements Document (CRD) Template

Use this template for a reusable Capability Requirements Document (CRD). Remove optional sections that add no contextual meaning; do not replace unknown information with invention.

## Identity

- **Name:**
- **Definition:**
- **Status:** draft | active | deprecated | unknown

## Core meaning

- **Capability purpose:**
- **Meaningful outcome:**
- **Boundaries — includes:**
- **Boundaries — excludes:**
- **Terms and concepts:**
- **Tags (optional):** universal only — a dimension not already derivable from another field. Pick the tag whose dimension the statement is actually about, not the nearest-sounding one (see `crd-specification.md` §7.3's disambiguation table — e.g. a notification side effect is `notification-triggering`, not `network-touching`, and `network-touching`/`local-only` is only useful when some of the product's capabilities genuinely differ on this, not for a capability inside a uniformly hosted service). Omit rather than restate what `exposure` or a contract's `transition` already says. In a rendered projection, these typically become a grouping/section key (or plain text), not a badge — the visual tag/badge convention is reserved for implementation tags below.

## Interaction Contract MLEs

### [Contract name]

- **Actor:**
- **Command / intent:**
- **Current state:**
- **Policies / invariants:**
- **Transition:**
- **Result:**
- **Events / effects:**
- **Unknowns:**

## Rules and defaults

### Rules / invariants

-

### Recommended defaults

-

### Decision precedence

Apply the standard order unless a higher-level governing policy explicitly establishes another order:

```text
Rule / invariant
→ explicit implementation requirement
→ explicit owner or user choice
→ recommended default
→ agent judgment
```

## Unknown / unresolved

-

## Optional: operational realization

- **Realization name and status:**
- **Execution mode:** software-primary | agent-primary-using-software | software-primary-calling-agents | unknown
- **Implementation/business rationale:**
- **Owner / operating context:**
- **Operational constraints:**
- **Exposure:** UI | API | MCP | tool | event | workflow | internal
- **Implementation tags (optional):** product-specific groupings meaningful only to this realization (e.g. `impl:inbox`) — never the CRD's own universal tags, and always distinguishable from them (a consistent prefix such as `impl:` is a common convention). In a rendered projection, this is the only kind of tag shown as a visual badge.
- **Implementation references:**
- **UX representations:**
- **Tests / verification:**
- **Telemetry / audit:**
- **Authority, grounding, approval gates:**
- **Provenance:**

## Optional: shared elements and approved reuse

| Shared element | Kind | Created for capability | Approved reuse by capabilities | Notes |
|---|---|---|---|---|
|  | tool |  |  |  |

## Optional: agentic mappings

| Element | Kind | Relationship to this Capability MLE | Notes |
|---|---|---|---|
|  | skill | realizes one capability |  |
|  | tool | executable primitive used by a contract |  |

## Optional: Related MLEs by Dimension

Traceability only — omit any dimension with no genuine content; do not fill every dimension to appear complete.

| Dimension | Relationship | Related MLE | Notes |
|---|---|---|---|
|  | defines \| implements \| supports \| constrains \| verifies \| exposes \| reused_by |  |  |

Dimensions: Business/Domain, UX/Experience, Communication, Interaction/Behaviour, Frontend/Interface, Backend/Execution, Data/Information, API/Interoperability, Agentic, Verification, Operations.

### Communication MLEs (if any)

Include only when this capability genuinely triggers a communication. Omit optional fields that add nothing. The representative example text is required for every Communication MLE: classify it as `example`; preserve authoritative wording when sourced, otherwise explicitly label it illustrative so it is never mistaken for shipped copy. Terminology and tone/style also carry a semantic class like any other statement (§6) — do not leave the tag implicit.

#### [Communication name]

- **Purpose:**
- **Trigger:**
- **Audience:**
- **Required meaning:**
- **Representative example text:** *(example; sourced wording where available, otherwise explicitly illustrative — not binding copy)*
- **Terminology (optional):**
- **Tone / style (optional):**
- **Rules (optional):**
- **Recommended default (optional):**
- **Possible realizations:** e.g. inline UI, toast, email, push, SMS, agent response
- **Example copy (optional):**

## Optional: audience projections

List or link projections for business/domain, UX, frontend, backend, API/MCP/tools, agents, or operations. Each projection must trace back to this CRD and must not create divergent requirements.

## Statement provenance

For material extracted or generated from sources, label statements as:

| Statement | Semantic class | Evidence status | Source / note |
|---|---|---|---|
|  | explicit fact | sourced |  |
