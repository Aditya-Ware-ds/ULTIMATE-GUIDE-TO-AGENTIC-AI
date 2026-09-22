"""Thin adapters translating shared/llm/types.py to/from each vendor SDK.

Each adapter imports its vendor SDK lazily inside __init__ so that importing
shared.llm never requires every SDK to be installed, and so offline tests (which
only use MockLLMProvider) never touch these modules at all.
"""
