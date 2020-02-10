# -*- coding: utf-8 -*-

import asyncio
import os

from recorder.utils import get_logger, load_config
from recorder.exceptions import FFmpegExecutableError, FFmpegExecutableNotFoundError, FFmpegProcessingError


config = load_config()


class Download():

    def __init__(self, url, filename, executable):
        self.url = url
        self.filename = filename
        self.executable = executable
        self.logger = get_logger(__name__)
        self.output_dir = config['output_dir']
        self.file = os.path.join(self.output_dir, self.filename)
    
    async def start(self) -> str:
        if os.path.exists(self.output_dir) is not True:
            self.logger.debug("Log folder is not exists, creating...")
            os.mkdir(self.output_dir)
        try:
            self.logger.info(f"Starting the stream download process, URL: {self.url}")
            proc = await asyncio.create_subprocess_exec(
                self.executable, "-i", self.url, "-c", "copy", self.file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
        except FileNotFoundError:
            self.logger.error("Start process failed: FFmpeg excutable not found!")
            raise FFmpegExecutableNotFoundError()
        except Exception as e:
            self.logger.error(f"Failed to download the stream, executable error: {e}")
            raise FFmpegExecutableError(e)
        if stdout:
            file_path = os.path.abspath(self.file)
            self.logger.info(f"Download completed! File saved to {file_path}")
            return file_path
        if stderr:
            self.logger.error(f"Failed to download the stream, processing error: \n{stderr.decode()}")
            raise FFmpegProcessingError(stderr.decode())
