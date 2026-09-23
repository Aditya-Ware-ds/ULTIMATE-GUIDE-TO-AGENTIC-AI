import json

from shared.tracing import get_exported_spans


def test_extract_citations_finds_bracketed_numbers_in_order(research_pipeline):
    article = "Revenue grew 12% [1]. Costs fell [2]. Overall strong [1]."

    assert research_pipeline.extract_citations(article) == [1, 2, 1]


def test_extract_citations_returns_empty_list_when_none_present(research_pipeline):
    assert research_pipeline.extract_citations("No citations here.") == []


def test_verify_citations_all_valid(research_pipeline):
    article = "Fact one [1]. Fact two [2]."
    facts = ["First fact.", "Second fact."]

    result = research_pipeline.verify_citations(article, facts)

    assert result == {"total_citations": 2, "valid_citations": 2, "citation_accuracy": 1.0}


def test_verify_citations_some_invalid(research_pipeline):
    article = "Fact one [1]. A hallucinated fact [5]."
    facts = ["First fact.", "Second fact."]

    result = research_pipeline.verify_citations(article, facts)

    assert result == {"total_citations": 2, "valid_citations": 1, "citation_accuracy": 0.5}


def test_verify_citations_no_citations_at_all(research_pipeline):
    result = research_pipeline.verify_citations("No citations here.", ["A fact."])

    assert result == {"total_citations": 0, "valid_citations": 0, "citation_accuracy": 0.0}


async def test_run_traced_pipeline_success_produces_nested_spans(research_pipeline, client):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["Fact A", "Fact B"]}))
    client.provider.add_text("Fact A matters [1]. Fact B too [2].")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "Good."}))

    result = await research_pipeline.run_traced_pipeline(client, "a topic")

    assert result["status"] == "success"
    assert result["revisions"] == 0
    assert result["citation_accuracy"] == 1.0

    spans = get_exported_spans()
    names = [s.name for s in spans]
    assert "invoke_agent research-pipeline" in names
    assert "invoke_agent researcher" in names
    assert "invoke_agent writer" in names
    assert "invoke_agent critic" in names
    assert names.count("chat mock-model") == 3  # research + draft + critique


async def test_run_traced_pipeline_worker_spans_nest_under_the_pipeline_span(
    research_pipeline, client
):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["Fact A"]}))
    client.provider.add_text("Fact A matters [1].")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "Good."}))

    await research_pipeline.run_traced_pipeline(client, "a topic")

    spans = get_exported_spans()
    spans_by_id = {s.context.span_id: s for s in spans}
    pipeline_span = next(s for s in spans if s.name == "invoke_agent research-pipeline")
    researcher_span = next(s for s in spans if s.name == "invoke_agent researcher")

    assert researcher_span.parent is not None
    assert researcher_span.parent.span_id == pipeline_span.context.span_id
    assert spans_by_id[researcher_span.parent.span_id] is pipeline_span


async def test_run_traced_pipeline_escalates_immediately_on_research_failure(
    research_pipeline, client
):
    client.provider.add_text(json.dumps({"status": "error", "reason": "no sources"}))

    result = await research_pipeline.run_traced_pipeline(client, "an obscure topic")

    assert result == {"status": "escalated", "reason": "no sources"}
    assert client.provider.call_count == 1


async def test_run_traced_pipeline_revises_once_then_succeeds(research_pipeline, client):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["Fact A"]}))
    client.provider.add_text("Draft v1, no citation.")
    client.provider.add_text(json.dumps({"approved": False, "feedback": "Add a citation."}))
    client.provider.add_text("Draft v2 with a citation [1].")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "Better."}))

    result = await research_pipeline.run_traced_pipeline(client, "a topic")

    assert result["status"] == "success"
    assert result["revisions"] == 1
    assert result["article"] == "Draft v2 with a citation [1]."

    spans = get_exported_spans()
    writer_spans = [s for s in spans if s.name == "invoke_agent writer"]
    assert len(writer_spans) == 2  # one per draft attempt
