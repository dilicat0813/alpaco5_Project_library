# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

from component.subscribe import make_subscribe_html
from component.chat_generator import ChatGenerator
from helper.gpt_search_csv import ask_librarian

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.CERULEAN]

app = Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='./assets')

conversation = [
    {
        "speaker":"bot",
        "text": "안녕하세요 \n 도서추천 봇입니다."
    }
]
chat_generator_instance = ChatGenerator(conversation)

tab1 = [html.Div([
        dcc.Loading(
            id='loading-output',
            type='circle',
            children=[html.Div(className="chat-container", id='output_chat')]
        ),
    ], className="row "),

    html.Div([
        html.Div([
            dcc.Input(id='input-box', type='text', placeholder='질문을 입력해주세요', style={"font-size": "13px", 'min-width':'45vw'}),
            dbc.Button('질문하기', color="primary", id='submit-button', n_clicks=0, style={"font-size": "13px"}),
        ], className='input-container')
    ], className='row'),]
tab2 = [
    html.Div([
        make_subscribe_html()
    ], className='row subscribe-container')
]

app.layout = html.Div(children=[
    dbc.Tabs([
        dbc.Tab(label='도서추천 봇', children=tab1),
        dbc.Tab(label='도서추천 메일서비스', children=tab2), 
    ], style={"font-size": "13px", 'font-weight':'bold'})
], className="body__sheet")


@app.callback(
    Output('output_chat', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, input_value):
    if not input_value:
        return chat_generator_instance.make_chat_list()

    chat_generator_instance.add_chat(input_value, speaker="user")
    try:
        if n_clicks > 0:
            answer = ask_librarian(input_value)
            
            chat_generator_instance.add_chat(answer, speaker="bot")
            return chat_generator_instance.make_chat_list()
        else:
            chat_generator_instance.add_chat('에러가 발생하여 답변을 전달하지 못했습니다', speaker='bot')
            return chat_generator_instance.make_chat_list()
    except Exception as e:
        print(e)
        return "에러 발생"


if __name__ == '__main__':
    app.run_server(debug=False)