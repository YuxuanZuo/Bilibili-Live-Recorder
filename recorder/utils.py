# -*- coding: utf-8 -*-

import os
import logging
import time
import json


def load_config():
    with open('config.json', 'r') as f:
        dict = json.load(f)
        return dict

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(filename)s[line:%(lineno)d] - %(name)s : %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        config = load_config()
        if config['save_log']:
            if os.path.exists('log') is not True:
                os.mkdir('log')
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            file_handler = logging.FileHandler(f"log/log-{date}.log")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
    return logger