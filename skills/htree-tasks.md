---
name: htree-tasks
description: Work the person's tasks on one or more htree task boards (Odoo backends exposing the OCAPI htree gateway) — load or edit their tree-account credentials, see which projects and tasks they have, read a task and its conversation, comment, attach files, update a field, vote on their Florum topics, or list / create the pieces of their own Studio. Invoke when the person says "my tasks", "what's pending on <project>", "comment on task N", "load / change my credentials", "my key changed", "vote for X", "what can I vote on", "my pieces", "create a piece", or pastes a Client ID / Secret Key. NOT for administering the board (creating accounts or projects is done by the board owner).
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
3b. **Create.** `htree.py new -p P --project <id|name> "title" [--desc …|-f file]` — dry-run first, then
   `--yes`. One task = one subject, with a title that says what it is (not "question" / "pending").
   If the board answers that the account cannot create tasks, propose it in the requests task instead.
3c. **Attach.** `htree.py attachments -p P <ID>` lists the files of a task; `htree.py attach -p P <ID> file… [-m text]`
   uploads each file **as a comment carrying it** (a portal account cannot attach to the record itself) and
   re-reads the list to verify. There is **no delete**: check the task id before `--yes`. Anyone who follows the
   task can download the file. **A secret (key, token, password) goes ONLY as a file, never in comment text**,
   and only scoped/read-only/rotatable credentials — ask the board owner to rotate them when the work ends.
3d. **Vote (Florum).** `htree.py florum -p P [--forum N]` lists the topics the person can vote on (votes, ✓ =
   theirs); `htree.py vote -p P <ID>` shows what would happen and `--yes` adds or removes the vote, printing the
   board's new count. A vote is the person's voice: cast it only when they asked for that topic, never in bulk.
3e. **Studio pieces.** A Studio has its **own** credential (created by the person on the Studio's Credentials
   page, with the permissions they tick) ⇒ load it as a **separate profile** (`credentials -p <STUDIO_NAME>`); the
   task-board profile stays as it is. `htree.py pieces -p <STUDIO_NAME>` lists their pieces (id, title, state,
   channel); `htree.py piece new -p <STUDIO_NAME> "title" [--year Y] [--technique T] [--desc …|-f file]` is dry-run,
   then `--yes` creates it as a **draft in their channel** and re-reads it. Publishing is the person's step, in the
   Studio. `permission_denied` = the credential lacks that box: they tick it on the Credentials page.
4. **Write = their words, their OK.** `new`, `comment`, `attach`, `set`, `vote` and `piece new` are **DRY-RUN by default** (exit 2). Show the
   person exactly what will be published, and re-run with `--yes` only after an explicit yes. After a
   `set`, the tool re-reads the field: report the re-read value, not the request.

## Reading failures
- `Could not REACH the board` = network / URL. Credentials are not the problem: do not regenerate them.
- `The board REJECTED` + `unauthorized` = wrong or rotated keys → step 1.
- `You cannot read/write ... fields` or `restricted` = the account deliberately does not reach that
  (a portal user only sees the projects it collaborates on). It is a permission, not a bug: ask the
  board owner, do not look for a way around it.

## Expected output
A short answer in the person's language: what they have pending (by project), what a task says, or
`✅ message N on #ID` / the re-read field. Never the keys.
