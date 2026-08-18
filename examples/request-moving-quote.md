# Example: Request a Moving Quote

Status: illustrative example. It demonstrates the template; it is not a specification for a particular moving company.

## Identity

- **Name:** Request a moving quote
- **Definition:** Enable a prospective customer or authorized caller to submit sufficient moving details for a provider to begin the quote process.
- **Status:** example

## Core meaning

- **Capability purpose:** Enable a move to be presented to a provider for quote consideration.
- **Meaningful outcome:** A quote request is accepted for processing, rejected with an intelligible reason, or identified as requiring more information.
- **Boundaries — includes:** collecting and submitting move details; validating the request; communicating the immediate submission outcome.
- **Boundaries — excludes:** calculating the final price; accepting a quote; scheduling a move; payment; ongoing quote-status tracking.
- **Terms and concepts:** `quote request`, `move details`, `serviceable route`, `submission outcome`.

## Interaction Contract MLEs

### Create draft quote request

- **Actor:** prospective customer or authorized agent
- **Command / intent:** begin a quote request
- **Current state:** no draft request exists for this interaction
- **Policies / invariants:** none specified in this illustrative example
- **Transition:** no request → draft quote request
- **Result:** draft request available for completion
- **Events / effects:** `QuoteRequestDraftCreated` example event
- **Unknowns:** draft retention and identity requirements

### Validate quote request

- **Actor:** prospective customer, authorized agent, or system
- **Command / intent:** validate supplied move details
- **Current state:** draft quote request
- **Policies / invariants:** required contact information and sufficient move details; serviceable route policy if applicable
- **Transition:** draft request remains draft, with validation result
- **Result:** valid | missing information | unsupported move
- **Events / effects:** none known
- **Unknowns:** exact required fields and service-area definition

### Submit quote request

- **Actor:** prospective customer or authorized agent
- **Command / intent:** submit a valid quote request
- **Current state:** valid draft quote request
- **Policies / invariants:** request must satisfy applicable validation rules
- **Transition:** valid draft → submitted request
- **Result:** submission confirmation or intelligible rejection
- **Events / effects:** `QuoteRequestSubmitted`; confirmation delivery may be requested
- **Unknowns:** idempotency, routing, and confirmation channel

## Rules and defaults

### Rules / invariants

- A submission requires sufficient information to identify the requester and the proposed move. **[example]**
- A provider may reject a route it does not serve. **[example]**

### Recommended defaults

- Preserve a draft when validation finds missing information, rather than discarding entered details. **[example]**
- Explain what information is missing in the validation result. **[example]**

## Unknown / unresolved

- The exact data schema, provider rules, authorization model, and operational workflow are intentionally unspecified.

## Optional: illustrative operational realization

- **Exposure:** responsive web form, customer-service tool, API, and agent tool
- **Operational constraint:** a particular provider may serve only configured geographic areas
- **Implementation choice:** an API may expose separate draft, validation, and submission endpoints
- **Rationale / intent:** a provider may implement this to obtain qualified leads; this is not part of the reusable capability purpose

## Provenance

All statements in this document are illustrative examples. They require replacement or confirmation when used for an actual service.
