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
from topic_modeling import get_topic_word_mat_select, select_articles
import matplotlib.pyplot as plt
import pickle
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


#%% Topic modeling 
method = 'nmf'
no_topics = 50
no_top_words = 1000 # orignallly looked at 10
no_labels = 5
n_grams = False
doc_type = 'normal'

# Run model 
topic_word_mat_select, topic_labels, doc_topic_mat, word_embedding = get_topic_word_mat_select(method, no_topics, no_top_words, no_labels, n_grams,doc_type)

# 
#adf = select_articles(doc_topic_mat,no_topics,topic_labels)

#%% How many docs per topic 
doc_topic = np.argmax(doc_topic_mat,axis=1)
docs_per_topic = []
for topic_no in range(1,no_topics+1):
    docs_per_topic.append(np.count_nonzero(doc_topic == topic_no))
        
plt.figure()    
plt.barh(range(1,no_topics+1), docs_per_topic)
ax = plt.gca()
ax.set_yticks(range(1,no_topics+1))
ax.set_yticklabels(topic_labels.values())
#plt.tight_layout()

#%% Remove topics that only have no documents associated with them 
# Find rare topics 
rare_topics = [idx for idx, value in enumerate(docs_per_topic) if value == 0]

# Get list of topics numbers not including rare topics 
topic_no_list = [x for x in range(0,no_topics) for y in rare_topics if x != y]

# Remove rows from topic_word_mat_select 
topic_word_mat_select = topic_word_mat_select[topic_no_list,:]

# Remove rows from topic labels 
for topic in rare_topics:
    del topic_labels[topic] 

#%% Get article info for selected topics 
selection_method = 'random'
select_articles(topic_no_list,doc_topic_mat,no_topics,topic_labels,word_embedding,selection_method)


#%% Calculate distances between the rows 
distance_method = 'old'
if distance_method == 'old':
    dist_mat = squareform(pdist(topic_word_mat_select, metric='cosine'))
    np.fill_diagonal(dist_mat,1) #Replace in place
elif distance_method == 'new':
    word_dist = squareform(pdist(topic_word_mat_select.T, metric='cosine'))
    
    

# Find max of each row 
graph_mat = np.zeros(dist_mat.shape)

# Draw connection if distance is below some arbitrary threshold
if method == 'lda':
    graph_mat = dist_mat < 0.5
else:
    graph_mat = dist_mat < 0.95
    
'''
# Draw connection only to nearest topic
max_idx = np.argmin(dist_mat,axis =1)
count = 0
for idx in max_idx:    
    graph_mat[count,idx] = 1
    count +=1
'''

#%% 
num_clusters = 8
kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit_predict(topic_word_mat_select)
for cluster_num in range(1,num_clusters+1):
    print('Cluster numer = ',cluster_num)
    topic_keys, = np.where(kmeans == cluster_num)
    print([topic_labels[key] for key in topic_keys])
    

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
    pickle.dump((graph_mat,topic_labels,dist_mat,doc_topic_mat), fp)
    
#%% Save graph as a png 
'''
fig_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\\figures\\'
fig_file = fig_folder + 'lda_graph.png'
nx.draw(G,fig_file, format='png', prog='neato')

'''

#%% Dendrogram 
from scipy.cluster.hierarchy import ward, dendrogram
from scipy.cluster.hierarchy import ward, dendrogram
from scipy.cluster.hierarchy import linkage

linkage_matrix = ward(dist_mat) #define the linkage_matrix using ward clustering pre-computed distances
#linkage_matrix = linkage(dist_mat)

fig, ax = plt.subplots(figsize=(15, 20)) # set size
ax = dendrogram(linkage_matrix, orientation="left", labels=list(topic_labels.values()));


#%% Visualize lda results 
'''
pyLDAvis.enable_notebook()
panel = pyLDAvis.sklearn.prepare(best_lda_model, data_vectorized, vectorizer, mds='tsne')
panel
'''