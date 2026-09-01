# Example: Generate a Recurring Report

Status: illustrative example. It demonstrates that `agent-built-software` is
construction provenance, not execution mode, by varying the two independently
across three realizations of the same Capability MLE and the same Interaction
Contract MLE: an agent building and running an implementation; that same
agent-built implementation later running unattended as ordinary deterministic
software; and that same agent-built implementation being reused while an
agent still directly supervises it. Construction provenance and execution
mode move independently across these three — the capability itself never
changes.

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

- **Actor:** an agent (while constructing and running a new implementation),
  or a previously agent-built implementation (running unattended, or reused
  under an agent's direct supervision) — see Optional: operational
  realizations for which realization puts which actor in control
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
report* contract, served by three realizations whose **construction
provenance** (`kind`) and **execution mode** vary independently of each
other, not in lockstep — the contract's requirements never change.

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
  agent-uninvolved execution mode (`software-primary`). This is half of the
  distinction the example exists to demonstrate: `agent-built-software`
  describes *how the implementation came to exist*, not *what controls it at
  runtime*.

### Realization C — the agent-built implementation is reused under direct agent supervision

- **Kind:** `agent-built-software`
- **Execution mode:** `agent-primary-using-software`
- **Exposure:** agent, tool
- **Rationale / intent:** report parameters changed since Realization A's
  implementation was last validated. Rather than trust it to run unattended
  (Realization B) or discard it and start over, an agent reuses the same
  agent-built implementation but directly invokes and supervises this
  occurrence's run — checking its output against the changed parameters
  before the implementation earns unattended (Realization B) status again.
  The implementation's construction provenance is unchanged from Realization
  B (`agent-built-software`); only who controls this occurrence's execution
  differs.
- **Implementation requirement:** the supervising agent MUST confirm the
  agent-built implementation's output against the current parameters before
  either releasing this occurrence's report or restoring the implementation
  to unattended (Realization B) use. **[implementation requirement — this is
  the same trust boundary named in Rules, defaults, and unknowns above,
  applied to a reuse rather than a first construction]**
- **Implementation references:** the same agent-built report-generation
  implementation as Realization B; parameter-resolution tool; data-access
  tool.

This is the other half of the distinction: `agent-built-software` (Realization
B and C's shared provenance) pairs with **both** `software-primary` (B) and
`agent-primary-using-software` (C) — construction provenance does not
determine execution mode, and the reverse also holds, since Realization A's
`agent-primary-using-software` pairs with `kind: agent`, not
`agent-built-software`. All three realizations satisfy the same *Produce
report* contract and the same capability; only provenance and execution mode
move, and they move independently rather than together.

## Optional: agentic mappings

| Element | Kind | Relationship to this Capability MLE | Notes |
|---|---|---|---|
| Report-construction assistant | skill | realizes-capability | Realization A only — invoked when no valid implementation currently exists for this report definition. |
| parameter-resolution tool | tool | supports-contract | Supports *Request a recurring report* and validation in *Produce report*. |
| data-access tool | tool | supports-contract | Supports *Produce report* in all three realizations. |
| Agent-built report-generation implementation | tool | realizes-capability | Realizations B and C — the artifact Realization A constructed and validated; not a "skill" in either realization, since no agent reasoning occurs inside the implementation itself, only around it in Realization C. |

## Provenance

This is an illustrative example, not extracted from a real reporting system.
It exists to make explicit a distinction the specification already states
(§3.3): `agent-built-software` is implementation provenance, while execution
mode is a separate, runtime-control question. `schedule-a-meeting.md`
demonstrates two realizations that differ in execution mode, with provenance
held constant (nothing there is agent-*built*, only optionally agent-*run*).
This example instead holds the Interaction Contract MLE constant and varies
provenance and execution mode independently, on purpose — with three
realizations rather than two, because two realizations alone would only show
that provenance and execution mode *can* differ once, not that either axis
can move while the other holds still. Realizations B and C share the same
`kind` (`agent-built-software`) but differ in execution mode
(`software-primary` vs. `agent-primary-using-software`); Realization A shares
its execution mode with neither B nor C but shares nothing in `kind` with B or
C either. That is the actual evidence for independence, not just an assertion
of it.

## Why this example matters

Without this example, a reader could reasonably (but wrongly) assume
`agent-built-software` is just another name for `agent-primary-using-software`
— that "built by an agent" and "run by an agent" are the same claim. They are
not. Realization B is built by an agent and then runs as ordinary software,
with no agent in the loop at execution time. Realization C uses the *same*
agent-built implementation, but under direct agent supervision — proving that
`agent-built-software` does not force `software-primary`, since B and C are
both agent-built with different execution modes. Realization A shows the
reverse: an agent controlling the flow (`agent-primary-using-software`)
without the resulting implementation itself being reused agent-built software
yet — it is what Realization B and C's implementation *becomes*, not what it
already is while under construction. The capability, and the *Produce report*
contract it must satisfy, do not change across any of the three — only
provenance and execution mode move, and the three realizations together show
that they move independently of each other, not that they merely could.
