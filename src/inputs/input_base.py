import typing

from utils.feature import FeatureDict


class InputBase:
    def __init__(self) -> None:
        self.current_time = 0

    def get_features(self, current_time: int) -> typing.List[FeatureDict]:
        self.current_time = current_time
        raise NotImplementedError

    def __del__(self):
        pass
