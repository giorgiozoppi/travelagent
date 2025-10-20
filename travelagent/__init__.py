"""Travel Agent - Parallelization Pattern Example."""

from travelagent.models import FlightQuery, FlightResult, HotelQuery, HotelResult, WeatherQuery, WeatherResult
from travelagent.parallel_agents import TravelAgent

__version__ = "1.0.0"

__all__ = [
    "TravelAgent",
    "FlightQuery",
    "FlightResult",
    "HotelQuery",
    "HotelResult",
    "WeatherQuery",
    "WeatherResult",
]
