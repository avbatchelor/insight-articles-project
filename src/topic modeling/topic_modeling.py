# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 19:18:48 2018

@author: Alex

Fit LDA or NNMF
"""
# Code modified from: https://medium.com/mlreview/topic-modeling-with-scikit-learn-e80d33668730

#%% Import packages 
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from scipy.misc import toimage
import PIL

#%% Vectorize 
no_features = 1000

# NMF is able to use tf-idf
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(documents)
tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

#%% NMF and LDA
no_topics = 20

# Run NMF
nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

# Run LDA
lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

#%% Display topics 
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

no_top_words = 10
display_topics(nmf, tfidf_feature_names, no_top_words)
display_topics(lda, tf_feature_names, no_top_words)

#%% Look at probabilities 
doc_topic_mat = lda.transform(tf)

topic_word_mat = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]  

'''
#Visualize matrix 
toimage(doc_topic_mat).show()
from matplotlib import pyplot as plt
ax = plt.imshow(doc_topic_mat, interpolation='nearest')
ax.set_aspect('box')
plt.show()
'''
