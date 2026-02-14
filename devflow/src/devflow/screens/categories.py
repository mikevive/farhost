"""Categories management screen with archive toggle."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import DataTable, Static

from devflow.db import queries
from devflow.widgets.modal import ConfirmModal, InputModal


class CategoriesScreen(Container):
    """Manage categories: list, add, edit, archive, restore."""

    can_focus = True

    DEFAULT_CSS = """
    CategoriesScreen {
        background: #282a36;
        padding: 1 2;
    }
    #title {
        text-style: bold;
        color: #f8f8f2;
        width: 100%;
        margin-bottom: 1;
    }
    DataTable {
        height: 1fr;
        background: #44475a;
        border: solid #6272a4;
    }
    #hints {
        color: #6272a4;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("a", "add", "Add", show=False),
        Binding("e", "edit", "Edit", show=False),
        Binding("d", "archive", "Archive", show=False),
        Binding("A", "toggle_archive", "Archive view", show=False),
        Binding("r", "restore", "Restore", show=False),
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._show_archived = False

    def compose(self) -> ComposeResult:
        yield Static("DevFlow - Categories", id="title")
        yield DataTable(id="categories-table")
        yield Static("(a)dd, (e)dit, (d) archive, (A) view archive", id="hints")

    def on_mount(self) -> None:
        table = self.query_one("#categories-table", DataTable)
        table.add_column("Name", key="name")
        table.cursor_type = "row"
        self._refresh_table()
        table.focus()

    def action_cursor_down(self) -> None:
        self.query_one("#categories-table", DataTable).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one("#categories-table", DataTable).action_cursor_up()

    def _refresh_table(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        table = self.query_one("#categories-table", DataTable)
        table.clear()

        title = self.query_one("#title", Static)
        hints = self.query_one("#hints", Static)

        if self._show_archived:
            title.update("DevFlow - Categories [Archive]")
            hints.update("(r) restore, (A) back to active")
            categories = queries.list_categories(conn, include_archived=True)
        else:
            title.update("DevFlow - Categories")
            hints.update("(a)dd, (e)dit, (d) archive, (A) view archive")
            categories = queries.list_categories(conn)

        for c in categories:
            table.add_row(c.name, key=str(c.id))

    def _get_selected_id(self) -> int | None:
        table = self.query_one("#categories-table", DataTable)
        if table.row_count == 0:
            return None
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        return int(row_key.value)

    def action_add(self) -> None:
        if self._show_archived:
            return

        def on_result(name: str | None) -> None:
            if name and self.app.db:
                queries.create_category(self.app.db, name)
                self._refresh_table()

        self.app.push_screen(InputModal("New Category", placeholder="Category name"), on_result)

    def action_edit(self) -> None:
        if self._show_archived:
            return
        cat_id = self._get_selected_id()
        if cat_id is None or self.app.db is None:
            return
        category = queries.get_category(self.app.db, cat_id)
        if category is None:
            return

        def on_result(name: str | None) -> None:
            if name and self.app.db:
                queries.update_category(self.app.db, cat_id, name)
                self._refresh_table()

        self.app.push_screen(
            InputModal("Edit Category", placeholder="Category name", value=category.name),
            on_result,
        )

    def action_archive(self) -> None:
        if self._show_archived:
            return
        cat_id = self._get_selected_id()
        if cat_id is None or self.app.db is None:
            return
        category = queries.get_category(self.app.db, cat_id)
        if category is None:
            return

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.archive_category(self.app.db, cat_id)
                self._refresh_table()

        self.app.push_screen(
            ConfirmModal(f'Archive "{category.name}"?', confirm_label="Archive"),
            on_result,
        )

    def action_restore(self) -> None:
        if not self._show_archived:
            return
        cat_id = self._get_selected_id()
        if cat_id is None or self.app.db is None:
            return
        category = queries.get_category(self.app.db, cat_id)
        if category is None:
            return

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.restore_category(self.app.db, cat_id)
                self._refresh_table()

        self.app.push_screen(
            ConfirmModal(f'Restore "{category.name}"?', confirm_label="Restore"),
            on_result,
        )

    def action_toggle_archive(self) -> None:
        self._show_archived = not self._show_archived
        self._refresh_table()
