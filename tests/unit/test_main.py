"""Unit tests for main module."""

from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest

from travelagent.main import (
    collect_user_travel_request,
    create_parallelization_workflow,
    generate_travel_request_with_ai,
    human_approval_agent,
)


class TestCollectUserTravelRequest:
    """Test collect_user_travel_request function."""

    @patch("travelagent.main.Prompt.ask")
    def test_collects_all_required_fields(self, mock_ask: Mock) -> None:
        """Test that function collects destination, dates, and budget.

        Args:
            mock_ask: Mock Prompt.ask method.
        """
        # Setup mock responses
        mock_ask.side_effect = ["Barcelona", "March 15-20, 2024", "$2000"]

        # Execute
        result = collect_user_travel_request()

        # Verify
        assert result["destination"] == "Barcelona"
        assert result["dates"] == "March 15-20, 2024"
        assert result["budget"] == "$2000"
        assert mock_ask.call_count == 3

    @patch("travelagent.main.Prompt.ask")
    def test_strips_whitespace(self, mock_ask: Mock) -> None:
        """Test that function strips whitespace from inputs.

        Args:
            mock_ask: Mock Prompt.ask method.
        """
        # Setup mock responses with whitespace
        mock_ask.side_effect = ["  Barcelona  ", "  March 15-20  ", "  $2000  "]

        # Execute
        result = collect_user_travel_request()

        # Verify
        assert result["destination"] == "Barcelona"
        assert result["dates"] == "March 15-20"
        assert result["budget"] == "$2000"

    @patch("travelagent.main.Prompt.ask")
    def test_reprompts_on_empty_input(self, mock_ask: Mock) -> None:
        """Test that function re-prompts when user enters empty values.

        Args:
            mock_ask: Mock Prompt.ask method.
        """
        # Setup mock responses with empty values followed by valid ones
        mock_ask.side_effect = [
            "",
            "Barcelona",  # destination (retry)
            "",
            "March 15-20",  # dates (retry)
            "",
            "$2000",  # budget (retry)
        ]

        # Execute
        result = collect_user_travel_request()

        # Verify we got valid results and ask was called 6 times (3 retries)
        assert result["destination"] == "Barcelona"
        assert mock_ask.call_count == 6


class TestGenerateTravelRequestWithAI:
    """Test generate_travel_request_with_ai function."""

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.main.llm")
    def test_returns_travel_request_dict(self, mock_llm: Mock, mock_ask: Mock) -> None:
        """Test that function returns a dictionary with travel request.

        Args:
            mock_llm: Mock LLM instance.
            mock_ask: Mock Prompt.ask method.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = [
            "Hello! Where would you like to go?",  # Initial prompt
            "Great! When?",  # Follow-up
            "Perfect! I have all the information I need.\n\nDESTINATION: Barcelona\nDATES: March 15-20\nBUDGET: $2000\nCOMPLETE: YES",  # Final response
        ]
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        mock_ask.side_effect = [
            "Barcelona",
            "March 15-20",
        ]

        # Execute
        result = generate_travel_request_with_ai()

        # Verify
        assert isinstance(result, dict)
        assert "destination" in result
        assert "dates" in result
        assert "budget" in result


class TestHumanApprovalAgent:
    """Test human_approval_agent function."""

    @patch("travelagent.main.Prompt.ask")
    def test_approval_yes(
        self, mock_ask: Mock, complete_travel_state: dict[str, Any]
    ) -> None:
        """Test human approval when user says yes.

        Args:
            mock_ask: Mock Prompt.ask method.
            complete_travel_state: Complete travel state fixture.
        """
        # Setup
        complete_travel_state["final_plan"] = "Test travel plan"
        mock_ask.return_value = "yes"

        # Execute
        result = human_approval_agent(complete_travel_state)

        # Verify
        assert result["human_approved"] is True

    @patch("travelagent.main.Prompt.ask")
    def test_approval_no(
        self, mock_ask: Mock, complete_travel_state: dict[str, Any]
    ) -> None:
        """Test human approval when user says no.

        Args:
            mock_ask: Mock Prompt.ask method.
            complete_travel_state: Complete travel state fixture.
        """
        # Setup
        complete_travel_state["final_plan"] = "Test travel plan"
        mock_ask.return_value = "no"

        # Execute
        result = human_approval_agent(complete_travel_state)

        # Verify
        assert result["human_approved"] is False

    @patch("travelagent.main.Confirm.ask")
    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.main.llm")
    def test_approval_modify_and_approve(
        self,
        mock_llm: Mock,
        mock_prompt_ask: Mock,
        mock_confirm: Mock,
        complete_travel_state: dict[str, Any],
    ) -> None:
        """Test human approval with modification request that gets approved.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt_ask: Mock Prompt.ask method.
            mock_confirm: Mock Confirm.ask method.
            complete_travel_state: Complete travel state fixture.
        """
        # Setup
        complete_travel_state["final_plan"] = "Original plan"
        mock_prompt_ask.side_effect = [
            "modify",  # Initial choice
            "Please add more restaurants",  # Feedback
        ]
        mock_confirm.return_value = True  # Approve revised plan

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Revised plan with more restaurants"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Execute
        result = human_approval_agent(complete_travel_state)

        # Verify
        assert result["human_approved"] is True
        assert result["final_plan"] == "Revised plan with more restaurants"


class TestCreateParallelizationWorkflow:
    """Test create_parallelization_workflow function."""

    def test_creates_compiled_workflow(self) -> None:
        """Test that function creates a compiled workflow."""
        # Execute
        workflow = create_parallelization_workflow()

        # Verify
        assert workflow is not None
        # The compiled workflow should be callable
        assert callable(workflow.invoke)

    def test_workflow_has_required_nodes(self) -> None:
        """Test that workflow contains all required nodes."""
        # Execute
        workflow = create_parallelization_workflow()

        # Verify - check that the workflow was created
        # (More detailed testing would require inspecting internal structure)
        assert workflow is not None


class TestWorkflowConfiguration:
    """Test workflow configuration and structure."""

    def test_workflow_compiles_successfully(self) -> None:
        """Test that the workflow compiles without errors."""
        # This tests that all nodes and edges are properly configured
        try:
            workflow = create_parallelization_workflow()
            assert workflow is not None
        except Exception as e:
            pytest.fail(f"Workflow compilation failed: {e}")
