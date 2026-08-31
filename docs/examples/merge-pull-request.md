# CRD: Merge a Pull Request

Status: draft — a real extraction from GitHub's own public REST API and webhook documentation (fetched 2026-08-26), independently audited for framework conformance and factual accuracy. See `github-pull-request-provenance.md` for the statement-provenance table and `github-pull-request-decision-log.md` for scope reasoning.

## Identity

- **Name:** Merge a pull request
- **Definition:** The ability for an authorized actor to integrate the changes proposed by an already-open, non-draft pull request into its target branch, subject to the repository's own merge policies, producing a definitive merged/closed outcome or an identifiable failure reason.
- **Status:** draft

## Core meaning

- **Capability purpose:** Enable the changes proposed by an open pull request to be incorporated into the target branch, using one of a small set of documented merge strategies, once the repository's own conditions for merging are satisfied. **[capability purpose]**
- **Meaningful outcome:** The pull request becomes merged (target branch now contains the proposed changes; response confirms `merged: true`), **or** the attempt is rejected with an identifiable reason (forbidden, not found, merge not currently possible, head-SHA mismatch, or validation failure). **[reasonable inference from documented response codes/fields]**
- **Boundaries — includes:**
  - Choosing (or accepting a default for) the merge strategy: merge commit, squash, or rebase. **[explicit fact — `merge_method` enum]**
  - Optionally overriding the automatic commit title/message. **[explicit fact — `commit_title`, `commit_message`]**
  - Optionally requiring the head branch to match a specific commit before merging, as a safety check. **[explicit fact — `sha` parameter]**
  - The immediate success/failure outcome of the merge attempt itself. **[reasonable inference from documented status codes]**
- **Boundaries — excludes:**
  - Opening the pull request being merged — a separate Capability MLE with a different actor and timing (see `open-pull-request.md`). **[MLE reasoning; see decision log]**
  - Reviewing/approving the pull request — governed by separate review mechanisms (`pull_request_review`) that this capability's policies may depend on, but do not themselves perform. **[explicit fact — webhook docs point to a separate event for review activity]**
  - Closing a pull request **without** merging — a distinct, separately documented operation (`PATCH .../pulls/{pull_number}` with `state: closed`), not the merge endpoint. **[explicit fact — distinct documented operation and status field]**
  - Enabling or disabling **auto-merge** (merging automatically once conditions are later satisfied) — a distinct, separately documented set of webhook actions (`auto_merge_enabled`, `auto_merge_disabled`) and CLI flag (`gh pr merge --auto`) whose immediate effect is "schedule a future merge," not "merge now." **[explicit fact for the action names/flag]** That this run doesn't draft it as its own CRD is this extraction's own scoping choice, not something GitHub's docs state — see decision log. **[this extraction's own scoping decision, not sourced]**
  - Checking whether a pull request has already been merged (`GET .../pulls/{pull_number}/merge`) — a distinct, separately documented read-only operation. **[explicit fact — distinct documented operation]**
  - Updating a pull request's branch with the latest base-branch changes (`PUT .../pulls/{pull_number}/update-branch`) — a distinct, separately documented operation. **[explicit fact — distinct documented operation]**
  - Configuring branch protection itself (required reviews, required status checks, required linear history) — those are policies this capability's contract is subject to, not actions this capability performs. **[explicit fact — separate documented feature]**
  - Merging a draft pull request: "You can't merge a draft pull request." **[rule/invariant — explicit fact]**
- **Terms and concepts:**
  - `actor` — the person or automated actor performing the merge → **schema.org/Person** for the human case ("A person (alive, dead, undead, or fictional)."). GitHub's own concrete role names (`Write`, `Maintain`, `Admin`) are preserved as-is since they are specific, documented permission levels, not a generic concept schema.org models. **[schema.org/Person fetched 2026-08-26; role names from repository-roles docs]**
  - `merge a pull request` (the command/intent) → **schema.org/UpdateAction** ("The act of managing by changing/editing the state of the object.") — merging changes the state of both the target branch and the pull request itself. **[schema.org/UpdateAction description fetched 2026-08-26]**
  - `review` (a policy input to this capability, not the capability itself) → **schema.org/ReviewAction** ("The act of producing a balanced opinion about the object for an audience. An agent reviews an object with participants resulting in a review.") — used here only to ground the concept referenced by "required reviews," not to claim GitHub's review mechanism is identical to this schema.org action. **[schema.org/ReviewAction description fetched 2026-08-26]**
  - `merge method` / `merge commit` / `squash` / `rebase` / `mergeable_state` / `SHA` / `status check` — GitHub's (and git's) own concrete terms; no closer standard-vocabulary equivalent was identified, so they are preserved as-is rather than forced into a generic term. **[explicit fact for each term's existence and, where quoted, its documented meaning]**
- **Tags:** `notification-triggering` — merging is explicitly documented as triggering notifications and being subject to the same secondary-rate-limiting warning as creation, a cross-cutting dimension not otherwise derivable from the fields above (chosen over `network-touching`, which would add nothing here beyond what `exposure: API/UI` on a hosted product already implies). **[explicit fact]**

## Interaction Contract MLEs

### Merge a pull request

- **Actor:** A repository member holding the `Write`, `Maintain`, or `Admin` repository role (or an actor whose access is otherwise elevated, e.g. an organization owner or a custom role with equivalent rights) — `Read` and `Triage` roles cannot merge. **[explicit fact — "the required role to merge a pull request is Write or higher... Write, Maintain, or Admin roles [can merge], with Read and Triage roles unable to perform this action"]**
- **Command / intent:** Integrate the pull request's proposed commits into its base branch using a specified or repository-permitted merge method, optionally supplying a commit title/message and a head-SHA precondition. **[explicit fact]**
- **Current state:** An open, non-draft pull request exists. **[explicit fact — draft PRs cannot be merged]** Its `mergeable`/`mergeable_state` may or may not currently be clean, depending on branch protection and conflict status; the full set of possible `mergeable_state` values and their individual meanings is not documented on the pages fetched today (one example value, `clean`, was observed) — see `github-pull-request-unresolved.md`.
- **Policies / invariants:**
  - The actor must hold `Write`, `Maintain`, or `Admin` repository access (or bypass rights). **[rule/invariant — explicit fact]**
  - A draft pull request cannot be merged. **[rule/invariant — explicit fact]**
  - If the target branch is protected and requires reviews: "collaborators can only push changes to a protected branch via a pull request that is approved by the required number of reviewers," and "if a collaborator attempts to merge a pull request with pending or rejected reviews into the protected branch, the collaborator will receive an error message." **[rule/invariant — explicit fact, exact wording from GitHub's protected-branches docs]**
  - If the target branch requires status checks: "all required status checks must pass before collaborators can merge changes into the protected branch"; merging is prevented "until checks achieve successful, skipped, or neutral status." **[rule/invariant — explicit fact]**
  - If the target branch requires linear history: only squash or rebase merges are permitted (merge commits are blocked). **[rule/invariant — explicit fact, "Enforcing a linear commit history prevents collaborators from pushing merge commits to the branch"]**
  - "By default, the restrictions of a branch protection rule don't apply to people with admin permissions to the repository or custom roles with the 'bypass branch protections' permission" — this is GitHub's own stated **default**, and an organization may instead choose to apply the restrictions to admins/bypass-roles as well. **[recommended default / explicit owner choice — preserving GitHub's own "by default" hedge language exactly; this is NOT a universal rule, since the docs explicitly describe both the default and an override]**
  - If `sha` is supplied, it must match the pull request's current head commit. **[rule/invariant — explicit fact, 409 "Conflict if sha was provided and pull request head did not match"]**
  - `merge_method`, when supplied, must be one of `merge`, `squash`, or `rebase`; no documented default value for this parameter was found — see Recommended defaults. **[rule/invariant for the enum; the absence of a stated default is `unknown/unresolved`, not assumed]**
- **Transition:** Open, non-draft pull request (mergeable state permitting) → merged pull request; the pull request's state also becomes closed as a result of merging. **[explicit fact for "merged"; "closed as a result" is a reasonable inference from the pull request resource's own `state`/`merged` fields observed in the REST schema, not a sentence quoted directly from the merge-endpoint docs]**
- **Result:** On success (`200`): a body containing `sha` (the resulting merge commit SHA), `merged: true`, and a `message` (e.g. "Pull Request successfully merged"). **[explicit fact — exact example response captured from GitHub's own structured docs data]** On failure: `403 Forbidden`; `404` resource not found; `405 Method Not Allowed if merge cannot be performed`; `409 Conflict if sha was provided and pull request head did not match`; `422` validation failed or the endpoint has been spammed. **[explicit fact — exact wording from GitHub's own documented status codes]**
- **Events / effects:** A `pull_request` webhook event with `action: closed` is a documented action type for this event, and GitHub's REST pull-request resource carries a `merged` boolean field distinguishing a merge from a plain close. **[explicit fact for both the `closed` action's existence and the `merged` field's existence, fetched separately]** Whether the webhook's `pull_request` object payload for the `closed` action itself explicitly documents the `merged` field's role in that specific event (as opposed to only in the REST resource schema) could not be confirmed from the dynamically-loaded webhook documentation content in today's session — treated as a **reasonable inference**, not a directly quoted fact; see `github-pull-request-unresolved.md`. Merging also triggers notifications and is subject to the same secondary-rate-limiting warning as creation. **[explicit fact]**
- **Unknowns:** The full enumeration and meaning of `mergeable_state` values; whether the webhook `closed` payload's description text explicitly ties `merged` to that action; whether any default `merge_method` is applied when the parameter is omitted; the precise conditions (beyond "cannot be performed") that produce `405` versus `422`. (Resolved since initial extraction: GitHub's merge queue itself performs this capability's merge action once required checks pass — see Optional: operational realization.)

## Rules and defaults

### Rules / invariants

- Only actors with `Write`, `Maintain`, or `Admin` repository access (or explicit bypass rights) may merge a pull request. **[rule/invariant]**
- A draft pull request cannot be merged. **[rule/invariant]**
- Required reviews, if configured on the target branch, must be satisfied (approved by the required number of reviewers, with no pending/rejected reviews blocking) before a merge can succeed. **[rule/invariant]**
- Required status checks, if configured, must reach a successful/skipped/neutral state before a merge can succeed. **[rule/invariant]**
- Required linear history, if configured, restricts the permitted `merge_method` to squash or rebase (merge commits are blocked). **[rule/invariant]**
- If `sha` is supplied in the request, it must match the pull request's current head commit, or the merge fails with `409`. **[rule/invariant]**

### Recommended defaults

- By default, branch-protection restrictions (required reviews/status checks) do not apply to actors with admin permissions or an explicit "bypass branch protections" role — this is GitHub's own stated default behavior, which an organization may deliberately turn off. **[recommended default — preserving the source's own "by default" language; must not be strengthened into a universal rule]**
- The web UI's plain "Merge pull request" button behavior is described as using a merge commit with `--no-ff`; whether the REST API's `merge_method` parameter shares an equivalent unstated default was not confirmed in today's material and is treated as `unknown/unresolved` rather than assumed to be the same. **[recommended default for the web-UI path only; explicitly not extended to the API by inference]**
- Optionally deleting the head branch after a successful merge "to keep the list of branches in your repository tidy" is described as a convenience, not a requirement. **[recommended default — explicit hedge language, "not a requirement"]**

### Decision precedence

Apply the standard order unless a higher-level governing policy explicitly establishes another order:

```text
Rule / invariant
→ explicit implementation requirement
→ explicit owner or user choice
→ recommended default
→ agent judgment
```

Concretely for this capability: a required-review or required-status-check policy (rule/invariant) cannot be overridden by a caller's choice of `merge_method` or by agent judgment; an admin's documented bypass right is itself an explicit, GitHub-stated exception to that rule, not a violation of it.

## Unknown / unresolved

- The full set of `mergeable_state` values and what each one means (only `clean` was observed as an example value in today's fetched material; the GitHub docs pages reviewed today do not enumerate or define the full set).
- Whether the webhook payload's own documentation (as opposed to the REST resource schema) explicitly states that `pull_request.merged` distinguishes a "closed via merge" outcome from a plain close for the `closed` action — the relevant per-action documentation content did not load statically in today's fetch attempts.
- Whether a default `merge_method` is applied by the REST/GraphQL API when the parameter is omitted.
- The precise, general conditions that distinguish a `405` from a `422` failure beyond the documented one-line descriptions.
- Whether GitHub Actions workflows or other bot tokens can be the actor for this capability under the general `Write`/`Maintain`/`Admin` rule, or need some additional grant — attempts to confirm the exact GITHUB_TOKEN permission scope for pull requests were inconclusive in today's session (the relevant permissions table did not load in the fetched content).
- Whether Dependabot, or any other GitHub-native bot, is documented as ever merging (as opposed to only opening) a pull request — the material fetched today explicitly describes Dependabot pull requests as manually reviewed and merged by the user, so no *third-party* bot/automation realization of *this* capability specifically is currently confirmed (see `open-pull-request.md` for the corresponding, confirmed *open* realization; GitHub's own merge queue, below, is a separate, confirmed first-party case).

## Optional: operational realization

- **Realization name and status:** GitHub's own realizations of this capability, as documented by GitHub itself, fetched 2026-08-26.
- **Execution mode:** `software-primary` for the REST/GraphQL/CLI/web-UI synchronous paths — the caller's single request is evaluated against current policy state and resolved immediately. GitHub also documents a second REST mechanism, "Merge a pull request asynchronously" (`PUT .../pulls/{pull_number}/merge-async`, paired with `GET .../merge-async/{uuid}`), whose existence is an **explicit fact** (both operations are listed in GitHub's own REST reference) but whose internal mechanics were not fetched in today's session — treated as the same capability's alternate realization, execution mode `unknown`. GitHub's merge queue (see known realizations below) is also `software-primary`: it is GitHub's own platform automation evaluating its own stated policy ("GitHub will merge all these changes into the base_branch once the checks required by the branch protections of base_branch pass"), not an agent making a judgment call.
- **Implementation/business rationale:** Not documented by GitHub as a business rationale for the capability itself — `none stated`.
- **Owner / operating context:** GitHub.com (and GitHub Enterprise, per the same plan cross-references used in `open-pull-request.md`).
- **Operational constraints:** Merging is gated by whatever branch-protection policy the target repository has configured (see Rules above); merging too quickly/repeatedly risks secondary rate limiting. **[explicit fact]**
- **Exposure:** UI, API (REST and, per GitHub's own cross-reference, GraphQL), tool (CLI).
- **Implementation references (known realizations):**

| Realization | Confirmed via (fetched 2026-08-26) | Notes |
|---|---|---|
| github.com web UI | `docs.github.com/en/pull-requests/.../merging-a-pull-request` and `.../about-pull-request-merges` | Merge button / dropdown with three merge-method choices; "You can't merge a draft pull request." **[explicit fact]** |
| REST API | `docs.github.com/en/rest/pulls/pulls#merge-a-pull-request` (`PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge`) | Full parameter/response/status-code set confirmed directly from GitHub's own structured docs data, including the exact `200`/`403`/`404`/`405`/`409`/`422` wording. **[explicit fact]** |
| GraphQL API | Cross-reference only, same as `open-pull-request.md` | Existence of a GraphQL path is an **explicit fact**; a `mergePullRequest`-style mutation's specific name/fields were not independently retrievable in today's session — see `github-pull-request-unresolved.md`. |
| GitHub CLI | `cli.github.com/manual/gh_pr_merge` | `gh pr merge [<number> \| <url> \| <branch>] [flags]`; merge-strategy flags `-m/-s/-r`, `--auto`/`--disable-auto` (auto-merge, out of this capability's scope — see boundaries), `--admin` (documented bypass of merge requirements using administrator privileges — this directly corroborates the branch-protection admin-bypass default above), `-d/--delete-branch`. **[explicit fact]** |
| GitHub merge queue | `docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue` (fetched and independently re-confirmed 2026-08-26, after initial extraction) | "GitHub will merge all these changes into the `base_branch` once the checks required by the branch protections of `base_branch` pass." A **confirmed, GitHub-native automated realization** of this capability — not just a sequencing mechanism. **[explicit fact]** |
| Third-party bots / automation | Not confirmed for this capability specifically (see `github-pull-request-unresolved.md`) | Distinguish from `open-pull-request.md`, where Dependabot is a confirmed bot realization of *opening* — no equivalent third-party-bot confirmation exists here for *merging* (GitHub's own merge queue, above, is a separate, confirmed case). |

- **UX representations:** The merge button and its adjacent merge-method dropdown, and the disabled/blocked state of that control when branch-protection conditions are unmet, as described in GitHub's own web-UI guide. **[explicit fact]**
- **Tests / verification:** Not documented by GitHub as part of this reference material.
- **Telemetry / audit:** Not documented in the fetched material beyond the notifications/secondary-rate-limit note above.
- **Authority, grounding, approval gates:** `Write`/`Maintain`/`Admin` repository role, subject to branch-protection policy and its documented default admin-bypass behavior, as stated above.
- **Provenance:** See `github-pull-request-provenance.md`.

## Optional: shared elements and approved reuse

| Shared element | Kind | Created for capability | Approved reuse by capabilities | Notes |
|---|---|---|---|---|
| Pull request resource schema (`merged`, `mergeable`, `mergeable_state`, `merged_by`, `state`, etc.) | schema | Open a pull request (first returned on creation) | Merge a pull request (read and mutated at merge time) | Same schema-overlap basis as noted in `open-pull-request.md`; a **reasonable inference**, not an explicit GitHub "shared schema" statement. |
| Branch protection rule (required reviews, required status checks, required linear history, admin bypass) | policy/configuration | Not created "for" either pull-request capability specifically — it is a repository-level configuration documented independently | Merge a pull request (governs whether a merge attempt succeeds) | GitHub documents branch protection as its own feature area, not as belonging to the merge capability; the merge capability's policies section only consumes it. |

## Optional: agentic mappings

| Element | Kind | Relationship to this Capability MLE | Notes |
|---|---|---|---|
| `PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge` | tool | executable primitive realizing this capability's Interaction Contract | REST operation, confirmed 2026-08-26. |
| `gh pr merge` | tool | executable primitive realizing this capability via the CLI realization | Confirmed 2026-08-26 via cli.github.com. |
| `PUT .../pulls/{pull_number}/merge-async` + `GET .../merge-async/{uuid}` | tool | alternate executable primitive pair for the same capability | Existence confirmed 2026-08-26; internal mechanics not fetched — see `github-pull-request-unresolved.md`. |
| GitHub merge queue | workflow | GitHub-native automated realization of this capability's Interaction Contract | Confirmed 2026-08-26 (see known realizations above); not a "skill" or "tool" in the agent sense — it is the platform performing this capability's own merge action on its own documented policy. |

## Statement provenance

See `github-pull-request-provenance.md` for the full statement-provenance table covering both CRDs.
