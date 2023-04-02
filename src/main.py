import asyncio
import signal
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def poll_controller():
    try:
        now = datetime.now()
        print(f"poll_controller {datetime.now()} {now}")
    except asyncio.CancelledError:
        pass


def main():
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(poll_controller, "interval", seconds=0.5, max_instances=3)

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
