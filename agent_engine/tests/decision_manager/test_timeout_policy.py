"""
===============================================================================
File Name   : test_timeout_policy.py
Module      : Decision Manager Tests
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Tests Phase F-3 timeout handling and timeout normalization.

Coverage:
    - Explicit timeout detection
    - Execution-time based timeout detection
    - Non-timeout execution
    - Timeout normalization
    - Successful outcome preservation
    - Original outcome immutability

Author : Team Agent
===============================================================================
"""

from agent_engine.contracts.enums import ExecutionStatus
from agent_engine.decision_manager.models.execution_outcome import (
    ExecutionOutcome,
    FailureType,
)
from agent_engine.decision_manager.timeout_policy import TimeoutPolicy


# =============================================================================
# Helpers
# =============================================================================


def build_outcome(
    *,
    task_id: int = 1,
    success: bool = False,
    execution_time: float | None = None,
    timeout_seconds: float | None = None,
    timed_out: bool = False,
    failure_type: FailureType = FailureType.NONE,
) -> ExecutionOutcome:
    """
    Build a test ExecutionOutcome.
    """

    return ExecutionOutcome(
        task_id=task_id,
        status=(
            ExecutionStatus.COMPLETED
            if success
            else ExecutionStatus.FAILED
        ),
        success=success,
        attempt=1,
        retry_count=0,
        max_retries=1,
        execution_time=execution_time,
        timeout_seconds=timeout_seconds,
        timed_out=timed_out,
        failure_type=failure_type,
    )


# =============================================================================
# Timeout Detection
# =============================================================================


def test_explicit_timeout_is_detected():
    """
    Explicit timed_out=True must be detected as a timeout.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timed_out=True,
        timeout_seconds=5.0,
        execution_time=3.0,
    )

    assert policy.is_timeout(outcome) is True


def test_execution_time_exceeding_limit_is_detected():
    """
    Execution time greater than configured timeout must be detected.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timeout_seconds=5.0,
        execution_time=6.0,
    )

    assert policy.is_timeout(outcome) is True


def test_execution_time_equal_to_limit_is_not_timeout():
    """
    Execution time equal to timeout_seconds is not considered a timeout.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timeout_seconds=5.0,
        execution_time=5.0,
    )

    assert policy.is_timeout(outcome) is False


def test_execution_within_timeout_is_not_timeout():
    """
    Execution completing before the timeout must not be classified
    as a timeout.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timeout_seconds=5.0,
        execution_time=3.0,
    )

    assert policy.is_timeout(outcome) is False


# =============================================================================
# Timeout Normalization
# =============================================================================


def test_explicit_timeout_is_normalized():
    """
    Explicit timeout must be normalized to a failed TIMEOUT outcome.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timed_out=True,
        timeout_seconds=5.0,
        execution_time=6.0,
    )

    normalized = policy.normalize(outcome)

    assert normalized.success is False
    assert normalized.status == ExecutionStatus.FAILED
    assert normalized.timed_out is True
    assert normalized.failure_type == FailureType.TIMEOUT


def test_execution_time_timeout_is_normalized():
    """
    Duration-based timeout must be normalized to TIMEOUT.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timeout_seconds=5.0,
        execution_time=7.0,
    )

    normalized = policy.normalize(outcome)

    assert normalized.success is False
    assert normalized.status == ExecutionStatus.FAILED
    assert normalized.timed_out is True
    assert normalized.failure_type == FailureType.TIMEOUT


def test_successful_outcome_is_preserved_when_within_timeout():
    """
    A successful execution within the timeout must remain successful.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        success=True,
        timeout_seconds=5.0,
        execution_time=2.0,
        failure_type=FailureType.NONE,
    )

    normalized = policy.normalize(outcome)

    assert normalized.success is True
    assert normalized.status == ExecutionStatus.COMPLETED
    assert normalized.timed_out is False
    assert normalized.failure_type == FailureType.NONE


# =============================================================================
# Immutability
# =============================================================================


def test_timeout_normalization_does_not_mutate_original():
    """
    Timeout normalization must return a copy and leave the original
    ExecutionOutcome unchanged.
    """

    policy = TimeoutPolicy()

    outcome = build_outcome(
        timeout_seconds=5.0,
        execution_time=8.0,
    )

    normalized = policy.normalize(outcome)

    assert outcome.timed_out is False
    assert outcome.failure_type == FailureType.NONE
    assert outcome.status == ExecutionStatus.FAILED
    assert outcome.success is False

    assert normalized is not outcome
    assert normalized.timed_out is True
    assert normalized.failure_type == FailureType.TIMEOUT