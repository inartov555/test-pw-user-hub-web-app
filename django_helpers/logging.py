"""Attach Django (or structlog) logging to test runs."""
import logging
import logging.config
import os

def configure_logging():
    ini = os.path.join(os.path.dirname(__file__), "..", "docker", "django-logging.ini")
    logging.config.fileConfig(ini)
    logging.getLogger("qa").info("QA logging configured")
