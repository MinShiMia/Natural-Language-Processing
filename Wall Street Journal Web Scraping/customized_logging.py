import logging
import sys

from colorlog import ColoredFormatter


class CustomizedLogger:

    @staticmethod
    def get_logger(logger_name="default_logger"):
        LOG_LEVEL = logging.DEBUG
        LOGFORMAT = "  %(log_color)s %(asctime)s [%(levelname)8s]: %(message)s%(reset)s"
        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(LOG_LEVEL)
        logger.addHandler(stream)
        return logger

    @staticmethod
    def get_file_logger(logger_name="default_logger"):
        LOG_LEVEL = logging.DEBUG
        logging.root.setLevel(LOG_LEVEL)
        formatter = logging.Formatter(" %(asctime)s [%(levelname)8s]: %(message)s")
        file_handler = logging.FileHandler("logs.log")
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)
        logger = logging.getLogger(logger_name)
        logger.setLevel(LOG_LEVEL)
        logger.addHandler(file_handler)
        return logger

    @staticmethod
    def get_file_and_stream_logger(logger_name="default_logger"):
        LOG_LEVEL = logging.DEBUG
        logging.root.setLevel(LOG_LEVEL)

        formatter = logging.Formatter(" %(asctime)s [%(levelname)8s]: %(message)s")
        file_handler = logging.FileHandler("logs2.log")
        file_handler.setLevel(LOG_LEVEL)
        file_handler.setFormatter(formatter)

        LOGFORMAT = "  %(log_color)s %(asctime)s [%(levelname)8s]: %(message)s%(reset)s"
        formatter = ColoredFormatter(LOGFORMAT)
        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)

        logger = logging.getLogger(logger_name)
        logger.setLevel(LOG_LEVEL)
        logger.addHandler(file_handler)
        logger.addHandler(stream)
        return logger
