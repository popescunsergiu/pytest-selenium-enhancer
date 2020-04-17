"""Pytest plugin entry point. Used for any fixtures needed."""
import pytest
from .pytest_selenium_enhancer import add_custom_commands


@pytest.fixture(scope='session')
def selenium_patcher():
    """Add custom ."""
    add_custom_commands()
