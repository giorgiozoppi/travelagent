"""Unit tests for models module."""

from typing import Any

import pytest

from travelagent.models import (
    TravelState,
    mock_attractions_search,
    mock_events_search,
    mock_flight_search,
    mock_hotel_search,
    mock_restaurant_search,
    mock_social_places_search,
)


class TestMockFlightSearch:
    """Test mock_flight_search function."""

    def test_returns_dict(self) -> None:
        """Test that mock_flight_search returns a dictionary."""
        result = mock_flight_search("Barcelona", "March 15-20", "$2000")
        assert isinstance(result, dict)

    def test_contains_flights_key(self) -> None:
        """Test that result contains 'flights' key."""
        result = mock_flight_search("Barcelona", "March 15-20", "$2000")
        assert "flights" in result

    def test_contains_destination(self) -> None:
        """Test that result contains destination information."""
        destination = "Barcelona"
        result = mock_flight_search(destination, "March 15-20", "$2000")
        assert result["destination"] == destination

    def test_contains_search_dates(self) -> None:
        """Test that result contains search dates."""
        dates = "March 15-20"
        result = mock_flight_search("Barcelona", dates, "$2000")
        assert result["search_dates"] == dates

    def test_flights_list_not_empty(self) -> None:
        """Test that flights list is not empty."""
        result = mock_flight_search("Barcelona", "March 15-20", "$2000")
        assert len(result["flights"]) > 0

    def test_flight_has_required_fields(self) -> None:
        """Test that each flight has required fields."""
        result = mock_flight_search("Barcelona", "March 15-20", "$2000")
        flight = result["flights"][0]
        assert "airline" in flight
        assert "price" in flight
        assert "departure" in flight
        assert "arrival" in flight
        assert "duration" in flight


class TestMockHotelSearch:
    """Test mock_hotel_search function."""

    def test_returns_dict(self) -> None:
        """Test that mock_hotel_search returns a dictionary."""
        result = mock_hotel_search("Barcelona", "March 15-20", "$2000")
        assert isinstance(result, dict)

    def test_contains_hotels_key(self) -> None:
        """Test that result contains 'hotels' key."""
        result = mock_hotel_search("Barcelona", "March 15-20", "$2000")
        assert "hotels" in result

    def test_contains_destination(self) -> None:
        """Test that result contains destination information."""
        destination = "Barcelona"
        result = mock_hotel_search(destination, "March 15-20", "$2000")
        assert result["destination"] == destination

    def test_hotels_list_not_empty(self) -> None:
        """Test that hotels list is not empty."""
        result = mock_hotel_search("Barcelona", "March 15-20", "$2000")
        assert len(result["hotels"]) > 0

    def test_hotel_has_required_fields(self) -> None:
        """Test that each hotel has required fields."""
        result = mock_hotel_search("Barcelona", "March 15-20", "$2000")
        hotel = result["hotels"][0]
        assert "name" in hotel
        assert "price" in hotel
        assert "rating" in hotel
        assert "amenities" in hotel


class TestMockEventsSearch:
    """Test mock_events_search function."""

    def test_returns_dict(self) -> None:
        """Test that mock_events_search returns a dictionary."""
        result = mock_events_search("Barcelona", "March 15-20")
        assert isinstance(result, dict)

    def test_contains_events_key(self) -> None:
        """Test that result contains 'events' key."""
        result = mock_events_search("Barcelona", "March 15-20")
        assert "events" in result

    def test_events_list_not_empty(self) -> None:
        """Test that events list is not empty."""
        result = mock_events_search("Barcelona", "March 15-20")
        assert len(result["events"]) > 0

    def test_event_has_required_fields(self) -> None:
        """Test that each event has required fields."""
        result = mock_events_search("Barcelona", "March 15-20")
        event = result["events"][0]
        assert "name" in event
        assert "date" in event
        assert "price" in event
        assert "category" in event


class TestMockRestaurantSearch:
    """Test mock_restaurant_search function."""

    def test_returns_dict(self) -> None:
        """Test that mock_restaurant_search returns a dictionary."""
        result = mock_restaurant_search("Barcelona")
        assert isinstance(result, dict)

    def test_contains_restaurants_key(self) -> None:
        """Test that result contains 'restaurants' key."""
        result = mock_restaurant_search("Barcelona")
        assert "restaurants" in result

    def test_restaurants_list_not_empty(self) -> None:
        """Test that restaurants list is not empty."""
        result = mock_restaurant_search("Barcelona")
        assert len(result["restaurants"]) > 0

    def test_restaurant_has_required_fields(self) -> None:
        """Test that each restaurant has required fields."""
        result = mock_restaurant_search("Barcelona")
        restaurant = result["restaurants"][0]
        assert "name" in restaurant
        assert "cuisine" in restaurant
        assert "rating" in restaurant
        assert "price_range" in restaurant


class TestMockAttractionsSearch:
    """Test mock_attractions_search function."""

    def test_returns_dict(self) -> None:
        """Test that mock_attractions_search returns a dictionary."""
        result = mock_attractions_search("Barcelona")
        assert isinstance(result, dict)

    def test_contains_attractions_key(self) -> None:
        """Test that result contains 'attractions' key."""
        result = mock_attractions_search("Barcelona")
        assert "attractions" in result

    def test_attractions_list_not_empty(self) -> None:
        """Test that attractions list is not empty."""
        result = mock_attractions_search("Barcelona")
        assert len(result["attractions"]) > 0

    def test_attraction_has_required_fields(self) -> None:
        """Test that each attraction has required fields."""
        result = mock_attractions_search("Barcelona")
        attraction = result["attractions"][0]
        assert "name" in attraction
        assert "type" in attraction
        assert "description" in attraction
        assert "rating" in attraction
        assert "admission" in attraction
        assert "recommended_duration" in attraction


class TestMockSocialPlacesSearch:
    """Test mock_social_places_search function."""

    def test_returns_dict(self) -> None:
        """Test that mock_social_places_search returns a dictionary."""
        result = mock_social_places_search("Barcelona")
        assert isinstance(result, dict)

    def test_contains_social_places_key(self) -> None:
        """Test that result contains 'social_places' key."""
        result = mock_social_places_search("Barcelona")
        assert "social_places" in result

    def test_social_places_list_not_empty(self) -> None:
        """Test that social places list is not empty."""
        result = mock_social_places_search("Barcelona")
        assert len(result["social_places"]) > 0

    def test_social_place_has_required_fields(self) -> None:
        """Test that each social place has required fields."""
        result = mock_social_places_search("Barcelona")
        place = result["social_places"][0]
        assert "name" in place
        assert "type" in place
        assert "description" in place
        assert "atmosphere" in place
        assert "best_time" in place
        assert "activities" in place


class TestTravelState:
    """Test TravelState TypedDict."""

    def test_travel_state_structure(self, sample_travel_state: dict[str, Any]) -> None:
        """Test that TravelState has correct structure.

        Args:
            sample_travel_state: Fixture providing sample travel state.
        """
        # Verify all required keys are present
        required_keys = {
            "destination",
            "dates",
            "budget",
            "flight_results",
            "hotel_results",
            "events_results",
            "restaurant_results",
            "attractions_results",
            "social_places_results",
            "final_plan",
            "human_approved",
        }
        assert set(sample_travel_state.keys()) == required_keys

    def test_travel_state_types(self, sample_travel_state: dict[str, Any]) -> None:
        """Test that TravelState values have correct types.

        Args:
            sample_travel_state: Fixture providing sample travel state.
        """
        assert isinstance(sample_travel_state["destination"], str)
        assert isinstance(sample_travel_state["dates"], str)
        assert isinstance(sample_travel_state["budget"], str)
        assert isinstance(sample_travel_state["flight_results"], dict)
        assert isinstance(sample_travel_state["hotel_results"], dict)
        assert isinstance(sample_travel_state["events_results"], dict)
        assert isinstance(sample_travel_state["restaurant_results"], dict)
        assert isinstance(sample_travel_state["attractions_results"], dict)
        assert isinstance(sample_travel_state["social_places_results"], dict)
        assert isinstance(sample_travel_state["final_plan"], str)
        assert isinstance(sample_travel_state["human_approved"], bool)
