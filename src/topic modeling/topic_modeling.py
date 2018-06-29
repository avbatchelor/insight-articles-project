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
from sklearn.feature_extraction import text 
from scipy.spatial.distance import pdist, squareform


#%%
def load_documents(n_grams,doc_type):
    
    processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
    
    if doc_type == 'normal':
        
        
        filename = processed_data_folder + 'kd_docs'
        
        with open (filename, 'rb') as fp:
            documents, included_blogs = pickle.load(fp)
            
    elif doc_type == 'meta':
        
        filename = processed_data_folder + 'meta_docs'
        
        with open (filename, 'rb') as fp:
            documents = pickle.load(fp)
        
        
    return documents
    
'''        
    if n_grams == True:
        filename = processed_data_folder + 'documents_ngrams'
    
        with open (filename, 'rb') as fp:
            documents = pickle.load(fp)
''' 
   

#%% Vectorize 
def get_features(method, documents):
    no_features = 1000
    
    my_stop_words = text.ENGLISH_STOP_WORDS.union(['use','make','good','example','zero'])

    
    if method == 'nmf':
        # NMF is able to use tf-idf
        vectorizer = TfidfVectorizer(max_features=no_features, stop_words=my_stop_words)
        word_embedding = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names()
        
    elif method == 'lda':
        # LDA can only use raw term counts for LDA because it is a probabilistic graphical model
        vectorizer = CountVectorizer(max_features=no_features, stop_words=my_stop_words)
        word_embedding = vectorizer.fit_transform(documents)
        feature_names = vectorizer.get_feature_names()
        
    return word_embedding, feature_names, vectorizer

#%% NMF and LDA
def generate_model(method, no_topics, word_embedding):
    
    if method == 'nmf':
        # Run NMF
        model = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd',verbose=1).fit(word_embedding)
        
    elif method == 'lda':
        # Run LDA
        model = LatentDirichletAllocation(n_topics=no_topics, max_iter=50, learning_method='online', learning_offset=50.,random_state=0,verbose=1,evaluate_every=1).fit(word_embedding)
        
        print("Log Likelihood: ", model.score(word_embedding))
        print("Perplexity: ", model.perplexity(word_embedding))

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
        '''
        # Print out topic number and top words
        print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        '''
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
def get_topic_word_mat_select(method, no_topics, no_top_words, no_labels, n_grams,doc_type):
    
    # Load document
    documents = load_documents(n_grams,doc_type)
    
    # Get embeddings and features 
    word_embedding, feature_names, vectorizer = get_features(method, documents)
    
    # Generate model 
    model = generate_model(method, no_topics, word_embedding)
    
    words, top_words, top_word_idxs, topic_labels, topic_word_mat, doc_topic_mat = display_topics(model, feature_names, no_top_words, no_topics, no_labels, word_embedding)
    
    topic_word_mat_select = select_top_words(top_word_idxs, topic_word_mat)
    
    # Save model, word_freqs and vectorizer  
    word_freqs = word_embedding 
    processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
    filename = processed_data_folder + 'lda_viz_data'
    
    with open(filename, 'wb') as fp:
        pickle.dump((model, word_freqs, vectorizer), fp)
    
    
    return topic_word_mat_select, topic_labels, doc_topic_mat, word_embedding

#%% Select articles 
def select_articles(topic_no_list,doc_topic_mat,no_topics,topic_labels,word_embedding,selection_method):
    
    adf = pd.DataFrame(columns=['source','title','author','link'])
    
    # Load article info 
    processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
    filename = processed_data_folder + 'kd_docs_info'

    with open (filename, 'rb') as fp:
        blog_info = pickle.load(fp)
    
    if selection_method == 'random':
        # Randomly select a document 
        doc_topic = np.argmax(doc_topic_mat,axis=1)

    for topic in topic_no_list:   
        '''
        Select document based on:
            which document has the most similar probability distribution
            over words at that topic 
        '''
        if selection_method == 'closest':
            # Find the cosine distance between that topic and all documents 
            topic_array = topic_word_mat[topic]
            word_embedding_temp = word_embedding.todense()
            comp_mat = np.vstack((topic_array,word_embedding_temp))
            distances = squareform(pdist(comp_mat,metric='cosine'))
            np.fill_diagonal(distances,1)
            chosen_doc = np.argmin(distances[0,:])
        else:
            topic_docs = np.squeeze(np.asarray(np.where(doc_topic == topic)))
            chosen_doc = np.random.choice(topic_docs)

        print(topic_labels[topic])
        print(blog_info.iloc[chosen_doc])  
        
        adf = adf.append(blog_info.iloc[chosen_doc],ignore_index=True)
        
        processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
        filename = processed_data_folder + 'article_info'
    
        with open(filename, 'wb') as fp:
            pickle.dump(adf, fp)
            

#%% Save documents 



'''
#Visualize matrix 
toimage(doc_topic_mat).show()
from matplotlib import pyplot as plt
ax = plt.imshow(doc_topic_mat, interpolation='nearest')
ax.set_aspect('box')
plt.show()
'''
