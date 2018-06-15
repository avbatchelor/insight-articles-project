import networkx as nx
import pickle
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx


processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
	graph_mat, topic_labels = pickle.load(fp)


G = nx.from_numpy_matrix(graph_mat) 
pos=nx.spring_layout(G)
nx.relabel_nodes(G,topic_labels)
nx.draw(G,pos)
nx.draw_networkx_labels(G,pos,topic_labels,font_size=16)

plot = figure(title="Blog Curator Demo", x_range=(-2.1,2.1), y_range=(-2.1,2.1),
              tools="", toolbar_location=None)

graph = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))
plot.renderers.append(graph)

output_file("networkx_graph.html")
show(plot)