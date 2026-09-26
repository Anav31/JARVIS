"""Application lifecycle controller for M5-K."""

from __future__ import annotations

from agent_engine.registry.application_registry import ApplicationRegistry

from .desktop_backend import DesktopBackend


class ApplicationController:
    """Owns application lifecycle operations, not workflow decisions."""

    def __init__(self, backend: DesktopBackend) -> None:
        self._backend = backend

    def _normalize(self, application: str) -> str:
        if not isinstance(application, str) or not application.strip():
            raise ValueError("application must be a non-empty string")
        return ApplicationRegistry.normalize(application)

    def launch(self, application: str):
        return self._backend.launch_application(self._normalize(application))

    def close(self, application: str):
        return self._backend.close_application(self._normalize(application))

    def restart(self, application: str):
        return self._backend.restart_application(self._normalize(application))

    def terminate(self, application: str):
        return self._backend.terminate_application(self._normalize(application))
