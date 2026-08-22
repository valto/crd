# Agent Transformation Instructions

## Objective

Transform existing material into Capability Requirements Documents (CRDs), Interaction Contract MLEs, and—only where evidence supports them—Operational Capability Realizations.

Possible source material includes PRDs, plans, applications, codebases, Storybook, OpenAPI, MCP servers, skills, API documentation, database schemas, user stories, tests, and operational runbooks.

Extract mode defaults to a **specific/operational CRD set**. Produce an additional generic/reusable projection only when the user asks for it, or when reuse by a second real consumer is already established or clearly imminent. A generic capability with zero known realizations is an unproven hypothesis, not demonstrated reuse.

For a substantial source that yields multiple capabilities, also produce a [Source Context Reference](source-context-template.md): a companion reference for product-wide and cross-cutting context that belongs to no single CRD.

## Non-negotiable rules

1. Do not invent product facts, policies, ownership, outcomes, or implementation details.
2. Preserve source uncertainty. Mark it `unknown/unresolved` rather than filling it with a plausible answer.
3. Distinguish an explicit fact from a reasonable inference, recommended default, example, implementation choice, and operational constraint.
4. Do not derive a reusable CRD solely from one operational realization without marking realization-specific facts.
5. Keep a capability small enough to retain a single contextual purpose; do not split it merely because it has multiple steps.
6. Resolve competing guidance in this order: rule/invariant → explicit implementation requirement → explicit owner/user choice → recommended default → agent judgment. Surface same-level conflicts or unclear scope as `unknown/unresolved`.
7. Do not infer a priority or conflict-ordering relationship between independently stated facts. If the source does not establish which applies first, record that ordering as `unknown/unresolved`.
8. Preserve source hedge language. A statement expressed as “preferably,” “should,” “recommended,” or an equivalent hedge is a recommended default or implementation choice—not a rule/invariant—unless the source explicitly makes it binding.

## Procedure

### 1. Inventory and classify sources

For each source, record its type, scope, date/version if known, and whether it describes intent, rules, interaction, implementation, operations, or evidence.

When a substantial source contains product-wide context that no one capability should own, create a Source Context Reference. Capture source citation, product/system intent, cross-cutting constraints, platform/client exposure, build sequencing, cross-capability verification material, and material not mapped elsewhere. The SCR carries no binding requirements of its own: every binding constraint must also appear in each CRD it governs.

### 2. Extract candidate statements

Extract statements about actors, goals, commands, states, policies, constraints, inputs, results, events, effects, interfaces, and tests. Label each as `explicit fact`, `reasonable inference`, or `unknown/unresolved`.

### 3. Identify candidate capabilities

Propose a Capability MLE only when there is a complete ability with a meaningful outcome and coherent purpose context. Test each candidate:

- Is it understandable independently?
- Can it be invoked or used meaningfully?
- Can its success or failure be determined?
- Would further splitting cause the pieces to lose their purpose context?

### 4. Combine and decompose

Decompose one apparent feature when it contains several independent complete abilities. Combine low-level endpoints, components, or functions only when they jointly form one ability and none is meaningful alone.

Before combining elements, run the Capability MLE test on **each element individually**, not only on the proposed combined result. Combine only when every candidate element fails the test alone. If one element has its own actor, command, state, and result, it is likely its own Capability MLE; record the decision in the log.

When a generic/reusable projection is authorized, treat generalizing phrases such as “or otherwise,” “or similar,” “any,” or “etc.” as a source-grounding checkpoint. They are not permission to broaden a requirement beyond what the source supports.

### 5. Define interaction contracts and optional diagrams

For each capability, derive one or more contracts using:

```text
Actor + Command + Current State
  -- subject to Policies/Invariants -->
New State + Result + Events/Effects
```

Do not infer a state transition, policy, or effect from a name alone. Mark it unknown until supported by evidence.

Mermaid diagrams are optional illustrative projections. Every state, transition, edge, and relationship MUST already be stated in the CRD text. In a state diagram, do not route a retained, persistent, or historical state to the `[*]` exit pseudostate unless the source explicitly describes it as terminal.

### 6. Separate reusable definition from realization

Place general purpose, boundaries, and reusable rules in the CRD. Put deployment, API/MCP exposure, code references, organizational rationale, ownership, and operational restrictions in a realization extension.

Record the realization’s execution mode when known. Distinguish an agent-primary flow that uses software from a software-primary flow that calls an agent at defined steps; the controlling runtime changes authority and failure handling.

### 6.1 Identify shared elements and agentic mappings

When a component, schema, prompt, workflow, tool, or skill supports more than one candidate capability:

- do not treat it as a capability merely because it is reusable;
- record the element’s `created for` capability context when evidence establishes it;
- record `approved reuse` only when approval is explicit; otherwise mark reuse approval unknown;
- distinguish a **tool** (executable primitive) from a **skill** (agentic realization package) and from the Capability MLE they may support.

A skill may realize one capability or bundle several; a tool may support many skills and capabilities.

### 7. Produce and validate the document

Use the human template. Verify that every required core field is present or explicitly unknown; every claimed fact has provenance; examples are non-binding; and implementation choices are not misrepresented as capability requirements.

## Required output format

Return:

1. A CRD using the template for each identified Capability MLE.
2. A statement-provenance table.
3. A short decision log for combination/decomposition, including each individual MLE check used before combination.
4. An unresolved-questions list.
5. Where applicable, a shared-element/reuse table, agentic mapping, and audience projection links.
6. For a substantial multi-capability source, a Source Context Reference.

## Quality checks

Reject or revise the output if it:

- treats an API endpoint, UI component, or database table as a capability without purpose context;
- expands a capability into a vague product area;
- hides unknowns behind generic language;
- confuses a business rationale with a reusable capability purpose;
- makes an example or current implementation appear binding;
- lets a recommended default or agent judgment override a rule/invariant or explicit requirement;
- treats a skill or tool name as proof of a Capability MLE without purpose context;
- invents a priority ordering, strengthens a source hedge into a rule, or generalizes beyond the evidence;
- uses a Mermaid diagram to assert a state, transition, or relationship that the CRD text does not establish; or
- presents a speculative generic capability as demonstrated reusable without known realizations.
