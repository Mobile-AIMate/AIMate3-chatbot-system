from enum import IntEnum
from typing import List, Optional

import serial
import serial.tools.list_ports
from serial.tools.list_ports_linux import SysFS

__CACHED_CONNECTION: Optional[serial.Serial] = None


class MachineryState(IntEnum):
    DEFAULT = 0x00
    FORWARD = 0x01
    BACKWARD = 0x02


class MachineryData:
    """
    电机数据
    """

    def __init__(
        self, state: MachineryState = MachineryState.DEFAULT, speed: int = 0
    ) -> None:
        assert (
            speed >= 0 and speed <= 0xFF
        ), f"Speed must in [0, 0xFF], but received {speed}"
        self.state = state
        self.speed = speed

    def __bytes__(self) -> bytes:
        return bytes([self.state, self.speed])


class EmotionType(IntEnum):
    """
    表情类型
    """

    DEFAULT = 0x00
    DISDAIN = 0x0B  # 不屑
    ANGRY = 0x0C
    SCARED = 0x0D
    SAD = 0x0E
    HAPPY = 0x0F


def build_frame_data(
    machinery_1: MachineryData = MachineryData(),
    machinery_2: MachineryData = MachineryData(),
    emotion: EmotionType = EmotionType.DEFAULT,
) -> bytes:
    buffer = bytes(machinery_1) + bytes(machinery_2) + bytes([emotion])

    if not any(buffer):  # 全是 0
        print(f"No meaningful data is built in build_frame_data ({buffer}).")

    buffer_head = bytes([0xFE])
    buffer_tail = bytes([0x0D, 0x0A])

    return buffer_head + buffer + buffer_tail


def list_available_by_name(name: str) -> List[SysFS]:
    """
    列出可用的串口
    """
    ports = serial.tools.list_ports.comports()

    ports = [p for p in ports if name in p.name]

    return ports


def connect_serial(port: SysFS) -> serial.Serial:
    """
    基于传入 port 连接串口
    """
    portx = port.device
    bps = 115200
    # timex = None # seconds, None means wait forever
    timeout = 0  # seconds, None means wait forever
    connection = serial.Serial(portx, bps, timeout=timeout)

    return connection


def connect_serial_by_name(name: str) -> serial.Serial:
    """
    自动连接 AMA 串口
    """
    ports = list_available_by_name(name)
    assert len(ports) == 1, f"Must be 1 available {name} port !!"

    connection = connect_serial(ports[0])
    return connection


def get_connection() -> serial.Serial:
    """
    自动连接串口，如果之前已经连接，则返回之前的连接
    """
    global __CACHED_CONNECTION
    if __CACHED_CONNECTION is None:
        connection = connect_serial_by_name("USB")
        __CACHED_CONNECTION = connection

    return __CACHED_CONNECTION


def send_action_data(
    machinery_1: MachineryData = MachineryData(),
    machinery_2: MachineryData = MachineryData(),
    emotion: EmotionType = EmotionType.DEFAULT,
):
    assert isinstance(
        machinery_1, MachineryData
    ), f"machinery_1 must be MachineryData, but received {machinery_1}"
    assert isinstance(
        machinery_2, MachineryData
    ), f"machinery_2 must be MachineryData, but received {machinery_2}"
    assert isinstance(
        emotion, EmotionType
    ), f"emotion must be EmotionType, but received {emotion}"

    connection = get_connection()
    buffer = build_frame_data(
        machinery_1=machinery_1, machinery_2=machinery_2, emotion=emotion
    )
    connection.write(buffer)


if __name__ == "__main__":
    send_action_data(emotion=EmotionType.SAD)
