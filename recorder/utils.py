# -*- coding: utf-8 -*-

import os
import logging
import time
import json

from recorder.exceptions import ConfigFileNotFoundError, ConfigFileReadError


class Utils():
    
    @classmethod
    def get_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(filename)s[line:%(lineno)d] - %(name)s : %(message)s")
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
            if (config := cls.load_config()) and config['save_log']:
                if os.path.exists('log') is not True:
                    os.mkdir('log')
                date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                file_handler = logging.FileHandler(f"log/log-{date}.log")
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        return logger

    @classmethod
    def load_config(cls):
        logger = cls.get_logger(__name__)
        try:
            with open('config.json', 'r') as f:
                dict = json.load(f)
                return dict
        except FileNotFoundError:
            logger.error("未找到配置文件!")
            raise ConfigFileNotFoundError()
        except Exception as e:
            logger.error(f"读取配置文件失败: {e}")
            raise ConfigFileReadError(e)
