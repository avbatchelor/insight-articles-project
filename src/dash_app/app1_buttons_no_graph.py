# -*- coding: utf-8 -*-
'''
Main app
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pickle
import boto3
import io
import numpy as np
import pandas
from dash.dependencies import Input, Output

from app import app

############################
# Load data

BUCKET_NAME = 'blog-seq-data' # replace with your bucket name

# list of topics
KEY = 'graph_and_labels' # replace with your object key
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
obj_str = obj['Body'].read()     
graph_mat,topic_labels,dist_mat,doc_topic_mat = pickle.loads(obj_str)

topic_list = list(topic_labels.values())

# article info
KEY = 'article_info' # replace with your object key
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
obj_str = obj['Body'].read()     
adf = pickle.loads(obj_str)

# topic sequence 
KEY = 'topic_seq' # replace with your object key
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
obj_str = obj['Body'].read()     
topic_sequence = pickle.loads(obj_str)


############################
# Navbar 
def get_menu():
    demo_slides = "https://docs.google.com/presentation/d/e/2PACX-1vTomIS7JWIKKHgNcO_Lh8uvxhAjREwyKYGEUPKTAyqkgpsrH00pdP7FBZsPSUWpT6txcI6tZdsYjniw/pub?start=false&loop=false&delayms=3000"

    menu = html.Div(children=[

        dcc.Link('App  |  ', href='/app', className="tab first"),

        dcc.Link('Methodology  |  ', href='/methodology', className="tab"),

        html.A('Demo Slides', href=demo_slides, target="_blank"),

        dcc.Link('  |  About Me   ', href='/about-me', className="tab"),

    ], className="six-columns offset-by-three")

    return menu

###########################
# Colors 
colors = {
    'background': '#FFFFFF', # white background 
    'text': '#000000' # black text 
}

#########################
# Layout
layout = html.Div([

    # Banner display
    html.Div([
        html.H2(
            'Blog curator',
            id='title'
        ),        

    ],
        className="banner"
    ),

    # Main content 
    html.Div(children=[

        # Menu row
        html.Div([
            get_menu(),
        ], className="row justify-content-center"),

        # Padding 
        html.Div(id='output-container',style={'padding': 10}),

        html.Div(children='''
            Pick a topic you'd like to learn about:
        '''),

        # Buttons row
        html.Div([
            html.Div([html.Button('Neural networks', id='nn-button', n_clicks_timestamp='0')], className = 'two columns'),
            html.Div([html.Button('Internet of things', id='rl-button', n_clicks_timestamp='0')], className = 'two columns'),
        ], className='row'),

        html.Div([
            html.Div([html.Button('Data science jobs', id='python-button', n_clicks_timestamp='0')], className = 'two columns'),
            html.Div([html.Button('Neural network libraries', id='big-button', n_clicks_timestamp='0')], className = 'two columns'),
        ], className='row'),

        html.Div([
            html.Div([html.Button('NLP', id='nlp-button', n_clicks_timestamp='0')], className = 'two columns'),
            html.Div([html.Button('Regression and classification', id='reg-button', n_clicks_timestamp='0')], className = 'two columns'),
        ], className='row'),

        # Padding 
        html.Div(id='output-container',style={'padding': 10}),

        # Data table
        html.Div(id='my-datatable'),
        

    ],className="container")
])





##############################
# Callbacks 

'''
# Data table callback
@app.callback(
    dash.dependencies.Output('my-datatable', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_rows(selected_value):
    output_arr = []
    for doc_no, topic in enumerate(topic_sequence[selected_value]):
        if doc_no != 0 and topic == selected_value:
            continue
        else:
            topic = int(topic)
            test_str = adf.iloc[topic]['title'] + '. ' + adf.iloc[topic]['author'] + ' ' + adf.iloc[topic]['link'] + ' ' + adf.iloc[topic]['source']
            output_arr.append(html.H3(topic_list[int(topic)]))
            output_arr.append(html.P(test_str))
    return output_arr
'''

# Data table callback v2 
@app.callback(Output('my-datatable', 'children'),
              [Input('nn-button', 'n_clicks_timestamp'),
               Input('rl-button', 'n_clicks_timestamp'),
               Input('python-button', 'n_clicks_timestamp'),
               Input('big-button', 'n_clicks_timestamp'),
               Input('nlp-button', 'n_clicks_timestamp'),
               Input('reg-button', 'n_clicks_timestamp'),
               ])
def display_sequence(btn1, btn2, btn3, btn4, btn5, btn6):
    # Determine which button was pressed
    btn_list = np.array([int(btn1),int(btn2),int(btn3),int(btn4),int(btn5),int(btn6)])
    btn_clicked = np.argmax(btn_list)

    # Determine corresponding topic 
    topic_lookup = [27,10,4,28,44,16]
    selected_topic = topic_lookup[btn_clicked]

    # Generate output 
    output_arr = []
    for doc_no, topic in enumerate(topic_sequence[selected_topic]):
        if doc_no != 0 and topic == selected_topic:
            continue
        else:
            topic = int(topic)
            test_str = adf.iloc[topic]['title'] + '. ' + adf.iloc[topic]['author'] + ' ' + adf.iloc[topic]['link'] + ' ' + adf.iloc[topic]['source']
            output_arr.append(html.H3(topic_list[int(topic)]))
            output_arr.append(html.P(test_str))

    # return output 
    return output_arr


##############################
# CSS 
'''
external_css = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
                "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]
'''
'''
external_css = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/0e463810ed36927caf20372b6411690692f94819/dash-drug-discovery-demo-stylesheet.css"]
'''
external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",  # Normalize the CSS
    "https://fonts.googleapis.com/css?family=Open+Sans|Roboto"  # Fonts
    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css",
    "https://rawgit.com/plotly/dash-live-model-training/master/custom_styles.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})