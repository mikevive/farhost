"""Reusable modal screens for CRUD operations."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Static


class InputModal(ModalScreen[str | None]):
    """Modal with a single text input. Returns the input value or None on cancel."""

    DEFAULT_CSS = """
    InputModal {
        align: center middle;
    }
    InputModal > Vertical {
        width: 50;
        height: auto;
        max-height: 12;
        background: #2C2C2E;
        border: solid #48484A;
        padding: 1 2;
    }
    InputModal Label {
        width: 100%;
        margin-bottom: 1;
        color: #FFFFFF;
    }
    InputModal Input {
        width: 100%;
        margin-bottom: 1;
    }
    InputModal Horizontal {
        width: 100%;
        align: center middle;
        height: 3;
    }
    InputModal Button {
        margin: 0 1;
    }
    InputModal #btn-save {
        background: #E8735A;
    }
    """

    def __init__(self, title: str, placeholder: str = "", value: str = "") -> None:
        super().__init__()
        self._title = title
        self._placeholder = placeholder
        self._initial_value = value

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self._title)
            yield Input(
                value=self._initial_value,
                placeholder=self._placeholder,
                id="modal-input",
            )
            with Horizontal():
                yield Button("Save", variant="primary", id="btn-save")
                yield Button("Cancel", id="btn-cancel")

    def on_mount(self) -> None:
        self.query_one("#modal-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-save":
            value = self.query_one("#modal-input", Input).value.strip()
            if value:
                self.dismiss(value)
        else:
            self.dismiss(None)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        value = event.value.strip()
        if value:
            self.dismiss(value)


class ConfirmModal(ModalScreen[bool]):
    """Modal for confirmation (archive, delete, restore). Returns True or False."""

    DEFAULT_CSS = """
    ConfirmModal {
        align: center middle;
    }
    ConfirmModal > Vertical {
        width: 50;
        height: auto;
        max-height: 12;
        background: #44475a;
        border: solid #6272a4;
        padding: 1 2;
    }
    ConfirmModal Static {
        width: 100%;
        margin-bottom: 1;
        color: #f8f8f2;
    }
    ConfirmModal Horizontal {
        width: 100%;
        align: center middle;
        height: 3;
    }
    ConfirmModal Button {
        margin: 0 1;
    }
    ConfirmModal #btn-confirm {
        background: #bd93f9;
    }
    ConfirmModal #btn-confirm.danger {
        background: #ff5555;
    }
    """

    def __init__(
        self, message: str, confirm_label: str = "Confirm", danger: bool = False
    ) -> None:
        super().__init__()
        self._message = message
        self._confirm_label = confirm_label
        self._danger = danger

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static(self._message)
            with Horizontal():
                btn = Button(self._confirm_label, variant="primary", id="btn-confirm")
                if self._danger:
                    btn.add_class("danger")
                yield btn
                yield Button("Cancel", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirm")
