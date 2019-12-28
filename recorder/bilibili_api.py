import asyncio
import aiohttp
import logging

from recorder.utils import get_logger
from recorder.exceptions import RequestError, APIError
from recorder.config import config


class BilibiliApi():

    def __init__(self, cid):
        self.cid = cid
        self.logger = get_logger(__name__)
    
    async def _request(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            try:
                if config['enable_proxy']:
                    proxy = config['proxy']
                    self.logger.debug(f"Requesting API '{url}' using proxy '{proxy}'")
                    async with session.get(url, proxy=proxy) as response:
                        data = await response.json()
                else:
                    self.logger.debug(f"Requesting API '{url}'")
                    async with session.get(url) as response:
                        data = await response.json()
            except Exception as e:
                self.logger.error("Failed to request API '{url}': {e}")
                raise RequestError(e)
        if data['code'] == 0:
            return data
        else:
            self.logger.error(f"Failed to request API '{url}': API error: [Code: {data['code']} Message: {data['message']}]")
            raise APIError(data['code'], data['message'], url)
    
    async def get_room_info(self):
        url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={self.cid}"
        return await self._request(url)
    
    async def get_play_url(self):
        url = f"https://api.live.bilibili.com/room/v1/Room/playUrl?cid={self.cid}&platform=h5&otype=json&quality=0"
        return await self._request(url)