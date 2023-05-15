import asyncio
import logging
import signal
import typing

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import functions
import inputs
from functions.function_base import FunctionBase
from inputs.input_base import InputBase
from utils import ts_counter
from utils.instantiation import instantiate
from utils.logger import get_logger

logger = get_logger("main", "main", level=logging.DEBUG)


# 循环的每次执行
async def poll_controller(
    inputs_: typing.List[InputBase], functions_: typing.List[FunctionBase]
):
    try:
        current_timestamp = ts_counter.get_timestamp()
        logger.info(f"poll_controller {current_timestamp}")

        input_features_lists = [inp.get_features(current_timestamp) for inp in inputs_]
        input_features = [
            feature
            for features_list in input_features_lists
            for feature in features_list
        ]

        logger.debug(f"input_features: {input_features}")

        check_results: typing.List[typing.Tuple[FunctionBase, bool]] = [
            (f, f.check(input_features, current_timestamp)) for f in functions_
        ]
        check_results.sort(key=lambda r: r[0].priority, reverse=True)

        logger.info(
            f"check_results: {[f.__class__.__name__ for f, cr in check_results if cr]}"
        )

        for f, cr in check_results:
            if cr:
                f.call(input_features, current_timestamp)
                break

        logger.info("========================================")
        ts_counter.increment()
    except asyncio.CancelledError:
        pass


def main():
    # 初始化所有类
    inputs_ = [instantiate(f"inputs.{input_}") for input_ in inputs.__all__]
    functions_ = [
        instantiate(f"functions.{function_}") for function_ in functions.__all__
    ]

    # 创建异步循环
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(
        poll_controller,
        "interval",
        seconds=0.1,
        max_instances=3,
        args=(inputs_, functions_),
    )

    scheduler.start()

    def close_all():
        try:
            logger.warning("exit.")
            for job in scheduler.get_jobs():
                job.remove()
            loop.stop()
            scheduler.shutdown()
        except Exception as e:
            logger.error(f"An error occurred during shutdown: {e}")
        finally:
            loop.stop()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, close_all)

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
