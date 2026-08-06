import logging

from config import DEBUG


def get_logger(name: str):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level = logging.DEBUG if DEBUG else logging.INFO

    logger.setLevel(level)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "[%(levelname)s] %(name)s: %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger