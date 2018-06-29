# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pickle
import io

############################
# Load data 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
        graph_mat,topic_labels,dist_mat,doc_topic_mat = pickle.load(fp)

topic_list = list(topic_labels.values())

filename = processed_data_folder + 'article_info'

with open (filename, 'rb') as fp:
        adf = pickle.load(fp)

filename = processed_data_folder + 'topic_seq'

with open (filename, 'rb') as fp:
        topic_sequence = pickle.load(fp)

############################
app = dash.Dash()
server = app.server
app.config['suppress_callback_exceptions']=True


#############################################################################
# Navbar 
def get_menu():
    menu = html.Div([

        dcc.Link('App   ', href='/app', className="tab first"),

        dcc.Link('Methodology   ', href='/methodology', className="tab"),

        dcc.Link('Demo Slides   ', href='/demo-slides', className="tab"),

        dcc.Link('About Me   ', href='/about-me', className="tab"),

    ], className="row justify-content-center")
    return menu

#########################
# Layout
layout = html.Div([
    # Title
    html.Div([
        html.H1(children='Blog curator'),
    ], className="row justify-content-center"),

    # Menu
    html.Div([
        get_menu(),
    ], className="row justify-content-center"),

    # Main content 
    html.Div(children=[

        html.Div(children='''
            Pick a topic you'd like to learn about:
        '''),

        # Buttons
        html.Div([
            html.Div([], className = 'one columns'),
            html.Div([html.Button('Neural networks', id='nn-button')], className = 'two columns'),
            html.Div([], className = 'two columns'),
            html.Div([html.Button('Reinforcement learning', id='rl-button')], className = 'two columns'),
            html.Div([], className = 'two columns'),
            html.Div([html.Button('Python', id='python-button')], className = 'two columns'),
        ], className='row'),

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
                    className="ten columns"
                ),

                html.Div(
                    [

                    ],className="twelve columns")
            ], className="row"
        ),

        html.Div(id='output-container',style={'padding': 10}),

        html.Div(id='my-datatable'),
        

    ]),
])





##############################
# Callbacks 

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


##############################
# CSS 
'''
external_css = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
                "https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "https://codepen.io/bcd/pen/KQrXdb.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]
'''
external_css = ["https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
                ]

for css in external_css:
    app.css.append_css({"external_url": css})



##############################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)