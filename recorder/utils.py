# -*- coding: utf-8 -*-

import json
import logging
import os
import time

from recorder.exceptions import ConfigFileNotFoundError, ConfigFileReadError


class Utils:
    @classmethod
    def gen_default_config(cls):
        logger = cls.get_logger(__name__)
        logger.info('尝试生成默认配置中……')
        default_config = {
            "enable_proxy": False,
            "proxy": "http://127.0.0.1:8080",
            "save_log": True,
            "max_retry_num": 3,
            "retry_sec": 1,
            "check_interval": 15,
            "output_type": ".mp4",
            "output_dir": "./output/",
            "users": [
                {
                    "room_id": 0,
                    "enable": True
                }
            ]
        }

        try:
            with open('./config.json', 'w+') as file:
                json.dump(default_config, file, indent=4)

            logger.info('默认配置文件生成完毕。请修改config.json')
            time.sleep(5)

            # Stale for user experience.
            exit(1)

        except IOError:
            logger.fatal('生成默认配置文件失败！请检查文件夹权限')

        except Exception as err:
            logger.fatal(f'生成默认配置文件失败！{err}')


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
                config = json.load(f)
                return config

        except FileNotFoundError:
            logger.error("未找到配置文件!")
            cls.gen_default_config()

        except Exception as e:
            logger.error(f"读取配置文件失败: {e}")
            raise ConfigFileReadError(e)
