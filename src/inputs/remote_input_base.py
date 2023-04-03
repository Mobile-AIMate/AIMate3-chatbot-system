import json
import socket
import typing

from inputs.input_base import InputBase
from utils.feature import FeatureDict


class RemoteInputBase(InputBase):
    def __init__(
        self, server_host: str = socket.gethostname(), server_port: int = 0
    ) -> None:
        super().__init__()
        self.host, self.port = server_host, server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.cached_data, self.cached_timestamp = None, -1

    def get_features(self, current_time: int) -> typing.List[FeatureDict]:
        self._fetch(current_time)

        return [(self.cached_timestamp, self.cached_data)]

    def _fetch(self, current_time: int) -> bool:
        payload = {"type": "fetch", "timestamp": current_time}
        self.client_socket.send(json.dumps(payload).encode())
        data_buffer = self.client_socket.recv(1024)
        if not data_buffer:
            raise ConnectionResetError("服务器断开连接。")
        data = json.loads(data_buffer.decode())
        self.cached_data, self.cached_timestamp = data["data"], data["timestamp"]

        return self.cached_timestamp == current_time

    def __del__(self):
        self.client_socket.close()
        super().__del__()
