# Module 03 pitfalls

## `eval()` is not a shortcut, even for "just arithmetic"

It's tempting to implement `calculate()` as `return eval(expression)` -- it's one
line and handles all the arithmetic cases correctly. It's also a full Python
interpreter available to anything that can produce a string reaching this
function, including a model whose output was influenced by injected content in
a document it read (Module 18 covers this attack class directly).
`eval("__import__('os').system('rm -rf /')")` runs exactly what it looks like it
runs. There is no safe way to sandbox `eval()`/`exec()` well enough to expose them
to model-controlled strings without a real sandbox (`shared/sandbox/`, Module 13)
around the whole process -- for a lab-scoped calculator, the `ast`-based
restricted evaluator is the correct level of effort, not a compromise.

## Forgetting the assistant's tool-call message in history

If `run_tool_loop` appends only the `Message(role=Role.TOOL, tool_result=...)`
messages and skips appending `response.message` (the assistant's own message
containing the tool calls it made), the conversation history is missing a step.
Against the mock provider this can still "work" in the sense that tests pass
(the mock doesn't validate conversation coherence), which is exactly why this
bug can slip through a lab's tests and only surface against a real provider,
which does validate the message sequence and may reject or error on a
tool-result message with no matching preceding tool-call message.

## Confusing "the loop stopped" with "the loop succeeded"

`run_tool_loop`'s `max_steps` exit path and its "got a final text answer" exit
path both return a string -- if calling code doesn't distinguish them (e.g. by
checking whether the returned text is the specific max-steps message, or by
having `run_tool_loop` signal this some other way in a more complete system),
a caller can mistake "the agent gave up" for "the agent successfully answered."
This lab's tests check for this distinction directly
(`test_run_tool_loop_stops_at_max_steps`); carry the same care into Module 04,
where the agent loop is more general and this distinction matters even more.

## Weather/unit conversion off-by-formula errors

Celsius-to-Fahrenheit is `C * 9/5 + 32`, not `C * 9/5` or `(C + 32) * 9/5`. This
is a small thing, but it's a good example of a broader pattern: unit conversions
and similar "obvious" formulas are exactly the kind of tool logic that's easy to
get subtly wrong and easy to not notice, because the output still *looks* like a
plausible temperature. Test conversions against a known reference value (e.g.
0°C should be exactly 32°F), not just "does it return a number."
