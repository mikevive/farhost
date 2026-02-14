"""Daily report screen with date navigation and entry management."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import DataTable, Static

from devflow.db import queries
from devflow.widgets.bar_chart import format_duration
from devflow.widgets.modal import ConfirmModal


class DailyReportScreen(Container):
    """Daily report: chronological log, totals by project/category, date navigation."""

    DEFAULT_CSS = """
    DailyReportScreen {
        background: #1C1C1E;
        padding: 1 2;
    }
    #title {
        text-style: bold;
        color: #FFFFFF;
        width: 100%;
        margin-bottom: 1;
    }
    #nav-hint {
        color: #A1A1A6;
        margin-bottom: 1;
    }
    DataTable {
        height: 1fr;
        background: #2C2C2E;
        border: solid #48484A;
    }
    #summary {
        height: auto;
        max-height: 15;
        color: #A1A1A6;
        margin-top: 1;
        padding: 1;
        background: #2C2C2E;
        border: solid #48484A;
    }
    #entry-hints {
        color: #A1A1A6;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("h,left", "prev_day", "Previous day", show=False),
        Binding("l,right", "next_day", "Next day", show=False),
        Binding("d", "delete_entry", "Delete entry", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._current_date = date.today()

    def compose(self) -> ComposeResult:
        yield Static("", id="title")
        yield Static("◄ h  Previous day  |  Next day  l ►", id="nav-hint")
        yield DataTable(id="daily-table")
        yield Static("", id="summary")
        yield Static("(d) delete entry", id="entry-hints")

    def on_mount(self) -> None:
        table = self.query_one("#daily-table", DataTable)
        table.add_columns("Start", "End", "Project", "Task", "Category", "Duration")
        table.cursor_type = "row"
        self._refresh()

    def _refresh(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        date_str = self._current_date.isoformat()
        today = date.today()

        # Title
        if self._current_date == today:
            day_label = "Today"
        else:
            day_label = self._current_date.strftime("%a")
        self.query_one("#title", Static).update(
            f"DevFlow - Daily Report ({date_str} {day_label})"
        )

        # Entries table
        table = self.query_one("#daily-table", DataTable)
        table.clear()

        entries = queries.list_time_entries_for_date(conn, date_str)
        for e in entries:
            task = queries.get_task(conn, e.task_id)
            cat = queries.get_category(conn, e.category_id)
            project_name = ""
            if task:
                project = queries.get_project(conn, task.project_id)
                project_name = project.name if project else "?"
            task_name = task.name if task else "?"
            cat_name = cat.name if cat else "?"

            start_time = e.start.split(" ")[1] if " " in e.start else e.start
            end_time = e.end.split(" ")[1] if " " in e.end else e.end

            table.add_row(
                start_time, end_time, project_name, task_name, cat_name,
                format_duration(e.duration_seconds),
                key=str(e.id),
            )

        # Summary
        project_totals = queries.daily_totals_by_project(conn, date_str)
        category_totals = queries.daily_totals_by_category(conn, date_str)

        lines = []
        if project_totals:
            lines.append("[bold #FFFFFF]Totals by Project:[/]")
            for name, secs in project_totals:
                lines.append(f"  {name}: {format_duration(secs)}")
        if category_totals:
            lines.append("")
            lines.append("[bold #FFFFFF]Totals by Category:[/]")
            for name, secs in category_totals:
                lines.append(f"  {name}: {format_duration(secs)}")

        self.query_one("#summary", Static).update("\n".join(lines) if lines else "No entries")

    def action_prev_day(self) -> None:
        self._current_date -= timedelta(days=1)
        self._refresh()

    def action_next_day(self) -> None:
        self._current_date += timedelta(days=1)
        self._refresh()

    def action_delete_entry(self) -> None:
        table = self.query_one("#daily-table", DataTable)
        if table.row_count == 0:
            return
        row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
        entry_id = int(row_key.value)

        def on_result(confirmed: bool) -> None:
            if confirmed and self.app.db:
                queries.delete_time_entry(self.app.db, entry_id)
                self._refresh()

        self.app.push_screen(
            ConfirmModal(
                "Permanently delete this time entry?",
                confirm_label="Delete",
                danger=True,
            ),
            on_result,
        )
