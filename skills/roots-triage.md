# roots-triage

> **The hand coming back.** Read what the community opened on the seed and decide what enters.
> Without this, "collaborative" runs in one direction only — outward — and a project that only
> speaks stops being a project and becomes a broadcast.

## When to use
Periodically (a weekly pass is enough), and always **before bumping the spec version**: a bump that
ignores what people reported ships the same problem again with a new number.

## Inputs
- Open issues and PRs on the upstream.
- Your local canonical's version and its local extensions.

## Steps
1. **List what is open.** With `gh`: `gh issue list -R <upstream> --limit 50`. Without it, read the
   repo's issues page — the ladder applies to reading too, and reading needs no credentials.
2. **Classify each one** — the four buckets are not about importance, they are about *what has to
   happen next*:

   | Bucket | It is | What it needs |
   |---|---|---|
   | **Correction** | the text is wrong/ambiguous | a wording fix — cheap, do it now |
   | **Convergence** | someone else's use found the same thing you did | merge the two statements into one; **their measurement plus yours is stronger than either** |
   | **Divergence** | their environment needs the opposite of yours | it is a `recipes/` pack or a documented option — **not** a core rule |
   | **Out of scope** | a request for a feature the seed is not | answer with *why* the boundary is there; that answer is documentation |

3. **Reply to every one, even the ones you decline.** An unanswered issue teaches the next person not
   to open one. A declined issue with a reason teaches them where the boundary is.
4. **Promote what enters** into the spec with its § and its changelog entry — **crediting the
   reporter**. The changelog is the only place where a contribution becomes visible to everyone else.
5. **Close the loop**: link the issue from the changelog entry, and the entry from the issue.

## Verification
- Every open item ended in one of: merged · answered with a reason · converted into a `recipe` ·
  labelled as pending a decision **with the decision named**.
- Nothing entered the core that is really one environment's rule (the most common drift: a domain
  quirk promoted to a universal law because one deployment hit it twice).

## Notes
- Convergence is the valuable bucket and the easiest to miss: two deployments reporting the same
  friction from different stacks is the strongest evidence a spec can get — stronger than the
  maintainer's own experience, because it is the only evidence that is not yours.
