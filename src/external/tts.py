import os
import queue
import re
import threading
import time

import requests

tts_server_url = "http://localhost:21452/tts"
default_audio_path = "~/project/PaddleSpeech/demos/TTSArmLinux/output/tts.wav"


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class TTS:

    """
    Usage:
    ```python
    tts = TTS()
    status = tts.check()
    res = tts.run('你好')
    ```
    """

    def __init__(
        self,
        enable_queue=False,
        log=True,
    ) -> None:

        self.log = log
        self.text = ""
        if enable_queue:
            self.queue = queue.Queue()

        self.thread_text_to_audio = threading.Thread(
            target=self.text_to_audio,
            args=[self.text],
        )
        self.thread_play_audio = threading.Thread(
            target=self.play_audio,
        )
        self.thread_detect = threading.Thread(
            target=self.detect,
        )
        self.thread_detect.setDaemon(True)
        self.thread_detect.start()

    def check(self) -> int:

        """
        检查 tts 状态。\n
        返回值：\n
        - 0 空闲状态
        - 1 正在 tts 中
        - 2 正在播放音频中
        """

        if self.thread_text_to_audio.is_alive():
            if self.log:
                print("[TTS] 正在 tts")
            return 1
        elif self.thread_play_audio.is_alive():
            if self.log:
                print("[TTS] 正在播放音频")
            return 2

        return 0

    def is_chinese_punctuation(self, text: str) -> bool:

        """
        检查字符串是否只含有中文和标点符号\n
        如果只含有中文和标点符号，返回真\n
        反之返回假
        """

        pattern = re.compile("[\u4e00-\u9fa5，。？！；：‘’“”（）《》【】]")
        result = pattern.findall(text)
        if len(result) == len(text):
            return True
        else:
            return False

    def run(self, text: str) -> int:

        """
        输入文本，tts后播放音频。\n
        输入文本必须为全中文，尽量只包含逗号和句号。\n
        长度建议不超过 25\n
        返回值：\n
        - 0 成功，开始运行
        - 1 失败，正在 tts 中
        - 2 失败，正在播放音频中
        - 3 失败，输入文本有误或为空
        """

        if not self.is_chinese_punctuation(text) or not text:
            if self.log:
                print(f"[TTS] 输入文本有误：{text}")
            return 3

        status = self.check()

        if status:
            return status

        self.text = text
        return status

    def text_to_audio(self, text: str):
        try:
            requests.post(tts_server_url, text.encode("utf-8"))
        except Exception:
            print("Failed to send post to tts-server.")

    def play_audio(self, path: str = default_audio_path):
        os.system(f"aplay {path}")
        self.text = ""

    def detect(self):
        while True:
            if (
                self.thread_text_to_audio.is_alive()
                or self.thread_play_audio.is_alive()
            ):
                ...
            else:
                if not self.text:
                    continue
                self.thread_text_to_audio = threading.Thread(
                    target=self.text_to_audio,
                    args=[self.text],
                )
                self.thread_play_audio = threading.Thread(
                    target=self.play_audio,
                )
                self.thread_text_to_audio.start()
                self.thread_text_to_audio.join()
                self.thread_play_audio.start()
                self.thread_play_audio.join()
            time.sleep(0.1)


if __name__ == "__main__":
    text1 = "这是一段中文文本，带有标点符号。"
    text2 = "This is an English text with punctuation marks."
    text3 = (
        "这是一段包含英文和中文、标点符号的文本，"
        "This is a mixed text with Chinese and English, punctuation marks."
    )
    text4 = ""
    text5 = ""

    tts1 = TTS()
    tts2 = TTS()
    print(id(tts1), id(tts2))

    print("[TTS] Check Chinese Test:")

    print(tts1.is_chinese_punctuation(text1))
    print(tts1.is_chinese_punctuation(text2))
    print(tts1.is_chinese_punctuation(text3))
    print(tts1.is_chinese_punctuation(text4))

    while True:
        s = input(">> ")
        if s == "q":
            break
        tts1.run(s)
