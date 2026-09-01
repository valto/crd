# CRD glossary

These definitions provide a concise controlled vocabulary for Capability Documentation. The [CRD Specification](crd-specification.md) remains authoritative where more detail or conformance language is required.

## Capability Documentation

The open, technology- and implementation-agnostic framework through which people, agents, applications, and developers can understand, use, build, compose, and operate capabilities.

## Capability MLE

The smallest complete, contextually meaningful ability that produces a meaningful outcome.

## Capability Requirements Document (CRD)

The canonical technology- and implementation-agnostic requirement specification for one Capability MLE.

## Interaction Contract MLE

The smallest contextually meaningful executable behaviour. It identifies the actor, command, relevant state, policies, transition, result, and effects required to perform part of a capability.

## Related MLEs by Dimension

An optional traceability section linking a Capability MLE to lower-level discipline-specific MLEs (Business/Domain, UX/Experience, Communication, Interaction/Behaviour, Frontend/Interface, Backend/Execution, Data/Information, API/Interoperability, Agentic, Verification, Operations). Traceability, not required coverage — a dimension with no genuine content is omitted, not filled.

## Communication MLE

The smallest contextually meaningful communication unit whose intended meaning should stay consistent across channels, interfaces, actors, and languages. Owned by the capability whose trigger produces it; realized through a canonical-meaning → channel-realization → language-realization chain rather than a single fixed wording.

## Realization

A software, agent, human-operated, or combined implementation of a capability or one of its interaction contracts.

## Operational Capability Documentation

Realization-specific documentation for a particular service or system, including the implementation and operational details that do not belong in the reusable CRD.

## Rule or invariant

A condition that must remain true for the capability to retain its intended meaning and correctness.

## Recommended default

A preferred choice that may be changed by an authorized owner or implementation without violating a rule or invariant.

## Example

Illustrative content that explains a requirement but does not create a universal requirement by itself.

## Implementation choice

A realization-specific decision that is not part of the reusable capability requirement.

## Operational constraint

A limitation or condition belonging to a particular operating environment or realization.

## Unknown or unresolved

Information that is not established by current evidence and must not be silently invented or promoted into a requirement.

## Skill

An agentic realization package that may realize one capability or bundle several capabilities.

## Tool

An executable primitive that may support many skills and capabilities. A tool is not automatically a capability because it may lack complete purpose context.

## Minimum Logical Element (MLE)

The smallest bundled unit that still retains logical sense and context. Capability MLE and Interaction Contract MLE apply this scope discipline to complete abilities and executable behaviour.
