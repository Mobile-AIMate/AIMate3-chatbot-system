import socket

from inputs.remote_input_base import RemoteInputBase


class remoteEmotionRecognition(RemoteInputBase):
    def __init__(
        self, server_host: str = socket.gethostname(), server_port: int = 6969
    ) -> None:
        super().__init__(server_host, server_port, "EmotionRecognition")

    def _fetch(self, current_time: int) -> bool:
        return super()._fetch(current_time)
