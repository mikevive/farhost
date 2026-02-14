"""Tests for the timer engine: start, stop, midnight split, crash recovery."""

from datetime import datetime, timedelta
from unittest.mock import patch

from devflow.db import queries
from devflow.timer import engine


class TestStartTimer:
    def test_start_timer_creates_session(self, conn):
        p = queries.create_project(conn, "EP")
        t = queries.create_task(conn, p.id, "ET")
        c = queries.list_categories(conn)[0]

        session = engine.start_timer(conn, t.id, c.id)
        assert session.task_id == t.id
        assert session.category_id == c.id
        assert queries.get_active_session(conn) is not None

    def test_start_timer_auto_stops_previous(self, conn):
        p = queries.create_project(conn, "EP2")
        t1 = queries.create_task(conn, p.id, "ET1")
        t2 = queries.create_task(conn, p.id, "ET2")
        c = queries.list_categories(conn)[0]

        engine.start_timer(conn, t1.id, c.id)
        engine.start_timer(conn, t2.id, c.id)

        # Previous timer should have created an entry
        session = queries.get_active_session(conn)
        assert session.task_id == t2.id


class TestStopTimer:
    def test_stop_timer_saves_entry(self, conn):
        p = queries.create_project(conn, "SP")
        t = queries.create_task(conn, p.id, "ST")
        c = queries.list_categories(conn)[0]

        engine.start_timer(conn, t.id, c.id)
        entries = engine.stop_timer(conn)
        assert len(entries) >= 1
        assert queries.get_active_session(conn) is None

    def test_stop_timer_no_session(self, conn):
        entries = engine.stop_timer(conn)
        assert entries == []


class TestMidnightSplit:
    def test_single_day_no_split(self, conn):
        p = queries.create_project(conn, "MSP")
        t = queries.create_task(conn, p.id, "MST")
        c = queries.list_categories(conn)[0]

        start = datetime(2024, 1, 15, 9, 0, 0)
        end = datetime(2024, 1, 15, 17, 0, 0)

        entries = engine._create_entries_with_midnight_split(conn, t.id, c.id, start, end)
        assert len(entries) == 1
        assert entries[0].duration_seconds == 8 * 3600

    def test_crosses_one_midnight(self, conn):
        p = queries.create_project(conn, "MSP2")
        t = queries.create_task(conn, p.id, "MST2")
        c = queries.list_categories(conn)[0]

        start = datetime(2024, 1, 15, 22, 0, 0)
        end = datetime(2024, 1, 16, 2, 0, 0)

        entries = engine._create_entries_with_midnight_split(conn, t.id, c.id, start, end)
        assert len(entries) == 2

        # First entry: 22:00 -> 23:59:59
        assert entries[0].start == "2024-01-15 22:00:00"
        assert entries[0].end == "2024-01-15 23:59:59"

        # Second entry: 00:00:00 -> 02:00:00
        assert entries[1].start == "2024-01-16 00:00:00"
        assert entries[1].end == "2024-01-16 02:00:00"

    def test_crosses_multiple_midnights(self, conn):
        p = queries.create_project(conn, "MSP3")
        t = queries.create_task(conn, p.id, "MST3")
        c = queries.list_categories(conn)[0]

        start = datetime(2024, 1, 15, 22, 0, 0)
        end = datetime(2024, 1, 18, 3, 0, 0)

        entries = engine._create_entries_with_midnight_split(conn, t.id, c.id, start, end)
        assert len(entries) == 4  # 15, 16, 17, 18

    def test_check_midnight_split_same_day(self, conn):
        p = queries.create_project(conn, "CMS")
        t = queries.create_task(conn, p.id, "CMST")
        c = queries.list_categories(conn)[0]

        now = datetime.now()
        start_str = now.strftime("%Y-%m-%d %H:%M:%S")
        queries.set_active_session(conn, t.id, c.id, start_str)

        entries = engine.check_midnight_split(conn)
        assert entries == []
        # Session should still be active
        assert queries.get_active_session(conn) is not None

    def test_check_midnight_split_crosses_midnight(self, conn):
        p = queries.create_project(conn, "CMS2")
        t = queries.create_task(conn, p.id, "CMST2")
        c = queries.list_categories(conn)[0]

        # Set session to yesterday
        yesterday = datetime.now() - timedelta(days=1)
        start_str = yesterday.strftime("%Y-%m-%d") + " 23:00:00"
        queries.set_active_session(conn, t.id, c.id, start_str)

        entries = engine.check_midnight_split(conn)
        assert len(entries) >= 1

        # Session should still be active but with today's date
        session = queries.get_active_session(conn)
        assert session is not None
        today_str = datetime.now().strftime("%Y-%m-%d")
        assert session.start_time.startswith(today_str)

    def test_check_midnight_no_session(self, conn):
        entries = engine.check_midnight_split(conn)
        assert entries == []


class TestCrashRecovery:
    def test_recover_saves_entry(self, conn):
        p = queries.create_project(conn, "CRP")
        t = queries.create_task(conn, p.id, "CRT")
        c = queries.list_categories(conn)[0]

        # Set session to yesterday to trigger a split
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        queries.set_active_session(conn, t.id, c.id, yesterday)

        entries = engine.recover_crashed_session(conn)
        assert len(entries) >= 1
        # Session should STILL be active
        assert queries.get_active_session(conn) is not None

    def test_recover_no_session(self, conn):
        entries = engine.recover_crashed_session(conn)
        assert entries == []

    def test_recover_applies_midnight_split(self, conn):
        p = queries.create_project(conn, "CRP2")
        t = queries.create_task(conn, p.id, "CRT2")
        c = queries.list_categories(conn)[0]

        # Session from 2 days ago
        two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d") + " 22:00:00"
        queries.set_active_session(conn, t.id, c.id, two_days_ago)

        entries = engine.recover_crashed_session(conn)
        assert len(entries) >= 2  # Entries for 2 days ago and yesterday
        
        # Session should be active with today's midnight
        session = queries.get_active_session(conn)
        assert session is not None
        today_midnight = datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
        assert session.start_time == today_midnight
