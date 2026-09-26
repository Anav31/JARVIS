"""Window-management controller for M5-K."""

from __future__ import annotations

from agent_engine.registry.application_registry import ApplicationRegistry

from .desktop_backend import DesktopBackend


class WindowController:
    """Owns activation, switching, sizing and positioning of windows."""

    def __init__(self, backend: DesktopBackend) -> None:
        self._backend = backend

    @staticmethod
    def _application(application: str) -> str:
        if not isinstance(application, str) or not application.strip():
            raise ValueError("application must be a non-empty string")
        return ApplicationRegistry.normalize(application)

    def focus(self, application: str):
        return self._backend.focus_window(self._application(application))

    def switch(self, target: str):
        if not isinstance(target, str) or not target.strip():
            raise ValueError("target must be a non-empty string")
        return self._backend.switch_window(target.strip())

    def resize(self, application: str, width: int, height: int):
        app = self._application(application)
        if isinstance(width, bool) or not isinstance(width, int) or width <= 0:
            raise ValueError("width must be a positive integer")
        if isinstance(height, bool) or not isinstance(height, int) or height <= 0:
            raise ValueError("height must be a positive integer")
        return self._backend.resize_window(app, width, height)

    def position(self, application: str, x: int, y: int):
        app = self._application(application)
        if isinstance(x, bool) or not isinstance(x, int):
            raise ValueError("x must be an integer")
        if isinstance(y, bool) or not isinstance(y, int):
            raise ValueError("y must be an integer")
        return self._backend.position_window(app, x, y)
