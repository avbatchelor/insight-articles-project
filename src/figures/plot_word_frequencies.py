# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 15:55:41 2018

@author: Alex
"""

#%% Import packages 
from topic_modeling import load_documents
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

#%% Get data 
documents = load_documents(False)

tfidf_vectorizer = TfidfVectorizer()
word_embedding = tfidf_vectorizer.fit_transform(documents)
words = tfidf_vectorizer.get_feature_names()
word_freqs = word_embedding.sum(axis=0)
top_word_idxs = word_freqs.argsort()
top_word_idxs = top_word_idxs.ravel()
[::-1]

tf_vectorizer = CountVectorizer()
word_embedding = tf_vectorizer.fit_transform(documents)
feature_names = tf_vectorizer.get_feature_names()
feature_counts = 

#%% Plot data 