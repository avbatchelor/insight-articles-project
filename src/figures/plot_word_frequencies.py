# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 15:55:41 2018

@author: Alex
"""

#%% Import packages 
import os 
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\topic modeling\\')
from topic_modeling import load_documents
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.feature_extraction import text 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


#%% Get data 
documents = load_documents(False,'normal')

#%% 

#%% Vectorize 
no_features = 1000
num_top_words = 50
my_stop_words = text.ENGLISH_STOP_WORDS.union(['use','make','good','example','zero'])
method = 'lda'
    
# NMF part
if method == 'nmf':
    tfidf_vectorizer = TfidfVectorizer(max_features=no_features, stop_words=my_stop_words)
    word_embedding = tfidf_vectorizer.fit_transform(documents)
    words = tfidf_vectorizer.get_feature_names()
elif method == 'lda':
    # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
    tf_vectorizer = CountVectorizer(max_features=no_features, stop_words=my_stop_words)
    word_embedding = tf_vectorizer.fit_transform(documents)
    words = tf_vectorizer.get_feature_names()

word_freqs = word_embedding.sum(axis=0)
top_word_idxs = np.fliplr(word_freqs.argsort())
top_100_words = top_word_idxs[0,0:num_top_words]
top_100_words = np.asarray(top_100_words).ravel()
idx_list = top_100_words.tolist()
top_words = [words[idx] for idx in idx_list]
word_freqs = np.asarray(word_freqs).ravel()
top_word_freqs = [word_freqs[idx] for idx in idx_list]
#top_word_idxs = top_word_idxs.ravel()
#[::-1]
        

#%% Generate histogram 
font = {'size'   : 18}
matplotlib.rc('font', **font)

top_word_freqs.reverse()
top_words.reverse()
plt.figure()    
plt.barh(range(1,num_top_words+1), top_word_freqs)
ax = plt.gca()
ax.set_yticks(range(1,num_top_words+1))
ax.set_yticklabels(top_words)

#%% Words per doc 
count_vectorizer = CountVectorizer
word_embedding2 = tf_vectorizer.fit_transform(documents)
word_embedding2 = word_embedding2.todense()
blog_size = word_embedding.sum(axis=1)

plt.figure()
plt.hist(blog_size)
plt.xlabel('Number of words')
plt.ylabel('Number of blogs')

font = {'size'   : 22}

matplotlib.rc('font', **font)

