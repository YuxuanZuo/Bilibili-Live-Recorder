# -*- coding: utf-8 -*-

import asyncio
import os

from recorder.utils import Utils
from recorder.exceptions import FFmpegExecutableError, FFmpegExecutableNotFoundError, FFmpegProcessingError


config = Utils.load_config()
logger = Utils.get_logger(__name__)


class Download():

    def __init__(self, url, cid, filename, executable):
        self.url = url
        self.cid = cid
        self.filename = filename
        self.executable = executable
        self.output_dir = config['output_dir']
        self.file = os.path.join(self.output_dir, self.filename)
    
    async def start(self) -> str:
        if os.path.exists(self.output_dir) is not True:
            logger.debug("Log folder is not exists, creating...")
            os.mkdir(self.output_dir)
        try:
            logger.info(f"Starting the stream download process, URL: {self.url}")
            proc = await asyncio.create_subprocess_exec(
                self.executable,
                '-user_agent', "Mozilla/5.0 (iPhone; CPU 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile Safari/604.1",
                '-referer', f"https://live.bilibili.com/h5/{self.cid}",
                '-i', self.url, '-c', 'copy', self.file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
        except FileNotFoundError:
            logger.error("Start process failed: FFmpeg excutable not found!")
            raise FFmpegExecutableNotFoundError()
        except Exception as e:
            logger.error(f"Failed to download the stream, executable error: {e}")
            raise FFmpegExecutableError(e)
        if stdout:
            file_path = os.path.abspath(self.file)
            logger.info(f"Download completed! File saved to {file_path}")
            return file_path
        if stderr:
            logger.error(f"Failed to download the stream, processing error: \n{stderr.decode()}")
            raise FFmpegProcessingError(stderr.decode())
