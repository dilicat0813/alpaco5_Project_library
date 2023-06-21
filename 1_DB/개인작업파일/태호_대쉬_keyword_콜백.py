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
from dash import Dash, dcc, html, Input, Output
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
도서분류 = ['총류', '철학', '종교', '사회과학', '자연과학', '기술과학', '예술', '언어', '문학', '역사']



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



app.layout = dbc.Container(
    [
       
        html.Br(),
        dbc.Row([dbc.Col(card) for card in cards]),
        html.Hr(),
        html.Div(['이메일:',
        dcc.Input(
            id="input",
            type= "text",
            placeholder=""), 
        html.Div(id="out-all-types")
    ]), 
        # html.Br(),       
        html.Div(['도서분류:',
        dcc.Dropdown(options=도서분류, value=도서분류[0], id='demo-dropdown'),
        html.Div(id='dd-output-container')
]), 
        html.Div(['키워드:',
        dcc.Input(
            id="input2",
            type= "text",
            placeholder=""), 
        html.Div(id="out-all-types2")
])
    
])



# In[7]:






# In[8]:


#@Callback Area

# 각 페이지별 앱 콜백
# callback

@app.callback(
    Output("out-all-types", "children"),
    Input("input", "value")
)
def cb_render(input):
    return u'Input {}'.format(input)



@app.callback(
    Output(component_id='dd-output-container', component_property='children'),
    Input(component_id='demo-dropdown', component_property='value'),
        # 이거 인풋에 컴포넌트 아이디와 컴포넌트 프로폴티 적어주는게 좋다. 나중에 해깔릴까봐.
    )                        #   인풋 아웃풋 콜백한거 def 함수를 이용해 받는다. 데코레이터 좀 더 공부해볼 것 뼈대는 있고 꾸미는 장식
def update_output(lines):
    return   # 함수 리턴으로 받는다.

@app.callback(
    Output("out-all-types2", "children"),
    Input("input2", "value")
)
def cb_render(input2):
    return u'Input {}'.format(input2)


if __name__== "__main__":
    app.run_server(debug=True, mode='inline', host='127.0.0.6')




