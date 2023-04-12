import random
import typing

from functions.function_base import FunctionBase
from utils.feature import FeatureDict


class ProactiveGreeting(FunctionBase):
    """
    主动问候功能：
        输入：人脸检测结果
        输出：主动问候回复
    """

    def __init__(self) -> None:
        super().__init__(priority=0)

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        if not super().check(features, current_time):
            return False

        print(features)
        my_features = [
            feature for feature in features if feature["name"] == "EmotionRecognition"  # 人脸检测结果
        ]

        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"] and len(my_features[0]["data"]): # 判断是否检测到人脸
                return True
            else:
                return False
        else:
            return False

    def call(self, features: typing.List[FeatureDict], current_time: int):
        super().call(features, current_time)

        print(f"process feature in ProactiveGreeting at {current_time}")
        proactive_greeting_text = [
            "主人，您的宠物机器人正在这里等您呢！快来和我玩玩吧！",
            "“嘿，主人，我好想你呀！有什么我能帮助你的吗？",
            "哇，主人回来了！我和你玩个小游戏吧！",
        ]
        response = random.choice(proactive_greeting_text)
        print(response)
        return response
