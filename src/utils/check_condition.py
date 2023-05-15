import typing
from functools import reduce

from utils.feature import FeatureDict
from utils.logger import get_logger

logger = get_logger("check_condition", "utils.check_condition")


def need_wakeup(func=None, negative=False, strict=False):
    """
    为 check 函数添加唤醒条件
    negative: 如果设置为 True，则在未唤醒时才执行 check 函数
    strict: 断言必然有且只有一个 wakeup 特征
    """
    if func is None:
        return lambda f: need_wakeup(f, negative=negative)

    is_check_func = func.__name__ == "check"

    assert is_check_func, "need_wakeup decorator should be used on check function."

    def wrapper(
        self, features: typing.List[FeatureDict], current_time: int, *args, **kwargs
    ):
        wakeup_features = [f for f in features if f["name"] == "wakeup"]
        wakeup_status = reduce(
            lambda x, y: x and y, [f["data"] for f in wakeup_features], True
        )

        if strict:
            assert (
                len(wakeup_features) == 1
            ), f"There is not only wakeup feature at {current_time},\
                but {len(wakeup_features)}. features is {features}"

            if wakeup_status:
                return func(self, features, current_time, *args, **kwargs)
            else:
                return False

        # non-strict mode

        if len(wakeup_features) != 1:
            logger.warn(
                f"There should be only one wakeup feature,\
                    but got {len(wakeup_features)}"
            )

        if wakeup_status:
            return func(self, features, current_time, *args, **kwargs)
        else:
            return False

    return wrapper
