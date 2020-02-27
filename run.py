import asyncio
import time

from recorder.monitor import Monitor
from recorder.utils import Utils


config = Utils.load_config()
logger = Utils.get_logger(__name__)


class LiveRecorder():
    def __init__(self, cids, executable='ffmpeg'):
        self.cids = cids
        self.executable = executable

    async def _tasks(self):
        tasks = []
        for cid in self.cids:
            task = Monitor(cid, self.executable).main()
            tasks.append(task)
        await asyncio.gather(*tasks)
    
    def main(self):
        asyncio.run(self._tasks())

if __name__ == "__main__":
    cids = []
    users = config['users']
    for cid in users:
        if cid['enable']:
            cids.append(cid['room_id'])
    LiveRecorder(cids).main()
