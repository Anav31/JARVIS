"""
===============================================================================
File Name   : intent_detector.py
Module      : Agent Brain
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Detects the high-level intent of each interpreted task.

This module performs lightweight rule-based intent detection using normalized
task text. The detected intent is stored as an IntentResult object and attached
to each InterpretedTask.

This module is intentionally designed so that the rule-based implementation can
later be replaced by a machine learning intent classifier without affecting the
rest of the pipeline.

Responsibilities:
    • Read interpreted tasks
    • Detect task intent
    • Create IntentResult objects
    • Attach intent to InterpretedTask
    • Record processing logs

Author      : Team JARVIS
===============================================================================
"""

from agent_engine.agent_brain.models.intent_result import IntentResult
from agent_engine.agent_brain.models.processing_context import ProcessingContext
from agent_engine.contracts.enums import IntentType, ProcessingStage


class IntentDetector:
    """
    Detects the intent of interpreted tasks.
    """

    def detect(
        self,
        context: ProcessingContext
    ) -> ProcessingContext:
        """
        Detect intents for every interpreted task.

        Parameters
        ----------
        context : ProcessingContext
            Current Agent Brain processing context.

        Returns
        -------
        ProcessingContext
            Updated processing context containing detected intents.
        """

        context.current_stage = ProcessingStage.DETECTING_INTENT

        context.log("Intent detection started.")

        for task in context.interpreted_tasks:

            intent_result = self._detect_intent(
                task.normalized_text
            )

            task.intent = intent_result

            context.log(
                f"Intent detected for Task {task.task_id}: "
                f"{intent_result.intent.value}"
            )

        context.log(
            f"Intent detection completed for "
            f"{len(context.interpreted_tasks)} task(s)."
        )

        return context

    # ------------------------------------------------------------------
    # Rule-Based Intent Detection
    # ------------------------------------------------------------------

    def _detect_intent(
        self,
        text: str
    ) -> IntentResult:
        """
        Detect intent using rule-based pattern matching.

        Website detection is performed before generic application opening so
        that tasks such as:

            "open https://example.com"

        are correctly classified as OPEN_WEBSITE rather than
        OPEN_APPLICATION.
        """

        import re

        text = text.lower().strip()

        # ------------------------------------------------------------------
        # Website Detection
        # ------------------------------------------------------------------
        # Detect URLs explicitly.
        # ------------------------------------------------------------------

        url_pattern = r"https?://[^\s]+|www\.[^\s]+"

        contains_url = re.search(
            url_pattern,
            text
        ) is not None

        website_keywords = [
            "visit",
            "browse",
            "go to",
            "open website",
            "open webpage",
            "open web page",
            "open url",
            "open link",
        ]

        if contains_url or any(
            keyword in text
            for keyword in website_keywords
        ):
            return IntentResult(
                intent=IntentType.OPEN_WEBSITE,
                confidence=1.0,
                detection_method="rule_based",
                reasoning=(
                    "Detected website-opening language or URL in task."
                )
            )

        # ------------------------------------------------------------------
        # Web Search
        # ------------------------------------------------------------------

        search_keywords = [
            "search",
            "find",
            "lookup",
            "google",
        ]

        for keyword in search_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.SEARCH_WEB,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent {IntentType.SEARCH_WEB.value}."
                    )
                )

        # ------------------------------------------------------------------
        # File Download
        # ------------------------------------------------------------------

        download_keywords = [
            "download",
            "fetch",
            "grab",
        ]

        for keyword in download_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.DOWNLOAD_FILE,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent {IntentType.DOWNLOAD_FILE.value}."
                    )
                )

        # ------------------------------------------------------------------
        # Document Summarization
        # ------------------------------------------------------------------

        summarize_keywords = [
            "summarize",
            "summary",
        ]

        for keyword in summarize_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.SUMMARIZE_DOCUMENT,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent "
                        f"{IntentType.SUMMARIZE_DOCUMENT.value}."
                    )
                )

        # ------------------------------------------------------------------
        # File Deletion
        # ------------------------------------------------------------------

        delete_keywords = [
            "delete",
            "remove",
            "erase",
        ]

        for keyword in delete_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.DELETE_FILE,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent {IntentType.DELETE_FILE.value}."
                    )
                )

        # ------------------------------------------------------------------
        # File Movement
        # ------------------------------------------------------------------

        move_keywords = [
            "move",
            "transfer",
        ]

        for keyword in move_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.MOVE_FILE,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent {IntentType.MOVE_FILE.value}."
                    )
                )

        # ------------------------------------------------------------------
        # File Copy
        # ------------------------------------------------------------------

        copy_keywords = [
            "copy",
            "duplicate",
        ]

        for keyword in copy_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.COPY_FILE,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent {IntentType.COPY_FILE.value}."
                    )
                )

        # ------------------------------------------------------------------
        # File Rename
        # ------------------------------------------------------------------

        rename_keywords = [
            "rename",
            "change name",
        ]

        for keyword in rename_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.RENAME_FILE,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent {IntentType.RENAME_FILE.value}."
                    )
                )

        # ------------------------------------------------------------------
        # Application Opening
        # ------------------------------------------------------------------

        application_keywords = [
            "open",
            "launch",
            "start",
            "run",
        ]

        for keyword in application_keywords:

            if keyword in text:

                return IntentResult(
                    intent=IntentType.OPEN_APPLICATION,
                    confidence=1.0,
                    detection_method="rule_based",
                    reasoning=(
                        f"Matched keyword '{keyword}' "
                        f"for intent "
                        f"{IntentType.OPEN_APPLICATION.value}."
                    )
                )

        # ------------------------------------------------------------------
        # Unknown Intent
        # ------------------------------------------------------------------

        return IntentResult(
            intent=IntentType.UNKNOWN,
            confidence=0.0,
            detection_method="rule_based",
            reasoning="No matching intent pattern was found."
        )