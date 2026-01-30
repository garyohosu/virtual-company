import logging

from magicboxai.db import cleanup_expired, connect_db
from magicboxai.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger("magicboxai.cleanup")


def main() -> None:
    with connect_db() as conn:
        removed = cleanup_expired(conn)
    logger.info("Cleanup removed %s expired files", removed)


if __name__ == "__main__":
    main()
