"""Pytest configuration and shared fixtures."""

import os
from typing import Any
from unittest.mock import Mock

import pytest
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


@pytest.fixture
def mock_llm() -> Mock:
    """Create a mock LLM for testing.

    Returns:
        Mock LLM instance that returns predefined responses.
    """
    mock = Mock(spec=ChatOpenAI)
    mock.invoke.return_value = "Mock LLM response"
    return mock


@pytest.fixture
def sample_travel_state() -> dict[str, Any]:
    """Create a sample travel state for testing.

    Returns:
        Dictionary containing sample travel state data.
    """
    return {
        "destination": "Barcelona",
        "dates": "March 15-20, 2024",
        "budget": "$2000",
        "flight_results": {},
        "hotel_results": {},
        "events_results": {},
        "restaurant_results": {},
        "attractions_results": {},
        "social_places_results": {},
        "final_plan": "",
        "human_approved": False,
    }


@pytest.fixture
def complete_travel_state() -> dict[str, Any]:
    """Create a complete travel state with all results populated.

    Returns:
        Dictionary containing complete travel state with mock results.
    """
    return {
        "destination": "Barcelona",
        "dates": "March 15-20, 2024",
        "budget": "$2000",
        "flight_results": {
            "data": {"flights": [{"airline": "Test Air", "price": "$450"}]},
            "analysis": "Flight analysis",
        },
        "hotel_results": {
            "data": {"hotels": [{"name": "Test Hotel", "price": "$150/night"}]},
            "analysis": "Hotel analysis",
        },
        "events_results": {
            "data": {"events": [{"name": "Test Event", "price": "Free"}]},
            "analysis": "Events analysis",
        },
        "restaurant_results": {
            "data": {"restaurants": [{"name": "Test Restaurant", "cuisine": "Local"}]},
            "analysis": "Restaurant analysis",
        },
        "attractions_results": {
            "data": {"llm_generated": True},
            "analysis": "Attractions analysis",
        },
        "social_places_results": {
            "data": {"llm_generated": True},
            "analysis": "Social places analysis",
        },
        "final_plan": "",
        "human_approved": False,
    }


@pytest.fixture
def mock_openai_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set a mock OpenAI API key for testing.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up test environment variables.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
