"""Unit tests for parallel_agents module."""

from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from travelagent.parallel_agents import (
    attractions_agent,
    consolidate_plan,
    events_agent,
    flight_agent,
    hotel_agent,
    restaurant_agent,
    social_places_agent,
)


class TestFlightAgent:
    """Test flight_agent function."""

    @patch("travelagent.parallel_agents.mock_flight_search")
    @patch("travelagent.parallel_agents.llm")
    def test_returns_flight_results(
        self,
        mock_llm: Mock,
        mock_flight_search: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that flight_agent returns flight results.

        Args:
            mock_llm: Mock LLM instance.
            mock_flight_search: Mock flight search function.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_flight_search.return_value = {"flights": []}
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Flight analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = flight_agent(sample_travel_state)

        # Verify
        assert "flight_results" in result
        assert "data" in result["flight_results"]
        assert "analysis" in result["flight_results"]

    @patch("travelagent.parallel_agents.mock_flight_search")
    @patch("travelagent.parallel_agents.llm")
    def test_calls_mock_flight_search(
        self,
        mock_llm: Mock,
        mock_flight_search: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that flight_agent calls mock_flight_search.

        Args:
            mock_llm: Mock LLM instance.
            mock_flight_search: Mock flight search function.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_flight_search.return_value = {"flights": []}
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Flight analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        flight_agent(sample_travel_state)

        # Verify
        mock_flight_search.assert_called_once_with(
            sample_travel_state["destination"],
            sample_travel_state["dates"],
            sample_travel_state["budget"],
        )


class TestHotelAgent:
    """Test hotel_agent function."""

    @patch("travelagent.parallel_agents.mock_hotel_search")
    @patch("travelagent.parallel_agents.llm")
    def test_returns_hotel_results(
        self,
        mock_llm: Mock,
        mock_hotel_search: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that hotel_agent returns hotel results.

        Args:
            mock_llm: Mock LLM instance.
            mock_hotel_search: Mock hotel search function.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_hotel_search.return_value = {"hotels": []}
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Hotel analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = hotel_agent(sample_travel_state)

        # Verify
        assert "hotel_results" in result
        assert "data" in result["hotel_results"]
        assert "analysis" in result["hotel_results"]


class TestEventsAgent:
    """Test events_agent function."""

    @patch("travelagent.parallel_agents.mock_events_search")
    @patch("travelagent.parallel_agents.llm")
    def test_returns_events_results(
        self,
        mock_llm: Mock,
        mock_events_search: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that events_agent returns events results.

        Args:
            mock_llm: Mock LLM instance.
            mock_events_search: Mock events search function.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_events_search.return_value = {"events": []}
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Events analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = events_agent(sample_travel_state)

        # Verify
        assert "events_results" in result
        assert "data" in result["events_results"]
        assert "analysis" in result["events_results"]


class TestRestaurantAgent:
    """Test restaurant_agent function."""

    @patch("travelagent.parallel_agents.mock_restaurant_search")
    @patch("travelagent.parallel_agents.llm")
    def test_returns_restaurant_results(
        self,
        mock_llm: Mock,
        mock_restaurant_search: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that restaurant_agent returns restaurant results.

        Args:
            mock_llm: Mock LLM instance.
            mock_restaurant_search: Mock restaurant search function.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_restaurant_search.return_value = {"restaurants": []}
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Restaurant analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = restaurant_agent(sample_travel_state)

        # Verify
        assert "restaurant_results" in result
        assert "data" in result["restaurant_results"]
        assert "analysis" in result["restaurant_results"]


class TestAttractionsAgent:
    """Test attractions_agent function."""

    @patch("travelagent.parallel_agents.llm")
    def test_returns_attractions_results(
        self,
        mock_llm: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that attractions_agent returns attractions results.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Attractions analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = attractions_agent(sample_travel_state)

        # Verify
        assert "attractions_results" in result
        assert "data" in result["attractions_results"]
        assert "analysis" in result["attractions_results"]
        assert result["attractions_results"]["data"]["llm_generated"] is True


class TestSocialPlacesAgent:
    """Test social_places_agent function."""

    @patch("travelagent.parallel_agents.llm")
    def test_returns_social_places_results(
        self,
        mock_llm: Mock,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that social_places_agent returns social places results.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Social places analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = social_places_agent(sample_travel_state)

        # Verify
        assert "social_places_results" in result
        assert "data" in result["social_places_results"]
        assert "analysis" in result["social_places_results"]
        assert result["social_places_results"]["data"]["llm_generated"] is True


class TestConsolidatePlan:
    """Test consolidate_plan function."""

    @patch("travelagent.parallel_agents.llm")
    def test_returns_final_plan(
        self,
        mock_llm: Mock,
        complete_travel_state: dict[str, Any],
    ) -> None:
        """Test that consolidate_plan returns final plan.

        Args:
            mock_llm: Mock LLM instance.
            complete_travel_state: Complete travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Final consolidated plan"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = consolidate_plan(complete_travel_state)

        # Verify
        assert "final_plan" in result
        assert isinstance(result["final_plan"], str)
        assert len(result["final_plan"]) > 0

    @patch("travelagent.parallel_agents.llm")
    def test_uses_all_results(
        self,
        mock_llm: Mock,
        complete_travel_state: dict[str, Any],
    ) -> None:
        """Test that consolidate_plan uses all search results.

        Args:
            mock_llm: Mock LLM instance.
            complete_travel_state: Complete travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Final consolidated plan"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        consolidate_plan(complete_travel_state)

        # Verify the chain was invoked with all required data
        mock_chain.invoke.assert_called_once()
        call_args = mock_chain.invoke.call_args[0][0]
        assert "destination" in call_args
        assert "dates" in call_args
        assert "budget" in call_args
        assert "flights" in call_args
        assert "hotels" in call_args
        assert "events" in call_args
        assert "restaurants" in call_args
        assert "attractions" in call_args
        assert "social_places" in call_args
