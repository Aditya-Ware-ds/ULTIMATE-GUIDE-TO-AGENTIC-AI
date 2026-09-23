# Progress files and resumability

**Last verified:** 2026-09-22
**Difficulty:** ★★★★★ · **Time:** ~45 minutes

## Learning objectives

- Extend Module 07's single-conversation checkpoint into a multi-task progress file.
- Design a progress file so a killed-and-restarted run resumes from the first incomplete task, never repeating finished work.
- Recognize this exact pattern in this repository's own `PROGRESS.md`.

## Intuition

Module 07's checkpoint resumes a single agent conversation mid-stream --
perfect for one bounded task interrupted mid-way. A long-horizon agent
working through many largely-independent sub-tasks needs a different
shape: not "where in this one conversation was I," but "which of these N
tasks are done, which is next." That's a **progress file**: a durable,
external record of task-level status, checked and updated after every
single task completes.

## The concept

### The data shape

```python
{
    "tasks": [
        {"name": "Research topic A", "status": "done", "result": "..."},
        {"name": "Draft section 1", "status": "done", "result": "..."},
        {"name": "Draft section 2", "status": "pending", "result": None},
        {"name": "Review and finalize", "status": "pending", "result": None},
    ]
}
```

This is structurally simple on purpose -- a list of tasks, each with a
status (`"pending"` or `"done"`) and its result once done. The simplicity
is the point: a progress file needs to be trivially loadable and
inspectable, including by a human, at any point mid-run.

### The resumable loop

```python
async def run_long_horizon_agent(client, progress_path: Path, task_names: list[str]) -> dict:
    tasks = load_progress(progress_path) or [
        {"name": name, "status": "pending", "result": None} for name in task_names
    ]
    for task in tasks:
        if task["status"] == "done":
            continue  # already completed in a previous run -- never redo it
        task["result"] = await run_task(client, task["name"])
        task["status"] = "done"
        save_progress(progress_path, tasks)  # persist immediately, not at the end
    return {"tasks": tasks}
```

The critical property: `save_progress` is called **after every single
task**, not once at the end. If the process is killed between task 2 and
task 3, tasks 1-2 are durably marked done; restarting calls
`run_long_horizon_agent` again, `load_progress` finds the existing file,
and the loop skips straight past the two completed tasks to task 3 --
exactly Module 07's kill-and-resume guarantee, now at the task-list level
instead of the single-conversation level.

### This is literally how this repository was built

Every module in this curriculum was built, verified, and committed one at
a time, with `PROGRESS.md` updated after each one -- a real, human-and-
agent-readable progress file with exactly this shape (a checklist of
modules, ✅/⬜ status, and an "Exact next step" section that's the human-
readable equivalent of `task["result"]` for whatever comes next). If this
multi-session build had been interrupted at any point, a fresh session
could resume correctly by reading `PROGRESS.md` alone -- which is precisely
the property this lesson's `run_long_horizon_agent` implements in code.
This isn't a coincidental analogy; it's the same underlying pattern, used
twice.

## Deeper: the progress file's granularity is a real design decision

Too coarse (one giant "build the whole thing" task) gives you none of this
lesson's benefit -- a crash anywhere still means starting over. Too fine
(tracking every tiny sub-step) adds overhead disproportionate to the risk
being managed. `PROGRESS.md`'s own granularity -- one entry per curriculum
module, each representing hours of real work -- was chosen because a
module is a natural, coherent unit: fully done or not started, with a
clear boundary for "resume from here."

## When not to use this

Don't build multi-task progress-file infrastructure for a task that's
genuinely one atomic unit of work with no natural sub-task boundaries --
Module 07's single-conversation checkpoint is the right granularity there;
this lesson's pattern needs real, independently-completable sub-tasks to
apply to.

## Common mistakes

- Persisting progress only at the very end of a run "for simplicity" --
  this defeats the entire purpose; the save must happen after each
  individual task, not once at the end.
- Choosing task granularity so coarse that a crash anywhere still loses
  most of the work, or so fine that the overhead of tracking every micro-step
  outweighs what it protects against.
- Re-running a task marked `"done"` "just to be safe" on resume -- if the
  status is trustworthy (verified, per lesson 01, not just claimed), a done
  task should never be redone; that's the entire efficiency gain resumability provides.

## Key takeaways

- A progress file tracks task-level status (pending/done + result) durably outside the live conversation, extending Module 07's single-conversation checkpoint to multi-task plans.
- Persist after every task, not just at the end -- that's what makes a mid-run crash cost only the in-flight task, not everything.
- This repository's own `PROGRESS.md` is a real, working instance of exactly this pattern, not a hypothetical example.

## Lab

[`labs/01-progress-file-agent/`](../labs/01-progress-file-agent/README.md)
