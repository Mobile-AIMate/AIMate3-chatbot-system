import os
import queue
import threading
import time

default_audio_path = "~/project/audio-all/rec/"


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class Play:

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

        if self.thread_play_audio.is_alive():
            if self.log:
                print("[PLAY] 正在播放音频")
            return 1

        return 0

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

        status = self.check()

        if status:
            return status

        if self.log:
            print(f"[PLAY] 开始：{text}")
        self.text = text
        return status

    def play_audio(self, text: str):
        os.system(f"aplay {default_audio_path}{text}.wav")
        self.text = ""

    def detect(self):
        while True:
            if self.thread_play_audio.is_alive() or not self.text:
                ...
            else:
                self.thread_play_audio = threading.Thread(
                    target=self.play_audio,
                    args=[self.text],
                )
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

    play = Play()

    while True:
        s = input(">> ")
        if s == "q":
            break
        play.run(s)
