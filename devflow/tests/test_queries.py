"""Tests for the data access layer (queries.py)."""

import pytest

from devflow.db import queries


# ---------------------------------------------------------------------------
# Projects CRUD
# ---------------------------------------------------------------------------

class TestProjectsCRUD:
    def test_list_projects_seeded(self, conn):
        projects = queries.list_projects(conn)
        assert len(projects) == 4
        # Should be alphabetical
        names = [p.name for p in projects]
        assert names == sorted(names)

    def test_create_project(self, conn):
        p = queries.create_project(conn, "NewProject")
        assert p.name == "NewProject"
        assert p.id is not None

    def test_get_project(self, conn):
        p = queries.create_project(conn, "GetMe")
        fetched = queries.get_project(conn, p.id)
        assert fetched is not None
        assert fetched.name == "GetMe"

    def test_get_project_not_found(self, conn):
        assert queries.get_project(conn, 99999) is None

    def test_update_project(self, conn):
        p = queries.create_project(conn, "Old")
        queries.update_project(conn, p.id, "New")
        fetched = queries.get_project(conn, p.id)
        assert fetched.name == "New"

    def test_archive_project(self, conn):
        p = queries.create_project(conn, "ToArchive")
        task = queries.create_task(conn, p.id, "Task1")
        queries.archive_project(conn, p.id)

        # Project should not appear in active list
        active = queries.list_projects(conn)
        assert all(proj.id != p.id for proj in active)

        # Should appear in archived list
        archived = queries.list_projects(conn, include_archived=True)
        assert any(proj.id == p.id for proj in archived)

        # Task should also be archived
        active_tasks = queries.list_tasks(conn, p.id)
        assert len(active_tasks) == 0

    def test_archive_project_stops_active_session(self, conn):
        p = queries.create_project(conn, "SessionProject")
        task = queries.create_task(conn, p.id, "SessionTask")
        cat = queries.list_categories(conn)[0]
        queries.set_active_session(conn, task.id, cat.id, "2024-01-01 09:00:00")

        queries.archive_project(conn, p.id)
        assert queries.get_active_session(conn) is None

    def test_restore_project(self, conn):
        p = queries.create_project(conn, "RestoreMe")
        task = queries.create_task(conn, p.id, "Task1")
        queries.archive_project(conn, p.id)
        queries.restore_project(conn, p.id)

        active = queries.list_projects(conn)
        assert any(proj.id == p.id for proj in active)

        active_tasks = queries.list_tasks(conn, p.id)
        assert len(active_tasks) == 1


# ---------------------------------------------------------------------------
# Tasks CRUD
# ---------------------------------------------------------------------------

class TestTasksCRUD:
    def test_create_and_list_tasks(self, conn):
        p = queries.create_project(conn, "TaskProject")
        t1 = queries.create_task(conn, p.id, "Zebra")
        t2 = queries.create_task(conn, p.id, "Alpha")

        tasks = queries.list_tasks(conn, p.id)
        assert len(tasks) == 2
        assert tasks[0].name == "Alpha"
        assert tasks[1].name == "Zebra"

    def test_get_task(self, conn):
        p = queries.create_project(conn, "P")
        t = queries.create_task(conn, p.id, "GetTask")
        fetched = queries.get_task(conn, t.id)
        assert fetched is not None
        assert fetched.name == "GetTask"

    def test_get_task_not_found(self, conn):
        assert queries.get_task(conn, 99999) is None

    def test_update_task(self, conn):
        p = queries.create_project(conn, "P2")
        t = queries.create_task(conn, p.id, "OldTask")
        queries.update_task(conn, t.id, "NewTask")
        fetched = queries.get_task(conn, t.id)
        assert fetched.name == "NewTask"

    def test_archive_task(self, conn):
        p = queries.create_project(conn, "P3")
        t = queries.create_task(conn, p.id, "ArchiveTask")
        queries.archive_task(conn, t.id)

        active = queries.list_tasks(conn, p.id)
        assert len(active) == 0

        archived = queries.list_tasks(conn, p.id, include_archived=True)
        assert len(archived) == 1

    def test_archive_task_stops_active_session(self, conn):
        p = queries.create_project(conn, "P4")
        t = queries.create_task(conn, p.id, "T")
        cat = queries.list_categories(conn)[0]
        queries.set_active_session(conn, t.id, cat.id, "2024-01-01 09:00:00")

        queries.archive_task(conn, t.id)
        assert queries.get_active_session(conn) is None

    def test_restore_task(self, conn):
        p = queries.create_project(conn, "P5")
        t = queries.create_task(conn, p.id, "RestoreTask")
        queries.archive_task(conn, t.id)
        queries.restore_task(conn, t.id)

        active = queries.list_tasks(conn, p.id)
        assert len(active) == 1


# ---------------------------------------------------------------------------
# Categories CRUD
# ---------------------------------------------------------------------------

class TestCategoriesCRUD:
    def test_list_categories_seeded(self, conn):
        cats = queries.list_categories(conn)
        assert len(cats) == 17
        names = [c.name for c in cats]
        assert names == sorted(names)

    def test_create_category(self, conn):
        c = queries.create_category(conn, "NewCat")
        assert c.name == "NewCat"

    def test_get_category(self, conn):
        c = queries.create_category(conn, "GetCat")
        fetched = queries.get_category(conn, c.id)
        assert fetched is not None
        assert fetched.name == "GetCat"

    def test_get_category_not_found(self, conn):
        assert queries.get_category(conn, 99999) is None

    def test_update_category(self, conn):
        c = queries.create_category(conn, "OldCat")
        queries.update_category(conn, c.id, "NewCat2")
        fetched = queries.get_category(conn, c.id)
        assert fetched.name == "NewCat2"

    def test_archive_category(self, conn):
        c = queries.create_category(conn, "ArchCat")
        queries.archive_category(conn, c.id)

        active = queries.list_categories(conn)
        assert all(cat.id != c.id for cat in active)

        archived = queries.list_categories(conn, include_archived=True)
        assert any(cat.id == c.id for cat in archived)

    def test_archive_category_stops_active_session(self, conn):
        p = queries.create_project(conn, "CatP")
        t = queries.create_task(conn, p.id, "CatT")
        c = queries.create_category(conn, "CatToArchive")
        queries.set_active_session(conn, t.id, c.id, "2024-01-01 09:00:00")

        queries.archive_category(conn, c.id)
        assert queries.get_active_session(conn) is None

    def test_restore_category(self, conn):
        c = queries.create_category(conn, "RestoreCat")
        queries.archive_category(conn, c.id)
        queries.restore_category(conn, c.id)

        active = queries.list_categories(conn)
        assert any(cat.id == c.id for cat in active)


# ---------------------------------------------------------------------------
# Time Entries
# ---------------------------------------------------------------------------

class TestTimeEntries:
    def _setup_entry(self, conn):
        p = queries.create_project(conn, "EntryP")
        t = queries.create_task(conn, p.id, "EntryT")
        c = queries.list_categories(conn)[0]
        return t.id, c.id

    def test_create_and_get_entry(self, conn):
        tid, cid = self._setup_entry(conn)
        e = queries.create_time_entry(conn, tid, cid, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 3600)
        fetched = queries.get_time_entry(conn, e.id)
        assert fetched is not None
        assert fetched.duration_seconds == 3600

    def test_get_entry_not_found(self, conn):
        assert queries.get_time_entry(conn, 99999) is None

    def test_list_entries_for_date(self, conn):
        tid, cid = self._setup_entry(conn)
        queries.create_time_entry(conn, tid, cid, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 3600)
        queries.create_time_entry(conn, tid, cid, "2024-01-15 14:00:00", "2024-01-15 15:00:00", 3600)
        queries.create_time_entry(conn, tid, cid, "2024-01-16 09:00:00", "2024-01-16 10:00:00", 3600)

        entries = queries.list_time_entries_for_date(conn, "2024-01-15")
        assert len(entries) == 2

    def test_list_entries_for_range(self, conn):
        tid, cid = self._setup_entry(conn)
        queries.create_time_entry(conn, tid, cid, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 3600)
        queries.create_time_entry(conn, tid, cid, "2024-01-17 09:00:00", "2024-01-17 10:00:00", 3600)

        entries = queries.list_time_entries_for_range(conn, "2024-01-15 00:00:00", "2024-01-16 00:00:00")
        assert len(entries) == 1

    def test_update_entry(self, conn):
        tid, cid = self._setup_entry(conn)
        e = queries.create_time_entry(conn, tid, cid, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 3600)
        queries.update_time_entry(conn, e.id, start="2024-01-15 08:00:00", end="2024-01-15 10:00:00")
        fetched = queries.get_time_entry(conn, e.id)
        assert fetched.duration_seconds == 7200

    def test_update_entry_not_found(self, conn):
        # Should not raise
        queries.update_time_entry(conn, 99999, start="2024-01-01 00:00:00")

    def test_delete_entry(self, conn):
        tid, cid = self._setup_entry(conn)
        e = queries.create_time_entry(conn, tid, cid, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 3600)
        queries.delete_time_entry(conn, e.id)
        assert queries.get_time_entry(conn, e.id) is None

    def test_entries_for_empty_date(self, conn):
        entries = queries.list_time_entries_for_date(conn, "2099-01-01")
        assert entries == []


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

class TestReporting:
    def _seed_entries(self, conn):
        p1 = queries.create_project(conn, "ReportP1")
        p2 = queries.create_project(conn, "ReportP2")
        t1 = queries.create_task(conn, p1.id, "T1")
        t2 = queries.create_task(conn, p2.id, "T2")
        cats = queries.list_categories(conn)
        c1, c2 = cats[0], cats[1]

        queries.create_time_entry(conn, t1.id, c1.id, "2024-01-15 09:00:00", "2024-01-15 11:00:00", 7200)
        queries.create_time_entry(conn, t2.id, c2.id, "2024-01-15 13:00:00", "2024-01-15 14:00:00", 3600)
        queries.create_time_entry(conn, t1.id, c1.id, "2024-01-16 09:00:00", "2024-01-16 10:00:00", 3600)

    def test_daily_totals_by_project(self, conn):
        self._seed_entries(conn)
        totals = queries.daily_totals_by_project(conn, "2024-01-15")
        assert len(totals) == 2
        total_map = dict(totals)
        assert total_map["ReportP1"] == 7200
        assert total_map["ReportP2"] == 3600

    def test_daily_totals_by_category(self, conn):
        self._seed_entries(conn)
        totals = queries.daily_totals_by_category(conn, "2024-01-15")
        assert len(totals) == 2

    def test_weekly_totals_by_day(self, conn):
        self._seed_entries(conn)
        totals = queries.weekly_totals_by_day(conn, "2024-01-15 00:00:00", "2024-01-22 00:00:00")
        day_map = dict(totals)
        assert day_map["2024-01-15"] == 10800
        assert day_map["2024-01-16"] == 3600

    def test_weekly_totals_by_project(self, conn):
        self._seed_entries(conn)
        totals = queries.weekly_totals_by_project(conn, "2024-01-15 00:00:00", "2024-01-22 00:00:00")
        assert len(totals) == 2

    def test_weekly_totals_by_category(self, conn):
        self._seed_entries(conn)
        totals = queries.weekly_totals_by_category(conn, "2024-01-15 00:00:00", "2024-01-22 00:00:00")
        assert len(totals) == 2

    def test_daily_totals_empty(self, conn):
        totals = queries.daily_totals_by_project(conn, "2099-01-01")
        assert totals == []

    def test_reports_include_archived_entities(self, conn):
        """Archived projects/categories should still appear in reports."""
        p = queries.create_project(conn, "ArchiveReportP")
        t = queries.create_task(conn, p.id, "ART")
        c = queries.create_category(conn, "ArchiveReportC")
        queries.create_time_entry(conn, t.id, c.id, "2024-01-15 09:00:00", "2024-01-15 10:00:00", 3600)

        queries.archive_project(conn, p.id)
        queries.archive_category(conn, c.id)

        totals = queries.daily_totals_by_project(conn, "2024-01-15")
        total_map = dict(totals)
        assert "ArchiveReportP" in total_map


# ---------------------------------------------------------------------------
# Active Session
# ---------------------------------------------------------------------------

class TestActiveSession:
    def test_no_active_session(self, conn):
        assert queries.get_active_session(conn) is None

    def test_set_and_get_session(self, conn):
        p = queries.create_project(conn, "SP")
        t = queries.create_task(conn, p.id, "ST")
        c = queries.list_categories(conn)[0]
        session = queries.set_active_session(conn, t.id, c.id, "2024-01-15 09:00:00")
        assert session.id == 1

        fetched = queries.get_active_session(conn)
        assert fetched is not None
        assert fetched.task_id == t.id

    def test_set_replaces_existing(self, conn):
        p = queries.create_project(conn, "SP2")
        t1 = queries.create_task(conn, p.id, "ST1")
        t2 = queries.create_task(conn, p.id, "ST2")
        c = queries.list_categories(conn)[0]

        queries.set_active_session(conn, t1.id, c.id, "2024-01-15 09:00:00")
        queries.set_active_session(conn, t2.id, c.id, "2024-01-15 10:00:00")

        session = queries.get_active_session(conn)
        assert session.task_id == t2.id

    def test_clear_session(self, conn):
        p = queries.create_project(conn, "SP3")
        t = queries.create_task(conn, p.id, "ST3")
        c = queries.list_categories(conn)[0]
        queries.set_active_session(conn, t.id, c.id, "2024-01-15 09:00:00")
        queries.clear_active_session(conn)
        assert queries.get_active_session(conn) is None
