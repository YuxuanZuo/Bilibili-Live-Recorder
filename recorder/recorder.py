import asyncio
import logging
import time

from retrying import retry

from recorder.bilibili_api import BilibiliApi
from recorder.downloader import Download
from recorder.utils import get_logger
from recorder.exceptions import UnexpectedError
from recorder.config import config


class Recorder():

    def __init__(self, cid, executable):
        self.cid = cid
        self.executable = executable
        self.logger = get_logger(__name__)
        self.api = BilibiliApi(self.cid)
        self.output_type = config['output_type']
    
    async def _get_live_status(self) -> int:
        data = await self.api.get_room_info()
        try:
            live_status = data["data"]["live_status"]
            self.logger.debug(f"[Room {self.cid}] Live status is {live_status}")
            return live_status
        except Exception as e:
            self.logger.error(f"[Room {self.cid}] Failed to get live status: {e}")
            raise UnexpectedError(e)

    async def _get_stream_url(self) -> str:
        data = await self.api.get_play_url()
        try:
            stream_url = data["data"]["durl"][0]["url"]
            self.logger.debug(f"[Room {self.cid}] Got a stream url '{stream_url}'")
            return stream_url
        except Exception as e:
            self.logger.error(f"[Room {self.cid}] Failed to get stream url: {e}")
            raise UnexpectedError(e)
    
    @retry(stop_max_attempt_number=config['max_retry_num'], wait_fixed=config['retry_sec'])
    async def main(self) -> str:
        live_status = await self._get_live_status()
        if live_status == 1:
            self.logger.info(f"[Room {self.cid}] Live has started!")
            stream_url = await self._get_stream_url()
            current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            splice = ['record-', str(self.cid), '_', current_time, self.output_type]
            filename = ''.join(splice)
            return await Download(stream_url, filename, self.executable).start()
        else:
            self.logger.info(f"[Room {self.cid}] Live has not started.")
            return ''