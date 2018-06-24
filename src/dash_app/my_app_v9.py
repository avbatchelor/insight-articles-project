# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pickle
import boto3
import io
import numpy
import pandas

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
app = dash.Dash()
server = app.server

###########################
# Layout dict 
layout = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Each dot is an NYC Middle School eligible for SONYC funding',
)


############################
# Layout section 
app.layout = html.Div(children=[
    html.H1(children='Blog curator'),

    html.Div(children='''
        Pick a topic you'd like to learn about:
    '''),

   
    html.Div(id='output-container',style={'padding': 10}),

    html.Div(children='''
        Select where you want to start and finish your reading:
    '''),

    html.Div(id='output-container',style={'padding': 10}),

    html.Div(id='my-datatable'),
    
    html.Div(
            [
            html.Div(
                [
                    dcc.Dropdown(
                        id='my-dropdown',
                        options=[{'label':topic, 'value':topic_no} for topic_no, topic in enumerate(topic_list)],
                        value=0)
                ], className = "six columns"
            ),

            html.Div(
                [

                ],
                style=layout_right,
                className="six columns"
            ),

            html.Div(
                [

                ],className="twelve columns")
        ], className="row"
    )

])

##############################
# Callbacks 
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

##############################
'''
external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})
'''
# Boostrap CSS.
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})

if __name__ == '__main__':
    app.run_server(debug=True)