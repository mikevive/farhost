"""Headless CLI logic for --status flag."""

from __future__ import annotations

import sqlite3
from datetime import datetime

from devflow.db import queries


def print_status(conn: sqlite3.Connection) -> str:
    """Return the status string for the active timer, or 'Timer Stopped'."""
    session = queries.get_active_session(conn)
    if session is None:
        return "Timer Stopped"

    task = queries.get_task(conn, session.task_id)
    category = queries.get_category(conn, session.category_id)

    if task is None or category is None:
        return "Timer Stopped"

    from devflow.db import queries as q

    project = q.get_project(conn, task.project_id)
    project_name = project.name if project else "Unknown"

    start = datetime.strptime(session.start_time, "%Y-%m-%d %H:%M:%S")
    elapsed = datetime.now() - start
    total_seconds = int(elapsed.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{project_name} > {task.name} > {category.name} | {hours:02d}:{minutes:02d}:{seconds:02d}"
