# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import logging

from recorder.utils import get_logger, load_config
from recorder.exceptions import RequestError, APIError


config = load_config()
logger = get_logger(__name__)


class BilibiliApi():

    def __init__(self, cid):
        self.cid = cid
 
    async def _request(self, url: str) -> dict:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile Safari/604.1'
        headers['Referer'] = f"https://live.bilibili.com/h5/{self.cid}"
        async with aiohttp.ClientSession() as session:
            try:
                if config['enable_proxy']:
                    proxy = config['proxy']
                    logger.debug(f"正在使用代理 {proxy} 请求API {url}")
                    async with session.get(url, headers=headers, proxy=proxy) as response:
                        dict = await response.json()
                else:
                    logger.debug(f"正在请求API {url}")
                    async with session.get(url, headers=headers) as response:
                        dict = await response.json()
            except Exception as e:
                logger.error("请求API {url} 失败: {e}")
                raise RequestError(e)
        if dict['code'] == 0:
            return dict
        else:
            logger.error(f"请求API {url} 失败: API error: [Code: {dict['code']} Message: {dict['message']}]")
            raise APIError(dict['code'], dict['message'], url)
    
    async def get_room_info(self):
        url = f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={self.cid}"
        return await self._request(url)
    
    async def get_play_url(self):
        url = f"https://api.live.bilibili.com/room/v1/Room/playUrl?cid={self.cid}&platform=h5&otype=json&quality=0"
        return await self._request(url)
