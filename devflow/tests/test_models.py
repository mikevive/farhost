"""Tests for data model dataclasses."""

from devflow.db.models import ActiveSession, Category, Project, Task, TimeEntry


def test_project_defaults():
    p = Project(id=1, name="Test")
    assert p.archived_at is None


def test_task_defaults():
    t = Task(id=1, project_id=1, name="Test")
    assert t.archived_at is None


def test_category_defaults():
    c = Category(id=1, name="Test")
    assert c.archived_at is None


def test_time_entry_fields():
    e = TimeEntry(
        id=1, task_id=1, category_id=1,
        start="2024-01-01 09:00:00", end="2024-01-01 10:00:00",
        duration_seconds=3600,
    )
    assert e.duration_seconds == 3600


def test_active_session_fields():
    s = ActiveSession(id=1, task_id=1, category_id=1, start_time="2024-01-01 09:00:00")
    assert s.start_time == "2024-01-01 09:00:00"


def test_project_with_archived():
    p = Project(id=1, name="Test", archived_at="2024-01-01 12:00:00")
    assert p.archived_at == "2024-01-01 12:00:00"
