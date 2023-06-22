#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Install modules Area

# !pip install dash
# !pip install jupyter-dash
# !pip install dash-bootstrap-components
# !pip install statsmodels
# !pip install catboost

## Import Modules Area
#import pandas as pd
import dash
#import plotly.express as px
from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output,State
import dash_bootstrap_components as dbc
#import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import numpy as np
#from catboost import CatBoostClassifier
import base64


# In[2]:


# DataFrame 정의 Area

# import year_earn, buyer form csv file

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
kdc_dict_total = {
    '0': '총류',
    '1': '철학',
    '2': '종교',
    '3': '사회과학',
    '4': '자연과학',
    '5': '기술과학',
    '6': '예술',
    '7': '언어',
    '8': '문학',
    '9': '역사',
}



# In[4]:

# In[5]:



# Card components

cards = [
    dbc.Card(
        [
            html.H2('도서추천해드립니다. 선택하세요', className="card-title"),
           
        ],
        body=True,
        color="#00E858",
        inverse=True,
    )
]












# In[6]:


#페이지별 레이아웃 정의 Area

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

df_table = pd.DataFrame(columns=["이메일", "도서분류", "키워드"])

app.layout = dbc.Container(
    [
       
        html.Br(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Hr(),
        html.Div(['이메일:',
        dcc.Input(
            id="input-email",
            type= "text",
            placeholder="",style={"height": "30px", "font-size": "16px", "margin-right": "15px"}), 
        html.Div(id="out-all-types")
    ]), 
        html.Br(),       
        html.Div(['도서분류:',
        dcc.Dropdown(options=[
                {"label": kdc_dict_total[kdc], "value": kdc}
                for kdc in kdc_dict_total
            ], value='0', id='demo-dropdown', style={"height": "25px", "width": "420px", "font-size": "16px"})
        
]),          
        html.Br(),
        html.Div(['키워드:',
        dcc.Input(
            id="input-keyword",
            type= "text",
            placeholder="",style={"height": "30px", "font-size": "16px"}), 
        
]),

        html.Br(),
        html.Button("입력", id="button-add-row", n_clicks=0),
        html.Br(),
        html.Table(id="table-data", children=[
        html.Thead(html.Tr([html.Th(col) for col in df_table.columns])),
        html.Tbody([html.Tr([html.Td(df_table.loc[i, col]) for col in df_table.columns]) for i in range(len(df_table))])
]),
    ])

# In[7]:






# In[8]:


#@Callback Area

# 각 페이지별 앱 콜백
# callback




@app.callback(
    Output("table-data", "children"),
    Output("button-add-row", "n_clicks"),
    Output("button-add-row", "disabled"),
    Output("button-add-row", "children"),
    Output("table-data", "style_data_conditional"),
    Output("table-data", "style_header"),
    Input("button-add-row", "n_clicks"),
    State("input-email", "value"),
    State("demo-dropdown", "value"),
    State("input-keyword", "value"),
    prevent_initial_call=True
)
def update_table(n_clicks, email, dropdown, keyword):
    if n_clicks == 0 or (email or dropdown or keyword):
        df_table.loc[len(df_table)] = [email, dropdown, keyword]
    return [
        html.Thead(html.Tr([html.Th(col) for col in df_table.columns])),
        html.Tbody([html.Tr([html.Td(df_table.loc[i, col]) for col in df_table.columns]) for i in range(len(df_table))])
    ], n_clicks, False, "입력", [], []


if __name__== "__main__":
    app.run_server(debug=True, mode='inline', host='127.0.0.6')




