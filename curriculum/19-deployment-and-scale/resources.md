# Module 19 resources

Verified 2026-09-22.

- [FastAPI -- official docs](https://fastapi.tiangolo.com/) -- confirmed current/actively maintained; source for `TestClient` (imported from `fastapi.testclient`) and `StreamingResponse` usage in this module's lab.
- [Anthropic: Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) -- current `cache_control` mechanics, TTL options, and cache-hit cost reductions (up to ~97.5% for some models) cited in lesson 03.
- [Stripe: Idempotent requests](https://docs.stripe.com/api/idempotent_requests) -- a widely-referenced, real-world production implementation of the idempotency-key pattern this module's lesson 02 and lab implement a minimal version of (confirms the ~24-hour key-expiry window cited in that lesson).
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) -- also referenced in Modules 04/08/12/17; its cost/latency framing underlies this module's model-routing material.
