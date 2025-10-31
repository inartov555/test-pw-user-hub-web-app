"""Centralized logging using Loguru, with per-test file logs."""
import os
from loguru import logger
import pytest

def configure_logger() -> None:
    os.makedirs("logs", exist_ok=True)
    logger.remove()
    logger.add("logs/automation.log", rotation="5 MB", retention=5, level="INFO", enqueue=True)

@pytest.fixture(autouse=True, scope="session")
def _setup_logging():
    configure_logger()
    yield
