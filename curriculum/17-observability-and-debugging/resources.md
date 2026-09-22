# Module 17 resources

Verified 2026-09-22.

- [OpenTelemetry: GenAI observability](https://opentelemetry.io/blog/2026/genai-observability/) -- the `gen_ai.*` semantic conventions and `invoke_agent`/`chat`/`execute_tool` span hierarchy `shared/tracing/tracer.py` implements, originally verified when that module was built in Phase 0.
- [OpenTelemetry Python SDK docs](https://opentelemetry.io/docs/languages/python/) -- the underlying `TracerProvider`/`SpanProcessor`/exporter concepts `shared/tracing/` is built directly on.
- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents) -- also referenced in Modules 04/08/12; its emphasis on visibility into an agent's intermediate steps (not just final output) is the same principle this module's tracing and replay lessons apply concretely.
