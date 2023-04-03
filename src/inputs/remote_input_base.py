import json
import socket
import typing

from inputs.input_base import InputBase
from utils.feature import FeatureDict
from utils.remote_payload import remoteFetch


class RemoteInputBase(InputBase):
    def __init__(
        self,
        server_host: str = socket.gethostname(),
        server_port: int = 0,
        feature_name: str = "remote-base",
    ) -> None:
        super().__init__()
        self.feature_name = feature_name
        self.cached_data, self.cached_timestamp = None, -1
        self._connect(server_host, server_port)

    def get_features(self, current_time: int) -> typing.List[FeatureDict]:
        try:
            self._fetch(current_time)
        except Exception as e:
            print(f"Failed to fetch {e}")

        return [
            FeatureDict(
                name=self.feature_name,
                data=self.cached_data,
                timestamp=self.cached_timestamp,
            )
        ]

    def _fetch(self, current_time: int) -> bool:
        payload = remoteFetch(current_time)
        self.client_socket.send(json.dumps(payload).encode())

        data_buffer = self.client_socket.recv(1024)
        if not data_buffer:
            raise ConnectionResetError("服务器断开连接。")
        data = json.loads(data_buffer.decode())
        self.cached_data, self.cached_timestamp = data["data"], data["timestamp"]

        return self.cached_timestamp == current_time

    def _connect(
        self, server_host: str = socket.gethostname(), server_port: int = 0
    ) -> None:
        self.host, self.port = server_host, server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f"Failed to connect {e}")

    def __del__(self):
        self.client_socket.close()
        super().__del__()
