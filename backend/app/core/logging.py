import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """Configure a single, consistent logging setup for the whole app."""

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if root.handlers:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root.addHandler(handler)

    # Keep SQLAlchemy quiet unless something is actually wrong.
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Returns a module-level logger."""
    return logging.getLogger(name)


__all__ = ["setup_logging", "get_logger"]
