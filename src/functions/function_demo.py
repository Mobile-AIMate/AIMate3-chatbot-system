import typing

from functions.function_base import FunctionBase
from utils.check_condition import need_wakeup
from utils.feature import FeatureDict
from utils.logger import add_logger
from utils.wakeup import wakeup


@add_logger
class FunctionDemo(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)

    @need_wakeup
    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        my_features = [
            feature for feature in features if feature["name"] == "remote-demo"
        ]

        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"]:
                return True
            else:
                return False
        else:
            return False

    @wakeup
    def call(self, features: typing.List[FeatureDict], current_time: int):
        self.logger.debug(f"process feature in FunctionDemo at {current_time}")
