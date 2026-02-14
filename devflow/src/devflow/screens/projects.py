"""Projects management screen with archive toggle."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import DataTable, Static

from devflow.db import queries
from devflow.widgets.modal import ConfirmModal, InputModal


class ProjectsScreen(Container):
    """Manage projects: list, add, edit, archive, restore."""

    DEFAULT_CSS = """
    ProjectsScreen {
        background: #1C1C1E;
        padding: 1 2;
    }
    #title {
        text-style: bold;
        color: #FFFFFF;
        width: 100%;
        margin-bottom: 1;
    }
    DataTable {
        height: 1fr;
        background: #2C2C2E;
        border: solid #48484A;
    }
    #hints {
        color: #A1A1A6;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("a", "add", "Add", show=False),
        Binding("e", "edit", "Edit", show=False),
        Binding("d", "archive", "Archive", show=False),
        Binding("A", "toggle_archive", "Archive view", show=False),
        Binding("r", "restore", "Restore", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._show_archived = False

    def compose(self) -> ComposeResult:
        yield Static("DevFlow - Projects", id="title")
        yield DataTable(id="projects-table")
        yield Static("(a)dd, (e)dit, (d) archive, (A) view archive", id="hints")

    def on_mount(self) -> None:
        table = self.query_one("#projects-table", DataTable)
        table.add_column("Name", key="name")
        table.cursor_type = "row"
        self._refresh_table()

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if self._show_archived:
            return
        if event.row_key.value is None:
            return
        project_id = int(event.row_key.value)
        self.app._navigate_to("tasks", project_id=project_id)

    def _refresh_table(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        table = self.query_one("#projects-table", DataTable)
        table.clear()

        title = self.query_one("#title", Static)
        hints = self.query_one("#hints", Static)

        if self._show_archived:
            title.update("DevFlow - Projects [Archive]")
            hints.update("(r) restore, (A) back to active")
            projects = queries.list_projects(conn, include_archived=True)
        else:
            title.update("DevFlow - Projects")
            hints.update("(a)dd, (e)dit, (d) archive, (A) view archive")
            projects = queries.list_projects(conn)

        for p in projects:
            table.add_row(p.name, key=str(p.id))

    def _get_selected_id(self) -> int | None:
        table = self.query_one("#projects-table", DataTable)
        if table.row_count == 0:
            return None
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        return int(row_key.value) if row_key.value else None

    def action_add(self) -> None:
        if self._show_archived:
            return

        def on_result(name: str | None) -> None:
            if name and self.app.db:
                queries.create_project(self.app.db, name)
                self._refresh_table()

        self.app.push_screen(InputModal("New Project", placeholder="Project name"), on_result)

    def action_edit(self) -> None:
        if self._show_archived:
            return
        project_id = self._get_selected_id()
        if project_id is None or self.app.db is None:
            return
        project = queries.get_project(self.app.db, project_id)
        if project is None:
            return

        def on_result(name: str | None) -> None:
            if name and self.app.db:
                queries.update_project(self.app.db, project_id, name)
                self._refresh_table()

        self.app.push_screen(
            InputModal("Edit Project", placeholder="Project name", value=project.name),
            on_result,
        )

    def action_archive(self) -> None:
        if self._show_archived:
            return
        project_id = self._get_selected_id()
        if project_id is None or self.app.db is None:
            return
        project = queries.get_project(self.app.db, project_id)
        if project is None:
            return

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.archive_project(self.app.db, project_id)
                self._refresh_table()

        self.app.push_screen(
            ConfirmModal(f'Archive "{project.name}" and all its tasks?', confirm_label="Archive"),
            on_result,
        )

    def action_restore(self) -> None:
        if not self._show_archived:
            return
        project_id = self._get_selected_id()
        if project_id is None or self.app.db is None:
            return
        project = queries.get_project(self.app.db, project_id)
        if project is None:
            return

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.restore_project(self.app.db, project_id)
                self._refresh_table()

        self.app.push_screen(
            ConfirmModal(f'Restore "{project.name}" and its tasks?', confirm_label="Restore"),
            on_result,
        )

    def action_toggle_archive(self) -> None:
        self._show_archived = not self._show_archived
        self._refresh_table()
