import logging

from settings import PATH_LOGS

# from logger_settings import get_logger
# logger = get_logger()


def get_file_handler():  # type:ignore
    file_handler = logging.FileHandler(PATH_LOGS, mode="a", encoding="UTF-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s %(message)s")
    )
    return file_handler


def get_stream_handler():  # type:ignore
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(
        logging.Formatter("%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s %(message)s")
    )
    return stream_handler


def get_logger():  # type:ignore
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
