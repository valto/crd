# Agent Transformation Instructions

## Objective

Transform existing material into Capability Requirements Documents (CRDs), Interaction Contract MLEs, and—only where evidence supports them—Operational Capability Realizations.

Possible source material includes PRDs, plans, applications, codebases, Storybook, OpenAPI, MCP servers, skills, API documentation, database schemas, user stories, tests, and operational runbooks.

## Non-negotiable rules

1. Do not invent product facts, policies, ownership, outcomes, or implementation details.
2. Preserve source uncertainty. Mark it `unknown/unresolved` rather than filling it with a plausible answer.
3. Distinguish an explicit fact from a reasonable inference, recommended default, example, implementation choice, and operational constraint.
4. Do not derive a reusable CRD solely from one operational realization without marking realization-specific facts.
5. Keep a capability small enough to retain a single contextual purpose; do not split it merely because it has multiple steps.
6. Resolve competing guidance in this order: rule/invariant → explicit implementation requirement → explicit owner/user choice → recommended default → agent judgment. Surface same-level conflicts or unclear scope as `unknown/unresolved`.

## Procedure

### 1. Inventory and classify sources

For each source, record its type, scope, date/version if known, and whether it describes intent, rules, interaction, implementation, operations, or evidence.

### 2. Extract candidate statements

Extract statements about actors, goals, commands, states, policies, constraints, inputs, results, events, effects, interfaces, and tests. Label each as `explicit fact`, `reasonable inference`, or `unknown/unresolved`.

### 3. Identify candidate capabilities

Propose a Capability MLE only when there is a complete ability with a meaningful outcome and coherent purpose context. Test each candidate:

- Is it understandable independently?
- Can it be invoked or used meaningfully?
- Can its success or failure be determined?
- Would further splitting cause the pieces to lose their purpose context?

### 4. Combine and decompose

Decompose one apparent feature when it contains several independent complete abilities. Combine low-level endpoints, components, or functions when they jointly form one ability and none is meaningful alone. Record the rationale for each decision as an inference unless directly stated by a source.

### 5. Define interaction contracts

For each capability, derive one or more contracts using:

```text
Actor + Command + Current State
  -- subject to Policies/Invariants -->
New State + Result + Events/Effects
```

Do not infer a state transition, policy, or effect from a name alone. Mark it unknown until supported by evidence.

### 6. Separate reusable definition from realization

Place general purpose, boundaries, and reusable rules in the CRD. Put deployment, API/MCP exposure, code references, organizational rationale, ownership, and operational restrictions in a realization extension.

Record the realization's execution mode when known. Distinguish an agent-primary flow that uses software from a software-primary flow that calls an agent at defined steps; the controlling runtime changes authority and failure handling.

### 6.1 Identify shared elements and agentic mappings

When a component, schema, prompt, workflow, tool, or skill supports more than one candidate capability:

- do not treat it as a capability merely because it is reusable;
- record the element's `created for` capability context when evidence establishes it;
- record `approved reuse` only when approval is explicit; otherwise mark reuse approval unknown;
- distinguish a **tool** (executable primitive) from a **skill** (agentic realization package) and from the Capability MLE they may support.

A skill may realize one capability or bundle several; a tool may support many skills and capabilities.

### 7. Produce and validate the document

Use the human template. Verify that every required core field is present or explicitly unknown; every claimed fact has provenance; examples are non-binding; and implementation choices are not misrepresented as capability requirements.

## Required output format

Return:

1. A CRD using the template.
2. A statement-provenance table.
3. A short decision log for capability combination/decomposition.
4. An unresolved-questions list.
5. Where applicable, a shared-element/reuse table, agentic mapping, and audience projection links.

## Quality checks

Reject or revise the output if it:

- treats an API endpoint, UI component, or database table as a capability without purpose context;
- expands a capability into a vague product area;
- hides unknowns behind generic language;
- confuses a business rationale with a reusable capability purpose; or
- makes an example or current implementation appear binding.
- lets a recommended default or agent judgment override a rule/invariant or explicit requirement.
- treats a skill or tool name as proof of a Capability MLE without purpose context.
