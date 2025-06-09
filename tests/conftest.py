"""Test configuration settings.
"""
import pytest

from src.core import logger


@pytest.fixture(scope="session", autouse=True)
def disable_logger() -> None:
    logger.enable = False
