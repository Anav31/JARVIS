"""
Tests for the concrete Automation Engine Action Dispatcher.
"""

from agent_engine.agent_brain.models.interpreted_task import InterpretedTask
from agent_engine.automation.dispatcher.action_dispatcher import (
    AutomationActionDispatcher,
)
from agent_engine.automation.integration.action_request_builder import (
    ActionRequestBuilder,
)
from agent_engine.automation.registry.action_registry import ActionRegistry
from agent_engine.contracts.enums import ExecutionStatus
from agent_engine.decision_manager.models.execution_outcome import FailureType


def create_task(
    *,
    task_id: int = 1,
    action: str = "open_url",
    tool: str = "browser_agent",
    parameters: dict | None = None,
) -> InterpretedTask:

    return InterpretedTask(
        task_id=task_id,
        original_text="Open example website",
        normalized_text="open example website",
        action=action,
        tool=tool,
        parameters=parameters or {},
    )


def test_successful_action_dispatch():
    registry = ActionRegistry()

    registry.register(
        "open_url",
        lambda **kwargs: "SUCCESS",
    )

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task(
        parameters={"url": "https://example.com"}
    )

    result = dispatcher.dispatch(
        task,
        attempt=1,
    )

    assert result.task_id == 1
    assert result.status == ExecutionStatus.COMPLETED
    assert result.success is True
    assert result.attempt == 1
    assert result.failure_type == FailureType.NONE
    assert result.execution_time is not None
    assert result.execution_time >= 0


def test_handler_receives_parameters():
    registry = ActionRegistry()

    received = {}

    def handler(**kwargs):
        received.update(kwargs)
        return "SUCCESS"

    registry.register("open_url", handler)

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task(
        parameters={
            "url": "https://example.com"
        }
    )

    dispatcher.dispatch(
        task,
        attempt=1,
    )

    assert received == {
        "url": "https://example.com"
    }


def test_unknown_action_returns_failed_outcome():
    registry = ActionRegistry()

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task(
        action="unknown_action"
    )

    result = dispatcher.dispatch(
        task,
        attempt=1,
    )

    assert result.task_id == 1
    assert result.status == ExecutionStatus.FAILED
    assert result.success is False
    assert result.failure_type == FailureType.UNKNOWN
    assert result.error_message is not None


def test_handler_exception_returns_failed_outcome():
    registry = ActionRegistry()

    def failing_handler(**kwargs):
        raise RuntimeError("Automation failed")

    registry.register(
        "open_url",
        failing_handler,
    )

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task()

    result = dispatcher.dispatch(
        task,
        attempt=1,
    )

    assert result.status == ExecutionStatus.FAILED
    assert result.success is False
    assert result.failure_type == FailureType.UNKNOWN
    assert result.error_message == "Automation failed"


def test_attempt_number_is_preserved():
    registry = ActionRegistry()

    registry.register(
        "open_url",
        lambda **kwargs: "SUCCESS",
    )

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task()

    result = dispatcher.dispatch(
        task,
        attempt=3,
    )

    assert result.attempt == 3
    assert result.retry_count == 2


def test_timeout_is_preserved():
    registry = ActionRegistry()

    registry.register(
        "open_url",
        lambda **kwargs: "SUCCESS",
    )

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task()

    result = dispatcher.dispatch(
        task,
        attempt=1,
        timeout_seconds=30,
    )

    assert result.timeout_seconds == 30
    assert result.timed_out is False


def test_missing_action_fails():
    registry = ActionRegistry()

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task(
        action=None
    )

    result = dispatcher.dispatch(
        task,
        attempt=1,
    )

    assert result.status == ExecutionStatus.FAILED
    assert result.success is False
    assert result.failure_type == FailureType.VALIDATION


def test_missing_tool_fails():
    registry = ActionRegistry()

    dispatcher = AutomationActionDispatcher(registry)

    task = create_task(
        tool=None
    )

    result = dispatcher.dispatch(
        task,
        attempt=1,
    )

    assert result.status == ExecutionStatus.FAILED
    assert result.success is False
    assert result.failure_type == FailureType.VALIDATION

# =============================================================================
# M5-E.2 Integration Tests
# =============================================================================

def test_dispatcher_uses_action_request_builder():
    """
    Dispatcher should use ActionRequestBuilder to construct the request.
    """

    class SpyBuilder(ActionRequestBuilder):
        def __init__(self):
            self.called = False

        def build(self, task, *, timeout_seconds=None):
            self.called = True
            return super().build(
                task,
                timeout_seconds=timeout_seconds,
            )

    registry = ActionRegistry()

    def open_url(**kwargs):
        return "SUCCESS"

    registry.register("open_url", open_url)

    builder = SpyBuilder()

    dispatcher = AutomationActionDispatcher(
        registry,
        request_builder=builder,
    )

    task = InterpretedTask(
        task_id=1,
        original_text="Open example website",
        normalized_text="open example website",
        action="open_url",
        tool="browser_agent",
        parameters={
            "url": "https://example.com",
        },
    )

    result = dispatcher.dispatch(
        task,
        attempt=1,
        timeout_seconds=30,
    )

    assert builder.called is True
    assert result.success is True
    assert result.status == ExecutionStatus.COMPLETED

def test_dispatcher_passes_timeout_to_action_request_builder():
    """
    Dispatcher should forward timeout configuration to the builder.
    """

    class SpyBuilder(ActionRequestBuilder):
        def __init__(self):
            self.received_timeout = None

        def build(self, task, *, timeout_seconds=None):
            self.received_timeout = timeout_seconds
            return super().build(
                task,
                timeout_seconds=timeout_seconds,
            )

    registry = ActionRegistry()

    def open_url(**kwargs):
        return "SUCCESS"

    registry.register("open_url", open_url)

    builder = SpyBuilder()

    dispatcher = AutomationActionDispatcher(
        registry,
        request_builder=builder,
    )

    task = InterpretedTask(
        task_id=1,
        original_text="Open example website",
        normalized_text="open example website",
        action="open_url",
        tool="browser_agent",
        parameters={
            "url": "https://example.com",
        },
    )

    dispatcher.dispatch(
        task,
        attempt=1,
        timeout_seconds=45,
    )

    assert builder.received_timeout == 45