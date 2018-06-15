# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:41:40 2018

@author: Alex

Generate distance matrix and directed graph 

"""
#%% Import packages 
from scipy.spatial.distance import pdist, squareform
import networkx as nx
import numpy as np
import os 
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\topic modeling\\')
from topic_modeling import get_topic_word_mat_select
import matplotlib.pyplot as plt
import pickle

#%% Topic modeling 
method = 'nmf'
no_topics = 20
no_top_words = 20 # orignallly looked at 10
no_labels = 5

# Run model 
topic_word_mat_select, topic_labels, doc_topic_mat = get_topic_word_mat_select(method, no_topics, no_top_words, no_labels)

#%% Calculate distances between the rows 
dist_mat = squareform(pdist(topic_word_mat_select, metric='cosine'))
temp_dist_mat = dist_mat
np.fill_diagonal(temp_dist_mat,1)

# Find max of each row 
graph_mat = np.zeros(dist_mat.shape)
max_idx = np.argmin(dist_mat,axis =1)
count = 0
for idx in max_idx:    
    graph_mat[count,idx] = 1
    count +=1

#%% Visualize graph 
# Code copied from: https://stackoverflow.com/questions/13513455/drawing-a-graph-or-a-network-from-a-distance-matrix

plt.close()
G = nx.from_numpy_matrix(graph_mat) 
#pos = nx.graphviz_layout(G)
#pos = nx.nx_agraph.graphviz_layout(G)
pos=nx.spring_layout(G)
nx.relabel_nodes(G,topic_labels)
nx.draw(G,pos)
nx.draw_networkx_labels(G,pos,topic_labels,font_size=16)

#%% Save graph mat and labels 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open(filename, 'wb') as fp:
    pickle.dump((graph_mat,topic_labels), fp)
    
#%% Generate linear paths 



'''

'''
# add labels 
'''


'''
'''
fig_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\\figures\\'
fig_file = fig_folder + 'lda_graph.png'
nx.draw(G,fig_file, format='png', prog='neato')

'''

#%% Dendrogram 
from scipy.cluster.hierarchy import ward, dendrogram

linkage_matrix = ward(dist_mat) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, orientation="left", labels=list(topic_labels.values()));
