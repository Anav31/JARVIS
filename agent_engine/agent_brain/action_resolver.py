"""
===============================================================================
File Name   : action_resolver.py
Module      : Agent Brain
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Resolves executable actions from detected task intents.

This module converts high-level intents into canonical actions using the
Action Registry.

Pipeline position:

    InterpretedTask
          ↓
    IntentDetector
          ↓
    ActionResolver
          ↓
    ParameterResolver
          ↓
    ToolResolver

The implementation is intentionally rule-based so it can later be replaced
by a machine-learning action prediction model without changing the rest of
the Agent Brain pipeline.

Responsibilities:
    • Read detected intents
    • Resolve canonical actions
    • Attach actions to interpreted tasks
    • Record processing logs

Author      : Team JARVIS
===============================================================================
"""

from __future__ import annotations

from agent_engine.agent_brain.models.processing_context import ProcessingContext
from agent_engine.contracts.enums import (
    IntentType,
    ProcessingStage,
)
from agent_engine.registry.action_registry import ActionRegistry


class ActionResolver:
    """
    Resolves canonical executable actions from detected intents.
    """

    # -------------------------------------------------------------------------
    # Intent → Canonical Action Mapping
    # -------------------------------------------------------------------------

    _INTENT_ACTION_MAP: dict[IntentType, str] = {

        IntentType.OPEN_APPLICATION: "open",

        IntentType.OPEN_WEBSITE: "open",

        IntentType.SEARCH_WEB: "search",

        IntentType.DOWNLOAD_FILE: "download",

        IntentType.SUMMARIZE_DOCUMENT: "summarize",

        IntentType.DELETE_FILE: "delete",

        IntentType.MOVE_FILE: "move",

        IntentType.COPY_FILE: "copy",

        IntentType.RENAME_FILE: "rename",
    }

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def resolve(
        self,
        context: ProcessingContext,
    ) -> ProcessingContext:
        """
        Resolve canonical actions for all interpreted tasks.

        The resolver expects intent detection to have already taken place.

        Parameters
        ----------
        context : ProcessingContext
            Current Agent Brain processing context.

        Returns
        -------
        ProcessingContext
            Updated context containing resolved actions.
        """

        context.current_stage = ProcessingStage.RESOLVING_ACTIONS

        context.log("Action resolution started.")

        resolved_count = 0
        unresolved_count = 0

        for task in context.interpreted_tasks:

            # -----------------------------------------------------------------
            # Validate intent availability
            # -----------------------------------------------------------------

            if task.intent is None:

                task.action = None

                unresolved_count += 1

                context.log(
                    f"Action resolution skipped for Task "
                    f"{task.task_id}: intent is missing."
                )

                continue

            # -----------------------------------------------------------------
            # Resolve action from intent
            # -----------------------------------------------------------------

            action = self._resolve_action(
                task.intent.intent
            )

            task.action = action

            if action is not None:

                resolved_count += 1

                context.log(
                    f"Action resolved for Task "
                    f"{task.task_id}: {action}"
                )

            else:

                unresolved_count += 1

                context.log(
                    f"Action resolution failed for Task "
                    f"{task.task_id}: unsupported intent "
                    f"{task.intent.intent}"
                )

        context.log(
            f"Action resolution completed. "
            f"Resolved: {resolved_count}, "
            f"Unresolved: {unresolved_count}"
        )

        return context

    # -------------------------------------------------------------------------
    # Internal Resolution
    # -------------------------------------------------------------------------

    @classmethod
    def _resolve_action(
        cls,
        intent: IntentType,
    ) -> str | None:
        """
        Resolve a canonical action from an IntentType.

        Returns
        -------
        str | None
            Canonical action registered in ActionRegistry, or None when
            the intent cannot be mapped to an executable action.
        """

        action = cls._INTENT_ACTION_MAP.get(intent)

        if action is None:
            return None

        # ---------------------------------------------------------------------
        # Ensure action belongs to the canonical Action Registry.
        # ---------------------------------------------------------------------

        if not ActionRegistry.contains(action):
            return None

        return ActionRegistry.normalize(action)