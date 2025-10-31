
import logging, logging.config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[%(asctime)s] %(levelname)s %(name)s:%(lineno)d | %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "file": {"class": "logging.FileHandler", "filename": "reports/pytest.log", "formatter": "verbose"},
    },
    "loggers": {
        "qa": {"handlers": ["console", "file"], "level": "INFO", "propagate": False},
    },
}

def setup_logging():
    logging.config.dictConfig(LOGGING)
    logging.getLogger("qa").info("Logging initialized")
