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
        height: 1;
        dock: bottom;
        background: #282a36;
    }
    CommandBar #nav-hints {
        width: 100%;
        color: #6272a4;
        padding: 0 1;
    }
    CommandBar #nav-hints.hidden {
        display: none;
    }
    CommandBar #input-container {
        display: none;
        width: 100%;
        height: 1;
        padding: 0 1;
    }
    CommandBar #input-container.visible {
        display: block;
    }
    CommandBar #input-prefix {
        width: auto;
        color: #bd93f9;
        text-style: bold;
    }
    CommandBar #command-input {
        width: 1fr;
        height: 1;
        background: transparent;
        border: none;
        padding: 0;
        color: #f8f8f2;
    }
    CommandBar #command-input:focus {
        border: none;
    }
    """

    def __init__(self, active_screen: str = "timer") -> None:
        super().__init__()
        self._active_screen = active_screen

    def compose(self) -> ComposeResult:
        hints = self._build_hints()
        yield Static(hints, id="nav-hints")
        with Horizontal(id="input-container"):
            yield Static(":", id="input-prefix")
            yield Input(id="command-input")

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
                parts.append(f"[bold #bd93f9]{shortcut}[/]")
            else:
                parts.append(f"{label} ({shortcut})")
        return " | ".join(parts)

    def activate_input(self) -> None:
        """Show the command input container and focus it, hiding hints."""
        hints = self.query_one("#nav-hints", Static)
        container = self.query_one("#input-container", Horizontal)
        inp = self.query_one("#command-input", Input)
        
        hints.add_class("hidden")
        container.add_class("visible")
        inp.value = ""
        inp.focus()

    def deactivate_input(self) -> None:
        """Hide the command input container and show hints."""
        hints = self.query_one("#nav-hints", Static)
        container = self.query_one("#input-container", Horizontal)
        inp = self.query_one("#command-input", Input)
        
        container.remove_class("visible")
        hints.remove_class("hidden")
        inp.value = ""

    def set_active_screen(self, screen_name: str) -> None:
        self._active_screen = screen_name
        self.query_one("#nav-hints", Static).update(self._build_hints())
