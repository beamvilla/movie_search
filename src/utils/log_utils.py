import logging


def get_logger(
    level: logging = logging.INFO
) -> logging:
    logging.basicConfig(
        level=level, format="%(asctime)s [%(levelname)s]  %(message)s"
    )
    logger = logging.getLogger()
    return logger