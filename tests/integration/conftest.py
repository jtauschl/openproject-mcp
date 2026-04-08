"""Shared fixtures for integration tests against a live OpenProject instance.

Required environment variables:
    OPENPROJECT_BASE_URL       e.g. https://op.example.com
    OPENPROJECT_API_TOKEN      API token with admin access
    OPENPROJECT_TEST_PROJECT   project identifier to use (default: mcp-test)
"""
from __future__ import annotations

import os

import pytest

from openproject_mcp.client import OpenProjectClient
from openproject_mcp.config import Settings


def _integration_settings() -> Settings | None:
    base_url = os.environ.get("OPENPROJECT_BASE_URL")
    api_token = os.environ.get("OPENPROJECT_API_TOKEN")
    if not base_url or not api_token:
        return None
    return Settings(
        base_url=base_url,
        api_token=api_token,
        auto_confirm_write=True,
        timeout=30,
        verify_ssl=True,
        default_page_size=20,
        max_page_size=50,
        max_results=100,
        log_level="WARNING",
        enable_admin_write=True,
        enable_project_write=True,
        enable_work_package_write=True,
        enable_membership_write=True,
        enable_version_write=True,
        enable_board_write=True,
    )


@pytest.fixture
def client():
    settings = _integration_settings()
    if settings is None:
        pytest.skip("OPENPROJECT_BASE_URL / OPENPROJECT_API_TOKEN not set")
    return OpenProjectClient(settings)


@pytest.fixture
def test_project() -> str:
    return os.environ.get("OPENPROJECT_TEST_PROJECT", "mcp-test")


# ---------------------------------------------------------------------------
# Cleanup helpers for write tests
# ---------------------------------------------------------------------------

@pytest.fixture
async def wp_ids(client: OpenProjectClient):
    """Yields a list to append created WP IDs; deletes them all after the test."""
    created: list[int] = []
    yield created
    for wp_id in created:
        try:
            await client.delete_work_package(work_package_id=wp_id, confirm=True)
        except Exception:
            pass


@pytest.fixture
async def version_ids(client: OpenProjectClient):
    created: list[int] = []
    yield created
    for version_id in created:
        try:
            await client.delete_version(version_id=version_id, confirm=True)
        except Exception:
            pass


@pytest.fixture
async def news_ids(client: OpenProjectClient):
    created: list[int] = []
    yield created
    for news_id in created:
        try:
            await client.delete_news(news_id=news_id, confirm=True)
        except Exception:
            pass


@pytest.fixture
async def time_entry_ids(client: OpenProjectClient):
    created: list[int] = []
    yield created
    for te_id in created:
        try:
            await client.delete_time_entry(time_entry_id=te_id, confirm=True)
        except Exception:
            pass
