# Decision Log: GitHub Pull Request Examples

## 1. Individual Capability MLE checks (run before any combine/decompose decision)

Per the skill's non-negotiable rule, each candidate element was tested against the Capability MLE questions **individually**, before deciding whether "open" and "merge" should be one CRD or two, and before deciding what else to fold in or exclude.

### 1a. "Open a pull request" — tested alone

| Question | Answer |
|---|---|
| Understandable independently? | Yes — proposing that changes on one branch be considered for integration into another is a complete, nameable idea on its own, regardless of what happens to the proposal afterward. |
| Can it be invoked/used meaningfully? | Yes — `POST /repos/{owner}/{repo}/pulls`, `gh pr create`, the web UI's "Compare & pull request" flow, and Dependabot's own automated raising of PRs all invoke exactly this. |
| Can success/failure be determined? | Yes — `201` with the created resource vs. `403`/`422` with an identifiable reason. |
| Would further splitting lose purpose context? | Yes — splitting "choose head branch" / "choose base branch" / "write title" into separate capabilities would leave three fragments, none of which is independently meaningful without the others; they are fields of one contract, not separate abilities. |
| Would enlarging it fold in other independently meaningful abilities? | Yes, if merging were folded in (see 1b) — so it must not be enlarged that way. |

**Result: passes alone.** Kept as its own Capability MLE.

### 1b. "Merge a pull request" — tested alone

| Question | Answer |
|---|---|
| Understandable independently? | Yes — integrating an already-open proposal's changes into its target branch is a complete, nameable idea that presupposes an open PR exists but does not require knowing *when* or *by whom* it was opened. |
| Can it be invoked/used meaningfully? | Yes — `PUT .../pulls/{pull_number}/merge`, `gh pr merge`, and the web UI's merge button all invoke exactly this, typically by a different actor (a maintainer/reviewer with `Write`+ access) than the PR's author, often at a much later time. |
| Can success/failure be determined? | Yes — `200` with `merged: true` vs. `403`/`404`/`405`/`409`/`422`, each with a distinct documented meaning. |
| Would further splitting lose purpose context? | Yes — splitting "check mergeable_state" / "pick merge_method" / "confirm sha" into separate capabilities would leave fragments with no independent purpose; they are policy inputs and parameters of one contract. |
| Would enlarging it fold in other independently meaningful abilities? | Yes, if opening were folded in (see below) — so it must not be enlarged that way either. |

**Result: passes alone.** Kept as its own Capability MLE.

### 1c. Combine check

Because **both** "open" and "merge" independently pass the MLE test on their own, the rule is explicit: do not combine them, even though they are obviously related and operate on the same underlying resource. Concretely:

- Different actors in the common case: the PR author opens it; a maintainer/reviewer with elevated access merges it. GitHub's own repository-role documentation states `Write`, `Maintain`, or `Admin` is required to merge, while opening only requires write access to the *head* branch (which may be a fork the author alone controls).
- Different, non-overlapping policy sets: opening is gated by plan-based draft availability and write-access-to-head; merging is gated by branch protection (required reviews, required status checks, linear history) that has nothing to do with whether the PR could be opened in the first place.
- Different, non-overlapping timing: a PR can be (and very often is) open for a long interval with zero relationship to whether or when it is ever merged, or whether it is merged at all.
- Combining them would produce exactly the "vague feature bucket" the MLE model warns against — a single document trying to carry two different actors, two different policy sets, and two different timings under one name.

**Decision: two CRDs, not one.** This matches the task's own expectation ("likely 'two, they're independently meaningful and usable'"), but the check was performed and recorded per the rule, not assumed from the task's hint.

## 2. Other candidate elements tested and excluded (in-scope task boundary)

The task fixed the scope at exactly two capabilities and instructed that any third candidate be noted here rather than documented. During extraction, several other GitHub-documented operations were encountered that would themselves independently pass the Capability MLE test (each has its own actor, command, determinable result, and would lose purpose context if fragmented further). They are named here, with a one-line MLE justification, and explicitly excluded from this run:

- **"Update a pull request" (`PATCH /repos/{owner}/{repo}/pulls/{pull_number}`)** — edits title/body/base, or sets `state: closed` to close *without* merging. Passes the MLE test alone (different actor timing than either open or merge; a distinct, determinable 200/403/422 outcome; splitting further would lose context). **Excluded from this run.**
- **"Check if a pull request has been merged" (`GET .../pulls/{pull_number}/merge`)** — a read-only query with its own determinable 204/404 outcome. Passes the MLE test alone (it is invoked independently of any create or merge attempt, e.g. by a CI system polling status). **Excluded from this run.**
- **Enable/disable auto-merge (`auto_merge_enabled`/`auto_merge_disabled` webhook actions; `gh pr merge --auto`/`--disable-auto`)** — the immediate, determinable outcome of invoking this is "a future merge is now scheduled," not "the PR is merged now." Passes the MLE test alone (different command/intent and different immediate result than the merge capability itself, even though it eventually causes a merge). **Excluded from this run; also recorded as an explicit boundary-exclusion inside `merge-pull-request.md`.**
- **"Update a pull request branch" (`PUT .../pulls/{pull_number}/update-branch`)** — syncs the PR's head branch with the latest base-branch changes. Passes the MLE test alone (independent actor/command/result; does not itself open or merge anything). **Excluded from this run.**
- **Reviewing a pull request (`pull_request_review` events, review approve/request-changes/comment)** — GitHub's own webhook docs explicitly separate this from the `pull_request` event. It clearly passes the MLE test alone and is a strong candidate capability, but is explicitly out of scope for this run (the task named only "open" and "merge"). It appears in `merge-pull-request.md` only as a **policy input** (a required-reviews condition merging is subject to), never as an action this run's CRDs perform.
- **Merge queue (`merge_group` webhook object)** — GitHub documents a "merge queue" that groups pull requests before merging. Initially left as an unresolved note because the dedicated documentation page 404'd at the guessed URL during this run; a post-audit re-check located the current page and confirmed the queue itself performs the merge action, so it is now recorded as a confirmed automated **realization** of "Merge a pull request" (not a separate capability) in `merge-pull-request.md`, rather than left unresolved.

No third capability was added to the required output. These are recorded here, per the task's own instruction, as the "stop and note it as out of scope" response to finding more than two viable candidates.

## 3. Input variants folded into "Open a pull request" without a separate MLE check

The `draft` boolean and the `issue`-to-PR conversion parameter are both handled by the *same* `POST /repos/{owner}/{repo}/pulls` operation, with the same actor, same command shape, and same success/failure outcome structure as a plain title/body creation — they are input variants of one contract, not separate named features with their own actor or determinable outcome, so no individual MLE test was needed before including them inside the single "Open a pull request" Interaction Contract.

## 4. Generic/reusable CRD from the start

The task explicitly required generic/reusable CRDs "from the start," which is a deliberate departure from Extract mode's default (specific/operational set only, generic projection only on request or demonstrated reuse). This is recorded here because it is a scope decision the skill would not have made on its own without the task's explicit instruction — and because it changes what "known realizations" must mean: for a generic CRD generalized from one product's own documented behavior, that product (GitHub.com itself) is realization #1 by construction and is listed as such in the inventory, per `inventory-format.md`'s own guidance, rather than treated as if the capability had no realizations yet.

## 5. Terms-and-concepts grounding: what was checked and rejected

Before grounding "merge" in schema.org, `schema.org/MergeAction` was checked directly and found not to exist (404 from schema.org itself, fetched today). Rather than either inventing a plausible-sounding schema.org type from memory or leaving the term ungrounded, `schema.org/UpdateAction` ("The act of managing by changing/editing the state of the object") was used instead, since merging does change the state of the base branch and the pull request itself, and its description was independently verified. This is recorded because it is exactly the kind of checkpoint the skill instructions call for on generalizing/grounding choices — verify, don't assume a plausible-sounding term is real.

## 6. VS Code extension: investigated, not asserted as a known realization

The VS Code "GitHub Pull Requests" extension was investigated as a candidate IDE-integration realization (the task's own example). Its existence, ownership (`microsoft` org), and general "review and manage pull requests" purpose were confirmed via `api.github.com` and its own README, fetched today. However, neither of those sources, in the content actually retrieved, explicitly stated that the extension performs the *create* or *merge* actions specifically (the README's own feature list emphasizes browsing, reviewing, and checking out PRs). Per the non-negotiable rule against presenting an unconfirmed capability as a live, verified outcome, it was **not** added to either CRD's known-realizations table, and is instead recorded as an open question in `github-pull-request-unresolved.md` and as an explicit inventory note.

## 7. Branch-protection source URL correction

The task-supplied URL for branch protection (`.../managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/about-protected-branches`) returned `404 Not Found` on first fetch. Per the task's own fallback instruction, the current equivalent page was located and used instead: `docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches`. This substitution is recorded in `github-pull-request-provenance.md` against every statement sourced from that page.

## 8. Post-audit fix-up (2026-08-26, same day)

An independent blind audit re-fetched a sample of this extraction's claims against GitHub's live docs and found the methodology solid overall, with one real defect and three small cleanups, all applied directly to the CRDs:

1. The merge queue's own documentation page, which 404'd at the URL guessed during extraction (see §2 above), was re-located and confirmed to state that GitHub's merge queue performs the merge itself once required checks pass — added as a confirmed automated realization in `merge-pull-request.md`, rather than left unresolved.
2. Both CRDs' universal tag was `network-touching`, justified entirely by notification/rate-limit language — retagged `notification-triggering` to match the actual justification (this also prompted a framework-level clarification of tag-selection guidance, tracked separately in the repository's own changelog, not here).
3. The "Meaningful outcome" statement in each CRD had been labeled with the semantic class of a different required field (`capability purpose`) — corrected to remove the mislabel.
4. Two "Boundaries — excludes" bullets (the "editing" exclusion in `open-pull-request.md`, the "auto-merge" exclusion in `merge-pull-request.md`) bundled a sourced fact and this extraction's own scoping decision under one `explicit fact` tag — split into two separately labeled clauses.

## 9. Related MLEs by Dimension trial, and why Communication was included for one CRD but not the other (2026-09-01)

Applied the framework's new "Related MLEs by Dimension" model to both CRDs, as a third and fourth trial of that model (after `reconcile-payments` and `request-moving-quote`, both illustrative). This trial is the more demanding one: everything traced to must be genuinely sourced in the material already fetched for this extraction, not written to fit the template.

Five dimensions across the two CRDs were deliberately omitted rather than filled, each recorded with a reason inline in the CRD itself: `Interaction/Behaviour` (self-referential to each CRD's own sole contract), `Backend/Execution` and `Data/Information` (GitHub documents its public contract, not its internal implementation or data model), and `Verification` (each CRD already states plainly that GitHub doesn't document test/verification evidence for this material).

`Communication` was included for `merge-pull-request` but omitted for `open-pull-request` — a deliberate asymmetry, not an inconsistency. GitHub's merge endpoint has an exact, quoted success-response string ("Pull Request successfully merged," already in `github-pull-request-provenance.md`) to ground a Communication MLE on; the create endpoint's documented response has no equivalent quoted text, only the separately-documented fact that creation "triggers notifications" without stating their content. Writing a Communication MLE for `open-pull-request` would have meant inventing wording GitHub hasn't published — exactly what the framework's evidence discipline forbids. The one Communication MLE that was written (`Merge Success Confirmation`) intentionally omits `terminology` and `toneStyle`: only one exact response string is sourced, not a broader tone/terminology policy behind it, and a second, blocked-merge communication was considered and rejected for the same reason (its existence is sourced — "an error message" — but not its wording).
