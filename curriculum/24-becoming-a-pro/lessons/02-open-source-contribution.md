# Open-source contribution

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~25 minutes

## Learning objectives

- Find a genuine, appropriately-scoped first contribution to an agent framework or tool.
- Use the exact verification skills this curriculum built (Module 10/11's install-and-inspect discipline) to find real gaps worth contributing to.
- Explain why a small, well-scoped documentation or bug fix is a better first contribution than a large new feature.

## Intuition

Module 11 built real, tested implementations against all 9 major agent
frameworks -- in the process of doing that (see each framework's lab and
this curriculum's own pitfalls.md entries), several real friction points,
unclear docs, and version-mismatch gotchas were discovered along the way.
That same process -- install a real tool, use it for a real task, notice
where it was harder or less clear than it should have been -- is exactly
how genuine open-source contributions get found, not by browsing an
issue tracker for something that sounds impressive.

## The concept

### Where a first contribution actually comes from

- **A gap you hit yourself, using the tool for a real task.** This
  curriculum's own Module 11 pitfalls.md and Module 20 pitfalls.md both
  document real friction discovered this way (a stale-looking API,
  undocumented adapter fallback behavior) -- exactly the kind of thing
  worth turning into a documentation PR or a minimal bug report once
  confirmed.
- **A specific, reproducible bug**, not a vague "this doesn't work." Module
  10's and Module 11's habit of installing a package and using
  `inspect.getsource()`/`dir()` to find ground truth is exactly the skill
  needed to file a bug report precise enough that a maintainer can act on
  it without first having to reproduce your entire environment.
- **A documentation fix**, which is almost always underrated as a starting
  point -- if a docs page describes stale behavior (the same kind of thing
  Module 14 and Module 18 caught in this curriculum's own research), a
  precise, small, verified correction is a genuinely useful, low-risk first
  contribution.

### Why small and well-scoped beats large and ambitious for a first contribution

A large new feature requires a maintainer to trust your judgment about
design decisions before they've seen any of your work. A small, precise,
already-verified fix (a docs correction, a minimal reproduction of a real
bug, a small test addition) requires much less trust to review and merge,
and builds the track record that makes a larger contribution possible
later.

### Applying this curriculum's own verification discipline

Before submitting anything, verify the gap still exists against the
project's *current* version (the maintainers may have already fixed it) --
the identical "install for real, check current behavior" discipline this
curriculum applied to every framework in Module 11 and every fast-moving
API throughout. Reporting an already-fixed bug wastes a maintainer's time
reviewing something that isn't actually a problem anymore.

## Deeper: this curriculum's own build process modeled the habit already

Every module that verified a framework or API by installing it and reading
its actual source (Module 10 onward) was practicing the exact skill open-
source contribution requires: don't guess, check the real, current thing.
The habit doesn't need to be relearned for contribution specifically -- it's
the same one, applied to a slightly different goal (fixing a gap for
others, not just for your own lesson content).

## When not to use this

Don't force a contribution to a project you don't actually use for real
work -- the "genuine gap discovered through real use" source of good first
contributions doesn't exist for a tool you're only touching to have
something to contribute to.

## Common mistakes

- Opening a large feature PR as a first contribution before establishing
  any track record with the maintainers.
- Reporting a bug without first verifying it against the project's current
  version, wasting review time on an already-fixed issue.
- Treating documentation contributions as lesser than code contributions,
  when a precise docs fix is often exactly as valuable and considerably
  easier to review and merge.

## Key takeaways

- Real first contributions come from gaps hit while genuinely using a tool, not from browsing for something impressive-sounding to fix.
- Small, precise, well-scoped fixes (docs, a minimal bug reproduction) are better first contributions than large new features -- they require less trust to review.
- Verify a gap still exists against the project's current version before submitting, using the same install-and-inspect discipline this curriculum used throughout.
