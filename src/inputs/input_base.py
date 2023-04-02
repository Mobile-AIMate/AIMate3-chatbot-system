import typing


class InputBase:
    def __init__(self) -> None:
        self.current_time = 0

    def get_features(self, current_time: int) -> typing.Tuple[int, typing.Any]:
        pass
