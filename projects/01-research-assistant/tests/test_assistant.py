from shared.llm.types import ToolCall


def test_load_documents_finds_all_five_files(documents):
    assert set(documents.keys()) == {
        "mercury-program.txt",
        "apollo-program.txt",
        "space-shuttle.txt",
        "iss.txt",
        "commercial-crew.txt",
    }


def test_hybrid_search_returns_source_and_chunk(assistant, index):
    results = assistant.hybrid_search("Apollo 11 Moon landing", index, top_k=2)

    assert len(results) <= 2
    for source, chunk in results:
        assert isinstance(source, str)
        assert isinstance(chunk, str)
    assert any(source == "apollo-program.txt" for source, _ in results)


def test_dispatch_labels_results_with_source(assistant, index):
    call = ToolCall(id="1", name="search_documents", arguments={"query": "Apollo 11"})

    result = assistant.dispatch(call, index)

    assert not result.is_error
    assert "[apollo-program.txt]" in result.content


def test_dispatch_never_raises_on_unknown_tool(assistant, index):
    call = ToolCall(id="2", name="not_a_tool", arguments={})

    result = assistant.dispatch(call, index)

    assert result.is_error


def test_extract_citations_finds_bracketed_sources(assistant):
    answer = "Apollo 11 landed in 1969 [apollo-program.txt], the ISS launched in 1998 [iss.txt]."

    citations = assistant.extract_citations(answer)

    assert citations == ["apollo-program.txt", "iss.txt"]


def test_extract_citations_empty_when_none_present(assistant):
    assert assistant.extract_citations("No citations here.") == []


def test_verify_citations_all_valid(assistant):
    answer = "Apollo 11 landed in 1969 [apollo-program.txt]."
    valid_sources = {"apollo-program.txt", "iss.txt"}

    assert assistant.verify_citations(answer, valid_sources) == []


def test_verify_citations_flags_fabricated_source(assistant):
    answer = "The Gemini program did X [gemini-program.txt]."
    valid_sources = {"apollo-program.txt", "iss.txt"}

    unverified = assistant.verify_citations(answer, valid_sources)

    assert unverified == ["gemini-program.txt"]


async def test_run_research_assistant_single_search_valid_citation(
    assistant, client, index, valid_sources
):
    client.provider.add_tool_call("search_documents", {"query": "Apollo 11"})
    client.provider.add_text("Apollo 11 landed on the Moon in 1969 [apollo-program.txt].")

    result = await assistant.run_research_assistant(
        client, index, valid_sources, "When did Apollo 11 land?"
    )

    assert result.citations == ["apollo-program.txt"]
    assert result.unverified_citations == []


async def test_run_research_assistant_flags_fabricated_citation(
    assistant, client, index, valid_sources
):
    client.provider.add_tool_call("search_documents", {"query": "Gemini program"})
    client.provider.add_text("The Gemini program ran from 1961-1966 [gemini-program.txt].")

    result = await assistant.run_research_assistant(
        client, index, valid_sources, "Tell me about Gemini."
    )

    assert result.unverified_citations == ["gemini-program.txt"]


async def test_run_research_assistant_multi_hop(assistant, client, index, valid_sources):
    client.provider.add_tool_call("search_documents", {"query": "Space Shuttle"})
    client.provider.add_tool_call("search_documents", {"query": "ISS assembly"})
    client.provider.add_text(
        "The Space Shuttle [space-shuttle.txt] was used to help build the ISS [iss.txt]."
    )

    result = await assistant.run_research_assistant(
        client, index, valid_sources, "How did the Shuttle relate to the ISS?"
    )

    assert set(result.citations) == {"space-shuttle.txt", "iss.txt"}
    assert result.unverified_citations == []
    assert client.provider.call_count == 3


async def test_run_research_assistant_stops_at_max_steps(assistant, client, index, valid_sources):
    for _ in range(10):
        client.provider.add_tool_call("search_documents", {"query": "anything"})

    result = await assistant.run_research_assistant(
        client, index, valid_sources, "Keep searching forever.", max_steps=3
    )

    assert client.provider.call_count == 3
    assert "3" in result.text or "stopped" in result.text.lower()
