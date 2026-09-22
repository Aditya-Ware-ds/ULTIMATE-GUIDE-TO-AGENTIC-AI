# How to use this repo

Pick the track that matches where you're starting from. All tracks go through the
same modules in the same order (see [ROADMAP.md](ROADMAP.md)) -- they differ in how
much of each module you do.

## Full track (recommended if you're new to AI/agents)

Do everything: read every lesson, run every example, complete every lab (write the
code yourself in `starter/` before looking at `solution/`), take every quiz, read
`pitfalls.md` even for labs that passed on your first try. Budget 5-8 hours/week;
expect 6-9 months end to end including capstones.

## Fast track (you know ML/AI already, agents are new)

Skim Level 0 (you likely know tokens, embeddings, and the messages API already --
but still skim `01-how-llms-work` and `02-talking-to-llms` for the parts specific to
*agentic* use: reasoning models, structured outputs, streaming). Do every lab from
Level 1 onward in full -- this is where the actual agent-specific skills live.
Budget 4-6 months.

## "I already code, just want agents" track

If you're an experienced software engineer new to LLMs entirely: don't skip Level 0
-- module 01 (how LLMs work) and 02 (talking to LLMs) cover things that don't map to
prior programming intuition (temperature, context windows, hallucination as a
structural property, not a bug). From Level 1 on, move quickly through explanations
and focus on the labs; you'll likely finish 30-40% faster than the full track.

## However you go through it

- **Don't skip labs by reading the solution first.** The starter's gaps are placed
  specifically so that filling them teaches the module's core idea. Reading the
  solution first turns a lab into a reading exercise.
- **Run the tests yourself**, even when a lab's README shows expected output. `cd`
  into the lab's `tests/` setup and run `uv run pytest <path>` against your own
  `starter/` code.
- **Do the quiz before checking answers.** It's in `quiz.md` with answers behind a
  collapsible `<details>` block specifically so you're not tempted to peek early.
- **Read `pitfalls.md` even when you passed.** It documents mistakes that pass tests
  but cause production incidents (e.g. a context-window bug that only shows up past
  a certain conversation length) -- test-passing and correct aren't the same thing.
- **Use projects as checkpoints.** If a project after a level feels too hard, that's
  signal to revisit that level's labs rather than push through.

## If you get stuck

1. Re-read the lesson's "common mistakes" section.
2. Check `pitfalls.md` for the lab.
3. Compare your `starter/` code against `solution/` for the *specific* function
   you're stuck on, not the whole file.
4. Check `GLOSSARY.md` if a term is unclear.

## Contributing back

If you find a stale framework claim, a broken link, or an outdated API shape (this
field moves monthly), open an issue or PR with a current source. See the
Contributing section in [README.md](README.md).
