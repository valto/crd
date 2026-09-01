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
| `known realizations` | Products, services, or apps already known to realize this capability, each linked to that realization's own CRD/Operational Capability Documentation, if any exist yet. |
| `tags` | The CRD's own universal tags (crd-specification.md §7.3), plus this row's implementation tags if any, each prefixed `impl:` so the two kinds are never mistaken for each other (e.g. `local-only, impl:inbox`). Also useful for grouping or filtering a long inventory by domain/module without inventing a separate taxonomy field. |
| `notes` | Important discovery, boundary, or unknown note. |

`known realizations` matters most for a general/reusable inventory (§3.4): it turns a claim that a capability is "reusable" into a checkable fact. A capability with zero known realizations can still be a valid planned requirement — what's unproven is a claim that it's generalized/reusable, not the capability itself. Cross-context reuse specifically remains unproven until a second real consumer exists or is imminent. When a generic capability was itself generalized from one specific product's capability, that product is realization #1 by construction and should be listed, not omitted. A single-service inventory documenting one product's own capabilities may leave this column empty or omit it — a service is usually not tracking who else realizes its own capabilities.

`tags` is optional in both inventory types and MAY be omitted entirely if it adds nothing beyond what `purpose` or `realization status` already conveys — don't populate it just to fill the column. This combined column is a convenience for the flat markdown table; an HTML projection of the inventory typically renders it as two tabs instead — one segmented by universal tag, one by implementation tag/domain — with the visual tag/badge convention reserved for implementation tags (see `inventory-html-template.html`).

## Example

| id | name | status | purpose | CRD | realization status | known realizations | tags |
|---|---|---|---|---|---|---|---|
| `moving.quote.request` | Request a moving quote | draft | Enable a move to be presented to a provider for quote consideration. | [Example CRD](examples/request-moving-quote.md) | illustrative | none yet | network-touching |

## Independence from product planning

A Capability Inventory can be linked from a product or PRD, but it does not depend on one. Reusable capabilities such as `Schedule a meeting` can be documented once and realized differently by many products or services.
