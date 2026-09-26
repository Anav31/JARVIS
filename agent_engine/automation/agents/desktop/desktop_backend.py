"""Windows-native backend interface for M5-K."""

from __future__ import annotations

import os
import subprocess
from abc import ABC, abstractmethod
from typing import Any


class DesktopBackend(ABC):
    """Backend contract used by application/window controllers."""

    @abstractmethod
    def launch_application(self, application: str) -> Any: ...

    @abstractmethod
    def close_application(self, application: str) -> Any: ...

    @abstractmethod
    def restart_application(self, application: str) -> Any: ...

    @abstractmethod
    def terminate_application(self, application: str) -> Any: ...

    @abstractmethod
    def focus_window(self, application: str) -> Any: ...

    @abstractmethod
    def switch_window(self, target: str) -> Any: ...

    @abstractmethod
    def resize_window(self, application: str, width: int, height: int) -> Any: ...

    @abstractmethod
    def position_window(self, application: str, x: int, y: int) -> Any: ...


class WindowsDesktopBackend(DesktopBackend):
    """Minimal Windows backend. OS-specific behavior stays out of the agent."""

    _COMMANDS = {
        "vscode": "code",
        "word": "winword",
        "excel": "excel",
        "powerpoint": "powerpnt",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "explorer": "explorer.exe",
        "cmd": "cmd.exe",
        "powershell": "powershell.exe",
    }

    def _command_for(self, application: str) -> str:
        command = self._COMMANDS.get(application.lower().strip())
        if command is None:
            raise ValueError(f"Unsupported registered application: {application}")
        return command

    def launch_application(self, application: str) -> Any:
        command = self._command_for(application)
        return subprocess.Popen([command])

    def close_application(self, application: str) -> Any:
        raise NotImplementedError("Window-aware graceful close is implemented in WindowController.")

    def restart_application(self, application: str) -> Any:
        raise NotImplementedError("Restart is composed by ApplicationController.")

    def terminate_application(self, application: str) -> Any:
        command = self._command_for(application)
        image = os.path.basename(command)
        return subprocess.run(
            ["taskkill", "/IM", image, "/T"],
            capture_output=True,
            text=True,
            check=False,
        )

    def focus_window(self, application: str) -> Any:
        raise NotImplementedError("Window operations are implemented in WindowController.")

    def switch_window(self, target: str) -> Any:
        raise NotImplementedError("Window operations are implemented in WindowController.")

    def resize_window(self, application: str, width: int, height: int) -> Any:
        raise NotImplementedError("Window operations are implemented in WindowController.")

    def position_window(self, application: str, x: int, y: int) -> Any:
        raise NotImplementedError("Window operations are implemented in WindowController.")
