# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 14:50:26 2018

@author: Alex

Check app data 
"""

#%% Import packages
import pickle 
import pandas as pd 

#%% Load data fed to app
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'topic_seq'

with open (filename, 'rb') as fp:
        topic_seq = pickle.load(fp)
        
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
        graph_mat,topic_labels, doc_topic_mat, word_embedding = pickle.load(fp)

topic_list = list(topic_labels.values())

filename = processed_data_folder + 'article_info'

with open (filename, 'rb') as fp:
        adf = pickle.load(fp)
        
#%% Add topic labels to data frame 
adf = adf.assign(topics=pd.Series(topic_list).values)

        
        