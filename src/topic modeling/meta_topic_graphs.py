# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 16:36:56 2018

@author: Alex
"""

#%% Import packages 
import pickle 
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import os 
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\topic modeling\\')
from plotly_network import plot


#%% Load data
# Load metatopic allocations 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'topic_assignments'

with open(filename, 'rb') as fp:
    topic_assignments, meta_topic_assignments = pickle.load(fp)
    
# Load distance matrix 
filename = processed_data_folder + 'graph_and_labels'

with open(filename, 'rb') as fp:
    graph_mat,topic_labels,dist_mat,doc_topic_mat = pickle.load(fp) 
    

#%% Loop through meta-topics 
plt.close()
#for meta_topic in np.unique(meta_topic_assignments):
meta_topic = 0
# Find the sub topics 
sub_topics, = np.where(meta_topic_assignments == meta_topic)

# Get the distance matrix just for those topics    
sub_dist_mat = dist_mat[sub_topics][:,sub_topics]

# Generate the graph matrix by selecting an appropriate threshold
graph_mat = sub_dist_mat < 0.95
if not np.any(graph_mat):
    min_val = np.min(sub_dist_mat)
    graph_mat = sub_dist_mat <= min_val

# Find the docs belonging to that subtopic 
#docs = np.in1d(topic_assignments,sub_topics)

# Get subtopic labels 
sub_topic_labels = {sub_topic:topic_labels[sub_topic] for sub_topic in sub_topics if sub_topic in topic_labels}
new_sub_topic_labels = {}

# 

# Rename the keys 
for counter, value in enumerate(sub_topic_labels.keys()):
    new_sub_topic_labels[counter] = sub_topic_labels[value]


# Plot the graph 
plt.figure()
G = nx.from_numpy_matrix(graph_mat) 
#pos = nx.graphviz_layout(G)
#pos = nx.nx_agraph.graphviz_layout(G)
#pos=nx.spring_layout(G)
pos = nx.layout.circular_layout(G)
nx.relabel_nodes(G,sub_topic_labels)
nx.draw(G,pos)
nx.draw_networkx_labels(G,pos,new_sub_topic_labels,font_size=16)

node_labels = list(sub_topic_labels.values())

#%% Calculate text positions
text_pos = []
for key, value in pos.items():
    if value[0] < 0:
        pos_part2 = ' left'
    else:
        pos_part2 = ' right'
    if value[1] < 0:
        pos_part1 = 'bottom'
    else:
        pos_part1 = 'top'
    text_pos.append(pos_part1 + pos_part2)

#%% Plot in plot 
url = plot(G,pos,node_labels,text_pos)
