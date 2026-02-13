"""Tests for the CLI --status headless output."""

from datetime import datetime, timedelta
from unittest.mock import patch

from devflow.cli import print_status
from devflow.db import queries


def test_status_no_timer(conn):
    result = print_status(conn)
    assert result == "Timer Stopped"


def test_status_with_active_timer(conn):
    p = queries.create_project(conn, "StatusP")
    t = queries.create_task(conn, p.id, "StatusT")
    c = queries.list_categories(conn)[0]

    start = (datetime.now() - timedelta(hours=1, minutes=23, seconds=45)).strftime("%Y-%m-%d %H:%M:%S")
    queries.set_active_session(conn, t.id, c.id, start)

    result = print_status(conn)
    assert "StatusP" in result
    assert "StatusT" in result
    assert c.name in result
    assert "|" in result
    # Check format: should contain HH:MM:SS
    parts = result.split("|")
    time_part = parts[1].strip()
    assert len(time_part.split(":")) == 3


def test_status_format(conn):
    p = queries.create_project(conn, "FmtP")
    t = queries.create_task(conn, p.id, "FmtT")
    c = queries.create_category(conn, "FmtC")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    queries.set_active_session(conn, t.id, c.id, now)

    result = print_status(conn)
    assert result.startswith("FmtP > FmtT > FmtC |")


def test_status_missing_task(conn):
    """Edge case: session references a task/category that no longer resolves."""
    p = queries.create_project(conn, "MissP")
    t = queries.create_task(conn, p.id, "MissT")
    c = queries.list_categories(conn)[0]

    # Insert a session referencing valid IDs, then disable FK checks to
    # simulate a corrupted state where the task row is gone.
    queries.set_active_session(conn, t.id, c.id, "2024-01-15 09:00:00")
    conn.execute("PRAGMA foreign_keys = OFF")
    conn.execute("DELETE FROM tasks WHERE id = ?", (t.id,))
    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON")

    result = print_status(conn)
    assert result == "Timer Stopped"
