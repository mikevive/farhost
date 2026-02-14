"""Tasks management screen for a specific project."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import DataTable, Static

from devflow.db import queries
from devflow.widgets.modal import ConfirmModal, InputModal


class TasksScreen(Container):
    """Manage tasks for a specific project."""

    DEFAULT_CSS = """
    TasksScreen {
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
        Binding("escape", "go_back", "Back", show=False),
    ]

    def __init__(self, project_id: int) -> None:
        super().__init__()
        self._project_id = project_id
        self._show_archived = False

    def compose(self) -> ComposeResult:
        yield Static("", id="title")
        yield DataTable(id="tasks-table")
        yield Static("(a)dd, (e)dit, (d) archive, (A) view archive, Esc back", id="hints")

    def on_mount(self) -> None:
        table = self.query_one("#tasks-table", DataTable)
        table.add_column("Name", key="name")
        table.cursor_type = "row"
        self._refresh_table()

    def _refresh_table(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        project = queries.get_project(conn, self._project_id)
        project_name = project.name if project else "?"

        table = self.query_one("#tasks-table", DataTable)
        table.clear()

        title = self.query_one("#title", Static)
        hints = self.query_one("#hints", Static)

        if self._show_archived:
            title.update(f'DevFlow - Tasks for "{project_name}" [Archive]')
            hints.update("(r) restore, (A) back to active, Esc back")
            tasks = queries.list_tasks(conn, self._project_id, include_archived=True)
        else:
            title.update(f'DevFlow - Tasks for "{project_name}"')
            hints.update("(a)dd, (e)dit, (d) archive, (A) view archive, Esc back")
            tasks = queries.list_tasks(conn, self._project_id)

        for t in tasks:
            table.add_row(t.name, key=str(t.id))

    def _get_selected_id(self) -> int | None:
        table = self.query_one("#tasks-table", DataTable)
        if table.row_count == 0:
            return None
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        return int(row_key.value)

    def action_add(self) -> None:
        if self._show_archived:
            return

        def on_result(name: str | None) -> None:
            if name and self.app.db:
                queries.create_task(self.app.db, self._project_id, name)
                self._refresh_table()

        self.app.push_screen(InputModal("New Task", placeholder="Task name"), on_result)

    def action_edit(self) -> None:
        if self._show_archived:
            return
        task_id = self._get_selected_id()
        if task_id is None or self.app.db is None:
            return
        task = queries.get_task(self.app.db, task_id)
        if task is None:
            return

        def on_result(name: str | None) -> None:
            if name and self.app.db:
                queries.update_task(self.app.db, task_id, name)
                self._refresh_table()

        self.app.push_screen(
            InputModal("Edit Task", placeholder="Task name", value=task.name),
            on_result,
        )

    def action_archive(self) -> None:
        if self._show_archived:
            return
        task_id = self._get_selected_id()
        if task_id is None or self.app.db is None:
            return
        task = queries.get_task(self.app.db, task_id)
        if task is None:
            return

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.archive_task(self.app.db, task_id)
                self._refresh_table()

        self.app.push_screen(
            ConfirmModal(f'Archive "{task.name}"?', confirm_label="Archive"),
            on_result,
        )

    def action_restore(self) -> None:
        if not self._show_archived:
            return
        task_id = self._get_selected_id()
        if task_id is None or self.app.db is None:
            return
        task = queries.get_task(self.app.db, task_id)
        if task is None:
            return

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.restore_task(self.app.db, task_id)
                self._refresh_table()

        self.app.push_screen(
            ConfirmModal(f'Restore "{task.name}"?', confirm_label="Restore"),
            on_result,
        )

    def action_toggle_archive(self) -> None:
        self._show_archived = not self._show_archived
        self._refresh_table()

    def action_go_back(self) -> None:
        self.app._navigate_to("projects")
