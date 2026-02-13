"""Data models for DevFlow entities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Category:
    id: int
    name: str
    archived_at: str | None = None


@dataclass
class Project:
    id: int
    name: str
    archived_at: str | None = None


@dataclass
class Task:
    id: int
    project_id: int
    name: str
    archived_at: str | None = None


@dataclass
class TimeEntry:
    id: int
    task_id: int
    category_id: int
    start: str
    end: str
    duration_seconds: int


@dataclass
class ActiveSession:
    id: int
    task_id: int
    category_id: int
    start_time: str
