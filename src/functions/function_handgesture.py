import typing

from external.tts import TTS
from functions.function_base import FunctionBase
from utils.feature import FeatureDict
from utils.logger import add_logger
from utils.wakeup import wakeup


@add_logger
class FunctionHandGesture(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)
        self.handgesture_response = {"good": "谢谢主人，我会一直陪伴你的", "bad": "对不起主人，我会继续努力的", "5": "嗨主人你来啦，我们一起玩吧", "2": "主人开心我也开心哦", "rock": "让我们一起摇滚吧", "6": "主人你也很棒哦", "8": "主人拜拜，期待下次再见哦", "0": "主人不要生气哦，我会一直支持你的"}
        self.last_call_time = 0
        self.interval_time = 20
        self.tts = TTS()

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        if current_time - self.last_call_time < self.interval_time:
            return False
        my_features = [
            feature for feature in features if feature["name"] == "HandGesture"
        ]
        status = self.tts.check()
        if status != 0:
            return False        
        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"]:
                label = my_features[0]["data"]["gesture"].lower()
                return label in self.handgesture_response.keys()
            else:
                return False
        else:
            return False

    @wakeup
    def call(self, features: typing.List[FeatureDict], current_time: int):
        self.logger.debug(f"process feature in FunctionDemo at {current_time}")
        my_feature = [
            feature for feature in features if feature["name"] == "HandGesture"
        ][0]
        response = self.handgesture_response[
            my_feature["data"]["gesture"]
        ]  # 使用label作为key
        self.logger.debug(response)                
        self.last_call_time = my_feature["timestamp"]
        res = self.tts.run(response)
        return res
