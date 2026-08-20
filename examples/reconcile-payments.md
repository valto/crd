# Example: Reconcile Payments

Status: illustrative internal-capability example. It demonstrates that a Capability MLE does not need to be externally visible.

## Identity

- **Name:** Reconcile payments
- **Definition:** Enable an organization to compare recorded payment obligations and transactions against authoritative payment records, identify discrepancies, and produce a reviewable reconciliation outcome.
- **Status:** example

## Core meaning

- **Capability purpose:** Maintain trustworthy financial records by detecting and resolving mismatches between expected and received payment information.
- **Meaningful outcome:** A reconciliation run produces matched records and clearly identified discrepancies that can be reviewed or resolved by an authorized finance actor.
- **Boundaries — includes:** importing payment records; matching records to obligations; classifying discrepancies; producing review outcomes.
- **Boundaries — excludes:** initiating payments; changing provider settlement; collecting from a payer; writing off a balance without authorized review.
- **Terms and concepts:** `payment record`, `obligation`, `reconciliation period`, `discrepancy case`.

## Interaction Contract MLEs

### Import payment records

- **Actor:** authorized scheduler, finance operator, or integration
- **Command / intent:** make authoritative payment records available for reconciliation
- **Current state:** a reconciliation period is open
- **Transition:** payment records become available for the period
- **Result:** a reconcilable payment-record set
- **Events / effects:** `PaymentRecordsImported`

### Run payment reconciliation

- **Actor:** reconciliation service or authorized finance operator
- **Command / intent:** compare payment records with recorded obligations
- **Current state:** reconcilable payment records and obligations are available
- **Rule / invariant:** a record must not be marked matched when required identifying evidence is absent. **[example]**
- **Transition:** open period → reconciled records and discrepancy cases
- **Result:** matched, unmatched, duplicate, or ambiguous payment outcomes
- **Events / effects:** `PaymentReconciliationCompleted`, `PaymentDiscrepancyDetected`

### Review payment discrepancy

- **Actor:** authorized finance operator
- **Command / intent:** review and classify a discrepancy
- **Current state:** a discrepancy case exists
- **Rule / invariant:** only an authorized finance actor may resolve or write off a discrepancy. **[example]**
- **Transition:** discrepancy remains open or is marked resolved with an audit note
- **Result:** a documented discrepancy-review outcome
- **Events / effects:** `PaymentDiscrepancyReviewed`

## Rules, defaults, and unknowns

- **Rule / invariant:** reconciliation outcomes must preserve enough evidence for an authorized reviewer to understand the match or discrepancy. **[example]**
- **Recommended default:** surface ambiguous matches for review rather than marking them reconciled automatically. **[example]**
- **Unknowns:** provider contracts, matching tolerances, authorization model, and accounting adjustment rules.

## Optional: illustrative operational realization

- **Realization:** reconciliation service
- **Execution mode:** `software-primary`
- **Exposure:** internal workflow
- **Rationale / intent:** an organization may implement this to improve financial-record integrity; this is not part of the reusable capability purpose.

## Why this example matters

No external customer needs to see this capability for it to be a complete Capability MLE. It has an independent purpose, meaningful outcome, rules, executable behaviours, and a realization. This is why external observability is not a requirement for a CRD.
