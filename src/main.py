import asyncio
import signal
import typing
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import inputs
from inputs.input_base import InputBase
from utils import ts_counter
from utils.instantiation import instantiate


# 循环的每次执行
async def poll_controller(inputs_: typing.List[InputBase], functions_):
    try:
        current_timestamp = ts_counter.get_timestamp()
        input_features = [inp.get_features(current_timestamp) for inp in inputs_]
        print(input_features)
        print(f"poll_controller {datetime.now()} {current_timestamp}")
        ts_counter.increment()
    except asyncio.CancelledError:
        pass


def main():
    # 初始化所有类
    inputs_ = [instantiate(f"inputs.{input_}") for input_ in inputs.__all__]
    print(inputs_)

    # 创建异步循环
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(
        poll_controller, "interval", seconds=0.5, max_instances=3, args=(inputs_, [])
    )

    scheduler.start()

    def close_all():
        print("exit.")
        for job in scheduler.get_jobs():
            job.remove()
        loop.stop()
        scheduler.shutdown()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, close_all)

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
