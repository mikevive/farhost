"""Timer screen: project/task/category selection and live timer display."""

from __future__ import annotations

from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Button, Label, Select, Static, Digits
from textual.timer import Timer

from devflow.db import queries
from devflow.timer import engine
from devflow.widgets.bar_chart import format_duration


class TimerScreen(Container):
    """Main timer view with selection controls and live elapsed display."""

    can_focus = True

    DEFAULT_CSS = """
    TimerScreen {
        background: #282a36;
        padding: 1 2;
    }
    #title {
        text-style: bold;
        color: #f8f8f2;
        width: 100%;
        text-align: center;
        margin-bottom: 1;
    }
    .selector-row {
        height: 3;
        width: 100%;
        margin-bottom: 1;
    }
    .selector-label {
        width: 12;
        color: #6272a4;
        padding-top: 1;
    }
    Select {
        width: 1fr;
    }
    #btn-row {
        width: 100%;
        align: center middle;
        height: 3;
        margin: 1 0;
    }
    #btn-start {
        background: #bd93f9;
        min-width: 20;
    }
    #btn-stop {
        background: #ff5555;
        min-width: 20;
    }
    #timer-display {
        width: 100%;
        height: auto;
        align: center middle;
        margin: 1 0;
        display: none;
    }
    #timer-info {
        width: 100%;
        text-align: center;
        color: #6272a4;
    }
    #timer-clock-container {
        width: 100%;
        height: auto;
        align: center middle;
    }
    #timer-clock {
        width: auto;
        color: #8be9fd;
        text-style: bold;
        margin: 1 0;
    }
    #timer-status {
        width: 100%;
        text-align: center;
        color: #50fa7b;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._timer_interval: Timer | None = None
        self._midnight_interval: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Static("DevFlow", id="title")
        with Vertical():
            with Vertical(id="selectors"):
                with Horizontal(classes="selector-row"):
                    yield Label("Project:", classes="selector-label")
                    yield Select([], id="sel-project", prompt="Select project...")
                with Horizontal(classes="selector-row"):
                    yield Label("Task:", classes="selector-label")
                    yield Select([], id="sel-task", prompt="Select task...")
                with Horizontal(classes="selector-row"):
                    yield Label("Category:", classes="selector-label")
                    yield Select([], id="sel-category", prompt="Select category...")
            with Vertical(id="timer-display"):
                yield Static("", id="timer-info")
                with Horizontal(id="timer-clock-container"):
                    yield Digits("00:00:00", id="timer-clock")
                yield Static("[Running]", id="timer-status")
            with Horizontal(id="btn-row"):
                yield Button("START TIMER", id="btn-start")
                yield Button("STOP TIMER", id="btn-stop")

    def on_mount(self) -> None:
        self._load_selectors()
        self._update_timer_display()
        self._timer_interval = self.set_interval(1, self._tick)
        self._midnight_interval = self.set_interval(60, self._check_midnight)

    def _load_selectors(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        projects = queries.list_projects(conn)
        self.query_one("#sel-project", Select).set_options(
            [(p.name, p.id) for p in projects]
        )

        categories = queries.list_categories(conn)
        self.query_one("#sel-category", Select).set_options(
            [(c.name, c.id) for c in categories]
        )

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "sel-project" and event.value is not Select.BLANK:
            conn = self.app.db
            if conn is None:
                return
            tasks = queries.list_tasks(conn, event.value)
            self.query_one("#sel-task", Select).set_options(
                [(t.name, t.id) for t in tasks]
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        conn = self.app.db
        if conn is None:
            return

        if event.button.id == "btn-start":
            task_sel = self.query_one("#sel-task", Select)
            cat_sel = self.query_one("#sel-category", Select)

            if task_sel.value is Select.BLANK or cat_sel.value is Select.BLANK:
                return

            engine.start_timer(conn, task_sel.value, cat_sel.value)
            self._update_timer_display()

        elif event.button.id == "btn-stop":
            engine.stop_timer(conn)
            self._update_timer_display()

    def _tick(self) -> None:
        self._update_timer_display()

    def _check_midnight(self) -> None:
        conn = self.app.db
        if conn is None:
            return
        engine.check_midnight_split(conn)

    def _update_timer_display(self) -> None:
        conn = self.app.db
        if conn is None:
            return

        display_container = self.query_one("#timer-display", Vertical)
        session = queries.get_active_session(conn)
        btn_start = self.query_one("#btn-start", Button)
        btn_stop = self.query_one("#btn-stop", Button)
        selectors = self.query_one("#selectors", Vertical)

        if session is None:
            display_container.display = False
            btn_start.display = True
            btn_stop.display = False
            selectors.display = True
            return

        display_container.display = True
        btn_start.display = False
        btn_stop.display = True
        selectors.display = False

        task = queries.get_task(conn, session.task_id)
        category = queries.get_category(conn, session.category_id)
        if task is None or category is None:
            display_container.display = False
            return

        project = queries.get_project(conn, task.project_id)
        project_name = project.name if project else "?"

        start = datetime.strptime(session.start_time, "%Y-%m-%d %H:%M:%S")
        elapsed = int((datetime.now() - start).total_seconds())
        clock_str = format_duration(elapsed)

        self.query_one("#timer-info", Static).update(f"{project_name} | {task.name} | {category.name}")
        self.query_one("#timer-clock", Digits).update(clock_str)
