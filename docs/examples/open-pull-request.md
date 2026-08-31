# CRD: Open a Pull Request

Status: draft — a real extraction from GitHub's own public REST API and webhook documentation (fetched 2026-08-26), independently audited for framework conformance and factual accuracy. See `github-pull-request-provenance.md` for the statement-provenance table and `github-pull-request-decision-log.md` for scope reasoning.

## Identity

- **Name:** Open a pull request
- **Definition:** The ability for an authorized actor to propose that a set of committed changes on one branch (or fork) be reviewed for integration into another branch, creating a durable, addressable request that others can inspect, discuss, and act on independently of the actor who created it.
- **Status:** draft

## Core meaning

- **Capability purpose:** Enable a proposed set of changes to be formally presented for review and eventual integration, without itself performing that integration. **[capability purpose]**
- **Meaningful outcome:** A new pull request exists in an intelligible state (open, either "ready for review" or "draft") and is addressable for further action, **or** the attempt is rejected with an identifiable reason (e.g. permission denied, validation failure). **[reasonable inference from documented response codes]**
- **Boundaries — includes:**
  - Supplying the two branches being compared (the branch containing the proposed changes, and the branch they should eventually be merged into) and enough metadata (title and/or body, or a source issue to convert) to make the proposal reviewable. **[explicit fact — GitHub REST "Create a pull request" required/optional body parameters `head`, `base`, `title`, `body`, `issue`]**
  - Marking the proposal as a draft rather than ready for review at creation time. **[explicit fact — `draft` body parameter]**
  - The immediate accept/reject outcome of the creation attempt itself. **[reasonable inference from documented status codes 201/403/422]**
- **Boundaries — excludes:**
  - Reviewing the proposal (approving, requesting changes, or commenting) — a separate documented capability area (`pull_request_review`, `pull_request_review_comment`). **[explicit fact — webhook docs: "For activity related to pull request reviews... use the `pull_request_review`... event[s] instead"]**
  - Editing an already-open pull request's title, body, base branch, or open/closed state after creation — a separate REST operation (`PATCH /repos/{owner}/{repo}/pulls/{pull_number}`, "Update a pull request"). **[explicit fact — distinct documented operation]** That this run doesn't draft it as its own CRD is this extraction's own scoping choice, not something GitHub's docs state — see decision log. **[this extraction's own scoping decision, not sourced]**
  - Converting a draft pull request to "ready for review" once already open — this is the `ready_for_review` webhook action / a follow-on state change, not part of the creation act itself. **[explicit fact — distinct documented `pull_request` action]**
  - Merging the pull request — a separate Capability MLE with its own actor, timing, and policies (see `merge-pull-request.md`). **[explicit fact + MLE reasoning; see decision log]**
  - Closing a pull request without merging (`state: closed` via the update operation). **[explicit fact — distinct documented operation]**
  - Creating or pushing the underlying commits/branch being proposed — a precondition, not part of this capability. **[reasonable inference — the create operation only references existing `head`/`base` branches, it does not create commits]**
- **Terms and concepts:**
  - `actor` — the person or authorized agent proposing the change → **schema.org/Person** ("A person (alive, dead, undead, or fictional)."). GitHub's docs describe this actor concretely as a "collaborator" or organization member; that concrete term is preserved as-is alongside the generic grounding. **[explicit fact for GitHub term + schema.org description fetched from schema.org/Person, 2026-08-26]**
  - `open a pull request` (the command/intent) → **schema.org/CreateAction** ("The act of deliberately creating/producing/generating/building a result out of the agent."). **[schema.org/CreateAction description fetched 2026-08-26]**
  - `proposed changes` (the content being proposed) → **schema.org/SoftwareSourceCode** ("Computer programming source code...") as the general-vocabulary analogue; GitHub's own concrete terms `commit`, `branch`, `head`, `base`, `diff` are preserved as-is since no closer standard-vocabulary equivalent exists. **[schema.org/SoftwareSourceCode description fetched 2026-08-26; branch/commit terms are explicit facts from GitHub docs]**
  - `title` / `body` (proposal metadata) → the generic **schema.org/Thing `name`/`description` properties**. **[reasonable inference — standard schema.org core properties; not independently re-fetched today but part of the base vocabulary, used only as a light grounding, not a load-bearing claim]**
  - `draft pull request` — a state in which the proposal is visible but explicitly not yet ready for review; no schema.org equivalent identified, preserved as GitHub's own term. **[explicit fact]**
  - `head` / `base` — GitHub's own concrete terms for the compare and target branches; preserved as-is. **[explicit fact]**
- **Tags:** `notification-triggering` — creating a pull request is documented as triggering notifications to other users/systems, a cross-cutting dimension not otherwise derivable from the fields above (chosen over `network-touching`, which would add nothing here beyond what `exposure: API/UI` on a hosted product already implies). **[explicit fact — REST docs: "This endpoint triggers notifications... may result in secondary rate limiting"]**

## Interaction Contract MLEs

### Create a pull request

- **Actor:** A repository collaborator (or organization member, for org-owned repositories) with write access to the branch containing the proposed changes (the "head"/"source" branch) — which may be a branch in a fork the actor owns. **[explicit fact — "To open or update a pull request in a public repository, you must have write access to the head or the source branch. For organization-owned repositories, you must be a member of the organization that owns the repository..."]** Whether a GitHub App, bot, or scheduled automation can be this actor without a human present is established for at least one case (Dependabot; see Optional: operational realization) but the general authorization boundary for non-human actors beyond that one case is `unknown/unresolved`.
- **Command / intent:** Propose that the commits on a named branch be integrated into a named target branch, supplying a title/body directly, or converting an existing issue into the proposal. **[explicit fact — `head`, `base` required; `title` required unless `issue` given; `issue` required unless `title` given]**
- **Current state:** Two distinguishable branches exist ("head"/compare and "base"/target); no equivalent open pull request is asserted to already exist for this pair by the documentation reviewed — whether GitHub enforces a uniqueness rule here (e.g., one open PR per head→base pair) is `unknown/unresolved` in the material fetched today.
- **Policies / invariants:**
  - The actor must have write access to the head/source branch, or organization membership for org-owned repositories. **[rule/invariant — explicit fact]**
  - "Pull requests can only be opened between two different branches." **[rule/invariant — explicit fact, from the web-UI creation guide]**
  - Draft pull requests are only available on certain plans: "public repositories with GitHub Free... GitHub Pro... and... GitHub Team and GitHub Enterprise Cloud" (private repos need Team/Enterprise Cloud). **[rule/invariant — explicit fact, exact plan-availability wording from the REST docs]**
  - The request must not be judged spam/invalid by GitHub's own validation. **[rule/invariant — explicit fact, 422 "Validation failed, or the endpoint has been spammed"]**
- **Transition:** No pull request for this proposal → an open pull request exists, in either "ready for review" or "draft" state. **[explicit fact]**
- **Result:** On success, the created pull request resource (id, number, `html_url`, `state`, `draft`, and related fields) is returned. **[explicit fact — 201 response schema]** On failure, a `403 Forbidden` (insufficient access) or `422` (validation failed or judged spam) is returned instead. **[explicit fact — documented status codes]**
- **Events / effects:** A `pull_request` webhook event with `action: opened` is a documented action type for this event and is the reasonable-inference correlate of this contract's success. **[explicit fact for the action's existence in the documented action list; the exact per-action description text for `opened` was not retrievable in today's session — see `github-pull-request-unresolved.md` — so the pairing of this contract with `opened` is a reasonable inference, not a directly quoted description]** Creating a pull request also triggers notifications and is explicitly subject to GitHub's secondary rate limiting if done too quickly/repeatedly. **[explicit fact]**
- **Unknowns:** Whether a duplicate/equivalent open pull request for the same head→base pair is blocked, and what a GitHub App/bot must additionally hold (beyond a human collaborator's write access) to be this actor in the general case, are unresolved from today's material.

## Rules and defaults

### Rules / invariants

- The actor must have write access to the head/source branch (or org membership for org-owned repos) to open or update a pull request in that repository. **[rule/invariant]**
- A pull request requires two distinct branches (head and base); it cannot be opened against itself. **[rule/invariant]**
- `title` is required unless `issue` is supplied (and vice versa) — the request must resolve to a title one way or another. **[rule/invariant]**
- Draft pull requests are gated by the repository's/organization's GitHub plan (see Policies above). **[rule/invariant, with GitHub's own plan-name specifics preserved as stated]**

### Recommended defaults

- The `application/vnd.github.raw+json` response media type — returning the raw markdown `body` — "is the default if you do not pass any specific media type." **[recommended default — explicit hedge/default language from GitHub's own docs]**
- No default value for `draft` is documented beyond it being an optional boolean; the reasonable reading is that a pull request is "ready for review" unless `draft` is explicitly set true, but GitHub's docs do not state this default in so many words for the create operation — treated here as a **reasonable inference**, not a confirmed default.

### Decision precedence

Apply the standard order unless a higher-level governing policy explicitly establishes another order:

```text
Rule / invariant
→ explicit implementation requirement
→ explicit owner or user choice
→ recommended default
→ agent judgment
```

## Unknown / unresolved

- Whether GitHub blocks creating a second open pull request for the same head→base pair (no statement found in the fetched material).
- The exact description text GitHub's webhook docs use for the `opened` action specifically (the action's existence in the documented list is confirmed; the per-action description text could not be retrieved from the dynamically-loaded documentation content in today's session).
- The general rule for which non-human actors (GitHub Apps, bots, scheduled automation generally, beyond the one confirmed Dependabot case) may hold the "write access to head branch" requirement without a human directly present.
- Whether there is a limit on how many pull requests may be open at once between the same repositories/branches, or any other request-volume rule beyond the general secondary-rate-limit warning.

## Optional: operational realization

- **Realization name and status:** GitHub's own realizations of this capability, as documented by GitHub itself, fetched 2026-08-26.
- **Execution mode:** `software-primary` for the REST/GraphQL/CLI/web-UI paths (the caller supplies all inputs in one request; GitHub's platform executes the creation deterministically). `unknown` for the Dependabot bot path — GitHub's docs describe Dependabot's own decision process only at the level of "identifies an outdated dependency," not its internal control flow. **[reasonable inference for the software-primary paths; explicit "unknown" for Dependabot's internals]**
- **Implementation/business rationale:** Not documented by GitHub as a business rationale for the capability itself (rationale belongs to whichever product/team integrates it) — `none stated`.
- **Owner / operating context:** GitHub.com (and GitHub Enterprise, where the same REST/GraphQL/webhook surface applies per the docs referencing Enterprise Cloud plans).
- **Operational constraints:** Draft-PR availability is plan-gated (see Rules above); creating pull requests too quickly risks secondary rate limiting. **[explicit fact]**
- **Exposure:** UI, API (REST and, per GitHub's own cross-reference, GraphQL), tool (CLI), workflow/automation (bots).
- **Implementation references (known realizations):**

| Realization | Confirmed via (fetched 2026-08-26) | Notes |
|---|---|---|
| github.com web UI | `docs.github.com/en/pull-requests/.../creating-a-pull-request` | "Compare & pull request" flow; base vs. compare branch selection; standard or draft creation button. **[explicit fact]** |
| REST API | `docs.github.com/en/rest/pulls/pulls` (`POST /repos/{owner}/{repo}/pulls`) | Full parameter/response/status-code set confirmed directly from GitHub's own structured docs data. **[explicit fact]** |
| GraphQL API | Cross-reference only: the `pull_request` webhook doc states "For information about the APIs to manage pull requests, see the GraphQL API documentation ... or 'Pulls' in the REST API documentation." | Existence of a GraphQL path is an **explicit fact**; the specific mutation name/fields were not independently retrievable in today's session — see `github-pull-request-unresolved.md`. Not asserted beyond existence. |
| GitHub CLI | `cli.github.com/manual/gh_pr_create` | `gh pr create [flags]`; flags for base (`-B`), head (`-H`), title (`-t`), body (`-b`), draft (`-d`) confirmed. **[explicit fact]** |
| Bot / automation | `docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates` | "When Dependabot identifies an outdated dependency, it raises a pull request to update the manifest to the latest version of the dependency." Confirms at least one GitHub-native automated actor realizes this capability. **[explicit fact]** |

- **UX representations:** The "Compare & pull request" banner and the base/compare branch dropdown UI, and the separate "Create Pull Request" vs. "Create Draft Pull Request" buttons, as described in GitHub's own web-UI guide. **[explicit fact]**
- **Tests / verification:** Not documented by GitHub as part of this reference material (test evidence belongs to a specific consumer's own implementation, not GitHub's own capability docs).
- **Telemetry / audit:** Not documented in the fetched material beyond the notifications/secondary-rate-limit note above.
- **Authority, grounding, approval gates:** Write access to the head branch, or organization membership for org-owned repositories, as stated above.
- **Provenance:** See `github-pull-request-provenance.md`.

## Optional: shared elements and approved reuse

| Shared element | Kind | Created for capability | Approved reuse by capabilities | Notes |
|---|---|---|---|---|
| Pull request resource schema (id, number, `html_url`, `state`, `draft`, `mergeable`, `merged`, etc.) | schema | Open a pull request (returned on creation) | Merge a pull request (same resource is read/mutated) | Reuse here is a **reasonable inference** from both operations documenting overlapping response fields on the same REST resource, not an explicit GitHub statement of "shared schema, approved reuse." |

## Optional: agentic mappings

| Element | Kind | Relationship to this Capability MLE | Notes |
|---|---|---|---|
| `POST /repos/{owner}/{repo}/pulls` | tool | executable primitive realizing this capability's sole Interaction Contract | REST operation, confirmed 2026-08-26. |
| `gh pr create` | tool | executable primitive realizing this capability via the CLI realization | Confirmed 2026-08-26 via cli.github.com. |
| Dependabot | agent/automation | a documented, GitHub-native automated actor that invokes this capability | Confirmed to open PRs; not confirmed to merge them (see `merge-pull-request.md`). |

## Statement provenance

See `github-pull-request-provenance.md` for the full statement-provenance table covering both CRDs.
