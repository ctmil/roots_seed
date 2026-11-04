---
name: htree-tasks
description: Work the person's tasks on one or more htree task boards (Odoo backends exposing the OCAPI htree gateway) — load or edit their tree-account credentials, see which projects and tasks they have, read a task and its conversation, comment, or update a field. Invoke when the person says "my tasks", "what's pending on <project>", "comment on task N", "load / change my credentials", "my key changed", or pastes a Client ID / Secret Key. NOT for administering the board (creating accounts or projects is done by the board owner).
---

# htree-tasks

> A person invited to work with an organisation gets a **tree account** (Client ID + Secret Key) per
> board. This skill is how their forest reads and works those boards — without them ever touching a
> terminal command or an Odoo password. The instrument is **`htree.py`** (stdlib only) at the workspace
> root — the installer copies it there; if it is missing, copy `roots_seed/scripts/htree.py` (after
> `git -C roots_seed pull`). Run it from the workspace root: that is where it looks for `.htree.env`.

## Where the credentials live
`.htree.env` at the repo root — **never committed** (`htree.py credentials` adds it to `.gitignore`).
One **profile** per board: any prefix `P` with `P_BASE`, `P_CLIENT_ID`, `P_SECRET_KEY`.

## Steps
1. **Credentials first.** If the person pastes new keys or says they changed:
   `python3 htree.py credentials -p <NAME>` — it asks URL / Client ID / Secret Key
   (Enter keeps the current value), **authenticates against the real board before saving**, and saves
   nothing if it fails. If they pasted the values in the chat, feed them on stdin; **never echo the
   Secret Key back**, never write it in a task, a commit or a `.roots/` file.
2. **Know who signs.** `htree.py whoami` — every comment goes out with the account's user name. If it
   is not the person, stop and say so.
3. **Read.** `htree.py projects -p P` · `htree.py tasks -p P [--project <id|name>] [--mine] [--all]` ·
   `htree.py tasks -p P <ID>` (description + conversation). Summarise for the person; link the task.
4. **Write = their words, their OK.** `comment` and `set` are **DRY-RUN by default** (exit 2). Show the
   person exactly what will be published, and re-run with `--yes` only after an explicit yes. After a
   `set`, the tool re-reads the field: report the re-read value, not the request.

## Reading failures
- `Could not REACH the board` = network / URL. Credentials are not the problem: do not regenerate them.
- `The board REJECTED` + `unauthorized` = wrong or rotated keys → step 1.
- `You cannot read/write ... fields` or `restricted` = the account deliberately does not reach that
  (a portal user only sees the projects it collaborates on). It is a permission, not a bug: ask the
  board owner, do not look for a way around it.
- Creating new tasks may not be available to portal accounts; propose them as a comment on a task.

## Expected output
A short answer in the person's language: what they have pending (by project), what a task says, or
`✅ message N on #ID` / the re-read field. Never the keys.
