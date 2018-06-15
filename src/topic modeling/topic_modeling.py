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
import pandas as pd
import pickle
import numpy as np

#%%
def load_documents():
    processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
    filename = processed_data_folder + 'kd_docs'

    with open (filename, 'rb') as fp:
        documents, included_blogs = pickle.load(fp)
    
    return documents

#%% Vectorize 
def get_features(method, documents):
    no_features = 1000
    
    if method == 'nmf':
        # NMF is able to use tf-idf
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
        word_embedding = tfidf_vectorizer.fit_transform(documents)
        feature_names = tfidf_vectorizer.get_feature_names()
        
    elif method == 'lda':
        # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
        word_embedding = tf_vectorizer.fit_transform(documents)
        feature_names = tf_vectorizer.get_feature_names()
        
    return word_embedding, feature_names

#%% NMF and LDA
def generate_model(method, no_topics, word_embedding):
    
    if method == 'nmf':
        # Run NMF
        model = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(word_embedding)
        
    elif method == 'lda':
        # Run LDA
        model = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(word_embedding)

    return model 

#%% Display topics 
def display_topics(model, feature_names, no_top_words,no_topics,no_labels, word_embedding):
    top_words = []
    topic_labels = {}
    top_word_idxs = []
    word_array = np.chararray((no_topics, no_top_words))
    word_array = np.chararray(word_array.shape,itemsize=20)
    for topic_idx, topic in enumerate(model.components_):
        word_count = 0
        # Print out topic number and top words
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        
        # Create a string that is a label for that topic
        topic_labels[topic_idx] = (" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_labels - 1:-1]]))
        
        for word_idx in topic.argsort()[:-no_top_words - 1:-1]:
            word_array[topic_idx,word_count] = feature_names[word_idx]
            word_count += 1
            top_words.append(feature_names[word_idx])
            top_word_idxs.append(word_idx)
            
            # Create a dataframe where rows are topics and columns are top words
        topic_word_mat = model.components_ / model.components_.sum(axis=1)[:, np.newaxis]  
        
        doc_topic_mat = model.transform(word_embedding)

    return word_array, top_words, top_word_idxs, topic_labels, topic_word_mat, doc_topic_mat


#%%
def select_top_words(top_word_idxs, topic_word_mat):
    # Get unique indexes 
    unique_idxs = np.array(list(set(top_word_idxs)))
    topic_word_mat_select = topic_word_mat[:,unique_idxs]
    
    return topic_word_mat_select 

#%% Look at probabilities
    

#%% 
    '''
from collections import Counter
counts = Counter(nmf_top_words)
print(counts)

# Get unique words
unique_words = set(nmf_top_words)
num_words = len(unique_words)

'''
'''
doc_topic_mat = lda.transform(tf)
'''


#%% Run model 
def get_topic_word_mat_select(method, no_topics, no_top_words, no_labels):
    
    # Load document
    documents = load_documents()
    
    # Get embeddings and features 
    word_embedding, feature_names = get_features(method, documents)
    
    # Generate model 
    model = generate_model(method, no_topics, word_embedding)
    
    words, top_words, top_word_idxs, topic_labels, topic_word_mat, doc_topic_mat = display_topics(model, feature_names, no_top_words, no_topics, no_labels, word_embedding)
    
    topic_word_mat_select = select_top_words(top_word_idxs, topic_word_mat)
    
    return topic_word_mat_select, topic_labels, doc_topic_mat

#%% Select articles 
def select_articles(doc_topic_mat,no_topics,topic_labels):
    
    adf = pd.DataFrame(columns=['source','title','author','link'])
    
    # Load article info 
    processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
    filename = processed_data_folder + 'kd_docs_info'

    with open (filename, 'rb') as fp:
        blog_info = pickle.load(fp)
        
    # Randomly select a document 
    doc_topic = np.argmax(doc_topic_mat,axis=1)

    for topic in range(0,no_topics):   
        topic_docs = np.squeeze(np.asarray(np.where(doc_topic == topic)))
        chosen_doc = np.random.choice(topic_docs)
    
        print(topic_labels[topic])
        print(blog_info.iloc[chosen_doc])  
        
        adf = adf.append(blog_info.iloc[chosen_doc],ignore_index=True)
        
    return adf
    

#%% Run model 
# Set parameters 
method = 'nmf'
no_topics = 40
no_top_words = 20 # orignallly looked at 10
no_labels = 5

# Run model 
topic_word_mat_select, topic_labels, doc_topic_mat = get_topic_word_mat_select(method, no_topics, no_top_words, no_labels)


# Select articles 
adf = select_articles(doc_topic_mat,no_topics,topic_labels)

#%% Save documents 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'article_info'

with open(filename, 'wb') as fp:
    pickle.dump(adf, fp)


'''
#Visualize matrix 
toimage(doc_topic_mat).show()
from matplotlib import pyplot as plt
ax = plt.imshow(doc_topic_mat, interpolation='nearest')
ax.set_aspect('box')
plt.show()
'''
