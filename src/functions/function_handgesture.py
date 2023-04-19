import typing

from external.tts import TTS
from functions.function_base import FunctionBase
from utils.feature import FeatureDict
from utils.wakeup import wakeup


class FunctionHandGesture(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)
        self.handgesture_response = {"good": "好", "bad": "坏", "5": "挥手", "2": "耶"}
        self.last_call_time = 0
        self.interval_time = 20
        self.tts = TTS()

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        if current_time - self.last_call_time < self.interval_time:
            return False

        my_features = [
            feature for feature in features if feature["name"] == "HandGesture"
        ]
        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"]:
                label = my_features[0]["data"]["gesture"].lower()
                return label in self.handgesture_response.keys()
            else:
                return False
        else:
            return False
        tts_text = self.handgesture_response[my_features[0]["data"]["gesture"]]
        if self.tts.run(tts_text) != 0:
            return False

    @wakeup
    def call(self, features: typing.List[FeatureDict], current_time: int):
        super().call(features, current_time)

        print(f"process feature in FunctionDemo at {current_time}")
        my_feature = [
            feature for feature in features if feature["name"] == "HandGesture"
        ][0]
        response = self.handgesture_response[
            my_feature["data"]["gesture"]
        ]  # 使用label作为key
        self.last_call_time = my_feature["timestamp"]
        res = self.tts.run(response)
        return res
