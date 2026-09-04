"""
===============================================================================
File Name   : tool_resolver.py
Module      : Agent Brain
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Resolves the appropriate automation tool/controller required to execute each
interpreted task.

The Tool Resolver examines the resolved action and extracted parameters and
maps them to the most suitable automation controller. This keeps downstream
components independent from natural language and allows the Dispatcher to
invoke the correct controller.

Current implementation is rule-based and intentionally modular so it can be
replaced with an ML-based routing model in the future.

Responsibilities:
    • Resolve execution tool
    • Assign controller to each task
    • Update processing stage
    • Record processing logs

Author      : Team JARVIS
===============================================================================
"""

from agent_engine.agent_brain.models.processing_context import ProcessingContext
from agent_engine.contracts.enums import ProcessingStage, ToolType


class ToolResolver:
    """
    Resolves the automation tool required for each interpreted task.
    """

    def resolve(
        self,
        context: ProcessingContext
    ) -> ProcessingContext:
        """
        Resolve execution tool for every interpreted task.

        Parameters
        ----------
        context : ProcessingContext

        Returns
        -------
        ProcessingContext
        """

        context.current_stage = ProcessingStage.TOOL_RESOLUTION

        context.log("Tool resolution started.")

        for task in context.interpreted_tasks:

            task.tool = self._resolve_tool(
                task.action,
                task.parameters
            )

            context.log(
                f"Tool resolved for Task {task.task_id}: "
                f"{task.tool}"
            )

        context.log(
            f"Tool resolution completed for "
            f"{len(context.interpreted_tasks)} task(s)."
        )

        return context

    # ------------------------------------------------------------------
    # Tool Resolution
    # ------------------------------------------------------------------

    def _resolve_tool(
        self,
        action: str | None,
        parameters: dict
    ) -> str | None:
        """
        Resolves the automation tool based on action and parameters.
        """

        if action is None:
            return None

        # --------------------------------------------------------------
        # Browser Automation
        # --------------------------------------------------------------

        if action in {

            "search",
            "download"

        }:
            return ToolType.BROWSER.value

        # --------------------------------------------------------------
        # Desktop Automation
        # --------------------------------------------------------------

        if action == "open":

            if (
                "browser" in parameters
                or
                "application" in parameters
            ):

                return ToolType.DESKTOP.value

            if "website" in parameters:

                return ToolType.BROWSER.value

        # --------------------------------------------------------------
        # Filesystem Automation
        # --------------------------------------------------------------

        if action in {

            "delete",
            "move",
            "copy",
            "rename"

        }:

            return ToolType.FILESYSTEM.value

        # --------------------------------------------------------------
        # Summarization
        # --------------------------------------------------------------

        if action == "summarize":

            return ToolType.FILESYSTEM.value

        return None