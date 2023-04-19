import random
import typing

from functions.function_base import FunctionBase
from utils.check_condition import need_wakeup
from utils.feature import FeatureDict


class WakeUpGreeting(FunctionBase):
    """
    唤醒词问候功能：
        输入：语音识别结果，是否包含唤醒词
        输出：唤醒回复
    """

    def __init__(self) -> None:
        super().__init__(priority=0)

    @need_wakeup(negative=True)
    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        print(features)
        my_features = [
            feature
            for feature in features
            if feature["name"] == "RemoteASR"  # 获取语音识别结果
        ]
        if my_features[0]["data"]:  # 判断语音识别结果不为空
            if len(my_features) == 1:
                """如果是刚得到的，就接受，否则拒绝"""
                if (
                    current_time <= my_features[0]["timestamp"]
                    and my_features[0]["data"].find("唤醒词") != -1
                ):
                    return True
                else:
                    return False
            else:
                return False

    def call(self, features: typing.List[FeatureDict], current_time: int):
        super().call(features, current_time)

        print(f"process feature in WakeUpGreeting at {current_time}")
        wake_up_text = [
            "主人我在，有什么可以帮助您的吗？",
            "主人，你好，需要我做些什么吗？",
            "主人，请告诉我您需要什么帮助，我会尽力满足您的需求。",
        ]
        response = random.choice(wake_up_text)
        print(response)
        return response
