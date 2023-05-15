import asyncio
import json
import signal
import socket
import threading
import typing
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

GLOBAL_TIMESTAMP = 0

# main:
# inputdemo.get_features(timestamp)  # get and update timestamp


class RemoteInputDemo:
    def __init__(
        self,
        server_host: str = socket.gethostname(),
        server_port: int = 2345,
        feature_name: str = "remote-base",
    ) -> None:
        super().__init__()
        self.feature_name = feature_name
        self.cached_data, self.cached_timestamp = None, -1
        self._connect(server_host, server_port)
        self.processed_time, self.current_time = -1, 0
        self.lock = threading.Lock()
        self.t = threading.Thread(target=RemoteInputDemo._fetch, args=(self,))
        self.td = threading.Thread(target=RemoteInputDemo._recv_data, args=(self,))
        self.t.setDaemon(True)
        self.t.start()
        self.td.setDaemon(True)
        self.td.start()

    def get_features(self, current_time: int) -> typing.List[typing.Any]:
        with self.lock:
            features = [
                {
                    "name": self.feature_name,
                    "data": self.cached_data,
                    "timestamp": self.cached_timestamp,
                }
            ]

            self.current_time = current_time
        return features

    def _fetch(self):
        while True:
            with self.lock:
                if self.processed_time < self.current_time:
                    payload = {"type": "fetch", "timestamp": self.current_time}
                    self.processed_time = self.current_time
                    self.client_socket.send(json.dumps(payload).encode())
                    print(f"sent {payload}")

    def _recv_data(self):
        while True:
            try:
                data_buffer = self.client_socket.recv(1024)
                # print(data_buffer)
                if not data_buffer:
                    raise ConnectionResetError("服务器断开连接。")

                data = json.loads(data_buffer.decode())
                response_payload = data

                self.cached_data, self.cached_timestamp = (
                    response_payload["data"],
                    response_payload["timestamp"],
                )

                print(response_payload)
            except Exception:
                # print(e)
                pass

    def _connect(
        self, server_host: str = socket.gethostname(), server_port: int = 0
    ) -> None:
        self.host, self.port = server_host, server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setblocking(False)
        self.client_socket.settimeout(0.05)

        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f"Failed to connect {e}")

    def __del__(self):
        payload = {"type": "cmd", "cmd": "exit"}
        self.client_socket.send(json.dumps(payload).encode())
        self.client_socket.close()


# 循环的每次执行
async def poll_controller(inputs_, functions_):
    global GLOBAL_TIMESTAMP
    try:
        current_timestamp = GLOBAL_TIMESTAMP

        input_features_lists = [inp.get_features(current_timestamp) for inp in inputs_]

        print(f"poll_controller {datetime.now()} {current_timestamp}")
        print(input_features_lists)
        GLOBAL_TIMESTAMP += 1
    except asyncio.CancelledError:
        pass


def main():
    # 初始化所有类
    inputs_ = [RemoteInputDemo(server_port=2345)]
    functions_ = []

    # 创建异步循环
    loop = asyncio.get_event_loop()
    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.add_job(
        poll_controller,
        "interval",
        seconds=0.1,
        max_instances=3,
        args=(inputs_, functions_),
    )

    scheduler.start()

    def close_all():
        print("exit.")
        for job in scheduler.get_jobs():
            job.remove()
        loop.stop()
        scheduler.shutdown()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, close_all)

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
