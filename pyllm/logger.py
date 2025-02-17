import logging
import os


class ColoredFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    green = "\x1b[1;32m"
    yellow = "\x1b[0;33m"
    red = "\x1b[0;31m"
    purple = "\x1b[1;35m"
    reset = "\x1b[0m"
    format_template = (
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
    )
    colored_format = {
        logging.DEBUG: grey + format_template + reset,
        logging.INFO: green + format_template + reset,
        logging.WARNING: yellow + format_template + reset,
        logging.ERROR: red + format_template + reset,
        logging.CRITICAL: purple + format_template + reset,
    }

    def format(self, record):
        log_fmt = self.colored_format.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log_file_path = os.path.join(os.path.dirname(__file__), "..", "pyllm_runtime.log")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ColoredFormatter())
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file_path), stream_handler],
)
