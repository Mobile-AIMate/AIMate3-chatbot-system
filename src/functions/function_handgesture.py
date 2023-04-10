import typing

from functions.function_base import FunctionBase
from utils.feature import FeatureDict


class FunctionHandGesture(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)
        self.handgesture_response = {"good": "好", "bad": "坏", "5": "挥手", "2": "耶"}

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        print(features)
        my_features = [
            feature for feature in features if feature["name"] == "HandGesture"
        ]
        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"]:
                label = my_features[0]["data"]["gesture"]
                return label in self.handgesture_response.keys()
            else:
                return False
        else:
            return False

    def call(self, features: typing.List[FeatureDict], current_time: int):
        print(f"process feature in FunctionDemo at {current_time}")
        my_feature = [
            feature for feature in features if feature["name"] == "HandGesture"
        ][0]
        response = self.handgesture_response[
            my_feature["data"]["gesture"]
        ]  # 使用label作为key
        return response
