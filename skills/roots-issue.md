---
name: roots-issue
description: Report that the seed's own text is wrong, ambiguous or silently harmful: a section that contradicts another, a rule that causes damage if followed literally, a term with two meanings. Invoke it when you can quote the offending line. NOT for proposing a new convention (that is `roots-suggest`) and NOT when you can just write the fix (that is `roots-pr`).
---

# roots-issue

> **Report that the seed itself is wrong, ambiguous or silently harmful** — as opposed to proposing
> something new (`roots-suggest`). The distinction matters: a proposal asks for a decision, a bug
> report asks for a correction and can be verified against the text.

## When to use
- A section **contradicts** another (the two most expensive kinds: a rule restated differently in a
  template, and a convention whose example does the opposite).
- A rule that, followed literally, **causes damage** (something gets committed that should not).
- An instruction that cannot be executed as written (a script that is referenced and does not exist,
  a field with no definition, a step that assumes a tool the reader does not have).
- A term used with **two meanings** in the same document.

## Inputs
- Spec **version** and the exact **line or heading**.
- What it says · what happens if you follow it · what it should say.
- Whether you hit it in practice (and what it cost) — a report with a scar gets fixed first.

## Steps
1. **Quote the text.** Not a paraphrase: the sentence, as it is. Reports that paraphrase get
   answered with "that is not what it says".
2. **Separate `is` from `should`.** *"§ X says the agent may do Y"* is the bug; *"it should say Z"* is
   the fix. Send both, labelled. (A real one, fixed in 1.19: the spec said light workbench files could
   be committed, while real use had converged on ignoring the folder wholesale — the section described
   the opposite of the practice, and anyone following it committed their work surface.)
3. **Scrub** — `scripts/roots-upstream.sh scrub <draft.md>`. On the publishing path it **refuses**
   if it flags anything, on all three rungs: a flagged body prints no URL either, because the
   prefilled URL *is* the body.
4. **Check the ladder and send** — `scripts/roots-upstream.sh issue "<title>" <body.md> bug --yes`,
   with the same rule: only a real publish counts as published.

## Body template
```markdown
**Seed version:** vX.Y · **Section:** <heading> · **Line:** <if known>

### It says
> <verbatim quote>

### What happens if you follow it
<the concrete consequence. If you hit it, say what it cost.>

### What it should say
<the corrected wording>
```

## Verification
- The quote matches the published upstream text (check the upstream, not your local copy — yours may
  already carry local extensions).
- The report is about the **text**, not about your setup.

## Notes
- If the fix is obvious and small, write it as a PR instead (`roots-pr`): a correction that arrives
  already written gets merged, one that arrives as a complaint waits.
