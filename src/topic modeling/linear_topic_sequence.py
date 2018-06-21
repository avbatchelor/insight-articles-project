# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 17:30:31 2018

@author: Alex

Generate linear paths 
"""

#%% Import packages 
import pickle 
import numpy as np

#%% Load data 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
        graph_mat,topic_labels,dist_mat = pickle.load(fp)
        
#%% 
np.argsort(dist_mat,axis=0)
no_topics = len(graph_mat)
sequence_len = 3
topic_sequence = np.empty([no_topics,sequence_len])

neighbors = np.argmax(graph_mat,axis=1)
topic_sequence[:,0] = range(0,no_topics)
topic_sequence[:,1] = neighbors
topic_sequence[:,2] = neighbors[neighbors]

#%% Slider dictionary 
slider_dict = {}
for topic_no, row in enumerate(topic_sequence):
    slider_dict[topic_no] = {}
    for seq_no in range(0,3):
        if seq_no != 0 and topic_sequence[topic_no,seq_no] == topic_sequence[topic_no,0]:
            continue
        else:
            topic_idx = topic_sequence[topic_no,seq_no]
            slider_dict[topic_no][seq_no] = topic_labels[topic_idx]
            
#%% Save slider_dict 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'slider_dict'

with open(filename, 'wb') as fp:
    pickle.dump(slider_dict, fp)
    
#%% Save slider_dict 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'topic_seq'

with open(filename, 'wb') as fp:
    pickle.dump(topic_sequence, fp)