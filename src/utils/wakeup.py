import typing

from utils.feature import FeatureDict

DEFAULT_WAKEUP_TIME = 100  # 100 frame (10 s) to sleep

TIMESTAMP_TO_SLEEP = -1
WAKEUP_STATUS = False


def get_wakeup_status(current_time: int) -> bool:
    global WAKEUP_STATUS

    if current_time >= TIMESTAMP_TO_SLEEP:
        WAKEUP_STATUS = False

    return WAKEUP_STATUS


def __wakeup(current_time: int, wakeup_time: int = DEFAULT_WAKEUP_TIME):
    global WAKEUP_STATUS, TIMESTAMP_TO_SLEEP
    WAKEUP_STATUS = True
    TIMESTAMP_TO_SLEEP = current_time + wakeup_time


def wakeup(func=None, wakeup_time: int = DEFAULT_WAKEUP_TIME):
    """
    唤醒系统
    当前函数调用后，系统会进入唤醒状态，并持续一段时间
    wakeup_time: 唤醒后到下次进入睡眠的时间，单位为帧
    """
    if func is None:
        return lambda f: wakeup(f)

    is_call_func = func.__name__ == "call"

    assert is_call_func, "wakeup decorator should be used on call function."

    def wrapper(
        self, features: typing.List[FeatureDict], current_time: int, *args, **kwargs
    ):
        func(self, features, current_time, *args, **kwargs)
        __wakeup(current_time, wakeup_time)

    return wrapper
