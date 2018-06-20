# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 11:57:20 2018

@author: Alex

Extract phrases 
"""

#%% Import packages 
from gensim import models
import pickle
from sklearn.feature_extraction import stop_words
 
# rename some functions
Phraser = models.phrases.Phraser
Phrases = models.phrases.Phrases

#%% Load documents 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'doc_sents'

with open (filename, 'rb') as fp:
    doc_sents = pickle.load(fp)

#%% Generate list of sentences 
sentence_stream = sum(doc_sents, [])

#%% Generate bigrams
common_terms = ["of", "with", "without", "and", "or", "the", "a", "as"]
phrases = Phrases(sentence_stream, common_terms=common_terms)
bigram = Phraser(phrases)

#%% Generate trigrams 
trigram = Phrases(bigram[sentence_stream])

#%% Generate output
output_strs = []
for idx in range(0,len(doc_sents)):
    doc = doc_sents[idx]
    output_doc = list(trigram[doc])
    output_str = sum(output_doc,[])
    output_strs.append(' '.join(output_str))

#%% Save output 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'documents_ngrams'

with open(filename, 'wb') as fp:
    pickle.dump(output_strs, fp)
    
