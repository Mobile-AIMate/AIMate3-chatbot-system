from revChatGPT.V1 import Chatbot
import time
import json

f = open('./token.json','r')

content = f.read()
token = content['access_token']

chatbot = Chatbot(config={
"access_token": token
})

def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class bot:
    def __init__(self, user):
        self.user = user
        self.q = ""

    def ask_gpt(self):
        i = 1
        conversation_id = 0
        while 1:
            if i%5 != 0:
                # print(i)
                # q = input(f"【user】")
                # print(q)
                q = self.q
                if q == "退出":
                    chatbot.reset_chat()
                    chatbot.clear_conversations()                
                    # print("*********退出程序**********")
                    break
                elif q == "重置":
                    try:
                        chatbot.reset_chat()
                        chatbot.clear_conversations()
                        # print("**************************")
                        # return("重置对话")
                        # print("**************************")
                    except Exception as e:
                        return("网络错误，重置失败，请再试一次")   
                else:
                    q = self.q + ",不能出现英语,20个汉字以内。"
                    try:
                        # start = time.time()
                        for data in chatbot.ask(q,conversation_id=conversation_id):
                            response = data['message']
                            # print(f"【ChatGPT】{response}")
                        return response
                        # end = time.time()
                        # print("time:",end - start)
                        i += 1
                    except Exception as e:
                        # print(e)
                        return("网络错误，再试一次")

            else:
                i = 1
                try:
                    chatbot.reset_chat()
                    chatbot.clear_conversations()
                    # print("**************************")
                    # print("*********重置对话**********")
                    # print("**************************")
                except Exception as e:
                    return("网络错误，重置失败，请再试一次")   

    

# print("Chatbot: ")
# prev_text = ""
# for data in chatbot.ask(
#     "Hello world",
#     conversation_id=0
# ):
#     message = data["message"][len(prev_text) :]
#     print(message, end="", flush=True)
#     prev_text = data["message"]
# print()
if __name__ == '__main__':
    chat = bot(user='user')
    chat.q = "你好"
    answer = chat.ask_gpt()
    print(answer)