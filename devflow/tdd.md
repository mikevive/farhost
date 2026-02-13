# Technical Design Document: DevFlow

## 1. Introduction
This document provides a detailed technical design for **DevFlow**, a local-first, keyboard-centric time tracking TUI. It translates the functional requirements outlined in `prd.md` into a concrete implementation plan, focusing on architecture, database structure, core logic, and UI composition using the Textual framework.

## 2. Project Structure

```
devflow/
├── pyproject.toml              # Package metadata, dependencies, console script entry point
├── README.md
├── src/
│   └── devflow/
│       ├── __init__.py
│       ├── __main__.py         # Entry point: argparse (--status) or launch TUI
│       ├── app.py              # Textual App class, screen routing, command mode
│       ├── db/
│       │   ├── __init__.py
│       │   ├── connection.py   # DB path resolution, connection factory, schema init
│       │   ├── schema.sql      # CREATE TABLE / CREATE INDEX statements
│       │   ├── models.py       # Dataclasses: Project, Task, Category, TimeEntry, ActiveSession
│       │   └── queries.py      # All CRUD and reporting SQL (data access layer)
│       ├── timer/
│       │   ├── __init__.py
│       │   └── engine.py       # start/stop/midnight-split logic, crash recovery
│       ├── screens/
│       │   ├── __init__.py
│       │   ├── timer.py        # TimerScreen
│       │   ├── daily.py        # DailyReportScreen
│       │   ├── weekly.py       # WeeklyReportScreen
│       │   ├── projects.py     # ProjectsScreen
│       │   ├── tasks.py        # TasksScreen
│       │   └── categories.py   # CategoriesScreen
│       ├── widgets/
│       │   ├── __init__.py
│       │   ├── modal.py        # Reusable CRUD modal (create/edit/delete)
│       │   ├── command_bar.py  # Footer command input (:timer, :daily, etc.)
│       │   └── bar_chart.py    # ASCII bar chart renderer for weekly report
│       └── cli.py              # --status headless output logic
├── tmux/
│   └── devflow.tmux            # Tmux plugin: status bar component + floating window toggle
└── tests/
    ├── __init__.py
    ├── test_engine.py          # Timer start/stop/midnight split unit tests
    ├── test_queries.py         # Data access layer tests (in-memory SQLite)
    └── test_cli.py             # --status output tests
```

### Key Decisions
- **`src/` layout:** Prevents accidental imports from the project root during development.
- **`db/schema.sql`:** Raw SQL file loaded by `connection.py` on first run, keeping schema readable and diffable.
- **`timer/engine.py`:** Isolates all timer business logic from the UI, making it testable without Textual.
- **`widgets/`:** Shared components used across multiple screens.
- **`tmux/`:** Kept at the repo root, outside the Python package — it's a shell script, not Python.
- **Console script:** `pyproject.toml` will define `[project.scripts] devflow = "devflow.__main__:main"` so the app can be run as `devflow` or `python -m devflow`.

## 3. System Architecture
DevFlow will be a monolithic, single-process Terminal User Interface (TUI) application built in Python using the **Textual** framework.

The architecture is layered into three primary concerns:

- **Presentation Layer (UI):** Managed by Textual. This includes all screens, widgets, modals, and user input handling. It is responsible for displaying data and capturing user intent.
- **Application Logic Layer (State & Business Rules):** This layer acts as the bridge between the UI and the database. It manages the application's state (e.g., the currently active view, running timer data), enforces business rules (e.g., midnight timer splits, single active timer), and orchestrates data flow.
- **Data Access Layer:** Responsible for all interactions with the SQLite database. This layer will abstract the SQL queries needed for all CRUD operations and reporting, ensuring a clean separation from the application logic.

### Technology Stack
- **Language:** Python 3.10+
- **Environment Management:** `uv`. The project will use `uv` for virtual environment creation and dependency management as a modern, high-speed replacement for `venv` and `pip`.
- **Framework:** Textual
- **Database:** `sqlite3` (standard library)
- **CLI Parsing:** `argparse` (standard library) for handling the `--status` flag.

### Packaging & Entry Point
The application is launched as a standalone `devflow` command, powered by a console script defined in `pyproject.toml`:

```toml
[project.scripts]
devflow = "devflow.__main__:main"
```

This also supports `python -m devflow` as a fallback via `__main__.py`.

**Installation modes:**
- **Development:** `uv pip install -e .` — installs an editable link into the active venv. The `devflow` binary is available when the venv is active.
- **Production / Tmux:** `uv tool install .` — installs into an isolated environment and symlinks `devflow` to `~/.local/bin/`, making it globally available without a venv. This is the recommended mode for tmux integration since `~/.local/bin/` is on PATH regardless of shell type.

**Tmux compatibility:** The `devflow.tmux` plugin will default to calling `devflow` on PATH. Users can override the path via a tmux option:
```bash
# .tmux.conf — optional override if devflow is not on PATH
set -g @devflow_cmd "/path/to/venv/bin/devflow"
```

## 4. Database Design
The application will use a single SQLite database file located at `~/.farhost/devflow/devflow.db`.

### Schema Definition
The schema is designed to be simple and relational, directly reflecting the data hierarchy from the PRD.

| Table | Columns | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `categories` | `id` (PK) | `INTEGER` | Auto-incrementing primary key. |
| | `name` | `TEXT` | Unique name of the category (e.g., "Code"). |
| | `archived_at` | `TEXT` | ISO 8601 timestamp when archived, `NULL` if active. |
| `projects` | `id` (PK) | `INTEGER` | Auto-incrementing primary key. |
| | `name` | `TEXT` | Unique name of the project. |
| | `archived_at` | `TEXT` | ISO 8601 timestamp when archived, `NULL` if active. |
| `tasks` | `id` (PK) | `INTEGER` | Auto-incrementing primary key. |
| | `project_id` (FK) | `INTEGER` | Foreign key referencing `projects.id`. |
| | `name` | `TEXT` | Name of the task. |
| | `archived_at` | `TEXT` | ISO 8601 timestamp when archived, `NULL` if active. |
| `time_entries`| `id` (PK) | `INTEGER` | Auto-incrementing primary key. |
| | `task_id` (FK) | `INTEGER` | Foreign key referencing `tasks.id`. |
| | `category_id` (FK)| `INTEGER` | Foreign key referencing `categories.id`. |
| | `start` | `TEXT` | ISO 8601 formatted timestamp (e.g., `YYYY-MM-DD HH:MM:SS`). |
| | `end` | `TEXT` | ISO 8601 formatted timestamp. |
| | `duration_seconds`| `INTEGER` | Calculated duration (`end` - `start`). |
| `active_session`| `id` (PK) | `INTEGER` | Primary key (always 1). |
| | `task_id` (FK) | `INTEGER` | Foreign key referencing `tasks.id`. |
| | `category_id` (FK)| `INTEGER` | Foreign key referencing `categories.id`. |
| | `start_time` | `TEXT` | ISO 8601 formatted timestamp. |

### Notes on Schema:
- **Timestamps:** Using `TEXT` with ISO 8601 strings is chosen for simplicity and human-readability. SQLite's built-in date and time functions work well with this format. All times will be stored in the user's local timezone.
- **Indexes:** To ensure fast query performance for reporting, indexes will be created on:
  - `time_entries.start`
  - `time_entries.task_id`
  - `time_entries.category_id`
- **Constraints:** `UNIQUE` constraints will be applied to `categories.name` and `projects.name`.
- **Archiving (Cascade):** All entity tables (`categories`, `projects`, `tasks`) will include an `archived_at` (`TEXT`, nullable) column. Archiving sets `archived_at` to the current ISO 8601 timestamp. This preserves historical data for reports while hiding entities from active use. Cascade behavior:
  - Archiving a **Project** → archives all its Tasks (and stops any active session referencing them).
  - Archiving a **Task** → archives only that Task (and stops any active session referencing it).
  - Archiving a **Category** → archives only that Category (and stops any active session referencing it).
  - **Restoring** a Project → restores all its Tasks that were archived at the same time (same `archived_at` timestamp). Restoring a Task or Category restores only that entity.
  - All list queries and selection dropdowns must filter by `WHERE archived_at IS NULL`.
  - Reports join freely regardless of `archived_at`, so historical entries still display their original Project/Task/Category names.
- **Hard Deletion (Time Entries only):** `time_entries` are the only records that can be permanently deleted (`DELETE FROM time_entries WHERE id = ?`). This allows users to correct mistakes. Projects, Tasks, and Categories are **never** hard-deleted.
- **Sort Order:** All list views and selection dropdowns for projects, tasks, and categories are sorted **alphabetically by name** (`ORDER BY name ASC`). Time entries in reports are sorted **chronologically** (`ORDER BY start ASC`).

## 5. Core Application Logic

### State Management
The application's state will be managed within Textual's `App` class and its `Screen` children.
- **Reactive Attributes:** Textual's `reactive` attributes will be used extensively to automatically refresh UI components when the underlying state changes. For example, the running timer display will be a reactive variable that, when updated, triggers a repaint of the widget.
- **Data Caching:** To avoid constant database queries, lists of Projects, Tasks, and Categories will be fetched once and cached in memory when their respective management screens are loaded. A refresh can be triggered after any CRUD operation.

### Timer Logic
- **`start_timer(project, task, category)`:**
  1. Check the `active_session` table for an existing entry.
  2. If an entry exists, call `stop_timer()` on it.
  3. Insert a new row into `active_session` with the new `task_id`, `category_id`, and the current `start_time`.
  4. Update the UI to show the new running timer.
- **`stop_timer()`:**
  1. Read the `task_id`, `category_id`, and `start_time` from the `active_session` table.
  2. Record the current time as `end_time`.
  3. Calculate `duration_seconds`.
  4. Insert a new record into the `time_entries` table.
  5. Delete the row from `active_session`.
  6. Update the UI, clearing the running timer display.
- **Midnight Splitting:**
  - A `set_interval` will run a check every minute.
  - If a timer is active and the current date is different from the `start_time`'s date, the logic will:
    1. Stop the current timer at `23:59:59` of the start date.
    2. Immediately start a new timer with the same Project/Task/Category at `00:00:00` of the new date.

## 6. UI/Component Design (Textual)

### Screen Architecture
The application will be composed of multiple `Screen` objects, with navigation handled by `app.switch_screen()`:
- `TimerScreen`: The default view. Contains controls for selecting Project/Task/Category and the live timer display.
- `DailyReportScreen`: Shows the daily log and summary totals. **Will also serve as the primary interface for editing and deleting past time entries.**
- `WeeklyReportScreen`: Shows the weekly bar chart and breakdowns.
- `ProjectsScreen`: Manages active projects. `A` (Shift+a) toggles to the archive view showing archived projects with a `r` restore action.
- `TasksScreen`: Manages active tasks for a selected project. `A` (Shift+a) toggles to the archive view.
- `CategoriesScreen`: Manages active categories. `A` (Shift+a) toggles to the archive view.

### Widget Breakdown
- **Navigation/Footer:** A `Static` widget at the bottom of the `App`, always visible, showing available commands.
- **Data Lists (`:projects`, `:tasks`, `:categories`):** A `DataTable` widget will be used to display these lists, allowing for selection and highlighting.
- **Timer Selection:**
  - `Static` widgets for labels ("Project:", "Task:").
  - `Input` widgets with `suggester` functionality will be used for a keyboard-friendly, filterable "dropdown" experience.
  - A `watch` method will be used to monitor the Project `Input`. When the project changes, the application logic will fetch the relevant tasks and update the `suggester` for the Task `Input`, ensuring the user can only select tasks belonging to the chosen project.
- **Reports:**
  - `DataTable` for the `Daily Log`. This table will be selectable, allowing users to choose an entry to edit or delete via keyboard shortcuts (`e`, `d`).
  - `Static` widgets for summary text and the ASCII bar charts.
- **Modals (CRUD):**
  - A reusable `ModalScreen` class will be implemented. It will be a `Screen` with `DEFAULT_CSS` styled to appear as a modal dialog.
  - It will contain `Input` widgets for data entry and `Button` widgets for actions (`[Save]`, `[Cancel]`, etc.).

### Theme & Color Scheme
The UI follows a **dark mode** aesthetic inspired by modern iOS dark interfaces: near-black backgrounds, subtle borders, and a warm coral accent.

**Color Palette:**
| Token | Hex | Usage |
| :--- | :--- | :--- |
| `background` | `#1C1C1E` | App and screen background |
| `surface` | `#2C2C2E` | Cards, panels, modal backgrounds |
| `border` | `#48484A` | Subtle borders on cards and panels |
| `text-primary` | `#FFFFFF` | Headings, primary labels, timer display |
| `text-secondary` | `#A1A1A6` | Secondary info, timestamps, hints |
| `text-muted` | `#636366` | Disabled items, placeholders |
| `accent` | `#E8735A` | Active states, running timer indicator, selected items, action buttons, bar charts |
| `accent-dim` | `#B85C48` | Hover/focus state on accent elements |
| `danger` | `#FF453A` | Delete confirmations, destructive actions |
| `success` | `#30D158` | Timer started confirmation |

**Application to Textual CSS:**
- `Screen` background: `$background`
- `DataTable` rows: `$surface` background, `$border` row separators, `$accent` for the cursor/highlighted row
- Buttons: `$accent` background with `$text-primary` label; `$danger` for delete buttons
- Modals: `$surface` background with `$border` outline
- Footer/command bar: `$background` with `$text-secondary` labels, `$accent` for the active screen indicator
- Running timer display: `$accent` text for the HH:MM:SS clock
- ASCII bar charts: `$accent` block characters (`█`) on `$background`
- Archived items (in archive view): `$text-muted`

### Command and Keyboard Handling
- **Command Mode:** The `App` will listen for the `:` key. On press, it will focus an `Input` widget in the footer to capture the command. On `Enter`, the command is parsed and the corresponding action (e.g., `app.switch_screen(...)`) is executed.
- **Shortcuts:** The `on_key` event handler on each screen will handle shortcuts like `a`, `e`, `d` for CRUD, and `hjkl` for `DataTable` row navigation.

## 7. Reporting Engine
The reporting engine will consist of functions in the Data Access Layer that execute aggregation queries.

- **Daily Report:**
  - `SELECT ... FROM time_entries WHERE date(start) = ? ORDER BY start ASC` — the date parameter is driven by the screen's current selected date.
  - `SELECT p.name, sum(te.duration_seconds) FROM time_entries te JOIN ... WHERE date(start) = ? GROUP BY p.name`
- **Weekly Report:**
  - **ISO 8601 week handling:** SQLite's `strftime('%W')` is **not** ISO 8601 compliant (it uses Sunday as week start). Instead, weekly grouping and date-range computation will be done in Python using `datetime.date.isocalendar()` and `datetime.date.fromisocalendar(year, week, day)`.
  - The query will select entries by a date range (`WHERE start >= ? AND start < ?`) computed in Python from the ISO week's Monday 00:00:00 to the following Monday 00:00:00, rather than relying on SQLite week functions.
- **ASCII Bar Chart Generation:**
  - A helper function `generate_bar(current_value, max_value, width=20)` will scale the `current_value` relative to the `max_value` for the week and return a string of block characters (`█`) of the appropriate length.
- **Historical Navigation:**
  - Both `DailyReportScreen` and `WeeklyReportScreen` support navigating through time using `h` / `l` or left/right arrow keys.
  - **Daily:** `h` moves to the previous day, `l` moves to the next day. Defaults to today on open. A header displays the selected date (e.g., `2023-10-27 (Today)` or `2023-10-25 (Wed)`).
  - **Weekly:** `h` moves to the previous ISO week, `l` moves to the next ISO week. Defaults to the current week on open. A header displays the week range (e.g., `Week 43: Oct 23 - Oct 29`).
  - Navigation triggers a re-query and full refresh of the screen content.

## 8. CLI and Tmux Integration

### `--status` Flag Implementation
- The main application entry point (`__main__.py` or `main` function) will use `argparse` to check for a `--status` flag.
- If the flag is present:
  1. The application will **not** instantiate the Textual `App`.
  2. It will connect directly to the SQLite database.
  3. Query the `active_session` table.
  4. If a timer is running, fetch the associated names, calculate the elapsed time, format the string `Project > Task > Category | HH:MM:SS`, print it to `stdout`, and exit.
  5. If no timer is running, print `Timer Stopped` and exit.

### Tmux Plugin Architecture
The plugin will consist of two parts:
1. **Tmux Script (`devflow.tmux`):**
   - A shell script that defines a tmux option, e.g., `@devflow_status`.
   - It reads the command path from `@devflow_cmd` (defaults to `devflow` on PATH, overridable in `.tmux.conf`).
   - It will contain a function that calls `devflow --status` and sets the content of the option.
   - This option can then be added to the user's `status-right` or `status-left` in their `.tmux.conf`.
   - It will also define the keybinding (e.g., `prefix + T`) that executes `tmux display-popup "devflow"`.
2. **Main Application:** The main TUI application, which is launched by the popup command.

## 9. Initialization and Error Handling

### Startup Sequence
On `App.mount`, the following will occur:
1.  **DB Check:** The app will verify that the database file and its parent directory (`~/.farhost/devflow/`) exist. If not, they will be created. The initial tables will be created using `CREATE TABLE IF NOT EXISTS ...`.
2.  **Seed Data:** After schema creation, insert default data if the tables are empty:
    - **Projects:** Architecture, Platform, Product, Team.
    - **Categories:** Admin, Break, Burnout, Code, Code review, Communication, Daily planning, Distraction, Improvements, Interviewing, Learning, Long-term planning, Meeting, Mentorship, Research, Support, System Design.
    - Seed rows are only inserted when the respective table has zero rows, so they won't duplicate on subsequent launches.
3.  **Crash Recovery:** Check if the `active_session` table contains a row.
   - If yes, this indicates a crash. The application will stop the orphaned timer using `now()` as the `end_time`, save the resulting time entry to `time_entries` (applying midnight-split logic if the session spans multiple days), and clear the `active_session` row. This preserves the tracked time rather than discarding it.
4.  **Launch Default Screen:** The `TimerScreen` will be pushed.

### Error Handling
- **Database Errors:** All database calls will be wrapped in `try...except` blocks to catch `sqlite3.Error` exceptions and display a user-friendly error message on a modal screen.
- **Input Validation:** Basic validation will be performed on modal inputs to prevent empty names for projects, tasks, etc.

## 10. Testing Strategy

### Goal
- **100% unit test coverage** across all non-UI modules.
- **Integration tests** for the main user flows end-to-end.

### Test Framework & Tooling
- **Framework:** `pytest`
- **Coverage:** `pytest-cov` with `--cov-fail-under=100` enforced on the `db/`, `timer/`, and `cli.py` modules.
- **TUI Testing:** Textual's built-in `App.run_test()` pilot API for simulating keypresses and verifying screen state.
- **Database:** All tests use in-memory SQLite (`:memory:`) via a shared fixture — no filesystem side effects.

### Unit Tests (100% coverage)
Target modules: `db/`, `timer/`, `cli.py`.

| Module | Test File | What's Covered |
| :--- | :--- | :--- |
| `db/connection.py` | `tests/test_connection.py` | Schema creation, seed data insertion (only on empty tables), `PRAGMA foreign_keys` enabled. |
| `db/queries.py` | `tests/test_queries.py` | All CRUD operations for projects, tasks, categories. Soft-delete cascades (project → tasks). Time entry insert/update/delete. Reporting aggregation queries (daily totals, weekly date-range). Edge cases: empty tables, duplicate names, deleted entities in reports. |
| `db/models.py` | `tests/test_models.py` | Dataclass construction, field defaults. |
| `timer/engine.py` | `tests/test_engine.py` | `start_timer`: inserts active session, auto-stops previous. `stop_timer`: saves entry, clears session. Midnight split: single split, multi-day split. Crash recovery: orphaned session saved with `now()`, midnight-split applied. |
| `cli.py` | `tests/test_cli.py` | `--status` with active timer: correct format `Project > Task > Category \| HH:MM:SS`. `--status` with no timer: outputs `Timer Stopped`. |

### Integration Tests
Target: full user flows through the Textual TUI using `App.run_test()`.

| Test File | Flow |
| :--- | :--- |
| `tests/integration/test_timer_flow.py` | Launch app → select project/task/category → start timer → verify running display → stop timer → verify entry saved in daily log. |
| `tests/integration/test_crud_flow.py` | Navigate to `:projects` → add project → edit project → delete project (soft) → verify cascade to tasks. Same for categories. |
| `tests/integration/test_navigation.py` | Command mode: type `:daily`, `:weekly`, `:projects`, `:categories`, `:timer` → verify correct screen is displayed. Keyboard shortcuts: `a`, `e`, `d` trigger modals. `Esc` closes modals. |
| `tests/integration/test_reports.py` | Seed time entries → navigate to `:daily` → verify log and totals. Navigate to `:weekly` → verify bar chart and breakdowns. Historical week navigation with arrow keys. |

### Test Directory Structure
```
tests/
├── conftest.py                      # Shared fixtures: in-memory DB, seeded data, app instance
├── test_connection.py
├── test_models.py
├── test_queries.py
├── test_engine.py
├── test_cli.py
└── integration/
    ├── __init__.py
    ├── conftest.py                  # Integration fixtures: App.run_test() helpers
    ├── test_timer_flow.py
    ├── test_crud_flow.py
    ├── test_navigation.py
    └── test_reports.py
```

### CI Enforcement
- Unit tests run on every commit.
- Coverage gate: `pytest --cov=devflow --cov-fail-under=100 --cov-report=term-missing` for `db/`, `timer/`, `cli.py`.
- Integration tests run as a separate step (may be slower due to TUI rendering).
