# Recipe — The forest of an invited collaborator

> Someone outside the organisation (an editor, a writer, a consultant, a partner) is invited to work on a
> few of its projects. They get a **tree account** on the organisation's board and keep **their own
> forest**. This recipe is how that forest behaves so the two sides can work in parallel without
> stepping on each other — the same discipline as the organisation's own sandbox, sized for one person.
> Tooling: `htree.py` + skill `htree-tasks` (v1.24).

## 1. The task is the channel
- Everything that concerns the organisation **lives on its board**, in the task it belongs to: questions,
  deliverables, decisions, links. A WhatsApp or a hallway agreement that is not on the task did not
  happen for the other side's sessions — they cannot see it.
- One task = one subject. A new subject is a **new task**, not a long thread on an old one.
- The collaborator's forest **reads before it writes**: every session starts by
  `htree.py tasks` on each board and reading what changed since last time.

## 2. Plan before acting (the seed's hard rule, unchanged)
Before each action — not once per session — the task goes to `.roots/tasks/` (or
`PLAN-<date>-<slug>.md` for a front with several steps): **what, why, on which project/task, and when it
is done**. Progress is marked as it happens. What is not written before it is done cannot be recovered.

## 3. Writing outward is dry-run + an explicit yes
`comment` / `set` are dry-run by default. The agent shows **exactly** what will be published, and sends
only after the person says yes. Comments are signed with the person's name: they are the person speaking.

## 4. Asking the organisation for something — the requests task
Invited (portal) accounts usually **cannot create tasks**. So the board has one task per collaborator
called **"Requests to <organisation>"**, and a request is a **comment there**, with this shape:

```
REQUEST: <one line>
For: <project / task #N>
Why: <what it unblocks>
I need it by: <date, or "no rush">
Done when: <what I will see>
```
The organisation answers in the same thread and, when it becomes work, opens a task and links it.
One request per comment — a list of five in one comment gets one answer.

## 5. Proposing a new project
Same channel, different header:
```
PROPOSAL: <name>
For whom: <who uses it / who pays>
What it uses from the platform: <data, tools, existing pieces>
First visible step: <the smallest thing that can be shown>
Open questions: <what must be decided first>
```
A proposal is not a promise to a third party: nothing is offered outside until the organisation says so.

## 6. Someone else's voice
If the work is editing a text whose author is another person, the forest **proposes, it does not
rewrite**: suggestions as comments or as a marked version, the author decides. Same for an
organisation's public positioning: drafts, never publishing.

## 7. Talking to third parties (clients, partners) on the organisation's behalf
- Only **counted** numbers, never projected ones: a figure that later goes down costs more credibility
  than not giving one. If a sentence needs `~` or "about", it goes out without the number.
- Personal data stays aggregated (by territory, by category) — never a list of people.
- Anything commercial (prices, dates of delivery, scope) is the organisation's call: bring it to the
  requests task first.

## 8. Session end
Before closing: `.roots/` up to date (what was done, what is pending, where), and a comment on each task
that moved. The next session — yours or theirs — starts from the board and `.roots/`, never from memory.

## 9. Secrets
`.htree.env` never enters git, never goes into a task, a chat or a `.roots/` file. If a key leaks,
ask the organisation to rotate it and reload with `htree.py credentials`.
