# chatbot-system

## Demo 测试

打开一个终端，执行 `python input_server.py` 用来启动一个输入服务器，这个程序用于模拟输入的实际处理模块。

再打开一个终端，执行 `python src/main.py` 用来启动主进程，就可以看到主进程可以通信，并通过 `RemoteInputDemo` 来输入，`FunctionDemo` 来执行具体功能。
