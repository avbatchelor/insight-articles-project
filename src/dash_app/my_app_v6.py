# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pickle
import dash_table_experiments as dt


############################
# Load data 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
        graph_mat,topic_labels,dist_mat = pickle.load(fp)

topic_list = list(topic_labels.values())

filename = processed_data_folder + 'article_info'

with open (filename, 'rb') as fp:
        adf = pickle.load(fp)

filename = processed_data_folder + 'topic_seq'

with open (filename, 'rb') as fp:
        topic_sequence = pickle.load(fp)

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
        id='my-dropdown',
        options=[{'label':topic, 'value':topic_no} for topic_no, topic in enumerate(topic_list)],
        value=0
    ),
    html.Div(id='output-container',style={'padding': 10}),

    html.Div(children='''
        Select where you want to start and finish your reading:
    '''),

    html.Div(id='output-container',style={'padding': 10}),

    html.Div(id='my-datatable')

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
            test_str = adf.iloc[doc_no]['title'] + '. ' + adf.iloc[doc_no]['author'] + ' ' + adf.iloc[doc_no]['link'] + ' ' + adf.iloc[doc_no]['source']
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
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


if __name__ == '__main__':
    app.run_server(debug=True)