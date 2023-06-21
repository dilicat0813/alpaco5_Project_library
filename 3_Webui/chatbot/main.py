# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from helper.chat_gpt import ask_chat_GPT
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.CERULEAN]

app = Dash(__name__, external_stylesheets=external_stylesheets, assets_folder='./assets')

app.layout = html.Div(children=[
    html.Div([dcc.Loading(
            id='loading-output',
            type='circle',
            children=[html.Div(id='output-container')]
        ),
    ], className='row'),

    html.Div([
        html.Div([
            dcc.Input(id='input-box', type='text', placeholder='Send a message'),
            dbc.Button('Submit', color="primary", id='submit-button', n_clicks=0),
        ], className='input-container')
    ], className='row')
])



@app.callback(
    Output('output-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-box', 'value')])
def update_output(n_clicks, input_value):
    try:
        if n_clicks > 0:
            answer = ask_chat_GPT(input_value)
            return f'{answer}'
        else:
            return ''
    except Exception as e:
        print(e)
        return "에러 발생"


if __name__ == '__main__':
    app.run_server(debug=True)