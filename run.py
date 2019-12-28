import asyncio
import time

from recorder.recorder import Recorder
from recorder.utils import get_logger
from recorder.config import config

class LiveRecorder():
    def __init__(self, cids, executable='ffmpeg'):
        self.cids = cids
        self.executable = executable
    
    async def _tasks(self):
        tasks = []
        for cid in self.cids:
            task = Recorder(cid, self.executable).main()
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