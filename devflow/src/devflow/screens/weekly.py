"""Weekly report screen with ISO week navigation and bar charts."""

from __future__ import annotations

from datetime import date, datetime, timedelta

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Static

from devflow.db import queries
from devflow.widgets.bar_chart import format_hours, generate_bar


class WeeklyReportScreen(Container):
    """Weekly report: ASCII bar charts per day, project/category breakdowns."""

    can_focus = True

    DEFAULT_CSS = """
    WeeklyReportScreen {
        background: #282a36;
        padding: 1 2;
    }
    #title {
        text-style: bold;
        color: #f8f8f2;
        width: 100%;
        margin-bottom: 1;
    }
    #nav-hint {
        color: #6272a4;
        margin-bottom: 1;
    }
    #chart {
        height: 1fr;
        color: #f8f8f2;
        padding: 1 2;
        background: #44475a;
        border: solid #6272a4;
        margin-bottom: 1;
    }
    #breakdown {
        height: 1fr;
        color: #f8f8f2;
        padding: 1 2;
        background: #44475a;
        border: solid #6272a4;
        display: none;
    }
    #footer-hints {
        color: #6272a4;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("h,left", "prev_week", "Previous week", show=False),
        Binding("l,right", "next_week", "Next week", show=False),
        Binding("v", "cycle_view", "Cycle View", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        today = date.today()
        # ISO week: find Monday of current week
        self._week_start = today - timedelta(days=today.weekday())
        # 0: Chart, 1: Projects, 2: Categories
        self._view_mode = 0

    def compose(self) -> ComposeResult:
        yield Static("", id="title")
        yield Static("◄ h  Previous week  |  Next week  l ►", id="nav-hint")
        yield Static("", id="chart")
        yield Static("", id="breakdown")
        yield Static("(v) change view", id="footer-hints")

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
        
        modes = ["Chart", "Projects", "Categories"]
        view_label = modes[self._view_mode]
        self.query_one("#title", Static).update(
            f"DevFlow - Weekly {view_label} (Week {iso.week}: {start_fmt} - {end_fmt})"
        )

        # Toggle visibility
        chart = self.query_one("#chart", Static)
        breakdown = self.query_one("#breakdown", Static)
        hints = self.query_one("#footer-hints", Static)

        if self._view_mode == 0:
            chart.display = True
            breakdown.display = False
        else:
            chart.display = False
            breakdown.display = True

        # Query data
        week_start_str = f"{self._week_start.isoformat()} 00:00:00"
        week_end_str = f"{week_end.isoformat()} 00:00:00"

        # Build Chart
        day_totals = queries.weekly_totals_by_day(conn, week_start_str, week_end_str)
        day_map = dict(day_totals)
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
                f"  {day_name} ({day_date.day:2d}): [#ff79c6]{bar}[/]{hours_label}"
            )
        chart_lines.append("")
        chart_lines.append(f"  [bold]Total Hours: {format_hours(total_seconds)}[/]")
        chart.update("\n".join(chart_lines))

        # Breakdown
        breakdown_lines = []
        if self._view_mode == 1:
            project_totals = queries.weekly_totals_by_project(conn, week_start_str, week_end_str)
            breakdown_lines.append("[bold #bd93f9]Breakdown by Project:[/]")
            for name, secs in project_totals:
                breakdown_lines.append(f"  {name}: {format_hours(secs)}")
        elif self._view_mode == 2:
            category_totals = queries.weekly_totals_by_category(conn, week_start_str, week_end_str)
            breakdown_lines.append("[bold #bd93f9]Breakdown by Category:[/]")
            for name, secs in category_totals:
                breakdown_lines.append(f"  {name}: {format_hours(secs)}")

        breakdown.update(
            "\n".join(breakdown_lines) if breakdown_lines else "No entries"
        )

    def action_prev_week(self) -> None:
        self._week_start -= timedelta(weeks=1)
        self._refresh()

    def action_next_week(self) -> None:
        self._week_start += timedelta(weeks=1)
        self._refresh()

    def action_cycle_view(self) -> None:
        self._view_mode = (self._view_mode + 1) % 3
        self._refresh()
        self.focus()
