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

## Related MLEs by Dimension

Traceability only — a dimension with no genuine content in this illustrative example is omitted rather than filled. `Interaction/Behaviour` and `API/Interoperability` are omitted here: the three Interaction Contract MLEs above already are this capability's behaviour, and no API shape is stated firmly enough to trace to (the operational realization only says an API "may" expose separate endpoints — a possibility, not a traceable reference).

| Dimension | Relationship | Ref | Notes |
|---|---|---|---|
| Business/Domain | constrains | Serviceable-route rejection rule ("a provider may reject a route it does not serve") | **[example]** |
| UX/Experience | supports | Draft → validate → submit flow; preserve-draft-on-missing-information default | |
| Communication | defines | Quote Request Submitted Confirmation | See communicationMLEs. |
| Frontend/Interface | supports | Quote request form (draft/validate/submit) | implementation choice |
| Backend/Execution | implements | CreateDraftQuoteRequest, ValidateQuoteRequest, SubmitQuoteRequest use cases | implementation choice |
| Data/Information | implements | QuoteRequest, ServiceableRoute entities | implementation choice |
| Agentic | supports | `moving-quote-assistant` skill; `submit-quote-request` tool | See agenticMappings — already declared elsewhere in this CRD, referenced here rather than restated. |
| Verification | verifies | "A submission is never accepted without sufficient identifying information"; "an unsupported route is rejected, not silently accepted" | |

`Operations` is also omitted: nothing in this illustrative example states a monitoring, scheduling, or operational-runbook fact to trace to.

### Communication MLE: Quote Request Submitted Confirmation

- **Purpose:** Confirm that the request was received and set an honest expectation for what happens next.
- **Trigger:** `Submit quote request` succeeds (`QuoteRequestSubmitted`).
- **Audience:** The prospective customer or authorized caller who submitted the request.
- **Required meaning:** the submission succeeded; the request is now stored; no further action is currently required from the requester; there is a next step, even if its exact timing is unknown.
- **Terminology:** call it a "quote request," not an "application" or "order." **[example]**
- **Tone / style:** clear, calm, concise — a routine acknowledgement, not a sales pitch. **[example]**
- **Rule:** must not promise a specific response time unless a realization's operational commitment actually guarantees it. **[rule/invariant — mirrors the capability's own "intelligible rejection" standard: don't imply a certainty the process doesn't have]**
- **Recommended default:** if no guaranteed response time exists, say something like "we'll be in touch soon" rather than inventing a number. **[recommended default]**
- **Possible realizations:** inline confirmation screen; email; SMS; agent response.
- **Example copy:** "Thanks — your moving quote request has been received. We'll be in touch soon." **[example]**

This is the second worked trial of the Related MLEs by Dimension / Communication MLE model (the first, on `reconcile-payments`, tested an internal capability with no direct UI). This one is customer-facing and confirms the model holds for that case too: the confirmation's required meaning is owned entirely by this capability's own `Submit quote request` contract, while the terminology convention ("quote request," never "application") is the kind of cross-cutting rule a Source Context Reference would hold if this illustrative provider had one — consistent with the resolution already recorded on `reconcile-payments`.

## Provenance

All statements in this document are illustrative examples. They require replacement or confirmation when used for an actual service.
