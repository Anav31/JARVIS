"""
===============================================================================
File Name   : action_registry.py
Module      : Registry
Project     : JARVIS - Agent Decision Engine & Automation Engine

Description:
-------------
Maintains the canonical action vocabulary used by the Agent Brain.

This registry normalizes different action verbs into a single standardized
action that can later be mapped to executable automation steps.

Author : Team JARVIS
===============================================================================
"""

from typing import Dict


class ActionRegistry:
    """
    Registry for action normalization.
    """

    _ACTION_MAP: Dict[str, str] = {

        # ------------------------------------------------------------------
        # Open
        # ------------------------------------------------------------------

        "launch": "open",
        "start": "open",
        "run": "open",
        "execute": "open",
        "open": "open",

        # ------------------------------------------------------------------
        # Search
        # ------------------------------------------------------------------

        "search": "search",
        "find": "search",
        "lookup": "search",
        "google": "search",

        # ------------------------------------------------------------------
        # Download
        # ------------------------------------------------------------------

        "download": "download",
        "fetch": "download",
        "grab": "download",
        "save": "download",

        # ------------------------------------------------------------------
        # Delete
        # ------------------------------------------------------------------

        "delete": "delete",
        "remove": "delete",
        "erase": "delete",

        # ------------------------------------------------------------------
        # Move
        # ------------------------------------------------------------------

        "move": "move",
        "transfer": "move",
        "relocate": "move",

        # ------------------------------------------------------------------
        # Copy
        # ------------------------------------------------------------------

        "copy": "copy",
        "duplicate": "copy",

        # ------------------------------------------------------------------
        # Rename
        # ------------------------------------------------------------------

        "rename": "rename",
        "change name": "rename",

        # ------------------------------------------------------------------
        # Close
        # ------------------------------------------------------------------

        "close": "close",
        "exit": "close",
        "quit": "close",

        # ------------------------------------------------------------------
        # Summarize
        # ------------------------------------------------------------------

        "summarize": "summarize",
        "summary": "summarize"
    }

    @classmethod
    def normalize(cls, word: str) -> str:
        """
        Returns the canonical action.
        """

        return cls._ACTION_MAP.get(word.lower(), word.lower())

    @classmethod
    def contains(cls, word: str) -> bool:
        """
        Checks whether an action exists.
        """

        return word.lower() in cls._ACTION_MAP

    @classmethod
    def all_actions(cls) -> Dict[str, str]:
        """
        Returns the complete action registry.
        """

        return cls._ACTION_MAP.copy()