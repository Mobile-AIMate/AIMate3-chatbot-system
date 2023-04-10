import typing

from functions.function_base import FunctionBase
from utils.feature import FeatureDict


class remoteHandGesture(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        print(features)
        my_features = [
            feature for feature in features if feature["name"] == "HandGesture"
        ]

        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"]:
                return True
            else:
                return False
        else:
            return False

    def call(self, features: typing.List[FeatureDict], current_time: int):
        print(f"process feature in FunctionDemo at {current_time}")
        hand_gesture_text={
            #tts 后续补充
        }