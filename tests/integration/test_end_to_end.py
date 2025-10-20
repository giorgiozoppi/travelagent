"""End-to-end integration tests for the travel agent system."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from travelagent.models import (
    mock_attractions_search,
    mock_events_search,
    mock_flight_search,
    mock_hotel_search,
    mock_restaurant_search,
    mock_social_places_search,
)
from travelagent.parallel_agents import (
    attractions_agent,
    consolidate_plan,
    events_agent,
    flight_agent,
    hotel_agent,
    restaurant_agent,
    social_places_agent,
)


class TestEndToEndAgentExecution:
    """End-to-end tests for agent execution without mocking underlying services."""

    @patch("travelagent.parallel_agents.llm")
    def test_flight_agent_with_real_mock_data(
        self, mock_llm: Any, sample_travel_state: dict[str, Any]
    ) -> None:
        """Test flight agent with actual mock data service.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup LLM mock only
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Comprehensive flight analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute with real mock_flight_search
        result = flight_agent(sample_travel_state)

        # Verify structure and content
        assert "flight_results" in result
        assert "data" in result["flight_results"]
        assert "analysis" in result["flight_results"]
        assert "flights" in result["flight_results"]["data"]
        assert len(result["flight_results"]["data"]["flights"]) > 0

    @patch("travelagent.parallel_agents.llm")
    def test_hotel_agent_with_real_mock_data(
        self, mock_llm: Any, sample_travel_state: dict[str, Any]
    ) -> None:
        """Test hotel agent with actual mock data service.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup LLM mock only
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Comprehensive hotel analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute with real mock_hotel_search
        result = hotel_agent(sample_travel_state)

        # Verify structure and content
        assert "hotel_results" in result
        assert "data" in result["hotel_results"]
        assert "hotels" in result["hotel_results"]["data"]
        assert len(result["hotel_results"]["data"]["hotels"]) > 0

    @patch("travelagent.parallel_agents.llm")
    def test_all_agents_execute_sequentially(
        self, mock_llm: Any, sample_travel_state: dict[str, Any]
    ) -> None:
        """Test executing all agents in sequence.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup LLM mock
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Agent analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        state = sample_travel_state.copy()

        # Execute all agents in sequence
        state.update(flight_agent(state))
        assert "flight_results" in state

        state.update(hotel_agent(state))
        assert "hotel_results" in state

        state.update(events_agent(state))
        assert "events_results" in state

        state.update(restaurant_agent(state))
        assert "restaurant_results" in state

        state.update(attractions_agent(state))
        assert "attractions_results" in state

        state.update(social_places_agent(state))
        assert "social_places_results" in state

        # Verify all results are present
        assert all(
            key in state
            for key in [
                "flight_results",
                "hotel_results",
                "events_results",
                "restaurant_results",
                "attractions_results",
                "social_places_results",
            ]
        )


class TestEndToEndConsolidation:
    """End-to-end tests for the consolidation process."""

    @patch("travelagent.parallel_agents.llm")
    def test_consolidation_with_all_results(
        self, mock_llm: Any, sample_travel_state: dict[str, Any]
    ) -> None:
        """Test consolidation after all agents have run.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup LLM mock
        mock_chain = MagicMock()

        def mock_invoke(args: dict[str, Any]) -> str:
            # Return different responses based on what's being invoked
            if "consolidate" in str(args).lower():
                return "Complete travel itinerary with all components"
            return "Analysis result"

        mock_chain.invoke.side_effect = mock_invoke
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        state = sample_travel_state.copy()

        # Run all agents
        state.update(flight_agent(state))
        state.update(hotel_agent(state))
        state.update(events_agent(state))
        state.update(restaurant_agent(state))
        state.update(attractions_agent(state))
        state.update(social_places_agent(state))

        # Run consolidation
        state.update(consolidate_plan(state))

        # Verify final plan was created
        assert "final_plan" in state
        assert len(state["final_plan"]) > 0
        assert isinstance(state["final_plan"], str)


class TestMockDataServices:
    """Test the mock data services produce valid data structures."""

    def test_mock_flight_search_structure(self) -> None:
        """Test mock_flight_search returns valid structure."""
        result = mock_flight_search("Barcelona", "March 15-20", "$2000")

        assert "flights" in result
        assert "destination" in result
        assert "search_dates" in result
        assert isinstance(result["flights"], list)
        assert len(result["flights"]) > 0

        # Check first flight structure
        flight = result["flights"][0]
        assert all(
            key in flight
            for key in ["airline", "price", "departure", "arrival", "duration"]
        )

    def test_mock_hotel_search_structure(self) -> None:
        """Test mock_hotel_search returns valid structure."""
        result = mock_hotel_search("Barcelona", "March 15-20", "$2000")

        assert "hotels" in result
        assert "destination" in result
        assert isinstance(result["hotels"], list)
        assert len(result["hotels"]) > 0

        # Check first hotel structure
        hotel = result["hotels"][0]
        assert all(key in hotel for key in ["name", "price", "rating", "amenities"])

    def test_mock_events_search_structure(self) -> None:
        """Test mock_events_search returns valid structure."""
        result = mock_events_search("Barcelona", "March 15-20")

        assert "events" in result
        assert "destination" in result
        assert isinstance(result["events"], list)
        assert len(result["events"]) > 0

        # Check first event structure
        event = result["events"][0]
        assert all(key in event for key in ["name", "date", "price", "category"])

    def test_mock_restaurant_search_structure(self) -> None:
        """Test mock_restaurant_search returns valid structure."""
        result = mock_restaurant_search("Barcelona")

        assert "restaurants" in result
        assert "destination" in result
        assert isinstance(result["restaurants"], list)
        assert len(result["restaurants"]) > 0

        # Check first restaurant structure
        restaurant = result["restaurants"][0]
        assert all(
            key in restaurant for key in ["name", "cuisine", "rating", "price_range"]
        )

    def test_mock_attractions_search_structure(self) -> None:
        """Test mock_attractions_search returns valid structure."""
        result = mock_attractions_search("Barcelona")

        assert "attractions" in result
        assert "destination" in result
        assert isinstance(result["attractions"], list)
        assert len(result["attractions"]) > 0

        # Check first attraction structure
        attraction = result["attractions"][0]
        assert all(
            key in attraction
            for key in [
                "name",
                "type",
                "description",
                "rating",
                "admission",
                "recommended_duration",
            ]
        )

    def test_mock_social_places_search_structure(self) -> None:
        """Test mock_social_places_search returns valid structure."""
        result = mock_social_places_search("Barcelona")

        assert "social_places" in result
        assert "destination" in result
        assert isinstance(result["social_places"], list)
        assert len(result["social_places"]) > 0

        # Check first social place structure
        place = result["social_places"][0]
        assert all(
            key in place
            for key in [
                "name",
                "type",
                "description",
                "atmosphere",
                "best_time",
                "activities",
            ]
        )


class TestStateManagement:
    """Test state management across agent executions."""

    @patch("travelagent.parallel_agents.llm")
    def test_state_immutability(
        self, mock_llm: Any, sample_travel_state: dict[str, Any]
    ) -> None:
        """Test that agents don't mutate original state.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup LLM mock
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Store original values
        original_destination = sample_travel_state["destination"]
        original_dates = sample_travel_state["dates"]
        original_budget = sample_travel_state["budget"]

        # Execute agent
        flight_agent(sample_travel_state)

        # Verify original state unchanged
        assert sample_travel_state["destination"] == original_destination
        assert sample_travel_state["dates"] == original_dates
        assert sample_travel_state["budget"] == original_budget

    @patch("travelagent.parallel_agents.llm")
    def test_state_accumulation(
        self, mock_llm: Any, sample_travel_state: dict[str, Any]
    ) -> None:
        """Test that state accumulates results from multiple agents.

        Args:
            mock_llm: Mock LLM instance.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup LLM mock
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        state = sample_travel_state.copy()
        initial_keys = set(state.keys())

        # Run agents and accumulate results
        state.update(flight_agent(state))
        state.update(hotel_agent(state))

        # Verify state has grown
        assert len(state.keys()) >= len(initial_keys)
        assert "flight_results" in state
        assert "hotel_results" in state
