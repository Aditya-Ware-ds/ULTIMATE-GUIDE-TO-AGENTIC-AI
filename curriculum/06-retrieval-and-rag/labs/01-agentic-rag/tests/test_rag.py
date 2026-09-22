import pytest

from shared.llm.types import ToolCall


def test_load_documents_finds_all_four_files(documents):
    assert set(documents.keys()) == {
        "refunds.txt",
        "shipping.txt",
        "warranty.txt",
        "account.txt",
    }


def test_chunk_text_produces_multiple_chunks_with_overlap(rag):
    text = "word " * 200
    chunks = rag.chunk_text(text, chunk_size=100, overlap=20)

    assert len(chunks) > 1
    # verify actual overlap: the tail of one chunk appears at the head of the next
    assert chunks[0][-20:] == chunks[1][:20]


def test_toy_embed_is_deterministic(rag):
    assert rag.toy_embed("hello world") == rag.toy_embed("hello world")


def test_toy_embed_similar_text_more_similar_than_different_text(rag):
    a = rag.toy_embed("the cat sat on the mat")
    b = rag.toy_embed("the cat sat on the rug")
    c = rag.toy_embed("quarterly revenue increased twelve percent")

    assert rag.cosine_similarity(a, b) > rag.cosine_similarity(a, c)


def test_cosine_similarity_self_is_one(rag):
    vector = rag.toy_embed("some text")

    assert rag.cosine_similarity(vector, vector) == pytest.approx(1.0, abs=1e-6)


def test_cosine_similarity_zero_vector_is_zero(rag):
    assert rag.cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_keyword_score_exact_overlap(rag):
    assert rag.keyword_score("warranty claim", "file a warranty claim today") == 1.0


def test_keyword_score_no_overlap(rag):
    assert rag.keyword_score("warranty claim", "totally unrelated text here") == 0.0


def test_hybrid_score_combines_both(rag):
    assert rag.hybrid_score(1.0, 0.0, alpha=0.5) == pytest.approx(0.5)
    assert rag.hybrid_score(0.0, 1.0, alpha=0.5) == pytest.approx(0.5)
    assert rag.hybrid_score(1.0, 1.0, alpha=0.5) == pytest.approx(1.0)


def test_hybrid_search_finds_relevant_chunk(rag, index):
    results = rag.hybrid_search("warranty claim defect", index, top_k=3)

    assert any("warranty" in r.lower() for r in results)


def test_hybrid_search_respects_top_k(rag, index):
    results = rag.hybrid_search("refund", index, top_k=2)

    assert len(results) <= 2


def test_dispatch_returns_results_for_valid_query(rag, index):
    call = ToolCall(id="1", name="search_documents", arguments={"query": "password reset"})

    result = rag.dispatch(call, index)

    assert not result.is_error
    assert "password" in result.content.lower() or "reset" in result.content.lower()


def test_dispatch_never_raises_on_unknown_tool(rag, index):
    call = ToolCall(id="2", name="not_a_tool", arguments={})

    result = rag.dispatch(call, index)

    assert result.is_error


async def test_run_agentic_rag_single_search(rag, client, index):
    client.provider.add_tool_call("search_documents", {"query": "refund policy"})
    client.provider.add_text("You can return items within 30 days for a full refund.")

    result = await rag.run_agentic_rag(client, index, "What's the refund policy?")

    assert result == "You can return items within 30 days for a full refund."


async def test_run_agentic_rag_multi_hop(rag, client, index):
    client.provider.add_tool_call("search_documents", {"query": "refund policy"})
    client.provider.add_tool_call("search_documents", {"query": "warranty claim"})
    client.provider.add_text("Refunds: 30 days. Warranty: 1 year, file a claim with support.")

    result = await rag.run_agentic_rag(
        client, index, "What's the refund policy and the warranty terms?"
    )

    assert result == "Refunds: 30 days. Warranty: 1 year, file a claim with support."
    assert client.provider.call_count == 3


async def test_run_agentic_rag_stops_at_max_steps(rag, client, index):
    for _ in range(10):
        client.provider.add_tool_call("search_documents", {"query": "anything"})

    result = await rag.run_agentic_rag(client, index, "Keep searching forever.", max_steps=3)

    assert client.provider.call_count == 3
    assert "3" in result or "stopped" in result.lower()
