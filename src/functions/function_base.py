import typing

from utils.feature import FeatureDict


class FunctionBase:
    def __init__(self, priority: int = 50) -> None:
        self.priority_ = priority

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        raise NotImplementedError

    def call(self, features: typing.List[FeatureDict], current_time: int):
        raise NotImplementedError

    @property
    def priority(self) -> int:
        return self.priority_

    def __del__(self):
        pass
