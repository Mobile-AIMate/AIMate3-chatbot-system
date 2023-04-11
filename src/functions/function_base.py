import typing

from utils.feature import FeatureDict
from utils.wakeup import wakeup


class FunctionBase:
    def __init__(self, priority: int = 50) -> None:
        self.priority_ = priority

    # check whether status is wake_up
    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        wakeup_features = [f for f in features if f["name"] == "wakeup"]
        assert (
            len(wakeup_features) == 1
        ), f"There is not only wakeup feature at {current_time},\
            but {len(wakeup_features)}. features is {features}"

        wakeup_status = wakeup_features[0]["data"]

        return wakeup_status

    # wake up in per call
    def call(self, features: typing.List[FeatureDict], current_time: int):
        wakeup(current_time)

    @property
    def priority(self) -> int:
        return self.priority_

    def __del__(self):
        pass
