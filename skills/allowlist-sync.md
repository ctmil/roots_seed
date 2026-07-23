# allowlist-sync

> Keep the agent's permission allowlist (`.claude/settings.json` → `permissions.allow`) in step with
> **real usage** and with the **evolving `.roots`/workspace structure**, so a long autonomous run is
> not interrupted by permission prompts for routine commands.

## When to use
The user says "it keeps asking for permissions", or after adding new scripts/structure under
`.roots/`, or on an explicit "update the allowlist".

## Principle
Prompts recur when the allowlist holds **exact** entries (a single fully-specified command line).
Prefer **command-family patterns** (`<cmd> *`) and **workspace-structure patterns** (the fleet
scripts, reading the read-only sources). An allowlist of exact lines is an allowlist that never
matches twice.

## Steps
1. **Read the current state**: the project settings file, plus any local/user-level one, so you do
   not add duplicates.
2. **Scan real usage**: count the commands actually issued in recent session transcripts (first
   token + subcommand). Identify which families are generating the prompts — typically version
   control, the language runtimes, file manipulation and HTTP clients.
3. **Generalize**: one broad-but-reasonable pattern per frequent family. Do not enumerate variants.
4. **Cover the workspace structure** (re-read `.roots/` so the allowlist tracks it):
   - fleet scripts present at the root → one pattern each;
   - read-only source trees → **`Read` only**, never `Write`/`Edit`;
   - new generators/migrators under `.roots/scripts/` → usually already covered by the runtime
     family pattern.
5. **Merge** into `permissions.allow`, de-duplicating. Never touch `deny`/`ask` — those are the
   human's guardrails, not yours to widen.
6. **Report** which families were added, and explicitly flag the broad-execution ones (language
   runtimes, shells, HTTP clients, delete) so the human widens them knowingly.

## Notes
- Conscious trade-off: a runtime or delete family pattern is effectively broad execution/deletion
  inside that workspace. That is the human's call for their own trusted workspace — record it in the
  report rather than deciding silently.
- If friction persists despite the allowlist, the answer is a looser **session-level** permission
  mode, not a hundred more exact entries.
- Register the convention in the project's `.roots/` too, so the allowlist keeps following the
  structure as it grows (new scripts, new source paths).
