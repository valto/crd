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
- **Tags (optional):** universal only — a dimension not already derivable from another field (e.g. `network-touching`/`local-only`, `data-sensitive`, `identity-related`, `notification-triggering`). Omit rather than restate what `exposure` or a contract's `transition` already says.

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
- **Implementation tags (optional):** product-specific groupings meaningful only to this realization (e.g. `impl:inbox`) — never the CRD's own universal tags, and always distinguishable from them (a consistent prefix such as `impl:` is a common convention).
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

## Optional: audience projections

List or link projections for business/domain, UX, frontend, backend, API/MCP/tools, agents, or operations. Each projection must trace back to this CRD and must not create divergent requirements.

## Statement provenance

For material extracted or generated from sources, label statements as:

| Statement | Semantic class | Evidence status | Source / note |
|---|---|---|---|
|  | explicit fact | sourced |  |
