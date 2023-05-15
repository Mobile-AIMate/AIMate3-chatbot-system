import socket
import typing

from inputs.remote_input_base import RemoteInputBase
from utils.feature import FeatureDict


class RemoteEmotionHand(RemoteInputBase):
    def __init__(
        self, server_host: str = socket.gethostname(), server_port: int = 8888
    ) -> None:
        super().__init__(server_host, server_port, "EmotionHand")

    def _fetch(self, current_time: int) -> bool:
        return super()._fetch(current_time)

    def get_features(self, current_time: int) -> typing.List[FeatureDict]:

        try:
            self._fetch(current_time)
        except Exception as e:
            print(f"Failed to fetch {e}")

        return [
            FeatureDict(
                name="EmotionRecognition",
                data=self.cached_data[0],
                timestamp=self.cached_timestamp,
            ),
            FeatureDict(
                name="HandGesture",
                data=self.cached_data[1],
                timestamp=self.cached_timestamp,
            ),
        ]
