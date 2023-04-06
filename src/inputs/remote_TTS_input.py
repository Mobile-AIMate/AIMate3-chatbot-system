import socket

from inputs.remote_input_base import RemoteInputBase


class RemoteTTSInput(RemoteInputBase):
    def __init__(
        self, server_host: str = socket.gethostname(), server_port: int = 21454
    ) -> None:
        super().__init__(server_host, server_port, "remote-TTS")

    def _fetch(self, current_time: int) -> bool:
        return super()._fetch(current_time)
