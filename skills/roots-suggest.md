# roots-suggest

> **Turn something this deployment learned into a proposal on the public seed.** The seed already
> said *what* to contribute (§ *Contributing to the upstream*) and *what* to scrub (§ *Public
> hygiene*). Both were written, and neither happened — because a policy with no invocable surface
> is a policy nobody runs. This is that surface.

## When to use
When the local use of `.roots/` taught something the spec does not say — or says the **opposite** of.
The typical trigger is an **incident with a measurement**: a rule that cost an error, a folder that
filled up, a convention that everyone quietly broke because it did not match reality.

Do **not** use it for: a preference, a naming taste, or something that only makes sense inside your
workspace. That belongs in your local canonical (§ *Sync with the canonical upstream*).

## Inputs
- **The lesson**, in one sentence.
- **The evidence**: what was measured, with the number if there is one, and the date. A proposal
  backed by *"1929 loose files, invisible to `git status`"* travels; one backed by *"it feels
  cleaner"* does not.
- **Which § of the spec it touches** — and whether it is **core** or belongs in a `recipes/` pack
  (domain-specific: a framework's upgrade rules, a vendor's API, a stack's quirks).

## Steps
1. **Isolate the lesson from the environment that produced it.** The test is mechanical: remove
   every name, host, id and path — *is there anything left?* If nothing survives, the piece was
   never generic; stop and keep it local. **This is the work**, not a formality: generalizing is
   what makes the thing reusable.
2. **Scrub** — `scripts/roots-upstream.sh scrub <draft.md>` runs the mechanical pass (domains, IPs,
   keys, absolute paths, emails). It **warns, never blocks**; a human still reads it.
3. **Write the body** with the template below. Keep the incident, drop the anecdote.
4. **Check what this machine can do** — `scripts/roots-upstream.sh check`. It prints the ladder:
   `gh` → `$GITHUB_TOKEN` → **prefilled URL** (always available, no credentials).
   ⛔ **Never report an issue as "opened" when only a URL was printed.** The rung you actually used
   is part of the result.
5. **Show the exact text and ask.** Publishing is an outward action: it goes out with an explicit OK,
   never as a side effect of drafting.
6. **Send** — `scripts/roots-upstream.sh issue "<title>" <body.md> proposal --yes` — and record the
   issue URL in `.roots/journal/notes.md`, so the next session does not propose it again.

## Body template
```markdown
**Seed version in use:** vX.Y · **Section:** <the § it touches> · **Scope:** core | recipe

### What we measured
<the fact, with its number and date — this is what makes it a proposal and not an opinion>

### What the spec says today
<quote the line. If it says the opposite of what real use converged to, say so plainly.>

### What we propose
<the convention, in the form it would be written into the spec>

### Why it generalizes
<what makes this true outside the deployment that found it>

*Specifics scrubbed: roles instead of names, no hosts/ids/paths.*
```

## Verification
- The body names **an existing section** of the spec (or proposes where a new one goes).
- `scrub` is clean, and a human read it after the machine did.
- The result states **which rung published it** — and if it was the URL, that nothing was published yet.

## Notes
- A proposal that would change a **hard rule** should carry the incident that made the rule wrong.
  The upstream cannot verify your environment; the measurement is the only thing that crosses over.
- Sibling commands: `roots-issue` (something is broken/ambiguous), `roots-pr` (the text is already
  written and you want it merged), `roots-triage` (read what the community sent back).
