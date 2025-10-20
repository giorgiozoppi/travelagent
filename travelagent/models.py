"""Data models and mock API functions for the travel agent application."""

from typing import TypedDict


class TravelState(TypedDict):
    """State object for travel planning workflow.

    Attributes:
        destination: Travel destination city and country.
        dates: Travel dates in string format.
        budget: Budget constraints for the trip.
        flight_results: Flight search results with data and analysis.
        hotel_results: Hotel search results with data and analysis.
        events_results: Events search results with data and analysis.
        restaurant_results: Restaurant search results with data and analysis.
        attractions_results: Main attractions search results with data and analysis.
        social_places_results: Social places search results with data and analysis.
        final_plan: Consolidated travel plan summary.
        human_approved: Flag indicating human approval status.
    """

    destination: str
    dates: str
    budget: str
    flight_results: dict
    hotel_results: dict
    events_results: dict
    restaurant_results: dict
    attractions_results: dict
    social_places_results: dict
    final_plan: str
    human_approved: bool


def mock_flight_search(destination: str, dates: str, budget: str) -> dict:
    """Mock flight search API call.

    Args:
        destination: Travel destination city.
        dates: Travel dates in string format.
        budget: Budget constraints for flights.

    Returns:
        Dictionary containing flight options with details including airline,
        price, departure, arrival, and duration.
    """
    return {
        "flights": [
            {
                "airline": "Ryanair",
                "price": "$450",
                "departure": "8:30 AM",
                "arrival": "2:15 PM",
                "duration": "1h 45m"
            },
            {
                "airline": "Aer Lingus",
                "price": "$420",
                "departure": "1:20 PM",
                "arrival": "7:05 PM",
                "duration": "1h 45m"
            }
        ],
        "destination": destination,
        "search_dates": dates
    }


def mock_hotel_search(destination: str, dates: str, budget: str) -> dict:
    """Mock hotel search API call.

    Args:
        destination: Travel destination city.
        dates: Travel dates in string format.
        budget: Budget constraints for accommodations.

    Returns:
        Dictionary containing hotel options with details including name,
        price, rating, and amenities.
    """
    return {
        "hotels": [
            {
                "name": "Hotel Catalonia",
                "price": "$150/night",
                "rating": "4.5/5",
                "amenities": ["Pool", "Gym", "WiFi", "Breakfast"]
            },
            {
                "name": "NH Hotels",
                "price": "$89/night",
                "rating": "4.2/5",
                "amenities": ["WiFi", "Parking", "24h Front Desk"]
            }
        ],
        "destination": destination,
        "search_dates": dates
    }


def mock_events_search(destination: str, dates: str) -> dict:
    """Mock events search API call.

    Args:
        destination: Travel destination city.
        dates: Travel dates in string format.

    Returns:
        Dictionary containing event options with details including name,
        date, price, and category.
    """
    return {
        "events": [
            {
                "name": "Local Art Festival",
                "date": "Weekend",
                "price": "Free",
                "category": "Arts & Culture"
            },
            {
                "name": "Food & Wine Tour",
                "date": "Daily",
                "price": "$75",
                "category": "Food & Drink"
            }
        ],
        "destination": destination
    }


def mock_restaurant_search(destination: str) -> dict:
    """Mock restaurant search API call.

    Args:
        destination: Travel destination city.

    Returns:
        Dictionary containing restaurant options with details including name,
        cuisine, rating, and price range.
    """
    return {
        "restaurants": [
            {
                "name": "The Local Bistro",
                "cuisine": "Local/Fusion",
                "rating": "4.7/5",
                "price_range": "$$"
            },
            {
                "name": "Seaside Grill",
                "cuisine": "Seafood",
                "rating": "4.5/5",
                "price_range": "$$$"
            }
        ],
        "destination": destination
    }


def mock_attractions_search(destination: str) -> dict:
    """Mock attractions search API call.

    Args:
        destination: Travel destination city.

    Returns:
        Dictionary containing attraction options with details including name,
        type, description, rating, admission price, and recommended duration.
    """
    return {
        "attractions": [
            {
                "name": "Historic City Center",
                "type": "Historical Site",
                "description": "Beautiful medieval architecture and cobblestone streets",
                "rating": "4.8/5",
                "admission": "Free",
                "recommended_duration": "2-3 hours"
            },
            {
                "name": "National Art Museum",
                "type": "Museum",
                "description": "World-class collection of contemporary and classical art",
                "rating": "4.6/5",
                "admission": "$15",
                "recommended_duration": "3-4 hours"
            },
            {
                "name": "Botanical Gardens",
                "type": "Nature",
                "description": "Stunning gardens with rare plants and peaceful walking paths",
                "rating": "4.5/5",
                "admission": "$10",
                "recommended_duration": "1-2 hours"
            }
        ],
        "destination": destination
    }


def mock_social_places_search(destination: str) -> dict:
    """Mock social places search API call.

    Args:
        destination: Travel destination city.

    Returns:
        Dictionary containing social places with details including name, type,
        description, atmosphere, best time to visit, and activities.
    """
    return {
        "social_places": [
            {
                "name": "Central Market Square",
                "type": "Public Space",
                "description": "Bustling marketplace where locals gather, perfect for meeting people",
                "atmosphere": "Lively and welcoming",
                "best_time": "Morning and evening",
                "activities": ["Shopping", "People watching", "Local food"]
            },
            {
                "name": "Community Sports Center",
                "type": "Recreation",
                "description": "Local sports clubs and fitness classes open to visitors",
                "atmosphere": "Friendly and active",
                "best_time": "Weekday evenings",
                "activities": ["Group fitness", "Tennis", "Swimming"]
            },
            {
                "name": "Language Exchange Café",
                "type": "Café/Social",
                "description": "Popular spot for language exchanges and meeting international travelers",
                "atmosphere": "Relaxed and international",
                "best_time": "Tuesday and Thursday evenings",
                "activities": ["Language practice", "Cultural exchange", "Board games"]
            },
            {
                "name": "Riverside Walking Path",
                "type": "Outdoor",
                "description": "Scenic walking path where locals jog and walk their dogs",
                "atmosphere": "Peaceful and community-oriented",
                "best_time": "Early morning and sunset",
                "activities": ["Walking", "Jogging", "Dog watching"]
            }
        ],
        "destination": destination
    }