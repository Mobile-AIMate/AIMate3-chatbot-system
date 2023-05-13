from typing import List, Optional

import serial
import serial.tools.list_ports
from serial.tools.list_ports_linux import SysFS

__CACHED_CONNECTION: Optional[serial.Serial] = None


def list_available_AMA() -> List[SysFS]:
    """
    列出可用的 AMA 串口
    """
    ports = serial.tools.list_ports.comports()

    AMA_ports = [p for p in ports if "AMA" in p.name]

    return AMA_ports


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


def connect_AMA_serial() -> serial.Serial:
    """
    自动连接 AMA 串口
    """
    ports = list_available_AMA()
    assert len(ports) == 1, "Must be 1 available AMA port !!"

    connection = connect_serial(ports[0])
    return connection


def get_AMA_connection() -> serial.Serial:
    """
    自动连接 AMA 串口，如果之前已经连接，则返回之前的连接
    """
    global __CACHED_CONNECTION
    if __CACHED_CONNECTION is None:
        connection = connect_AMA_serial()
        __CACHED_CONNECTION = connection

    return __CACHED_CONNECTION
