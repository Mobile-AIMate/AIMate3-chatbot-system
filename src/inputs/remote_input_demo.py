import socket

from inputs.remote_input_base import RemoteInputBase


class RemoteInputDemo(RemoteInputBase):
    def __init__(
        self, server_host: str = socket.gethostname(), server_port: int = 7777
    ) -> None:
        super().__init__(server_host, server_port, "remote-demo")

    def _fetch(self, current_time: int) -> bool:
        return super()._fetch(current_time)
