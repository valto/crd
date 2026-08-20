# Capability Inventory

A Capability Inventory is a catalogue of available or planned Capability MLEs. It is not a substitute for a CRD; it makes capabilities discoverable and points to their canonical requirements documents.

## Inventory entry

| Field | Meaning |
|---|---|
| `id` | Stable identifier. |
| `name` | Capability MLE name. |
| `status` | planned, draft, active, deprecated, or unknown. |
| `purpose` | One-line general outcome enabled by the capability. |
| `CRD` | Link or reference to the Capability Requirements Document, if available. |
| `realization status` | Available, partial, planned, deprecated, or unknown. |
| `notes` | Important discovery, boundary, or unknown note. |

## Example

| id | name | status | purpose | CRD | realization status |
|---|---|---|---|---|---|
| `moving.quote.request` | Request a moving quote | draft | Enable a move to be presented to a provider for quote consideration. | [Example CRD](examples/request-moving-quote.md) | illustrative |

## Independence from product planning

A Capability Inventory can be linked from a product or PRD, but it does not depend on one. Reusable capabilities such as `Schedule a meeting` can be documented once and realized differently by many products or services.
