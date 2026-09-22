# Git, virtual environments, and the terminal

**Difficulty:** ★☆☆☆☆ · **Time:** ~1 hour

## Learning objectives

- Use git for the day-to-day loop this repo's own workflow follows: status, add, commit, diff, branch, log.
- Explain what a virtual environment is and why `uv` manages one for you automatically.
- Be comfortable enough in a terminal to run this repo's `Makefile` targets and navigate directories.

## Intuition

Git is a save-point system for code: every commit is a snapshot you can return to,
compare against, or branch off from. A virtual environment is an isolated set of
installed Python packages *per project*, so this repo's dependencies (a specific
`anthropic` SDK version, say) don't collide with some other project's different
version of the same package on your machine.

## The concept

### Git, the commands you'll actually use

```bash
git status              # what's changed since the last commit?
git diff                # show the actual changes, line by line
git add <file>           # stage a file's changes for the next commit
git commit -m "message"  # snapshot the staged changes
git log --oneline        # history of commits
git branch <name>         # create a new branch
git checkout <name>       # switch to a branch
```

A **commit** is a snapshot plus a message explaining why. A **branch** is a
named pointer to a line of commits -- it lets you work on something (a new
module, say) without touching `main` until you're ready. This repo's own build
workflow commits after every module, with a message describing what that module
added -- the same discipline you should use in your own projects.

### Virtual environments, and why `uv` hides them from you

Without a virtual environment, `pip install anthropic` installs into your
system's global Python, shared by every project on your machine -- version
conflicts between projects become inevitable. A **virtual environment** is a
self-contained copy of Python plus its own package directory, isolated per
project.

`uv` (this repo's package manager) creates and manages a `.venv/` directory for
you automatically the first time you run `uv sync` or `uv run` -- you never run
`python -m venv` or `source .venv/bin/activate` by hand for this repo. `uv run
pytest` runs `pytest` using this repo's isolated environment without you needing
to "activate" anything first.

### Terminal basics you'll use constantly

```bash
cd path/to/dir     # change directory
ls                 # list files (dir on old Windows cmd, but WSL/PowerShell also support ls)
pwd                # print current directory
cat file.txt       # print a file's contents
mkdir new-dir      # create a directory
```

Every `make` target in this repo (`make setup`, `make test`, `make lint`) is just
a named shortcut for a longer `uv run ...` command -- read `Makefile` at the repo
root to see exactly what each one runs.

## Deeper: why this matters for agent development specifically

Later modules have you build coding agents (Module 13) that run git commands and
manage their own file changes. Understanding git yourself is a prerequisite for
understanding whether an *agent's* git usage is safe (Module 18 covers destructive
actions an agent could take, git among them) or correct.

## When not to use this

Don't commit generated files (`.venv/`, `site/`, `__pycache__/`, `.env` with real
secrets) -- this repo's `.gitignore` already excludes these. Don't use `git add .`
reflexively without checking `git status` first; it's easy to accidentally stage a
secret or a large generated file that way.

## Common mistakes

- Committing a `.env` file with real API keys. `.env.example` (no real values) is
  meant to be committed; `.env` (your real keys) is gitignored -- double check
  before pushing if you ever rename or copy it.
- Force-pushing or `git reset --hard` without checking `git status` first --
  these discard uncommitted work permanently. When in doubt, commit or stash
  first.
- Running commands from the wrong directory. If `uv sync` or `make test` fails
  with a confusing error, `pwd` first -- you may not be in the repo root.

## Key takeaways

- Git commits are snapshots; branches let you isolate in-progress work.
- `uv` manages an isolated virtual environment per project automatically -- you shouldn't need to think about activation.
- `Makefile` targets are named shortcuts; read it to see what actually runs.

## Lab

[`labs/01-async-fetch-cli/`](../labs/01-async-fetch-cli/README.md)
