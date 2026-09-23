# Module 19 quiz

**1. Why is `TestClient` preferable to actually starting `uvicorn` and making real HTTP requests in a test suite?**

<details><summary>Answer</summary>

`TestClient` exercises the same routing and handler logic in-process, with
no real socket, port, or network involved -- faster, more reliable, and
not flaky the way a real running server in a test suite would be, the same
"test the real thing without the real infrastructure" principle as Module
00/10's fixtures.

</details>

**2. How does a "durable job" relate to Module 07's checkpoint/resume pattern?**

<details><summary>Answer</summary>

A durable job is the same checkpoint/resume idea, triggered by
infrastructure events (a worker restart, a deploy, a timeout) instead of a
simulated crash in a test -- the checkpoint format doesn't need to change,
only who/when triggers a resume.

</details>

**3. Why does FastAPI's dependency-injection system matter for testing an agent service?**

<details><summary>Answer</summary>

It lets tests override `get_llm_client` with a function returning a
scripted mock client (`app.dependency_overrides[...]`), so the whole HTTP
service is testable with zero API keys -- the same "swap the real provider
for a scriptable fake" principle `shared/llm/mock.py` provides for plain
function tests, applied at the service layer.

</details>

**4. Why is a naive retry dangerous for an agent that can call consequential tools (Module 18's `send_email`, for instance)?**

<details><summary>Answer</summary>

If the first request actually succeeded and only the response was lost in
transit, a naive retry re-runs the underlying work -- including any
consequential tool calls -- a second time, causing a real duplicate action
(a second email sent, a second refund issued) the user never asked for.

</details>

**5. What must an idempotency key be generated from, and why does a timestamp not work as one?**

<details><summary>Answer</summary>

It must be a value the client generates once per *logical* request and
reuses on every retry of that same request. A timestamp changes on every
attempt, so using one as the "key" would treat every retry as a brand-new
request -- defeating the entire mechanism.

</details>

**6. Why can't idempotency keys be stored forever?**

<details><summary>Answer</summary>

Unbounded storage growth in a long-running production service -- real
systems define an expiry window (commonly around 24 hours) after which the
same key is treated as a new request. Too short risks treating a legitimate
late retry as new work; too long wastes storage on keys that will never be
reused again.

</details>

**7. How does a rate limit relate to Module 04's `max_steps` step budget?**

<details><summary>Answer</summary>

Both convert an unbounded resource into a bounded, known one -- `max_steps`
bounds how long a single agent run can go, a rate limit bounds how many
requests a client can make in a given window. Both exist to convert
"unbounded damage" (from a bug, a misbehaving client, or deliberate abuse)
into "bounded, known damage."

</details>

**8. Why does prompt caching benefit a stable system prompt and tool definitions much more than the actual user message?**

<details><summary>Answer</summary>

Caching rewards content that's identical across many requests -- a system
prompt or tool set that rarely changes gets cached and reused cheaply. The
user's actual message changes on every request, so it gets no benefit from
caching and shouldn't be placed inside a cached block.

</details>

**9. Why should a model-routing rule be validated with Module 16's eval harness before trusting it in production?**

<details><summary>Answer</summary>

Routing purely by task category without checking the cheaper model's
actual success rate on that category risks silently degrading quality --
an eval harness gives concrete evidence of whether the cheaper model
performs acceptably on the routed traffic, rather than relying on intuition
about which tasks are "easy enough" for it.

</details>

**10. A team optimizes to reduce cost per request by switching to a cheaper model, but doesn't track cost per successful outcome. What could this hide?**

<details><summary>Answer</summary>

A cheaper model that fails more often, requiring more retries or
escalations to a stronger model, can end up costing more overall once those
follow-up costs are counted -- cost per request looks better while the
actual cost of getting a correct result gets worse.

</details>
