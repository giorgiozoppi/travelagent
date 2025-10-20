"""Parallel agent functions for the travel planning application."""

import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from travelagent.models import (
    TravelState,
    mock_attractions_search,
    mock_events_search,
    mock_flight_search,
    mock_hotel_search,
    mock_restaurant_search,
    mock_social_places_search,
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def flight_agent(state: TravelState) -> TravelState:
    """Search for flights to the destination.

    Args:
        state: Current travel state containing destination, dates, and budget.

    Returns:
        Updated state dictionary with flight search results including data
        and AI-generated analysis.
    """
    flight_prompt = ChatPromptTemplate.from_template(
        """You are a flight search specialist. Based on the travel requirements,
        provide flight recommendations and analysis.

        Destination: {destination}
        Dates: {dates}
        Budget: {budget}

        Flight Search Results: {results}

        Provide a summary of flight options with recommendations:"""
    )

    flight_data = mock_flight_search(state["destination"], state["dates"], state["budget"])

    chain = flight_prompt | llm | StrOutputParser()
    flight_analysis = chain.invoke({
        "destination": state["destination"],
        "dates": state["dates"],
        "budget": state["budget"],
        "results": json.dumps(flight_data, indent=2)
    })

    return {
        "flight_results": {
            "data": flight_data,
            "analysis": flight_analysis
        }
    }


def hotel_agent(state: TravelState) -> TravelState:
    """Search for hotels at the destination.

    Args:
        state: Current travel state containing destination, dates, and budget.

    Returns:
        Updated state dictionary with hotel search results including data
        and AI-generated analysis.
    """
    hotel_prompt = ChatPromptTemplate.from_template(
        """You are a hotel search specialist. Based on the travel requirements,
        provide hotel recommendations and analysis.

        Destination: {destination}
        Dates: {dates}
        Budget: {budget}

        Hotel Search Results: {results}

        Provide a summary of hotel options with recommendations:"""
    )

    hotel_data = mock_hotel_search(state["destination"], state["dates"], state["budget"])

    chain = hotel_prompt | llm | StrOutputParser()
    hotel_analysis = chain.invoke({
        "destination": state["destination"],
        "dates": state["dates"],
        "budget": state["budget"],
        "results": json.dumps(hotel_data, indent=2)
    })

    return {
        "hotel_results": {
            "data": hotel_data,
            "analysis": hotel_analysis
        }
    }


def events_agent(state: TravelState) -> TravelState:
    """Search for events and activities at the destination.

    Args:
        state: Current travel state containing destination and dates.

    Returns:
        Updated state dictionary with events search results including data
        and AI-generated analysis.
    """
    events_prompt = ChatPromptTemplate.from_template(
        """You are an events and activities specialist. Based on the travel requirements,
        provide recommendations for events and activities.

        Destination: {destination}
        Dates: {dates}

        Events Search Results: {results}

        Provide a summary of events and activities with recommendations:"""
    )

    events_data = mock_events_search(state["destination"], state["dates"])

    chain = events_prompt | llm | StrOutputParser()
    events_analysis = chain.invoke({
        "destination": state["destination"],
        "dates": state["dates"],
        "results": json.dumps(events_data, indent=2)
    })

    return {
        "events_results": {
            "data": events_data,
            "analysis": events_analysis
        }
    }


def restaurant_agent(state: TravelState) -> TravelState:
    """Search for restaurants at the destination.

    Args:
        state: Current travel state containing destination and budget.

    Returns:
        Updated state dictionary with restaurant search results including data
        and AI-generated analysis.
    """
    restaurant_prompt = ChatPromptTemplate.from_template(
        """You are a restaurant and dining specialist. Based on the travel requirements,
        provide dining recommendations.

        Destination: {destination}
        Budget: {budget}

        Restaurant Search Results: {results}

        Provide a summary of dining options with recommendations:"""
    )

    restaurant_data = mock_restaurant_search(state["destination"])

    chain = restaurant_prompt | llm | StrOutputParser()
    restaurant_analysis = chain.invoke({
        "destination": state["destination"],
        "budget": state["budget"],
        "results": json.dumps(restaurant_data, indent=2)
    })

    return {
        "restaurant_results": {
            "data": restaurant_data,
            "analysis": restaurant_analysis
        }
    }


def attractions_agent(state: TravelState) -> TravelState:
    """Search for main attractions at the destination.

    Args:
        state: Current travel state containing destination, dates, and budget.

    Returns:
        Updated state dictionary with attractions search results including
        AI-generated comprehensive attraction guide.
    """
    attractions_prompt = ChatPromptTemplate.from_template(
        """You are a local attractions specialist with deep knowledge of {destination}.
        Generate a comprehensive list of the main attractions and must-see places in this city.

        Destination: {destination}
        Dates: {dates}
        Budget: {budget}

        Please provide detailed information about the top attractions including:
        - Historical sites and landmarks
        - Museums and cultural attractions
        - Natural attractions (parks, gardens, etc.)
        - Architectural highlights
        - Local specialties unique to this destination

        For each attraction, include:
        - Name and type
        - Brief description
        - Typical admission cost (if any)
        - Recommended visit duration
        - Rating/popularity
        - Best time to visit

        Format your response as a detailed travel guide for attractions in {destination}."""
    )

    chain = attractions_prompt | llm | StrOutputParser()
    attractions_analysis = chain.invoke({
        "destination": state["destination"],
        "dates": state["dates"],
        "budget": state["budget"]
    })

    return {
        "attractions_results": {
            "data": {"llm_generated": True},
            "analysis": attractions_analysis
        }
    }


def social_places_agent(state: TravelState) -> TravelState:
    """Search for places to meet people at the destination.

    Args:
        state: Current travel state containing destination, dates, and budget.

    Returns:
        Updated state dictionary with social places search results including
        AI-generated comprehensive guide for meeting locals and travelers.
    """
    social_places_prompt = ChatPromptTemplate.from_template(
        """You are a local social life specialist with extensive knowledge of {destination}.
        Generate comprehensive recommendations for places where travelers can meet locals and other travelers,
        make social connections, and experience the local community culture.

        Destination: {destination}
        Dates: {dates}
        Budget: {budget}

        Please provide detailed information about social places and opportunities including:
        - Public spaces and community gathering spots
        - Cafés and social venues where locals and travelers mingle
        - Sports and recreation centers with group activities
        - Markets and social shopping areas
        - Language exchange venues and international meetups
        - Outdoor spaces popular with locals
        - Community events and social activities
        - Co-working spaces and social clubs

        For each place/activity, include:
        - Name and type of venue
        - Description of the social atmosphere
        - Best times to visit for social interaction
        - Types of people you'll likely meet
        - Activities or ways to engage with others
        - Cost (if any)
        - Tips for approaching and meeting people there

        Focus specifically on genuine local experiences and places that foster authentic connections
        rather than tourist-only venues. Format as a comprehensive social guide for {destination}."""
    )

    chain = social_places_prompt | llm | StrOutputParser()
    social_places_analysis = chain.invoke({
        "destination": state["destination"],
        "dates": state["dates"],
        "budget": state["budget"]
    })

    return {
        "social_places_results": {
            "data": {"llm_generated": True},
            "analysis": social_places_analysis
        }
    }


def consolidate_plan(state: TravelState) -> TravelState:
    """Consolidate all search results into a comprehensive travel plan.

    Args:
        state: Current travel state containing all search results from parallel
            agents (flights, hotels, events, restaurants, attractions, social places).

    Returns:
        Updated state dictionary with final consolidated travel plan including
        itinerary and recommendations.
    """
    consolidation_prompt = ChatPromptTemplate.from_template(
        """You are a travel planning specialist. Consolidate the following search results
        into a comprehensive, well-organized travel plan that includes main attractions and social opportunities.

        Destination: {destination}
        Dates: {dates}
        Budget: {budget}

        Flight Results: {flights}

        Hotel Results: {hotels}

        Events Results: {events}

        Restaurant Results: {restaurants}

        Main Attractions: {attractions}

        Social Places (Places to Meet People): {social_places}

        Create a detailed travel plan with recommendations and itinerary that includes:
        1. Transportation and accommodation
        2. Must-see attractions and sightseeing
        3. Social opportunities and places to meet locals and other travelers
        4. Dining recommendations
        5. Events and activities

        Focus especially on highlighting the main attractions and social connection opportunities."""
    )

    chain = consolidation_prompt | llm | StrOutputParser()
    final_plan = chain.invoke({
        "destination": state["destination"],
        "dates": state["dates"],
        "budget": state["budget"],
        "flights": state["flight_results"]["analysis"],
        "hotels": state["hotel_results"]["analysis"],
        "events": state["events_results"]["analysis"],
        "restaurants": state["restaurant_results"]["analysis"],
        "attractions": state["attractions_results"]["analysis"],
        "social_places": state["social_places_results"]["analysis"]
    })

    return {
        "final_plan": final_plan
    }