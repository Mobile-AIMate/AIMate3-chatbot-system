import typing

from external.action import EmotionType, send_action_data
from external.tts import TTS
from functions.function_base import FunctionBase
from utils.feature import FeatureDict


class FunctionHandGesture(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)
        self.handgesture_response = {
            "1": "手势一",
            "3": "手势三",
            "4": "手势四",
            "6": "手势六",
            "good": "好",
            "bad": "坏",
            "5": "挥手",
            "2": "手势二",
        }
        self.handgesture_response_robot = {
            "1": EmotionType.DISDAIN,
            "2": EmotionType.ANGRY,
            "3": EmotionType.SCARED,
            "4": EmotionType.SAD,
            "5": EmotionType.HAPPY,
            "6": "",
            "7": "",
            "8": "",
            "9": "",
            "good": "",
        }
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

    def call(self, features: typing.List[FeatureDict], current_time: int):
        super().call(features, current_time)

        print(f"process feature in FunctionDemo at {current_time}")
        my_feature = [
            feature for feature in features if feature["name"] == "HandGesture"
        ][0]
        gesture = my_feature["data"]["gesture"]
        response = self.handgesture_response[gesture]  # 使用label作为key
        response_robot = self.handgesture_response_robot[gesture]
        if not response_robot:
            response_robot = EmotionType.DEFAULT
        self.last_call_time = my_feature["timestamp"]
        # todo: serial
        send_action_data(emotion=response_robot)
        res = self.tts.run(response)
        return res
