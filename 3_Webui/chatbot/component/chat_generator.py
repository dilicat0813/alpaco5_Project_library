from .bot_textbox import bot_textbox
from .user_textbox import user_textbox
from dash import html


class ChatGenerator:

    conversation = [
        # {
        #     "speaker":"user",
        #     "text": "교육 책 추천해줘"
        # },
        # {
        #     "speaker":"bot",
        #     "text": "수학의 정석 추천합니다"
        # }
    ]

    def __init__(self, conversation):
        self.conversation = conversation

    def add_chat(self, text, speaker='user'):
        new_chat = {
            "speaker": speaker,
            "text": text
        }
        self.conversation.append(new_chat)
        print(self.conversation)
    
    def make_chat_list(self):
        chat_list = []
        for chat in self.conversation:
            if chat["speaker"] == 'user':
                chat_list.append(
                    html.Div([
                        user_textbox(chat["text"])
                    ], className="row chat_right"))
            elif chat["speaker"] == 'bot':
                chat_list.append(
                    html.Div([
                        bot_textbox(chat["text"])
                    ], className="row chat_left"))
        return chat_list

        
