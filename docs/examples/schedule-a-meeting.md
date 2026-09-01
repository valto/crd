# Example: Schedule a Meeting

Status: illustrative example. It demonstrates that one Capability MLE can have both an agent-primary and a software-primary realization without changing the capability itself.

## Identity

- **Name:** Schedule a meeting
- **Definition:** Enable a requester to have a meeting arranged with one or more other participants, resulting in a mutually available time being found and confirmed on the relevant calendars, or an intelligible reason why it could not be scheduled.
- **Status:** example

## Core meaning

- **Capability purpose:** Enable a meeting between people to be arranged without the requester manually coordinating availability.
- **Meaningful outcome:** A meeting is confirmed and placed on the calendars of all required participants, or the request is rejected or deferred with an identifiable reason.
- **Boundaries — includes:** resolving the intended participants; determining collective availability within stated constraints; proposing and confirming a time; placing the event on calendars; communicating the outcome.
- **Boundaries — excludes:** creating participant contact records; rescheduling or canceling an existing meeting (a separate capability); the organizational calendar-permission system itself (this capability is governed by it, but does not implement it).
- **Terms and concepts:** `requester`, `participant`, `candidate time`, `confirmed meeting`.

## Interaction Contract MLEs

### Request a meeting

- **Actor:** requester (a person, or an agent acting on a person's behalf)
- **Command / intent:** propose a meeting with named participants within given constraints (duration, timeframe, purpose)
- **Current state:** no scheduling attempt exists for this request
- **Rule / invariant:** a duration and at least one participant are required. **[example]**
- **Transition:** no request → pending scheduling attempt
- **Result:** pending attempt acknowledged
- **Events / effects:** `MeetingRequested`

### Resolve participant availability

- **Actor:** the scheduling capability's own realization (agent or software)
- **Command / intent:** determine which time windows are available for all required participants within the requested constraints
- **Current state:** a pending scheduling attempt exists
- **Rule / invariant:** only calendars this capability is authorized to read may be consulted. **[example]**
- **Transition:** pending attempt → one or more candidate times, or a no-availability outcome
- **Result:** candidate time(s), or an identifiable no-availability reason
- **Events / effects:** `AvailabilityResolved`

### Confirm meeting time

- **Actor:** the requester, or an authorized participant if confirmation authority is delegated **[example]**
- **Command / intent:** select and confirm one candidate time
- **Current state:** one or more candidate times exist
- **Rule / invariant:** a meeting must not be placed on a calendar this capability is not authorized to write to. **[example]**
- **Transition:** candidate time(s) → confirmed meeting
- **Result:** confirmed meeting placed on calendars, or an expiry/decline outcome
- **Events / effects:** `MeetingConfirmed`, `MeetingSchedulingFailed`

## Rules, defaults, and unknowns

- **Rule / invariant:** a meeting must not be confirmed on a calendar the capability is not authorized to write to. **[example]**
- **Recommended default:** if no single candidate time satisfies every participant's stated constraints, surface the closest partial match rather than only reporting failure. **[example]**
- **Unknowns:** exact availability-data source and freshness; the participant-authorization model; conflict-resolution policy when constraints contradict; time-zone handling.

## Optional: operational realizations

This is the point of the example: the same capability, same three Interaction Contract MLEs, with two genuinely different realizations.

### Realization A — agent-assisted scheduling assistant

- **Execution mode:** `agent-primary-using-software`
- **Exposure:** agent, tool
- **Rationale / intent:** let an agent interpret intent ("find 30 minutes with Markus next week") and operate tools directly, instead of the requester manually checking calendars.
- **Implementation requirement:** the agent MUST obtain requester (or delegated-participant) confirmation before any candidate time is written to a calendar — the agent proposes, it does not unilaterally commit. **[implementation requirement, not a recommended default — this is the approval/confirmation boundary that keeps agent-primary control distinct from unchecked agent autonomy]**
- **Implementation references:** contact-resolution tool; availability-lookup tool; calendar-creation tool.

### Realization B — traditional scheduling UI

- **Execution mode:** `software-primary`
- **Exposure:** ui
- **Rationale / intent:** a deterministic calendar-picker UI where the requester reviews a grid of participant availability and clicks to confirm — the same *Confirm meeting time* contract, no agent involved.

## Optional: agentic mappings

| Element | Kind | Relationship to this Capability MLE | Notes |
|---|---|---|---|
| Scheduling assistant | skill | realizes-capability | Realization A only. |
| contact-resolution tool | tool | supports-contract | Supports *Request a meeting*. |
| availability-lookup tool | tool | supports-contract | Supports *Resolve participant availability*. |
| calendar-creation tool | tool | supports-contract | Supports *Confirm meeting time*; used by Realization A only — Realization B writes the calendar entry directly from the UI. |

## Provenance

This is an illustrative example, not extracted from a real scheduling system. It exists to make CRD's agentic thesis concrete: the capability and its Interaction Contract MLEs do not change between an agent-primary and a software-primary realization — only the realization does.

## Why this example matters

The earlier examples show a capability can be customer-facing, internal, or extracted from real multi-realization software. None of them puts an agent in control of the flow. This one does — while showing the exact boundary that keeps that safe: the agent may resolve availability and propose a time on its own, but confirming a meeting on someone's calendar is gated behind an explicit approval step, stated as an implementation requirement, not left as an assumed default.
