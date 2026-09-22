# HTTP and REST

**Difficulty:** ★☆☆☆☆ · **Time:** ~45-60 minutes

## Learning objectives

- Explain what happens on the wire when you call an LLM API.
- Read an API's docs and know what method, headers, and body to send.
- Make HTTP requests in Python with `httpx`, including async requests.

## Intuition

Every LLM API call in this repo -- and in production agents everywhere -- is an
HTTP request: your code sends a request over the network to a server, the server
runs the model, and sends a response back. Understanding HTTP means you can debug
"why did my API call fail?" from first principles (wrong method? bad auth header?
malformed body? rate limited?) instead of guessing.

## The concept

### Anatomy of a request

```
POST /v1/messages HTTP/1.1
Host: api.anthropic.com
x-api-key: sk-ant-...
content-type: application/json

{"model": "claude-haiku-4-5", "max_tokens": 100, "messages": [...]}
```

- **Method** (`POST`, `GET`, `PUT`, `DELETE`, ...) says what kind of operation.
  LLM completions are almost always `POST` because you're sending data (the
  messages) that doesn't fit in a URL.
- **Headers** carry metadata: auth (`x-api-key` or `Authorization: Bearer ...`),
  content type, and provider-specific extras.
- **Body** carries the actual payload, JSON for essentially every LLM API.

### Anatomy of a response

```
HTTP/1.1 200 OK
content-type: application/json

{"id": "msg_...", "content": [{"type": "text", "text": "Hi there!"}], ...}
```

The **status code** tells you what happened before you even look at the body:

| Range | Meaning | Example |
|---|---|---|
| 2xx | Success | 200 OK |
| 4xx | Your request was wrong | 401 Unauthorized (bad key), 429 Too Many Requests (rate limited) |
| 5xx | The server failed | 500 Internal Server Error, 503 Service Unavailable |

### REST, briefly

REST is a set of conventions for designing HTTP APIs around **resources**:
`GET /users/42` reads user 42, `POST /users` creates a user, `DELETE /users/42`
deletes it. LLM APIs aren't fully RESTful (a "completion" isn't really a stored
resource you `GET` back), but they borrow REST's conventions: JSON bodies,
standard status codes, versioned URL paths (`/v1/...`).

### Making requests with `httpx`

```python
import httpx

# Synchronous
response = httpx.get("https://api.example.com/status")
response.raise_for_status()  # raises httpx.HTTPStatusError on 4xx/5xx
data = response.json()


# Asynchronous (what shared/llm/ uses throughout)
async def fetch(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

`httpx` is this repo's HTTP library (it's what every provider SDK uses under the
hood, and what you'll use directly in this module's lab).

## Deeper: streaming responses

LLM APIs often stream responses token-by-token instead of waiting for the whole
completion (Module 02 covers this in depth). Under the hood, that's HTTP
chunked-transfer-encoding or Server-Sent Events -- the connection stays open and
the server pushes chunks as they're ready, instead of one request/response
round-trip.

## When not to use this

Don't reach for raw HTTP calls when a well-maintained SDK exists for the service
you're calling (e.g. use `anthropic`'s SDK, not raw `httpx` POSTs to
`api.anthropic.com`) -- SDKs handle auth, retries, and response parsing correctly
and get updated when the API changes. This lesson is about understanding what the
SDK does for you, not replacing it in production code.

## Common mistakes

- Not checking the status code before using the response body -- a 429 or 500
  response still has a JSON body, just one describing the error, not your data.
  Always call `.raise_for_status()` or check `.status_code` explicitly.
- Forgetting `await` on an async call, which in Python doesn't error loudly --
  you get a coroutine object back instead of a result, and bugs downstream that
  are confusing to trace to the real cause.
- Hardcoding timeouts of "however long it takes" (no timeout) -- a hung network
  call with no timeout can block an agent forever. `shared/sandbox/`'s subprocess
  calls all set explicit timeouts for the same reason.

## Key takeaways

- Every LLM API call is HTTP: method + headers + body out, status code + body back.
- Status codes tell you the category of outcome before you parse anything.
- `httpx` (sync and async) is this repo's HTTP client; SDKs wrap it for real provider calls.

## Lab

[`labs/01-async-fetch-cli/`](../labs/01-async-fetch-cli/README.md)
