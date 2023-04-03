import typing


class FeatureDict(typing.TypedDict):
    name: str
    data: typing.Any
    timestamp: int
