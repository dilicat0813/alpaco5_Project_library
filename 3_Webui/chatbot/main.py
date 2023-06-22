# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from helper.chat_gpt import ask_chat_GPT
import dash_bootstrap_components as dbc
from component.chat_generator import ChatGenerator
from time import sleep

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.CERULEAN]

app = Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='./assets')

conversation = []
chat_generator_instance = ChatGenerator(conversation)


app.layout = html.Div(children=[

    html.Div([
        dcc.Loading(
            id='loading-output',
            type='circle',
            children=[html.Div(className="chat-container", id='output_chat')]
        ),
    ], className="row "),
    
    html.Div([
        html.Div([
            dcc.Input(id='input-box', type='text', placeholder='Send a message'),
            dbc.Button('Submit', color="primary", id='submit-button', n_clicks=0),
        ], className='input-container')
    ], className='row')
])



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
            sleep(0.5)
            answer = "임시 답변"
            #answer = ask_chat_GPT(input_value)
            chat_generator_instance.add_chat(answer, speaker="bot")
            return chat_generator_instance.make_chat_list()
        else:
            chat_generator_instance.add_chat('에러가 발생하여 답변을 전달하지 못했습니다', speaker='bot')
            return chat_generator_instance.make_chat_list()
    except Exception as e:
        print(e)
        return "에러 발생"


if __name__ == '__main__':
    app.run_server(debug=True)