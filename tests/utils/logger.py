"""Django-style logging setup for tests."""
import logging, logging.config, os, yaml

def setup_logging():
    cfg = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "logging.yaml")
    with open(cfg, "r") as f:
        conf = yaml.safe_load(f)
    logging.config.dictConfig(conf)

setup_logging()
logger = logging.getLogger("e2e")
