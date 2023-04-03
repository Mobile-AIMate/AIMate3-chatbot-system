import asyncio
import signal
import typing
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from inputs.input_base import InputBase


# 循环的每次执行
async def poll_controller(inputs_: typing.List[InputBase], functions_):
    try:
        now = datetime.now()
        print(f"poll_controller {datetime.now()} {now}")
    except asyncio.CancelledError:
        pass


def main():
    # 初始化所有类

    # 创建异步循环
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(
        poll_controller, "interval", seconds=0.5, max_instances=3, args={}
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
