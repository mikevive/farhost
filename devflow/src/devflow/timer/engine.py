"""Timer business logic: start, stop, midnight split, crash recovery."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta

from devflow.db import queries
from devflow.db.models import ActiveSession, TimeEntry


def start_timer(
    conn: sqlite3.Connection, task_id: int, category_id: int
) -> ActiveSession:
    """Start a new timer. Auto-stops any running timer first."""
    existing = queries.get_active_session(conn)
    if existing:
        stop_timer(conn)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return queries.set_active_session(conn, task_id, category_id, now)


def stop_timer(conn: sqlite3.Connection) -> list[TimeEntry]:
    """Stop the running timer and save time entries (with midnight splits).

    Returns the list of created time entries.
    """
    session = queries.get_active_session(conn)
    if session is None:
        return []

    now = datetime.now()
    start = datetime.strptime(session.start_time, "%Y-%m-%d %H:%M:%S")

    entries = _create_entries_with_midnight_split(
        conn, session.task_id, session.category_id, start, now
    )
    queries.clear_active_session(conn)
    return entries


def recover_crashed_session(conn: sqlite3.Connection) -> list[TimeEntry]:
    """Recover an orphaned active session on startup.

    Keeps the session running, but handles midnight splits if needed.
    Returns any entries created by splits.
    """
    return check_midnight_split(conn)


def check_midnight_split(conn: sqlite3.Connection) -> list[TimeEntry]:
    """Check if the active timer crossed midnight and split if needed.

    Called periodically (e.g., every minute) and on startup. If the current
    date differs from the session's start date, splits the timer at each
    midnight boundary and continues the session for today.

    Returns any entries created by the split.
    """
    session = queries.get_active_session(conn)
    if session is None:
        return []

    start = datetime.strptime(session.start_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    if start.date() == now.date():
        return []

    # Split: save all entries up to today's midnight
    today_midnight = datetime.combine(now.date(), datetime.min.time())
    entries = _create_entries_with_midnight_split(
        conn, session.task_id, session.category_id, start, today_midnight
    )

    # Start new session at midnight of today so it continues running
    today_str = today_midnight.strftime("%Y-%m-%d %H:%M:%S")
    queries.set_active_session(conn, session.task_id, session.category_id, today_str)

    return entries


def _create_entries_with_midnight_split(
    conn: sqlite3.Connection,
    task_id: int,
    category_id: int,
    start: datetime,
    end: datetime,
) -> list[TimeEntry]:
    """Create time entries, splitting at each midnight boundary."""
    entries: list[TimeEntry] = []

    current_start = start
    while current_start.date() < end.date():
        # End of day: 23:59:59
        day_end = datetime.combine(
            current_start.date(), datetime.max.time().replace(microsecond=0)
        )
        entry = _save_entry(conn, task_id, category_id, current_start, day_end)
        entries.append(entry)

        # Next day starts at 00:00:00
        current_start = datetime.combine(
            current_start.date() + timedelta(days=1), datetime.min.time()
        )

    # Final segment (same day)
    if current_start < end:
        entry = _save_entry(conn, task_id, category_id, current_start, end)
        entries.append(entry)

    return entries


def _save_entry(
    conn: sqlite3.Connection,
    task_id: int,
    category_id: int,
    start: datetime,
    end: datetime,
) -> TimeEntry:
    duration = int((end - start).total_seconds())
    return queries.create_time_entry(
        conn,
        task_id=task_id,
        category_id=category_id,
        start=start.strftime("%Y-%m-%d %H:%M:%S"),
        end=end.strftime("%Y-%m-%d %H:%M:%S"),
        duration_seconds=duration,
    )
