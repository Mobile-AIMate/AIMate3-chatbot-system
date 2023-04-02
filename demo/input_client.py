import json
import socket
import sys
import threading
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 7777

client_socket.connect((host, port))

# 设置客户端时间戳
client_timestamp = 0


# 发送数据
def send_data():
    global client_timestamp
    while True:
        # 发送数据
        client_timestamp += 1
        payload = {"type": "fetch", "timestamp": client_timestamp}
        client_socket.send(json.dumps(payload).encode())
        time.sleep(0.5)


t = threading.Thread(target=send_data)
t.setDaemon(True)
t.start()

# 接收服务器发来的数据
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(data.decode().strip())
except KeyboardInterrupt:
    # 在 Ctrl-C 的时候发送 <exit> 消息给服务器
    payload = {"type": "cmd", "cmd": "exit"}
    client_socket.send(json.dumps(payload).encode())
    client_socket.close()
    sys.exit(0)
except ConnectionResetError:
    print("服务器断开连接。")

client_socket.close()
