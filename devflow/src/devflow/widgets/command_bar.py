"""Footer command bar with vim-style command input."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Static
from textual.widget import Widget

COMMANDS = {
    "timer": "timer",
    "t": "timer",
    "daily": "daily",
    "d": "daily",
    "weekly": "weekly",
    "w": "weekly",
    "projects": "projects",
    "p": "projects",
    "categories": "categories",
    "c": "categories",
    "quit": "quit",
    "q": "quit",
}


class CommandBar(Widget):
    """Footer widget with navigation hints and a command input."""

    DEFAULT_CSS = """
    CommandBar {
        height: 3;
        dock: bottom;
        background: #1C1C1E;
    }
    CommandBar Horizontal {
        height: 1;
        width: 100%;
    }
    CommandBar #nav-hints {
        width: 100%;
        color: #A1A1A6;
        padding: 0 1;
    }
    CommandBar #command-input {
        display: none;
        width: 100%;
    }
    CommandBar #command-input.visible {
        display: block;
    }
    """

    def __init__(self, active_screen: str = "timer") -> None:
        super().__init__()
        self._active_screen = active_screen

    def compose(self) -> ComposeResult:
        hints = self._build_hints()
        yield Static(hints, id="nav-hints")
        yield Input(placeholder=":", id="command-input")

    def _build_hints(self) -> str:
        screens = [
            ("Timer", ":t", "timer"),
            ("Daily", ":d", "daily"),
            ("Weekly", ":w", "weekly"),
            ("Projects", ":p", "projects"),
            ("Categories", ":c", "categories"),
            ("Quit", ":q", "quit"),
        ]
        parts = []
        for label, shortcut, key in screens:
            if key == self._active_screen:
                parts.append(f"[bold #E8735A]{shortcut}[/]")
            else:
                parts.append(f"{label} ({shortcut})")
        return " | ".join(parts)

    def activate_input(self) -> None:
        """Show the command input and focus it."""
        inp = self.query_one("#command-input", Input)
        inp.add_class("visible")
        inp.value = ""
        inp.focus()

    def deactivate_input(self) -> None:
        """Hide the command input."""
        inp = self.query_one("#command-input", Input)
        inp.remove_class("visible")
        inp.value = ""

    def set_active_screen(self, screen_name: str) -> None:
        self._active_screen = screen_name
        self.query_one("#nav-hints", Static).update(self._build_hints())
