# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 10:41:40 2018

@author: Alex

Generate distance matrix and directed graph 

"""

#%% Calculate distances between the rows 
from scipy.spatial.distance import pdist, squareform

dist_mat = squareform(pdist(topic_word_mat, metric='cosine'))

#%% Visualize graph 
import networkx as nx
import numpy as np
import string

# Code copied from: https://stackoverflow.com/questions/13513455/drawing-a-graph-or-a-network-from-a-distance-matrix

G = nx.from_numpy_matrix(dist_mat) 
nx.draw(G,with_labels = True)

# add labels 
pos=nx.spring_layout(G)
labels={'0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19'}
nx.draw_networkx_labels(G,pos,labels,font_size=16)


'''
fig_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\\figures\\'
fig_file = fig_folder + 'lda_graph.png'
nx.draw(G,fig_file, format='png', prog='neato')

'''