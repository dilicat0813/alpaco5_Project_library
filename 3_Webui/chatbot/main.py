# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
from component.textbox import textbox

app = Dash(__name__)

conversation = [
    {
        "speaker": 'user',
        "text":"교육책 추천해줘"
    },
    {
        "speaker": 'bot',
        "text": "수학의 정석 추천합니다"
    }
]
# 1. conversation을 for loop 돌려서 text가 밑으로 떨어지도록
# 2. speaker에 따라서 bot_textbox, user_textbox 따로 사용
# 3. bot_textbox, user_textbox 둘이 달라보이게 스타일링


app.layout = html.Div(children=[
    textbox('텍스트 박스 ')
])

if __name__ == '__main__':
    app.run_server(debug=True)