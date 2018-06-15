# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pickle

############################
# Load data 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
        graph_mat,topic_labels = pickle.load(fp)

topic_list = list(topic_labels.values())

# Slider data 
filename = processed_data_folder + 'slider_dict'

with open (filename, 'rb') as fp:
        slider_dict = pickle.load(fp)

############################
app = dash.Dash()


############################
# Layout section 
app.layout = html.Div(children=[
    html.H1(children='Blog curator'),

    html.Div(children='''
        Pick a topic you'd like to learn about:
    '''),

    dcc.Dropdown(
        id='topic_dropdown',
        options=[{'label':topic, 'value':topic_no} for topic_no, topic in enumerate(topic_list)],
        value='NYC'
    ),
    html.Div(id='output-container',style={'padding': 10}),

    html.Div(children='''
        Select where you want to start and finish your reading:
    '''),

    dcc.RangeSlider(
        id='topic_slider',
        min=0,
        max=20,
        step=None,
        value=[0, 5]
    ),

])

##############################
# Callbacks 
@app.callback(
    dash.dependencies.Output('topic_slider', 'marks'),
    [dash.dependencies.Input('topic_dropdown', 'value')])
def update_slider(topic_no):
    selected_dict = slider_dict[topic_no]
    return dcc.RangeSlider(
        marks=selected_dict,
        )

if __name__ == '__main__':
    app.run_server(debug=True)