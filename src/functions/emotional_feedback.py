import typing

from external.tts import TTS
from functions.function_base import FunctionBase
from utils.check_condition import need_wakeup
from utils.feature import FeatureDict


class EmotionalFeedback(FunctionBase):
    """
    情绪反馈功能：
        输入：情绪类别结果
        输出：情绪反馈回复
    """

    def __init__(self) -> None:
        super().__init__(priority=3)
        self.tts = TTS()

    @need_wakeup
    def check(self, features: typing.List[FeatureDict], current_time: int) -> bool:
        print(features)
        my_features = [
            feature
            for feature in features
            if feature["name"] == "EmotionRecognition"  # 情绪识别结果
        ]

        if len(my_features) == 1:
            """如果是刚得到的，就接受，否则拒绝"""
            if current_time <= my_features[0]["timestamp"] and len(
                my_features[0]["data"]
            ):  # 有人脸就有情绪
                return True
            else:
                return False
        else:
            return False

    def call(self, features: typing.List[FeatureDict], current_time: int):
        super().call(features, current_time)

        print(f"process feature in EmotionalFeedback at {current_time}")
        emotional_feedback_text = {
            "Angry": "主人，我注意到你现在感到很生气。如果你想发泄，可以尝试向我说出你的感受，我会一直在你身边支持你的",
            "Happy": "看到主人这么开心，我也感到很高兴！",
            "Surprise": "我很高兴能为你带来这种惊喜，让我们一起分享这种美好的时刻。",
            "Sad": "主人，你看起来好像很难过，如果你想分享你的感受，我愿意倾听你的故事。",
            "Fear": "主人，不要害怕，我会一直在你身边陪伴你",
            "Neutral": "主人，你快来和我一起玩呀",
        }
        this_feature = [
            feature
            for feature in features
            if feature["name"] == "EmotionRecognition"  # 情绪识别结果
        ]
        response = emotional_feedback_text[
            this_feature[0]["data"][0]["emotion_label"]
        ]  # this_feature[0]["data"] = [{"emotion_label":""}]
        # 使用情感label作为key
        print(response)
        print(f'======{this_feature[0]["data"][0]["emotion_label"]}======')
        res = self.tts.run(response)
        return res
        # print(response)
        return response
