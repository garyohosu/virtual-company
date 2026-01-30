import logging
import sys
from datetime import datetime
from pathlib import Path


class DualWriter:
    def __init__(self, *files):
        self._files = files

    def write(self, msg):
        for f in self._files:
            f.write(msg)
            f.flush()

    def flush(self):
        for f in self._files:
            f.flush()


def setup_logging(log_dir: str = "results/codex") -> dict:
    """Configure logging to console + files and return log paths."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    execution_log = log_path / f"execution_{timestamp}.log"
    error_log = log_path / "error.log"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid duplicate handlers if reloaded
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        exec_handler = logging.FileHandler(execution_log, encoding="utf-8")
        exec_handler.setFormatter(formatter)
        logger.addHandler(exec_handler)

        err_handler = logging.FileHandler(error_log, encoding="utf-8")
        err_handler.setLevel(logging.ERROR)
        err_handler.setFormatter(formatter)
        logger.addHandler(err_handler)

    # Mirror stdout/stderr to logs for automatic capture
    exec_stream = open(execution_log, "a", encoding="utf-8")
    err_stream = open(error_log, "a", encoding="utf-8")
    sys.stdout = DualWriter(sys.__stdout__, exec_stream, err_stream)
    sys.stderr = DualWriter(sys.__stderr__, exec_stream, err_stream)

    # Capture uncaught exceptions
    def _handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.getLogger("magicboxai").error(
            "Uncaught exception",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = _handle_exception

    return {
        "execution_log": str(execution_log),
        "error_log": str(error_log),
        "execution_stream": exec_stream,
        "error_stream": err_stream,
    }
