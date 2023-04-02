import json
import queue
import random
import socket
import threading
import time
import traceback
from datetime import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 7777

server_socket.bind((host, port))

server_socket.listen(1)

# 线程安全队列
request_queue = queue.Queue()
data_queue = queue.Queue()


def create_data():
    while True:
        data = f"DATA: {datetime.now()}"
        data_queue.put(data)
        print(f"build data: {data}")
        time.sleep(3.5 * random.random() + 0.5)  # 模拟数据生成时间
    print("leave create data.")


ct = threading.Thread(target=create_data)
ct.setDaemon(True)
ct.start()


# 线程处理函数，用于发送数据
def send_to_client():
    last_data = None
    last_timestamp = -1
    while True:
        try:
            request = request_queue.get()
            print(f"request is {request}")
            if request is None:
                # 遇到 None 时退出线程
                break
            if request["type"] == "fetch":
                while not data_queue.empty():
                    last_data = data_queue.get()
                    last_timestamp = request["timestamp"]

                payload = {
                    "type": "reply",
                    "data": last_data,
                    "timestamp": last_timestamp,
                }
                client_socket.send(json.dumps(payload).encode())
            elif request["type"] == "cmd":
                if request["cmd"] == "exit":
                    # 处理退出信号
                    break
                else:
                    print("未知命令：", request["cmd"])
        except (ConnectionResetError, BrokenPipeError):
            print("客户端断开连接。")
            break
        except Exception as e:
            print("发生异常：", e)
            break


# 启动发送数据线程
t = threading.Thread(target=send_to_client)
t.setDaemon(True)
t.start()

while True:
    print("等待客户端连接...")
    client_socket, addr = server_socket.accept()
    print("连接地址：", addr)

    # 线程处理函数，用于处理连接数据
    def handle_client():
        while True:
            try:
                # 接收客户端发送来的数据
                request = client_socket.recv(1024).decode()
                print(request.strip())
                payload = json.loads(request.strip())

                if payload["type"] == "cmd" and payload["cmd"] == "exit":
                    # 处理退出信号
                    request_queue.put(None)
                    break
                else:
                    request_queue.put(payload)
            except (ConnectionResetError, BrokenPipeError):
                print("客户端断开连接。")
                request_queue.put(None)
                break
            except Exception as e:
                print("发生异常：", e)
                traceback.print_exc()
                request_queue.put(None)
                break
        client_socket.close()

    t = threading.Thread(target=handle_client)
    t.setDaemon(True)
    t.start()

while not request_queue.empty():
    request_queue.get()
server_socket.close()
