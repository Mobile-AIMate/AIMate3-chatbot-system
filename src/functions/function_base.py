import typing

from utils.check_condition import need_wakeup
from utils.feature import FeatureDict
from utils.wakeup import wakeup


class FunctionBase:
    def __init__(self, priority: int = 50) -> None:
        self.priority_ = priority

    # check whether status is wake_up
    @need_wakeup
    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        raise NotImplementedError

    # wake up in per call
    def call(self, features: typing.List[FeatureDict], current_time: int):
        wakeup(current_time)

    @property
    def priority(self) -> int:
        return self.priority_

    def __del__(self):
        pass
