"""Pattern 3: Parallelization - LangGraph Implementation.

This example demonstrates the Parallelization pattern using LangGraph.
The pattern executes multiple independent operations simultaneously
to improve efficiency and performance.

Use Case: Travel planning with concurrent flight, hotel, events, and restaurant searches.
"""

import json
import os
import re

from colorama import init
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from rich import print as rich_print
from rich.columns import Columns
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text

from travelagent.models import TravelState
from travelagent.parallel_agents import (
    attractions_agent,
    consolidate_plan,
    events_agent,
    flight_agent,
    hotel_agent,
    restaurant_agent,
    social_places_agent,
)

# Initialize colorama and rich console
init(autoreset=True)
console = Console()

# Load environment variables from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Initialize the Language Model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def collect_user_travel_request() -> dict[str, str]:
    """Collect travel request details from user input.

    Returns:
        Dictionary containing destination, dates, and budget provided by the user.
    """
    console.print(Panel.fit(
        "[bold blue]TRAVEL PLANNING REQUEST[/bold blue]",
        border_style="blue"
    ))
    console.print("[cyan]Please provide your travel details:[/cyan]\n")

    destination = Prompt.ask("[yellow]Destination[/yellow]")
    while not destination.strip():
        destination = Prompt.ask("[red]Please enter a destination[/red]")

    dates = Prompt.ask("[yellow]Travel dates[/yellow] (e.g., March 15-20, 2024)")
    while not dates.strip():
        dates = Prompt.ask("[red]Please enter travel dates[/red]")

    budget = Prompt.ask("[yellow]Budget[/yellow] (e.g., $2000 total)")
    while not budget.strip():
        budget = Prompt.ask("[red]Please enter your budget[/red]")

    return {
        "destination": destination.strip(),
        "dates": dates.strip(),
        "budget": budget.strip()
    }

def generate_travel_request_with_ai() -> dict[str, str]:
    """Use OpenAI to help generate or validate a travel request with improved conversation flow.

    Returns:
        Dictionary containing destination, dates, and budget collected through
        AI-assisted conversation.
    """
    console.print(Panel.fit(
        "[bold green]AI-ASSISTED TRAVEL PLANNING[/bold green]",
        border_style="green"
    ))

    # Initialize conversation state
    conversation_history = []
    collected_info = {"destination": "", "dates": "", "budget": ""}

    # Initial prompt
    initial_prompt = ChatPromptTemplate.from_template(
        """You are a helpful travel planning assistant. Help the user create a travel request.

        Start a friendly conversation to collect:
        - Destination (city, country)
        - Travel dates
        - Budget constraints

        Begin by asking: "I'd be happy to help you plan your trip! Where would you like to go?"
        """
    )

    chain = initial_prompt | llm | StrOutputParser()
    ai_response = chain.invoke({})
    console.print(f"[bold green]AI Assistant:[/bold green] {ai_response}")
    conversation_history.append(f"AI: {ai_response}")

    # Conversation loop with context preservation
    max_turns = 10  # Prevent infinite loops
    turn_count = 0

    while turn_count < max_turns:
        user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
        if not user_input:
            continue

        conversation_history.append(f"User: {user_input}")

        # Create context-aware prompt
        context_prompt = ChatPromptTemplate.from_template(
            """You are a travel planning assistant. Based on the conversation history, help collect travel information.

            CONVERSATION HISTORY:
            {conversation_history}

            CURRENTLY COLLECTED INFO:
            Destination: {destination}
            Dates: {dates}
            Budget: {budget}

            Latest user input: "{user_input}"

            Instructions:
            1. If the user provided new information, acknowledge it and update what you know
            2. If you have ALL required info (destination, dates, budget), respond with:
               "Perfect! I have all the information I need.

               DESTINATION: [destination]
               DATES: [travel dates]
               BUDGET: [budget amount]
               COMPLETE: YES"

            3. If information is still missing, ask for the next missing piece specifically
            4. Be conversational and helpful, not repetitive
            5. Don't ask for information already provided
            """
        )

        # Extract any new information from user input
        extraction_prompt = ChatPromptTemplate.from_template(
            """Extract travel information from: "{user_input}"

            Current info: Destination="{destination}", Dates="{dates}", Budget="{budget}"

            Return JSON with any new information found:
            {{"destination": "value or empty", "dates": "value or empty", "budget": "value or empty"}}

            Only include fields that were mentioned in the user input. Use empty string for fields not mentioned.
            """
        )

        extraction_chain = extraction_prompt | llm | StrOutputParser()
        try:
            extraction_result = extraction_chain.invoke({
                "user_input": user_input,
                "destination": collected_info["destination"],
                "dates": collected_info["dates"],
                "budget": collected_info["budget"]
            })

            # Parse extracted info
            json_match = re.search(r'\{.*\}', extraction_result)
            if json_match:
                extracted = json.loads(json_match.group())
                for key, value in extracted.items():
                    if value and value.strip():
                        collected_info[key] = value.strip()
        except Exception:  # noqa: S110
            pass  # Continue even if extraction fails

        # Generate response with context
        context_chain = context_prompt | llm | StrOutputParser()
        ai_response = context_chain.invoke({
            "conversation_history": "\n".join(conversation_history[-6:]),  # Keep last 6 exchanges
            "user_input": user_input,
            "destination": collected_info["destination"] or "Not provided",
            "dates": collected_info["dates"] or "Not provided",
            "budget": collected_info["budget"] or "Not provided"
        })

        console.print(f"[bold green]AI Assistant:[/bold green] {ai_response}")
        conversation_history.append(f"AI: {ai_response}")

        # Check if complete
        if "COMPLETE: YES" in ai_response:
            # Extract final information from AI response
            lines = ai_response.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith("DESTINATION:"):
                    collected_info["destination"] = line.split(":", 1)[1].strip()
                elif line.startswith("DATES:"):
                    collected_info["dates"] = line.split(":", 1)[1].strip()
                elif line.startswith("BUDGET:"):
                    collected_info["budget"] = line.split(":", 1)[1].strip()
            break

        turn_count += 1

    # Validate we have all required information
    if not all(collected_info.values()):
        console.print("[yellow]Warning: Some information may be missing. Using what was collected.[/yellow]")

    return collected_info


def human_approval_agent(state: TravelState) -> TravelState:
    """Get human approval for the travel plan.

    Args:
        state: Current travel state containing the final travel plan.

    Returns:
        Updated state dictionary with human_approved flag and potentially
        revised final_plan if modifications were requested.
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold blue]TRAVEL PLAN READY FOR REVIEW[/bold blue]",
        border_style="blue"
    ))

    # Create info table
    info_table = Table(show_header=False, box=None)
    info_table.add_column("Label", style="cyan", width=12)
    info_table.add_column("Value", style="white")
    info_table.add_row("Destination:", state['destination'])
    info_table.add_row("Dates:", state['dates'])
    info_table.add_row("Budget:", state['budget'])
    console.print(info_table)

    console.print("\n[bold yellow]Generated Travel Plan:[/bold yellow]")
    console.print(Panel(
        Markdown(state["final_plan"]),
        border_style="yellow"
    ))

    # Get human feedback
    while True:
        approval = Prompt.ask(
            "\n[bold]Do you approve this travel plan?[/bold]",
            choices=["yes", "no", "modify"],
            default="yes"
        ).lower().strip()

        if approval in ['yes', 'y']:
            console.print("[bold green]✅ Travel plan approved! Booking can proceed.[/bold green]")
            return {
                "human_approved": True
            }
        elif approval in ['no', 'n']:
            console.print("[bold red]❌ Travel plan rejected.[/bold red]")
            return {
                "human_approved": False
            }
        elif approval in ['modify', 'm']:
            console.print("[cyan]Please provide feedback for modifications:[/cyan]")
            feedback = Prompt.ask("[yellow]Your feedback[/yellow]").strip()

            # Use AI to incorporate feedback
            modification_prompt = ChatPromptTemplate.from_template(
                """The user has provided feedback on the travel plan. Please revise the plan based on their input.

                Original Plan: {original_plan}

                User Feedback: {feedback}

                Provide a revised travel plan that addresses the user's concerns:"""
            )

            chain = modification_prompt | llm | StrOutputParser()
            revised_plan = chain.invoke({
                "original_plan": state["final_plan"],
                "feedback": feedback
            })

            console.print("\n")
            console.print(Panel.fit(
                "[bold green]REVISED TRAVEL PLAN[/bold green]",
                border_style="green"
            ))
            console.print(Panel(
                Markdown(revised_plan),
                border_style="green"
            ))

            # Ask for approval again
            final_approval = Confirm.ask("\n[bold]Do you approve the revised plan?[/bold]")
            if final_approval:
                console.print("[bold green]✅ Revised travel plan approved![/bold green]")
                return {
                    "final_plan": revised_plan,
                    "human_approved": True
                }
            else:
                console.print("[bold red]❌ Revised travel plan rejected.[/bold red]")
                return {
                    "final_plan": revised_plan,
                    "human_approved": False
                }

def create_parallelization_workflow() -> StateGraph:
    """Create and compile the parallelization workflow.

    Returns:
        Compiled StateGraph representing the travel planning workflow with
        parallel agent execution.
    """
    workflow = StateGraph(TravelState)

    # Add parallel agents
    workflow.add_node("flight_search", flight_agent)
    workflow.add_node("hotel_search", hotel_agent)
    workflow.add_node("events_search", events_agent)
    workflow.add_node("restaurant_search", restaurant_agent)
    workflow.add_node("attractions_search", attractions_agent)
    workflow.add_node("social_places_search", social_places_agent)
    workflow.add_node("consolidate", consolidate_plan)
    workflow.add_node("human_approval", human_approval_agent)

    # Set entry points for parallel execution
    workflow.set_entry_point("flight_search")
    workflow.set_entry_point("hotel_search")
    workflow.set_entry_point("events_search")
    workflow.set_entry_point("restaurant_search")
    workflow.set_entry_point("attractions_search")
    workflow.set_entry_point("social_places_search")

    # All parallel agents feed into consolidation
    workflow.add_edge("flight_search", "consolidate")
    workflow.add_edge("hotel_search", "consolidate")
    workflow.add_edge("events_search", "consolidate")
    workflow.add_edge("restaurant_search", "consolidate")
    workflow.add_edge("attractions_search", "consolidate")
    workflow.add_edge("social_places_search", "consolidate")

    # Consolidation goes to human approval
    workflow.add_edge("consolidate", "human_approval")

    # Human approval ends the workflow
    workflow.add_edge("human_approval", END)

    return workflow.compile()


def main() -> None:
    """Example usage of the parallelization pattern with user input and human-in-the-loop."""
    console.print(Panel.fit(
        "[bold magenta]PARALLELIZATION PATTERN: TRAVEL PLANNING[/bold magenta]\n[cyan]This system demonstrates parallel processing with human oversight.[/cyan]",
        border_style="magenta"
    ))

    # Get travel request input method preference
    console.print("\n[bold]How would you like to provide your travel request?[/bold]")

    choice_table = Table(show_header=False, box=None)
    choice_table.add_column("Choice", style="cyan", width=5)
    choice_table.add_column("Description", style="white")
    choice_table.add_row("1.", "Direct input (manual)")
    choice_table.add_row("2.", "AI-assisted conversation")
    console.print(choice_table)

    choice = Prompt.ask(
        "\n[yellow]Enter your choice[/yellow]",
        choices=["1", "2"],
        default="1"
    )

    if choice == "1":
        user_request = collect_user_travel_request()
    else:
        user_request = generate_travel_request_with_ai()

    # Create the workflow
    travel_system = create_parallelization_workflow()

    # Prepare the travel request state
    travel_request = {
        "destination": user_request["destination"],
        "dates": user_request["dates"],
        "budget": user_request["budget"],
        "flight_results": {},
        "hotel_results": {},
        "events_results": {},
        "restaurant_results": {},
        "attractions_results": {},
        "social_places_results": {},
        "final_plan": "",
        "human_approved": False
    }

    console.print("\n")
    console.print(Panel.fit(
        "[bold blue]PROCESSING TRAVEL REQUEST[/bold blue]",
        border_style="blue"
    ))

    # Display request details in a table
    request_table = Table(title="Travel Request Details", show_header=True, header_style="bold cyan")
    request_table.add_column("Field", style="cyan", width=12)
    request_table.add_column("Value", style="white")
    request_table.add_row("Destination", travel_request['destination'])
    request_table.add_row("Dates", travel_request['dates'])
    request_table.add_row("Budget", travel_request['budget'])
    console.print(request_table)

    console.print("\n[yellow]Executing parallel searches for flights, hotels, events, restaurants, attractions, and social places...[/yellow]")

    # Show progress with rich progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Processing travel searches...", total=None)

        # Execute the parallelization workflow
        result = travel_system.invoke(travel_request)
        progress.update(task, description="Travel searches completed!")

    # Final status
    console.print("\n")
    console.print(Panel.fit(
        "[bold blue]TRAVEL PLANNING COMPLETE[/bold blue]",
        border_style="blue"
    ))

    if result["human_approved"]:
        console.print(Panel(
            "[bold green]✅ Your travel plan has been approved and is ready for booking![/bold green]\n\n[cyan]Next steps: Proceed with reservations based on the approved plan.[/cyan]",
            border_style="green",
            title="Success"
        ))
    else:
        console.print(Panel(
            "[bold red]❌ Travel plan was not approved.[/bold red]\n\n[yellow]You may restart the process with modified requirements.[/yellow]",
            border_style="red",
            title="Not Approved"
        ))

if __name__ == "__main__":
    # Set your OpenAI API key
    # os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    main()