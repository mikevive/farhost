"""DevFlow TUI Application: screen routing and command mode."""

from __future__ import annotations

import sqlite3
from typing import cast

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Input

from devflow.db.connection import get_connection
from devflow.timer.engine import recover_crashed_session
from devflow.widgets.command_bar import COMMANDS, CommandBar


class DevFlowApp(App):
    """The main DevFlow application."""

    CSS = """
    Screen {
        background: #282a36;
    }

    #main-content {
        height: 1fr;
        width: 1fr;
    }
    """

    BINDINGS = [
        Binding("colon", "command_mode", "Command mode", show=False),
        Binding("escape", "escape", "Cancel", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.db: sqlite3.Connection | None = None
        self._command_bar: CommandBar | None = None

    def compose(self) -> ComposeResult:
        yield Container(id="main-content")
        yield CommandBar(active_screen="timer")

    def on_mount(self) -> None:
        self.db = get_connection()
        recover_crashed_session(self.db)
        self._command_bar = self.query_one(CommandBar)
        self.call_later(self._navigate_to, "timer")

    def action_command_mode(self) -> None:
        if self._command_bar:
            self._command_bar.activate_input()

    def action_escape(self) -> None:
        if self._command_bar:
            self._command_bar.deactivate_input()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id != "command-input":
            return

        command = event.value.strip().lower()
        if self._command_bar:
            self._command_bar.deactivate_input()

        screen_name = COMMANDS.get(command)
        if screen_name:
            if screen_name == "quit":
                self.exit()
            else:
                self._navigate_to(screen_name)

    def _navigate_to(self, screen_name: str, **kwargs) -> None:
        from devflow.screens.categories import CategoriesScreen
        from devflow.screens.daily import DailyReportScreen
        from devflow.screens.projects import ProjectsScreen
        from devflow.screens.tasks import TasksScreen
        from devflow.screens.timer import TimerScreen
        from devflow.screens.weekly import WeeklyReportScreen

        screen_map: dict[str, type[Widget]] = {
            "timer": TimerScreen,
            "daily": DailyReportScreen,
            "weekly": WeeklyReportScreen,
            "projects": ProjectsScreen,
            "categories": CategoriesScreen,
            "tasks": TasksScreen,
        }

        screen_class = screen_map.get(screen_name)
        if screen_class is None:
            return

        # Mount the new screen in the main content area
        content_area = self.query_one("#main-content")
        for child in content_area.children:
            child.remove()
        content_area.mount(screen_class(**kwargs))

        # Don't change the footer's active command for the tasks screen
        if self._command_bar and screen_name != "tasks":
            self._command_bar.set_active_screen(screen_name)
