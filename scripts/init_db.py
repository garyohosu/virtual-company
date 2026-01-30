import logging

from magicboxai.db import connect_db, init_db
from magicboxai.logging_utils import setup_logging

setup_logging()
logger = logging.getLogger("magicboxai.init_db")


def main() -> None:
    with connect_db() as conn:
        init_db(conn)
    logger.info("Database initialized")


if __name__ == "__main__":
    main()
