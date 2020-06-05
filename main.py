import time

from src import connect_pool
from src.utils import run_coroutine


async def main():
    await connect_pool.run()
   

if __name__ == '__main__':
    run_coroutine(main)
    time.sleep(1)  # FIXME waiting for libindy thread complete
