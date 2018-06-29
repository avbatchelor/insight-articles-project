# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 18:03:01 2018

@author: Alex

Cluster topics using NMF 
"""

#%% Import packages 
import os
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\topic modeling\\') 
from topic_modeling import load_documents
import pickle
import numpy as np
from topic_modeling import get_topic_word_mat_select


#%% Load relevant data 
#Load documents 
documents = load_documents(True,'normal')

# Load topic assignments 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'graph_and_labels'

with open (filename, 'rb') as fp:
        graph_mat,topic_labels,dist_mat,doc_topic_mat = pickle.load(fp)

topic_list = list(topic_labels.values())
        
#%% Get the topic assignments for each document
topic_assignments = np.argmax(doc_topic_mat,axis=1)


#%% Sum the strings of the documents that belong to the same topics 
meta_documents = []
for topic_no in range(0,len(topic_list)):
    doc_nos, = np.where(topic_assignments == topic_no)
    temp_documents = [documents[doc_no] for doc_no in doc_nos]
    meta_documents.append(' '.join(temp_documents))

# Save meta documents 
# Save documents 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'meta_docs'

with open(filename, 'wb') as fp:
    pickle.dump(meta_documents, fp)    
    
    
#%% Perform NMF 
method = 'nmf'
no_topics = 20
no_top_words = 1000 # orignallly looked at 10
no_labels = 5
n_grams = False
doc_type = 'meta'

# Run model 
topic_word_mat_select, meta_topic_labels, meta_doc_topic_mat, word_embedding = get_topic_word_mat_select(method, no_topics, no_top_words, no_labels, n_grams,doc_type)

#%% Find the max topic for each 'document' i.e. the meta-topic assignment
meta_topic_assignments = np.argmax(meta_doc_topic_mat,axis=1)

#%% Print topic assignment results
for topic_no in range(0,no_topics):
    topic_idxs, = np.where(meta_topic_assignments == topic_no)
    print('Meta topic no = ',topic_no,' ',meta_topic_labels[topic_no])
    print([topic_labels[key] for key in topic_idxs])
    
#%% Save assigments 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'topic_assignments'

with open(filename, 'wb') as fp:
    pickle.dump((topic_assignments, meta_topic_assignments), fp)  
