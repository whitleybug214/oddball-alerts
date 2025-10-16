import time
import asyncio
from src.core.decorators import timed
from src.core.logging_config import configure_logging

configure_logging()

@timed("sync_demo")
def sync_demo():
    time.sleep(0.3)
    return "sync done"

@timed("async demo")
async def async_demo():
    await asyncio.sleep(0.3)
    return "async done"

if __name__ == "__main__":
    print(sync_demo())
    print(asyncio.run(async_demo()))