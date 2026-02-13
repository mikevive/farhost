"""Weekly report screen with ISO week navigation and bar charts."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Static

from devflow.db import queries
from devflow.widgets.bar_chart import format_hours, generate_bar


class WeeklyReportScreen(Screen):
    """Weekly report: ASCII bar charts per day, project/category breakdowns."""

    DEFAULT_CSS = """
    WeeklyReportScreen {
        background: #1C1C1E;
        padding: 1 2;
    }
    WeeklyReportScreen #title {
        text-style: bold;
        color: #FFFFFF;
        width: 100%;
        margin-bottom: 1;
    }
    WeeklyReportScreen #nav-hint {
        color: #A1A1A6;
        margin-bottom: 1;
    }
    WeeklyReportScreen #chart {
        height: auto;
        color: #FFFFFF;
        padding: 1;
        background: #2C2C2E;
        border: solid #48484A;
        margin-bottom: 1;
    }
    WeeklyReportScreen #breakdown {
        height: auto;
        color: #A1A1A6;
        padding: 1;
        background: #2C2C2E;
        border: solid #48484A;
    }
    """

    BINDINGS = [
        Binding("h,left", "prev_week", "Previous week", show=False),
        Binding("l,right", "next_week", "Next week", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        today = date.today()
        # ISO week: find Monday of current week
        self._week_start = today - timedelta(days=today.weekday())

    def compose(self) -> ComposeResult:
        yield Static("", id="title")
        yield Static("◄ h  Previous week  |  Next week  l ►", id="nav-hint")
        yield Static("", id="chart")
        yield Static("", id="breakdown")

    def on_mount(self) -> None:
        self._refresh()

    def _refresh(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        week_end = self._week_start + timedelta(days=7)
        iso = self._week_start.isocalendar()

        # Title
        start_fmt = self._week_start.strftime("%b %d")
        end_fmt = (self._week_start + timedelta(days=6)).strftime("%b %d")
        self.query_one("#title", Static).update(
            f"DevFlow - Weekly Report (Week {iso.week}: {start_fmt} - {end_fmt})"
        )

        # Query data
        week_start_str = f"{self._week_start.isoformat()} 00:00:00"
        week_end_str = f"{week_end.isoformat()} 00:00:00"

        day_totals = queries.weekly_totals_by_day(conn, week_start_str, week_end_str)
        day_map = dict(day_totals)

        # Build bar chart
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        max_seconds = max(day_map.values()) if day_map else 0
        total_seconds = sum(day_map.values()) if day_map else 0

        chart_lines = []
        for i, day_name in enumerate(day_names):
            day_date = self._week_start + timedelta(days=i)
            day_str = day_date.isoformat()
            secs = day_map.get(day_str, 0)

            bar = generate_bar(secs, max_seconds) if secs > 0 else ""
            hours_label = f" ({format_hours(secs)})" if secs > 0 else ""
            chart_lines.append(
                f"  {day_name} ({day_date.day:2d}): [#E8735A]{bar}[/]{hours_label}"
            )

        chart_lines.append("")
        chart_lines.append(f"  [bold]Total Hours: {format_hours(total_seconds)}[/]")

        self.query_one("#chart", Static).update("\n".join(chart_lines))

        # Breakdown
        project_totals = queries.weekly_totals_by_project(conn, week_start_str, week_end_str)
        category_totals = queries.weekly_totals_by_category(conn, week_start_str, week_end_str)

        breakdown_lines = []
        if project_totals:
            breakdown_lines.append("[bold #FFFFFF]Breakdown by Project:[/]")
            for name, secs in project_totals:
                breakdown_lines.append(f"  {name}: {format_hours(secs)}")
        if category_totals:
            breakdown_lines.append("")
            breakdown_lines.append("[bold #FFFFFF]Breakdown by Category:[/]")
            for name, secs in category_totals:
                breakdown_lines.append(f"  {name}: {format_hours(secs)}")

        self.query_one("#breakdown", Static).update(
            "\n".join(breakdown_lines) if breakdown_lines else "No entries"
        )

    def action_prev_week(self) -> None:
        self._week_start -= timedelta(weeks=1)
        self._refresh()

    def action_next_week(self) -> None:
        self._week_start += timedelta(weeks=1)
        self._refresh()
