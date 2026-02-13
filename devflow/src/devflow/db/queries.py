"""Data access layer: all CRUD and reporting SQL queries."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from devflow.db.models import (
    ActiveSession,
    Category,
    Project,
    Task,
    TimeEntry,
)


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

def list_projects(conn: sqlite3.Connection, *, include_archived: bool = False) -> list[Project]:
    if include_archived:
        rows = conn.execute(
            "SELECT id, name, archived_at FROM projects WHERE archived_at IS NOT NULL ORDER BY name ASC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, archived_at FROM projects WHERE archived_at IS NULL ORDER BY name ASC"
        ).fetchall()
    return [Project(**dict(r)) for r in rows]


def get_project(conn: sqlite3.Connection, project_id: int) -> Project | None:
    row = conn.execute(
        "SELECT id, name, archived_at FROM projects WHERE id = ?", (project_id,)
    ).fetchone()
    return Project(**dict(row)) if row else None


def create_project(conn: sqlite3.Connection, name: str) -> Project:
    cursor = conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
    conn.commit()
    return Project(id=cursor.lastrowid, name=name)


def update_project(conn: sqlite3.Connection, project_id: int, name: str) -> None:
    conn.execute("UPDATE projects SET name = ? WHERE id = ?", (name, project_id))
    conn.commit()


def archive_project(conn: sqlite3.Connection, project_id: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("UPDATE projects SET archived_at = ? WHERE id = ?", (now, project_id))
    conn.execute(
        "UPDATE tasks SET archived_at = ? WHERE project_id = ? AND archived_at IS NULL",
        (now, project_id),
    )
    # Stop active session if it references a task in this project
    conn.execute(
        "DELETE FROM active_session WHERE task_id IN "
        "(SELECT id FROM tasks WHERE project_id = ?)",
        (project_id,),
    )
    conn.commit()


def restore_project(conn: sqlite3.Connection, project_id: int) -> None:
    project = get_project(conn, project_id)
    if project and project.archived_at:
        conn.execute(
            "UPDATE tasks SET archived_at = NULL WHERE project_id = ? AND archived_at = ?",
            (project_id, project.archived_at),
        )
        conn.execute("UPDATE projects SET archived_at = NULL WHERE id = ?", (project_id,))
        conn.commit()


# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------

def list_tasks(
    conn: sqlite3.Connection,
    project_id: int,
    *,
    include_archived: bool = False,
) -> list[Task]:
    if include_archived:
        rows = conn.execute(
            "SELECT id, project_id, name, archived_at FROM tasks "
            "WHERE project_id = ? AND archived_at IS NOT NULL ORDER BY name ASC",
            (project_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, project_id, name, archived_at FROM tasks "
            "WHERE project_id = ? AND archived_at IS NULL ORDER BY name ASC",
            (project_id,),
        ).fetchall()
    return [Task(**dict(r)) for r in rows]


def get_task(conn: sqlite3.Connection, task_id: int) -> Task | None:
    row = conn.execute(
        "SELECT id, project_id, name, archived_at FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    return Task(**dict(row)) if row else None


def create_task(conn: sqlite3.Connection, project_id: int, name: str) -> Task:
    cursor = conn.execute(
        "INSERT INTO tasks (project_id, name) VALUES (?, ?)", (project_id, name)
    )
    conn.commit()
    return Task(id=cursor.lastrowid, project_id=project_id, name=name)


def update_task(conn: sqlite3.Connection, task_id: int, name: str) -> None:
    conn.execute("UPDATE tasks SET name = ? WHERE id = ?", (name, task_id))
    conn.commit()


def archive_task(conn: sqlite3.Connection, task_id: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("UPDATE tasks SET archived_at = ? WHERE id = ?", (now, task_id))
    conn.execute("DELETE FROM active_session WHERE task_id = ?", (task_id,))
    conn.commit()


def restore_task(conn: sqlite3.Connection, task_id: int) -> None:
    conn.execute("UPDATE tasks SET archived_at = NULL WHERE id = ?", (task_id,))
    conn.commit()


# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

def list_categories(
    conn: sqlite3.Connection, *, include_archived: bool = False
) -> list[Category]:
    if include_archived:
        rows = conn.execute(
            "SELECT id, name, archived_at FROM categories WHERE archived_at IS NOT NULL ORDER BY name ASC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, archived_at FROM categories WHERE archived_at IS NULL ORDER BY name ASC"
        ).fetchall()
    return [Category(**dict(r)) for r in rows]


def get_category(conn: sqlite3.Connection, category_id: int) -> Category | None:
    row = conn.execute(
        "SELECT id, name, archived_at FROM categories WHERE id = ?", (category_id,)
    ).fetchone()
    return Category(**dict(row)) if row else None


def create_category(conn: sqlite3.Connection, name: str) -> Category:
    cursor = conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    return Category(id=cursor.lastrowid, name=name)


def update_category(conn: sqlite3.Connection, category_id: int, name: str) -> None:
    conn.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
    conn.commit()


def archive_category(conn: sqlite3.Connection, category_id: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute("UPDATE categories SET archived_at = ? WHERE id = ?", (now, category_id))
    conn.execute("DELETE FROM active_session WHERE category_id = ?", (category_id,))
    conn.commit()


def restore_category(conn: sqlite3.Connection, category_id: int) -> None:
    conn.execute("UPDATE categories SET archived_at = NULL WHERE id = ?", (category_id,))
    conn.commit()


# ---------------------------------------------------------------------------
# Time Entries
# ---------------------------------------------------------------------------

def list_time_entries_for_date(conn: sqlite3.Connection, date_str: str) -> list[TimeEntry]:
    """Get all time entries for a given date (YYYY-MM-DD), sorted chronologically."""
    rows = conn.execute(
        "SELECT id, task_id, category_id, start, end, duration_seconds "
        "FROM time_entries WHERE date(start) = ? ORDER BY start ASC",
        (date_str,),
    ).fetchall()
    return [TimeEntry(**dict(r)) for r in rows]


def list_time_entries_for_range(
    conn: sqlite3.Connection, start: str, end: str
) -> list[TimeEntry]:
    """Get all time entries within a date range [start, end), sorted chronologically."""
    rows = conn.execute(
        "SELECT id, task_id, category_id, start, end, duration_seconds "
        "FROM time_entries WHERE start >= ? AND start < ? ORDER BY start ASC",
        (start, end),
    ).fetchall()
    return [TimeEntry(**dict(r)) for r in rows]


def create_time_entry(
    conn: sqlite3.Connection,
    task_id: int,
    category_id: int,
    start: str,
    end: str,
    duration_seconds: int,
) -> TimeEntry:
    cursor = conn.execute(
        "INSERT INTO time_entries (task_id, category_id, start, end, duration_seconds) "
        "VALUES (?, ?, ?, ?, ?)",
        (task_id, category_id, start, end, duration_seconds),
    )
    conn.commit()
    return TimeEntry(
        id=cursor.lastrowid,
        task_id=task_id,
        category_id=category_id,
        start=start,
        end=end,
        duration_seconds=duration_seconds,
    )


def update_time_entry(
    conn: sqlite3.Connection,
    entry_id: int,
    *,
    task_id: int | None = None,
    category_id: int | None = None,
    start: str | None = None,
    end: str | None = None,
) -> None:
    entry = get_time_entry(conn, entry_id)
    if entry is None:
        return

    new_task_id = task_id if task_id is not None else entry.task_id
    new_category_id = category_id if category_id is not None else entry.category_id
    new_start = start if start is not None else entry.start
    new_end = end if end is not None else entry.end

    start_dt = datetime.strptime(new_start, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(new_end, "%Y-%m-%d %H:%M:%S")
    new_duration = int((end_dt - start_dt).total_seconds())

    conn.execute(
        "UPDATE time_entries SET task_id = ?, category_id = ?, start = ?, end = ?, "
        "duration_seconds = ? WHERE id = ?",
        (new_task_id, new_category_id, new_start, new_end, new_duration, entry_id),
    )
    conn.commit()


def get_time_entry(conn: sqlite3.Connection, entry_id: int) -> TimeEntry | None:
    row = conn.execute(
        "SELECT id, task_id, category_id, start, end, duration_seconds "
        "FROM time_entries WHERE id = ?",
        (entry_id,),
    ).fetchone()
    return TimeEntry(**dict(row)) if row else None


def delete_time_entry(conn: sqlite3.Connection, entry_id: int) -> None:
    """Hard-delete a time entry (permanent)."""
    conn.execute("DELETE FROM time_entries WHERE id = ?", (entry_id,))
    conn.commit()


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def daily_totals_by_project(
    conn: sqlite3.Connection, date_str: str
) -> list[tuple[str, int]]:
    """Return (project_name, total_seconds) pairs for a given date."""
    rows = conn.execute(
        "SELECT p.name, SUM(te.duration_seconds) as total "
        "FROM time_entries te "
        "JOIN tasks t ON te.task_id = t.id "
        "JOIN projects p ON t.project_id = p.id "
        "WHERE date(te.start) = ? "
        "GROUP BY p.name ORDER BY p.name ASC",
        (date_str,),
    ).fetchall()
    return [(row["name"], row["total"]) for row in rows]


def daily_totals_by_category(
    conn: sqlite3.Connection, date_str: str
) -> list[tuple[str, int]]:
    """Return (category_name, total_seconds) pairs for a given date."""
    rows = conn.execute(
        "SELECT c.name, SUM(te.duration_seconds) as total "
        "FROM time_entries te "
        "JOIN categories c ON te.category_id = c.id "
        "WHERE date(te.start) = ? "
        "GROUP BY c.name ORDER BY c.name ASC",
        (date_str,),
    ).fetchall()
    return [(row["name"], row["total"]) for row in rows]


def weekly_totals_by_day(
    conn: sqlite3.Connection, week_start: str, week_end: str
) -> list[tuple[str, int]]:
    """Return (date_str, total_seconds) pairs for each day in the range [start, end)."""
    rows = conn.execute(
        "SELECT date(start) as day, SUM(duration_seconds) as total "
        "FROM time_entries "
        "WHERE start >= ? AND start < ? "
        "GROUP BY date(start) ORDER BY day ASC",
        (week_start, week_end),
    ).fetchall()
    return [(row["day"], row["total"]) for row in rows]


def weekly_totals_by_project(
    conn: sqlite3.Connection, week_start: str, week_end: str
) -> list[tuple[str, int]]:
    """Return (project_name, total_seconds) for a week range [start, end)."""
    rows = conn.execute(
        "SELECT p.name, SUM(te.duration_seconds) as total "
        "FROM time_entries te "
        "JOIN tasks t ON te.task_id = t.id "
        "JOIN projects p ON t.project_id = p.id "
        "WHERE te.start >= ? AND te.start < ? "
        "GROUP BY p.name ORDER BY p.name ASC",
        (week_start, week_end),
    ).fetchall()
    return [(row["name"], row["total"]) for row in rows]


def weekly_totals_by_category(
    conn: sqlite3.Connection, week_start: str, week_end: str
) -> list[tuple[str, int]]:
    """Return (category_name, total_seconds) for a week range [start, end)."""
    rows = conn.execute(
        "SELECT c.name, SUM(te.duration_seconds) as total "
        "FROM time_entries te "
        "JOIN categories c ON te.category_id = c.id "
        "WHERE te.start >= ? AND te.start < ? "
        "GROUP BY c.name ORDER BY c.name ASC",
        (week_start, week_end),
    ).fetchall()
    return [(row["name"], row["total"]) for row in rows]


# ---------------------------------------------------------------------------
# Active Session
# ---------------------------------------------------------------------------

def get_active_session(conn: sqlite3.Connection) -> ActiveSession | None:
    row = conn.execute(
        "SELECT id, task_id, category_id, start_time FROM active_session"
    ).fetchone()
    return ActiveSession(**dict(row)) if row else None


def set_active_session(
    conn: sqlite3.Connection, task_id: int, category_id: int, start_time: str
) -> ActiveSession:
    conn.execute("DELETE FROM active_session")
    conn.execute(
        "INSERT INTO active_session (id, task_id, category_id, start_time) VALUES (1, ?, ?, ?)",
        (task_id, category_id, start_time),
    )
    conn.commit()
    return ActiveSession(id=1, task_id=task_id, category_id=category_id, start_time=start_time)


def clear_active_session(conn: sqlite3.Connection) -> None:
    conn.execute("DELETE FROM active_session")
    conn.commit()
