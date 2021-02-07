# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 18:58:27 2021

@author: mbourque
"""

import pandas as pd
import numpy as np
from yldcrv_funcs import *
import datetime as dt

import plotly.express as plx
import plotly.graph_objects as go
import plotly.io as pio
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

df_cad, df_ont, df_que, df_ab, df_bc = get_data(sdate = '20000101',
                                                edate=dt.datetime.today().strftime("%Y%m%d"))


maxda = max(df_cad.index)
default_date = maxda - dt.timedelta(weeks=1)

while not is_busday(default_date):
    default_date = default_date - dt.timedelta(days=1)
 
    
app.layout = html.Div([

    html.H1("Canadian Yield Curves", style={'text-align': 'center'}),

    dcc.Dropdown(id="crv",
                 options=[
                     {"label": "CAD", "value": 0},
                     {"label": "ONT", "value": 1},
                     {"label": "QUE", "value": 2},
                     {"label": "AB", "value": 3},
                     {"label": "BC", "value": 4}],
                 multi=False,
                 value=0,
                 style={'width': "40%"}
                 ),
    
    dcc.DatePickerSingle(id="date",
                         style={'width': "40%"},
                         max_date_allowed=maxda, 
                         date=default_date), 

    html.Div(id='message1', children=[]),
    html.Br(), # break between drop down and graph

    dcc.Graph(id='yldcrv', figure={}),
    dcc.Graph(id='slp', figure={}),
    dcc.Graph(id='roc', figure={}),
    
    dcc.Dropdown(id="sprdcrv",
                 options=[
                     {"label": "CAD", "value": 0},
                     {"label": "ONT", "value": 1},
                     {"label": "QUE", "value": 2},
                     {"label": "AB", "value": 3},
                     {"label": "BC", "value": 4}],
                 multi=False,
                 value=0,
                 style={'width': "40%"}
                 ),
    
    html.Div(id='message2', children=[]),
    
    dcc.Graph(id='sprd', figure={})
    
])

@app.callback(
    [Output(component_id='message1', component_property='children'),
    Output(component_id='yldcrv', component_property='figure'),
    Output(component_id='slp', component_property='figure'),
    Output(component_id='roc', component_property='figure')],
    [Input(component_id='crv', component_property='value'),
     Input(component_id='date', component_property='date')]
)

def choose_crv(crvId, hdate):
    
    if crvId == 0:
        crv = "CAD"
        df = df_cad
        
    elif crvId == 1:
        crv = "ONT"
        df = df_ont
        
    elif crvId == 2:
        crv = "QUE"
        df = df_que

    elif crvId == 3:
        crv = "AB"
        df = df_ab        
        
    elif crvId == 4:
        crv = "BC"
        df = df_bc   
        
    td = dt.datetime.today()
    
    while not is_busday(td):
        td = td - dt.timedelta(days=1)
        
    temp = dt.datetime.strptime(hdate[:10], '%Y-%m-%d')
    while not is_busday(hdate):
        temp = temp - dt.timedelta(days=1)
        
    hdate = temp.strftime('%Y-%m-%d')
        
    try:
        df_hist = df.loc[hdate]
        df = df.loc[td.strftime("%Y-%m-%d")]
        x = [d[5:8] for d in df_cad.loc[td.strftime("%Y-%m-%d")].index.values]   
        
        message = ""
        
        # yield curve
        yldcrv = go.Figure(data=go.Scatter(x = x,
                                           y = df.values,
                                           name = td.strftime("%Y-%m-%d")))
        yldcrv.add_trace(go.Scatter(x = x,
                                    y = df_hist.values,
                                    name = hdate,
                                    line = dict(dash='dot')))
        
        yldcrv.update_layout(title= "Yield Curve")
                            #,template ="plotly_dark")
        
        # steepness plot
        slp_y = df.values - df.values[0]
        slp_y_hist = df_hist.values - df_hist.values[0]
        slp = go.Figure(data=go.Scatter(x = x,
                                        y = slp_y,
                                        name = td.strftime("%Y-%m-%d")))
        slp.add_trace(go.Scatter(x = x,
                                 y = slp_y_hist,
                                 name = hdate,
                                 line = dict(dash='dot')))
                                
        slp.update_layout(title = "Rolldown")
                          #,template ="plotly_dark")
        
        # rate of change plot
        roc_y = np.append(np.zeros(1), np.diff(df.values))
        roc_y_hist = np.append(np.zeros(1), np.diff(df_hist.values))
        roc = go.Figure(data=go.Scatter(x = x,
                                        y = roc_y,
                                        name = td.strftime("%Y-%m-%d")))
        
        roc.add_trace(go.Scatter(x = x,
                                 y = roc_y_hist,
                                 name = hdate,
                                 line = dict(dash='dot')))
        
        roc.update_layout(title = "Rate of Change")
                          #,template ="plotly_dark")
     
          
    except:
        message = "Data does not exist for {} curve".format(crv)
        yldcrv = {}
        slp = {}
        roc = {}

    return message, yldcrv, slp, roc

@app.callback(
    Output(component_id='sprd', component_property='figure'),
    [Input(component_id='sprdcrv', component_property='value'),
     State(component_id='crv', component_property='value')],
    prevent_initial_call=True
)

def update_sprd(sprdcrvId, crvId):
        
    ### original curve ###
    if crvId == 0:
        crv = "CAD"
        df = df_cad
       
    elif crvId == 1:
        crv = "ONT"
        df = df_ont
        
    elif crvId == 2:
        crv = "QUE"
        df = df_que

    elif crvId == 3:
        crv = "AB"
        df = df_ab        
        
    elif crvId == 4:
        crv = "BC"
        df = df_bc  
    
    ### spread  ###
    if sprdcrvId == 0:
        crv_sprd = "CAD"
        df_sprd = df_cad
    
    elif sprdcrvId == 1:
        crv_sprd = "ONT"
        df_sprd = df_ont
        
    elif sprdcrvId == 2:
        crv_sprd = "QUE"
        df_sprd = df_que

    elif sprdcrvId == 3:
        crv_sprd = "AB"
        df_sprd = df_ab
        
    elif sprdcrvId == 4:
        crv_sprd = "BC"
        df_sprd = df_bc
        
    td = dt.datetime.today()

    while not is_busday(td):
        td = td - dt.timedelta(days=1)
    
        
    try:
        df = df.loc[td.strftime("%Y-%m-%d")]
        df_sprd = df_sprd.loc[td.strftime("%Y-%m-%d")]
        x = [d[5:8] for d in df_cad.loc[td.strftime("%Y-%m-%d")].index.values]
        
        y = df.values - df_sprd.values
    
        sprd = go.Figure(data=go.Scatter(x = x,
                                         y = y))
        sprd.update_layout(title = "Spread",
                       yaxis_title = crv + " - " + crv_sprd)
    except:
        sprd = {}
        
    return sprd

#debug=True, use_reloader=False

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
    
    
    