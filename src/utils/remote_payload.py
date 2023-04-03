import typing


class RemotePayload(typing.TypedDict, total=False):
    type: str
    timestamp: int


def remoteFetch(timestamp: int) -> RemotePayload:
    return RemotePayload(type="fetch", timestamp=timestamp)
