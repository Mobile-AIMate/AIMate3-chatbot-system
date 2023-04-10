import random
import typing

from functions.function_base import FunctionBase
from utils.feature import FeatureDict


class WakeUpGreeting(FunctionBase):
    """
    唤醒词问候功能：
        输入：语音识别结果，是否包含唤醒词
        输出：唤醒回复
    """

    def __init__(self) -> None:
        super().__init__(priority=0)

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        print(features)
        my_features = [
            feature for feature in features if feature["name"] == "asr"  # 获取语音识别结果
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
        print(f"process feature in WakeUpGreeting at {current_time}")
        wake_up_text = [
            "主人我在，有什么可以帮助您的吗？",
            "主人，你好，需要我做些什么吗？",
            "主人，请告诉我您需要什么帮助，我会尽力满足您的需求。",
        ]
        response = random.choice(wake_up_text)  # 在哪判断是否存在唤醒词？？？
        return response
