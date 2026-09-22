# Module 07 pitfalls

## Mutating `messages` in place inside `run_one_step`

If `run_one_step` does `messages.append(...)` directly on the list it was
passed, instead of building and returning a new list (or being careful about
aliasing), a caller that keeps its own reference to the "before" list can be
surprised to find it mutated too -- both names point at the same list object.
The solution sidesteps this by rebinding `messages = [*messages, response.message]`
(a new list) before appending further, but appending further tool-result
messages after that still mutates the *new* list in place, which is fine since
nothing else holds a reference to it. Be deliberate about this distinction --
implicit aliasing bugs are subtle exactly because "it works" in simple test
cases where no one's holding a stale reference to compare against.

## Off-by-one in step counting across a resume

If `step` in a checkpoint means "steps completed" in one place but "the next
step to run" somewhere else in the same codebase, resuming can either skip a
step or repeat one. This module's solution is consistent: `step` always means
"steps completed so far," incremented immediately after each `run_one_step`
call and saved right after. If you design your own variant, pick one meaning
and audit every place `step` is read or written for consistency with it --
this is exactly the kind of bug that "looks right" on a fresh start (where
`step` begins at 0 either way) and only surfaces on a resume.

## Forgetting that `load_checkpoint` returning `None` and returning `(empty_list, 0)` mean different things

`load_checkpoint` returning `None` means "no checkpoint exists, start fresh."
A checkpoint that happens to contain an empty message list would be a real
(if unusual) saved state, not the same as "no checkpoint." Code that checks
`if not load_checkpoint(path):` instead of `if load_checkpoint(path) is None:`
would treat both cases identically -- probably harmless here since a
checkpoint's `messages` list is never actually empty in this lab's design, but
it's the kind of implicit truthiness check that becomes a real bug the moment
an assumption like that stops holding.

## Testing round-trip serialization with `==` on dataclasses

`Message == Message` works out of the box because dataclasses generate
`__eq__` automatically (Module 00, lesson 01) -- this is precisely why the
lab's round-trip tests can assert `restored == original` directly instead of
comparing field by field. If `Message` were a plain class without
`@dataclass`, this same test would need to compare every field manually
(or `id()` comparison would falsely pass only when it's the literal same
object) -- worth noticing how much this convenience is doing for you here.
