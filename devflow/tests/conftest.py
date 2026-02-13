"""Shared test fixtures: in-memory database with seed data."""

import pytest

from devflow.db.connection import get_memory_connection


@pytest.fixture
def conn():
    """Provide a fresh in-memory database connection with schema and seed data."""
    connection = get_memory_connection()
    yield connection
    connection.close()
