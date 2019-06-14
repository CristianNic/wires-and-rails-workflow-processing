"""Configure file and console logger streams"""
import logging


def setup_logger(logger_name, file_name, log_level=logging.DEBUG):
    """Configure file and console logger streams"""
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    try:
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # on test we need to supress the logging
        pass

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
