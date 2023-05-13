from typing import List

import serial
import serial.tools.list_ports
from serial.tools.list_ports_linux import SysFS

__CACHED_CONNECTION: serial.Serial = None


def list_available() -> List[SysFS]:
    ports = serial.tools.list_ports.comports()

    AMA_ports = [p for p in ports if "AMA" in p.name]

    return AMA_ports


def connect_serial(port: SysFS) -> serial.Serial:
    portx = port.device
    bps = 115200
    # timex = None # seconds, None means wait forever
    timex = 0  # seconds, None means wait forever
    connection = serial.Serial(portx, bps, timeout=timex)

    return connection


def auto_connect() -> serial.Serial:
    ports = list_available()
    assert len(ports) == 1, "Must be 1 available port !!"

    return connect_serial(ports[0])
