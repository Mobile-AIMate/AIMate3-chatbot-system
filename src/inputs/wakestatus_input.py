import typing

from inputs.input_base import InputBase
from utils.feature import FeatureDict
from utils.wakeup import get_wakeup_status


class WakeupStatus(InputBase):
    def __init__(self) -> None:
        super().__init__()

    def get_features(self, current_time: int) -> typing.List[FeatureDict]:
        status = get_wakeup_status(current_time)

        return [{"name": "wakeup", "data": status, "timestamp": current_time}]
