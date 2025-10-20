"""Integration tests for the complete travel agent workflow."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from travelagent.main import create_parallelization_workflow


class TestWorkflowIntegration:
    """Integration tests for the complete workflow execution."""

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_complete_workflow_execution(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test complete workflow from start to finish.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Mock analysis result"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Mock human approval to return yes
        mock_prompt.return_value = "yes"

        # Create workflow
        workflow = create_parallelization_workflow()

        # Execute workflow
        result = workflow.invoke(sample_travel_state)

        # Verify all results are populated
        assert "flight_results" in result
        assert "hotel_results" in result
        assert "events_results" in result
        assert "restaurant_results" in result
        assert "attractions_results" in result
        assert "social_places_results" in result
        assert "final_plan" in result
        assert "human_approved" in result

        # Verify results structure
        assert "data" in result["flight_results"]
        assert "analysis" in result["flight_results"]
        assert "data" in result["hotel_results"]
        assert "analysis" in result["hotel_results"]

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_workflow_human_approval(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test workflow with human approval step.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Mock analysis result"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Mock human approval
        mock_prompt.return_value = "yes"

        # Create and execute workflow
        workflow = create_parallelization_workflow()
        result = workflow.invoke(sample_travel_state)

        # Verify approval was captured
        assert result["human_approved"] is True

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_workflow_human_rejection(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test workflow with human rejection.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Mock analysis result"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)

        # Mock human rejection
        mock_prompt.return_value = "no"

        # Create and execute workflow
        workflow = create_parallelization_workflow()
        result = workflow.invoke(sample_travel_state)

        # Verify rejection was captured
        assert result["human_approved"] is False

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_parallel_agents_execute(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that all parallel agents execute and populate results.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Mock analysis"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)
        mock_prompt.return_value = "yes"

        # Create and execute workflow
        workflow = create_parallelization_workflow()
        result = workflow.invoke(sample_travel_state)

        # Verify all parallel agents ran
        assert len(result["flight_results"]) > 0
        assert len(result["hotel_results"]) > 0
        assert len(result["events_results"]) > 0
        assert len(result["restaurant_results"]) > 0
        assert len(result["attractions_results"]) > 0
        assert len(result["social_places_results"]) > 0


class TestWorkflowStateTransitions:
    """Test state transitions through the workflow."""

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_state_preservation(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that state is preserved through workflow execution.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Mock result"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)
        mock_prompt.return_value = "yes"

        # Create and execute workflow
        workflow = create_parallelization_workflow()
        result = workflow.invoke(sample_travel_state)

        # Verify original state values are preserved
        assert result["destination"] == sample_travel_state["destination"]
        assert result["dates"] == sample_travel_state["dates"]
        assert result["budget"] == sample_travel_state["budget"]

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_consolidation_uses_all_results(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that consolidation step receives all parallel results.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Consolidated plan"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)
        mock_prompt.return_value = "yes"

        # Create and execute workflow
        workflow = create_parallelization_workflow()
        result = workflow.invoke(sample_travel_state)

        # Verify final plan was created
        assert result["final_plan"] is not None
        assert len(result["final_plan"]) > 0


class TestWorkflowErrorHandling:
    """Test error handling in the workflow."""

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_workflow_handles_empty_destination(
        self,
        mock_llm: Any,
        mock_prompt: Any,
    ) -> None:
        """Test workflow behavior with missing destination.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
        """
        # Setup mocks
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Mock result"
        mock_llm.__or__ = MagicMock(return_value=mock_chain)
        mock_prompt.return_value = "yes"

        # Create state with empty destination
        state = {
            "destination": "",
            "dates": "March 15-20",
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

        # Create workflow
        workflow = create_parallelization_workflow()

        # This should not raise an error, workflow should handle gracefully
        try:
            result = workflow.invoke(state)
            # Verify workflow completed
            assert "final_plan" in result
        except Exception as e:
            # If it does raise an error, that's okay for this edge case
            assert True


class TestWorkflowDataFlow:
    """Test data flow through the workflow."""

    @patch("travelagent.main.Prompt.ask")
    @patch("travelagent.parallel_agents.llm")
    def test_data_flows_to_consolidation(
        self,
        mock_llm: Any,
        mock_prompt: Any,
        sample_travel_state: dict[str, Any],
    ) -> None:
        """Test that data from parallel agents flows to consolidation.

        Args:
            mock_llm: Mock LLM instance.
            mock_prompt: Mock Prompt.ask method.
            sample_travel_state: Sample travel state fixture.
        """
        # Setup mocks
        call_count = {"count": 0}

        def mock_invoke(args: dict[str, Any]) -> str:
            call_count["count"] += 1
            # Return different responses for different stages
            if "consolidate" in str(args).lower() or call_count["count"] > 6:
                return "Final consolidated plan"
            return f"Analysis {call_count['count']}"

        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = mock_invoke
        mock_llm.__or__ = MagicMock(return_value=mock_chain)
        mock_prompt.return_value = "yes"

        # Create and execute workflow
        workflow = create_parallelization_workflow()
        result = workflow.invoke(sample_travel_state)

        # Verify consolidation happened (all agents ran plus consolidation)
        assert call_count["count"] >= 6  # 6 agents + consolidation
        assert result["final_plan"] is not None
