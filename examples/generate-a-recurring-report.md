# Example: Generate a Recurring Report

Status: illustrative example. It demonstrates that `agent-built-software` is
construction provenance, not execution mode — the same Capability MLE and the
same Interaction Contract MLE can be served first by an agent building an
implementation, then by that implementation running as ordinary deterministic
software, without the capability changing.

## Identity

- **Name:** Generate a recurring report
- **Definition:** Enable a requester to receive a report, produced on a
  schedule or on demand, that reflects current data against stated
  parameters — without requiring a suitable report-generation implementation
  to already exist before the first request.
- **Status:** example

## Core meaning

- **Capability purpose:** Enable a defined report to be produced repeatedly
  from current data, without the requester having to build or maintain the
  generation logic themselves.
- **Meaningful outcome:** A report instance is produced that reflects the
  current data against the stated parameters, or the attempt is rejected or
  deferred with an identifiable reason.
- **Boundaries — includes:** specifying the report's parameters and cadence;
  producing one report instance per request or scheduled occurrence; when no
  suitable generation implementation yet exists, constructing and validating
  one as part of fulfilling that occurrence.
- **Boundaries — excludes:** authoring or approving the report's underlying
  business definition/template (a separate, prior capability or configuration
  concern); distributing the produced report to its recipients (delivery is a
  separate concern); modifying the underlying source data being reported on.
- **Terms and concepts:** `requester`, `report parameters`, `report instance`,
  `generation implementation`.

## Interaction Contract MLEs

### Request a recurring report

- **Actor:** requester
- **Command / intent:** define report parameters and a production cadence
  (on demand, or on a schedule)
- **Current state:** no report definition exists for this request
- **Rule / invariant:** parameters must be sufficient to determine what data
  the report draws on and how it is scoped. **[example]**
- **Transition:** no report definition → a standing report definition
- **Result:** report definition acknowledged and scheduled (or ready for
  on-demand production)
- **Events / effects:** `RecurringReportDefined`

### Produce report

- **Actor:** the capability's own realization (agent, agent-built software, or
  software)
- **Command / intent:** produce one report instance matching the current
  definition against current data
- **Current state:** a standing report definition exists; this occurrence is
  due (by schedule or on-demand request)
- **Rule / invariant:** a produced report instance must reflect the actual
  current data available at generation time — it must not silently substitute
  stale or cached data without disclosing that it did. **[example]**
- **Transition:** due occurrence → produced report instance, or an
  identifiable failure
- **Result:** a report instance, or an identifiable failure reason (e.g. data
  unavailable, parameters no longer resolvable)
- **Events / effects:** `ReportProduced`, `ReportGenerationFailed`

## Rules, defaults, and unknowns

- **Rule / invariant:** an agent-built implementation must be validated
  against the current report parameters before it is reused, unattended, for
  a subsequent occurrence. **[implementation requirement, not a recommended
  default — this is the trust boundary that keeps unattended reuse of
  agent-built software distinct from blind reuse]**
- **Recommended default:** if a previously agent-built implementation fails
  validation against new parameters or a changed data shape, fall back to
  agent-primary construction again for that occurrence rather than silently
  reusing an implementation that no longer fits. **[example]**
- **Unknowns:** the exact scheduling/trigger mechanism; where a constructed
  implementation is stored, versioned, and audited; the policy for retiring an
  implementation once report parameters change materially; how a partial or
  degraded data source is disclosed within a produced report.

## Optional: operational realizations

This is the point of the example: the same capability and the same *Produce
report* contract, served by two realizations that differ in **construction
provenance**, not in what the contract requires.

### Realization A — agent constructs, then produces, the first occurrence

- **Kind:** `agent`
- **Execution mode:** `agent-primary-using-software`
- **Exposure:** agent, tool
- **Rationale / intent:** the first time this report definition is due, no
  suitable generation implementation exists yet. An agent interprets the
  parameters, determines that no reusable implementation is available, builds
  a function or script that produces the report from the current data, and
  validates it before producing this occurrence's report instance with it.
- **Implementation requirement:** the newly built implementation MUST pass
  validation against the current parameters (and a known-correct sample, if
  one is available) before it is treated as reusable for future occurrences —
  not merely because it produced *an* output this one time. **[implementation
  requirement]**
- **Implementation references:** parameter-resolution tool; data-access tool;
  report-construction and validation tooling.

### Realization B — the agent-built implementation produces subsequent occurrences

- **Kind:** `agent-built-software`
- **Execution mode:** `software-primary`
- **Exposure:** workflow, internal
- **Rationale / intent:** once Realization A's implementation has been
  validated, every subsequent due occurrence of *Produce report* runs that
  implementation directly and deterministically — the same Interaction
  Contract MLE, the same required outcome, but now served by construction
  provenance (`agent-built-software`) paired with an ordinary,
  agent-uninvolved execution mode (`software-primary`). This is the
  distinction the example exists to demonstrate: `agent-built-software`
  describes *how the implementation came to exist*, not *what controls it at
  runtime* — those are two separate questions, and this realization answers
  them differently (agent-built; software-run).

## Optional: agentic mappings

| Element | Kind | Relationship to this Capability MLE | Notes |
|---|---|---|---|
| Report-construction assistant | skill | realizes-capability | Realization A only — invoked when no valid implementation currently exists for this report definition. |
| parameter-resolution tool | tool | supports-contract | Supports *Request a recurring report* and validation in *Produce report*. |
| data-access tool | tool | supports-contract | Supports *Produce report* in both realizations. |
| Agent-built report-generation implementation | tool | realizes-capability | Realization B — the artifact Realization A constructed and validated; not a "skill," since no agent reasoning occurs when it runs. |

## Provenance

This is an illustrative example, not extracted from a real reporting system.
It exists to make explicit a distinction the specification already states
(§3.3): `agent-built-software` is implementation provenance, while execution
mode is a separate, runtime-control question. `schedule-a-meeting.md`
demonstrates two realizations that differ in execution mode, with provenance
held constant (nothing there is agent-*built*, only optionally agent-*run*).
This example instead holds the Interaction Contract MLE constant and varies
provenance and execution mode independently, on purpose.

## Why this example matters

Without this example, a reader could reasonably (but wrongly) assume
`agent-built-software` is just another name for `agent-primary-using-software`
— that "built by an agent" and "run by an agent" are the same claim. They are
not. Realization B here is built by an agent and then runs as ordinary
software, with no agent in the loop at execution time; Realization A is
software-assisted but agent-controlled. The capability, and the *Produce
report* contract it must satisfy, do not change between them — only how the
realization came to exist, and what controls it once it does, and those two
facts vary independently of each other.
