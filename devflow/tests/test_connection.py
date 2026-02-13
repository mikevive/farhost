"""Tests for database connection, schema creation, and seed data."""

from devflow.db.connection import get_memory_connection, _SEED_CATEGORIES, _SEED_PROJECTS


def test_schema_creates_tables():
    conn = get_memory_connection()
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    table_names = [r["name"] for r in tables]
    assert "categories" in table_names
    assert "projects" in table_names
    assert "tasks" in table_names
    assert "time_entries" in table_names
    assert "active_session" in table_names
    conn.close()


def test_seed_data_projects():
    conn = get_memory_connection()
    rows = conn.execute("SELECT name FROM projects ORDER BY name").fetchall()
    names = [r["name"] for r in rows]
    assert names == sorted(_SEED_PROJECTS)
    conn.close()


def test_seed_data_categories():
    conn = get_memory_connection()
    rows = conn.execute("SELECT name FROM categories ORDER BY name").fetchall()
    names = [r["name"] for r in rows]
    assert names == sorted(_SEED_CATEGORIES)
    conn.close()


def test_seed_data_not_duplicated():
    conn = get_memory_connection()
    count_before = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    # Re-seeding should not duplicate
    from devflow.db.connection import _seed_data
    _seed_data(conn)
    count_after = conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    assert count_before == count_after
    conn.close()


def test_foreign_keys_enabled():
    conn = get_memory_connection()
    result = conn.execute("PRAGMA foreign_keys").fetchone()
    assert result[0] == 1
    conn.close()


def test_indexes_created():
    conn = get_memory_connection()
    indexes = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
    ).fetchall()
    idx_names = {r["name"] for r in indexes}
    assert "idx_time_entries_start" in idx_names
    assert "idx_time_entries_task_id" in idx_names
    assert "idx_time_entries_category_id" in idx_names
    assert "idx_tasks_project_id" in idx_names
    conn.close()


def test_active_session_check_constraint():
    """active_session.id must be 1."""
    conn = get_memory_connection()
    # First need a task and category to reference
    project_id = conn.execute("SELECT id FROM projects LIMIT 1").fetchone()[0]
    conn.execute("INSERT INTO tasks (project_id, name) VALUES (?, 'test')", (project_id,))
    task_id = conn.execute("SELECT id FROM tasks LIMIT 1").fetchone()[0]
    cat_id = conn.execute("SELECT id FROM categories LIMIT 1").fetchone()[0]

    # id=1 should work
    conn.execute(
        "INSERT INTO active_session (id, task_id, category_id, start_time) VALUES (1, ?, ?, '2024-01-01 00:00:00')",
        (task_id, cat_id),
    )
    conn.commit()

    # id=2 should fail
    import sqlite3
    import pytest
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO active_session (id, task_id, category_id, start_time) VALUES (2, ?, ?, '2024-01-01 00:00:00')",
            (task_id, cat_id),
        )
    conn.close()
