"""Pytest plugin entry point. Used for any fixtures needed."""
import pytest

from .custom_wait import CustomWait
from .pytest_selenium_enhancer import add_custom_commands
from .pytest_selenium_enhancer import add_method


@pytest.fixture(scope='session')
def selenium_patcher():
    """Add custom ."""
    add_custom_commands()
