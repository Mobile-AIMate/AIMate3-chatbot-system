from revChatGPT.V1 import Chatbot
import time
chatbot = Chatbot(config={
"access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJhaW1hdGUxMjJAeWFob28uY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJodHRwczovL2FwaS5vcGVuYWkuY29tL2F1dGgiOnsidXNlcl9pZCI6InVzZXItQUpvVzZEckxZOTgzc3BsVzFQT0ZqZUlqIn0sImlzcyI6Imh0dHBzOi8vYXV0aDAub3BlbmFpLmNvbS8iLCJzdWIiOiJhdXRoMHw2NDJhNjJlYjRkMWMyZWMyNmY2OWNlMjAiLCJhdWQiOlsiaHR0cHM6Ly9hcGkub3BlbmFpLmNvbS92MSIsImh0dHBzOi8vb3BlbmFpLm9wZW5haS5hdXRoMGFwcC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjgxMzA5ODI5LCJleHAiOjE2ODI1MTk0MjksImF6cCI6IlRkSkljYmUxNldvVEh0Tjk1bnl5d2g1RTR5T282SXRHIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBtb2RlbC5yZWFkIG1vZGVsLnJlcXVlc3Qgb3JnYW5pemF0aW9uLnJlYWQgb2ZmbGluZV9hY2Nlc3MifQ.BxA97CFo23P7TWQjw4MQnaR_5LwWpEuf29GB9C6P-WsLRaQmk6TFLey_C3irafIill28VYoNk8iJtSPejHOGebn6aZphMIi3NO0r2EZJyo9r_hFGEC8eegl5lVcLva4-5VV-8-9ywjfZXQNPuxCLorMs8oQTjSXWPh0Nx5wshlfhkliHuW6bv63QSyeFK-y1QR4Oc7q01BBcu1Kw3Pj-QxBbzBpXtbE2wXqZW2FqjzkFhysqH88RlCe-lwHiJbmR7JVBABq1I3LO8kgTavbJExZOIMiOXe-gtgWUknMmu8mLcr_CKb05hMxYuH4m3xkWxCbPdg5MRtTABjGLKgKU1g"
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
                q = self.q + ",不能出现英语,20个汉字以内。"
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