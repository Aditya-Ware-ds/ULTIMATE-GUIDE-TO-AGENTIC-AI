# Module 02 resources

Verified 2026-09-22. All links are to official documentation.

- [Claude Platform Docs: Messages API](https://platform.claude.com/docs/en/api/messages) -- the request/response shape `shared/llm/providers/anthropic_provider.py` targets.
- [Claude Platform Docs: Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) -- GA `output_config` shape referenced in lesson 03.
- [OpenAI Platform Docs: Function calling / Responses API](https://developers.openai.com/api/docs/guides/function-calling) -- the current tool-calling and structured-output request shape.
- [Google AI for Developers: Structured output (Interactions API)](https://ai.google.dev/gemini-api/docs/structured-output) -- the current `response_format` shape referenced in lesson 03.
- [JSON Schema -- official spec site](https://json-schema.org/) -- the schema format every provider's structured-output feature is built on.
- [`jsonschema` (Python) -- PyPI](https://pypi.org/project/jsonschema/) -- the validation library used in this module's lab and examples.
- [Anthropic: Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) -- official guidance behind lesson 04's techniques.
