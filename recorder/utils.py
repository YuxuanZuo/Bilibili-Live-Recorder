import os
import logging
import time


def get_logger(name):
    is_exists = os.path.exists('log')
    if is_exists is not True:
        os.mkdir('log')
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file_handler = logging.FileHandler(f"log/log-{date}.log")
        file_handler.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(filename)s[line:%(lineno)d] - %(name)s : %(message)s")
        stream_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
    return logger