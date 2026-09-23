# Agentic AI Mastery

A complete, open-source curriculum that takes you from zero programming-adjacent AI
knowledge to designing, building, evaluating, securing, and shipping production-grade
AI agents. Every module teaches concepts, ships working code, makes you build
something, and checks your understanding.

This is a teaching product, not a link dump. You will write an agent loop, tool
calling, memory, and multi-agent orchestration **by hand** before you touch a single
framework -- so when frameworks show up in [Module 11](curriculum/11-frameworks), you
understand exactly what they're abstracting away.

## Who this is for

Anyone with basic computer literacy and no AI background who wants to reach a level
where they can design agent systems, read current agent research, and pass senior
agent system-design interviews. If you already code, see [HOW_TO_USE.md](HOW_TO_USE.md)
for a faster track.

## What you'll be able to do when you finish

- Build an agent loop, tool calling, memory, and retrieval from first principles, no framework
- Build the same reference agent in every major current agent framework, and know when to reach for which one
- Wire up MCP servers/clients, Agent Skills, and agent-to-agent protocols
- Design multi-agent systems and know when multi-agent is the wrong answer
- Evaluate agents rigorously (golden datasets, LLM-as-judge, trajectory evals) instead of vibes-checking them
- Trace, debug, and cost-optimize an agent in production
- Red-team your own agent against prompt injection and excessive-agency failures, then fix it
- Ship a durable, streaming, rate-limited agent API
- Read a current agent paper and reproduce its core result

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full level-by-level path, time estimates, and
prerequisite graph. Short version:

```
Level 0  Foundations              -> how LLMs and their APIs actually work
Level 1  First agent, no frameworks -> tool use, the agent loop, context, RAG
Level 2  Capable agents           -> memory, planning patterns, human-in-the-loop
Level 3  The ecosystem            -> MCP/A2A/Skills, all 9 major frameworks, multi-agent
Level 4  Specialized agents       -> coding agents, browser/computer use, voice & vision
Level 5  Production engineering   -> evals, observability, security, deployment
Level 6  Expert / frontier        -> DSPy optimization, RLVR, long-horizon agents, research literacy
```

Plus `projects/` (portfolio-sized builds between levels) and `capstones/` (three
large end-to-end builds with specs, threat models, and eval suites).

## Getting started

1. Read [SETUP.md](SETUP.md) for your OS.
2. Read [HOW_TO_USE.md](HOW_TO_USE.md) to pick a study track.
3. Start at `curriculum/00-programming-prerequisites/`.

```bash
git clone <this-repo>
cd agentic-ai-mastery
make setup   # installs deps with uv, no API keys required
make test    # runs the whole offline test suite against a mock LLM provider
```

You do **not** need any API keys to work through the curriculum. Every lab's tests
run against a scripted mock LLM provider (`shared/llm/mock.py`). Real-provider calls
are opt-in, cost-estimated, and live behind `make test-live` -- see `.env.example`.

## Repository layout

| Path | What's there |
|---|---|
| `shared/` | The provider-agnostic LLM client, mock provider, tracing, and sandbox used by every lab |
| `curriculum/NN-module-name/` | Lessons, examples, labs, quiz, pitfalls, and resources for each module |
| `projects/` | Mid-size portfolio projects between levels |
| `capstones/` | Three large end-to-end builds |
| `cheatsheets/` | One-page references |
| `papers/` | Annotated, verified reading list |
| `system-design/` | Agent system-design case studies and interview prep |
| `docs/` | MkDocs Material config for the docs-site view of this repo |

## Status

This repo is built incrementally, module by module, with tests passing at every
step. See [PROGRESS.md](PROGRESS.md) for exactly what's built, what's in progress,
and what's next.

## Contributing

Issues and PRs welcome. If you add or change claim about framework, protocol,
model, or benchmark, verify it against current official docs and date it -- this
field moves monthly and stale claims are worse than no claims.

## License

MIT -- see [LICENSE](LICENSE).
