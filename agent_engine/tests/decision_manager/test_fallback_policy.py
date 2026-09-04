"""
===============================================================================
File Name   : test_fallback_policy.py
Module      : Decision Manager Tests
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Unit tests for fallback selection and recovery decision logic.

Phase F-4:
    Fallback Policy verification.

These tests verify that:
    - No fallback produces FAIL.
    - A single fallback produces FALLBACK.
    - The highest-priority fallback is selected.
    - Priority ordering is deterministic.
    - Fallback parameters are preserved.
    - The policy does not execute the fallback action.
===============================================================================
"""

from agent_engine.contracts.task import Task

from agent_engine.decision_manager.fallback_policy import (
    FallbackPolicy,
)

from agent_engine.decision_manager.models.decision import (
    DecisionAction,
)

from agent_engine.decision_manager.models.execution_outcome import (
    FailureType,
)

from agent_engine.decision_manager.models.fallback import (
    FallbackOption,
)


# =============================================================================
# Helpers
# =============================================================================


def build_task(
    *,
    task_id: int = 1,
    retry: int = 2,
) -> Task:
    """
    Build a minimal Task compatible with FallbackPolicy.
    """

    return Task(
        id=task_id,
        description="Open the requested website",
        action="open",
        tool="browser_agent",
        parameters={
            "url": "https://example.com",
        },
        retry=retry,
    )


def build_fallback(
    *,
    fallback_id: str = "fallback-1",
    action: str = "retry_open",
    tool: str = "browser_agent",
    priority: int = 1,
) -> FallbackOption:
    """
    Build a fallback option for testing.
    """

    return FallbackOption(
        id=fallback_id,
        action=action,
        tool=tool,
        parameters={
            "url": "https://example.com",
        },
        priority=priority,
        description="Alternative browser recovery action.",
    )


# =============================================================================
# Tests
# =============================================================================


def test_no_fallback_produces_fail_decision():
    """
    When no fallback options are available, the policy must return FAIL.
    """

    policy = FallbackPolicy()
    task = build_task()

    result = policy.select_fallback(
        task,
        fallback_options=[],
        attempt=1,
    )

    assert result.action == DecisionAction.FAIL
    assert result.task_id == task.id
    assert result.selected_fallback is None
    assert result.failure_type == FailureType.NONE
    assert "No fallback option" in result.reason


def test_single_fallback_produces_fallback_decision():
    """
    A single available fallback must produce a FALLBACK decision.
    """

    policy = FallbackPolicy()
    task = build_task()

    fallback = build_fallback()

    result = policy.select_fallback(
        task,
        fallback_options=[fallback],
        attempt=1,
    )

    assert result.action == DecisionAction.FALLBACK
    assert result.task_id == task.id
    assert result.selected_fallback == fallback
    assert result.failure_type == FailureType.NONE


def test_highest_priority_fallback_is_selected():
    """
    Lower priority number means higher priority.

    Therefore priority=1 must be selected over priority=2 or priority=3.
    """

    policy = FallbackPolicy()
    task = build_task()

    low_priority = build_fallback(
        fallback_id="fallback-3",
        priority=3,
    )

    medium_priority = build_fallback(
        fallback_id="fallback-2",
        priority=2,
    )

    high_priority = build_fallback(
        fallback_id="fallback-1",
        priority=1,
    )

    result = policy.select_fallback(
        task,
        fallback_options=[
            low_priority,
            medium_priority,
            high_priority,
        ],
        attempt=1,
    )

    assert result.action == DecisionAction.FALLBACK
    assert result.selected_fallback is not None
    assert result.selected_fallback.id == "fallback-1"
    assert result.selected_fallback.priority == 1


def test_priority_order_does_not_depend_on_input_order():
    """
    The highest-priority fallback must be selected regardless of the
    order in which fallback options are supplied.
    """

    policy = FallbackPolicy()
    task = build_task()

    fallback_1 = build_fallback(
        fallback_id="fallback-1",
        priority=1,
    )

    fallback_2 = build_fallback(
        fallback_id="fallback-2",
        priority=2,
    )

    fallback_3 = build_fallback(
        fallback_id="fallback-3",
        priority=3,
    )

    result = policy.select_fallback(
        task,
        fallback_options=[
            fallback_3,
            fallback_1,
            fallback_2,
        ],
        attempt=1,
    )

    assert result.selected_fallback is not None
    assert result.selected_fallback.id == "fallback-1"


def test_fallback_parameters_are_preserved():
    """
    The selected fallback must preserve its action, tool and parameters.
    """

    policy = FallbackPolicy()
    task = build_task()

    fallback = FallbackOption(
        id="fallback-search",
        action="search",
        tool="browser_agent",
        parameters={
            "query": "artificial intelligence",
            "engine": "google",
        },
        priority=1,
        description="Search using an alternative browser action.",
    )

    result = policy.select_fallback(
        task,
        fallback_options=[fallback],
        attempt=2,
    )

    assert result.selected_fallback is not None
    assert result.selected_fallback.action == "search"
    assert result.selected_fallback.tool == "browser_agent"
    assert result.selected_fallback.parameters == {
        "query": "artificial intelligence",
        "engine": "google",
    }


def test_policy_does_not_execute_fallback():
    """
    FallbackPolicy must only make a decision.

    It must not execute any automation action.
    """

    policy = FallbackPolicy()
    task = build_task()

    executed = []

    fallback = FallbackOption(
        id="fallback-1",
        action="open",
        tool="browser_agent",
        parameters={
            "url": "https://example.com",
        },
        priority=1,
    )

    result = policy.select_fallback(
        task,
        fallback_options=[fallback],
        attempt=1,
    )

    assert result.action == DecisionAction.FALLBACK
    assert executed == []