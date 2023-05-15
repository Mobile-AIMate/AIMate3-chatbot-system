import typing

from external.chatbot import bot as ChatBot
from external.tts import TTS
from functions.function_base import FunctionBase
from utils.feature import FeatureDict


class FunctionChat(FunctionBase):
    def __init__(self) -> None:
        super().__init__(priority=0)
        self.bot = ChatBot()
        self.tts = TTS()

    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        my_features = [
            feature for feature in features if feature["name"] == "remote-asr"
        ]

        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            f_time = my_features[0]["timestamp"]
            print(f"[CHAT]:{current_time}||{f_time}")
            if current_time <= my_features[0]["timestamp"] and my_features[0]["data"]:
                return False
            else:
                return False
        else:
            return False

    def call(self, features: typing.List[FeatureDict], current_time: int):
        super().call(features, current_time)

        my_features = [
            feature for feature in features if feature["name"] == "remote-asr"
        ]
        asr_result = my_features[0]["data"].split(" ")[-1]
        self.bot.q = asr_result
        ret = self.bot.ask_gpt()
        if not self.tts.check():
            self.tts.run(ret)

        print(f"process feature in FunctionChat at {current_time}")
