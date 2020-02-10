# -*- coding: utf-8 -*-

import asyncio
import logging
import time

from retrying import retry

from recorder.bilibili_api import BilibiliApi
from recorder.downloader import Download
from recorder.utils import get_logger, load_config
from recorder.exceptions import UnexpectedError


config = load_config()
logger = get_logger(__name__)


class Monitor():

    def __init__(self, cid, executable):
        self.cid = cid
        self.executable = executable
        self.api = BilibiliApi(self.cid)
        self.output_type = config['output_type']
    
    async def _get_live_status(self) -> int:
        data = await self.api.get_room_info()
        try:
            live_status = data["data"]["live_status"]
            logger.debug(f"[房间 {self.cid}] 直播状态为 {live_status}")
            return live_status
        except Exception as e:
            logger.error(f"[房间 {self.cid}] 获取直播状态失败: {e}")
            raise UnexpectedError(e)

    async def _get_stream_url(self) -> str:
        data = await self.api.get_play_url()
        try:
            stream_url = data["data"]["durl"][0]["url"]
            logger.debug(f"[房间 {self.cid}] 获取到一个直播流地址 {stream_url}")
            return stream_url
        except Exception as e:
            logger.error(f"[房间 {self.cid}] 获取直播流地址失败: {e}")
            raise UnexpectedError(e)
    
    @retry(stop_max_attempt_number=config['max_retry_num'], wait_fixed=config['retry_sec'])
    async def main(self) -> str:
        live_status = await self._get_live_status()
        if live_status == 1:
            logger.info(f"[房间 {self.cid}] 直播已开始!")
            stream_url = await self._get_stream_url()
            current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            splice = ['record-', str(self.cid), '_', current_time, self.output_type]
            filename = ''.join(splice)
            return await Download(stream_url, filename, self.executable).start()
        else:
            logger.info(f"[房间 {self.cid}] 直播未开始.")
            return ''
