"""Database connection factory, schema initialization, and seed data."""

from __future__ import annotations

import sqlite3
from pathlib import Path

_DEFAULT_DB_PATH = Path.home() / ".farhost" / "devflow" / "devflow.db"

_SEED_PROJECTS = [
    "Architecture",
    "Platform",
    "Product",
    "Team",
]

_SEED_CATEGORIES = [
    "Admin",
    "Break",
    "Burnout",
    "Code",
    "Code review",
    "Communication",
    "Daily planning",
    "Distraction",
    "Improvements",
    "Interviewing",
    "Learning",
    "Long-term planning",
    "Meeting",
    "Mentorship",
    "Research",
    "Support",
    "System Design",
]


def _schema_sql() -> str:
    schema_path = Path(__file__).parent / "schema.sql"
    return schema_path.read_text()


def get_connection(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Create and return a database connection with schema initialized."""
    if db_path is None:
        db_path = _DEFAULT_DB_PATH

    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    conn.executescript(_schema_sql())
    _seed_data(conn)

    return conn


def get_memory_connection() -> sqlite3.Connection:
    """Create an in-memory database connection for testing."""
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    conn.executescript(_schema_sql())
    _seed_data(conn)

    return conn


def _seed_data(conn: sqlite3.Connection) -> None:
    """Insert default projects and categories if tables are empty."""
    cursor = conn.execute("SELECT COUNT(*) FROM projects")
    if cursor.fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO projects (name) VALUES (?)",
            [(name,) for name in _SEED_PROJECTS],
        )

    cursor = conn.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO categories (name) VALUES (?)",
            [(name,) for name in _SEED_CATEGORIES],
        )

    conn.commit()
