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

############################
# Generate graph
G = nx.from_numpy_matrix(graph_mat) 
pos=nx.spring_layout(G)


#%% Create edges
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += [x0, x1, None]
    edge_trace['y'] += [y0, y1, None]

#%% Create nodes 
node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'].append(x)
    node_trace['y'].append(y)


############################
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Blog curator'),

    html.Div(children='''
        Pick a topic you'd like to learn about:
    '''),

    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montreal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC'
    ),
    html.Div(id='output-container',style={'padding': 10}),

    html.Div(children='''
        Select where you want to start and finish your reading:
    '''),

    dcc.RangeSlider(
        min=0,
        max=10,
        step=None,
        marks={
            0: '0 °F',
            3: '3 °F',
            5: '5 °F',
            7.65: '7.65 °F',
            10: '10 °F'
        },
        value=[3, 7.65]
    ),

    dcc.Graph(
        id='topic_network',
        figure={
            'data': [
                go.Figure(data=[edge_trace, node_trace]),
            ],
            'layout': go.Layout(
                title='<br>Network graph made with Python',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        }
    ),


])


if __name__ == '__main__':
    app.run_server(debug=True)