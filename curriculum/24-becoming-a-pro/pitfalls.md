# Module 24 pitfalls

## Leading a portfolio writeup with a technology list

"Built with LangGraph, DSPy, and FastAPI" tells a reader what you touched,
not what you decided or why. Lead with the specific problem and trade-off
instead (lesson 01) -- the technology list, if included at all, belongs at
the end as supporting detail, not the headline.

## Treating every module lab as an equally important portfolio item

This curriculum has dozens of labs; showcasing all of them dilutes
attention away from the pieces actually built at portfolio scale (the five
projects and three capstones). Pick a small number of your strongest,
most-defensible pieces and go deep on those rather than listing everything
you built.

## Contributing a large feature as a first interaction with a project

Even a genuinely good large-feature idea is a hard first ask -- it
requires a maintainer to evaluate your design judgment with zero prior
track record. Start with something small and precise (lesson 02); earn
trust before asking for it on something bigger.

## Reporting a bug or gap without re-verifying it against the project's current version

The exact mistake this curriculum's own ground rules exist to prevent:
trusting an old assumption instead of checking current, real behavior.
A bug report against an already-fixed issue costs a maintainer real time
to discover it's stale -- always re-check before submitting, using the
same install-and-inspect discipline used throughout Modules 10, 11, 14,
and 20.

## Answering a system-design question by reciting technique names without reasoning

Naming "I'd use RAG, multi-agent, and human-in-the-loop" without
explaining *why each one fits this specific question's constraints* sounds
like recited terminology, not real judgment. The [`system-design/`](../../system-design/README.md)
case studies model the alternative: explicit constraint clarification
first, then a topology/architecture choice justified by those specific
constraints, not a default toolkit applied uniformly to every question.
