# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 15:00:26 2018

@author: Alex

# reads and parses local html 

"""

#%% Import libraries
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import codecs
import os 
import re
import pickle
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

#%% Hard coded variables 
blog_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\raw\\kd_blogs\\'

#%% Read in saved html
# read in saved html back in
def read_local_html(blog_folder,blog_num):
    
    # make filename
    filename = blog_folder + 'kd_blog' + str(blog_num).zfill(4) + '.html'
    
    # read in file    
    f = codecs.open(filename, 'r', 'utf-8')
    
    # parse file
    soup = BeautifulSoup(f.read(), 'html.parser')

    return soup

#%% 
def get_article_str(soup):
    
    # Titles 
    title = soup.title.text
    
    # Tag data
    tag = soup.find_all('div', class_ = 'tag-data')
    tags = tag[0].text
    tags = tags.replace('Tags: ','')
            
    # Paragraphs
    paras = soup.find_all('p')
    
    # The first paragraph always contains a description of the article
    description = paras[0].text
    
    # Get main text
    main_text = ""
    # remove second paragraph if it just contains author name
    if "By " not in paras[1].text:
        main_text = paras[1].text
        
    for i in range(2,len(paras)):
        # These if statements remove later paragraphs if they don't contain the main text of the article 
        if i > len(paras)-5 and "Bio" in paras[i].text:
            continue
        elif i > len(paras)-5 and "Original" in paras[i].text:
            continue
        elif i > len(paras)-5 and "Related" in paras[i].text:
            continue
        elif i > len(paras)-5 and "disqus" in paras[i].text:
            continue
        elif i > len(paras)-5 and "Pages" in paras[i].text:
            continue
        else:
            main_text = main_text + ' ' + paras[i].text
        
    # Create an article string 
    article_str = title + '. ' + tags + '. ' + description + ' ' + main_text
    
    return article_str

#%%
def clean_article(article_str):   
    # lowercase
    article_str = article_str.lower()

    #Remove any non alphanumeric characters
    article_str = re.sub('[^a-z\s]+','', article_str)
    article_str = re.sub('\s+',' ', article_str)
    
    return article_str

#%% Split each blog post into sentences 
def get_sentences(article_str):
    # lowercase
    article_str = article_str.lower()

    #Remove any non alphanumeric characters
    article_str = re.sub('[^a-z\s\.]+','', article_str)
    article_str = re.sub('\s+',' ', article_str)
    
    # Split doc into sentences 
    sent_text = nltk.sent_tokenize(article_str)
    
    # Split sentences into words 
    tokenized_sentences = []
    for sentence in sent_text:
        # remove periods 
        sentence = re.sub('\.','', sentence)
        # tokenize
        tokenized_sentences.append(nltk.word_tokenize(sentence))
        
    return tokenized_sentences

#%% 
def lemmatize(tokenized_sentences):
    lemma = WordNetLemmatizer()
    new_docs = []
    for sentence in tokenized_sentences:
        new_sentence = []
        for word in sentence:
            new_sentence.append(lemma.lemmatize(word)
        new_docs.append(new_sentence)
        
    return new_docs

#%% Loop through all the blog posts 
os.chdir(blog_folder)
num_blog_posts = len(os.listdir(blog_folder))
documents = []
num_skipped = 0
blogs_included = []
doc_sents = []

for blog_num in range(1,num_blog_posts+1):
    try:
        soup = read_local_html(blog_folder,blog_num)
        article_str = get_article_str(soup)
        cleaned_article = clean_article(article_str)
        documents.append(cleaned_article)
        blogs_included.append(blog_num)
        # Extract sentences for phrase extraction 
        tokenized_sentences = get_sentences(article_str)
        new_docs = lemmatize(tokenized_sentences)
        doc_sents.append(tokenized_sentences)
    except:
        print('Blog ' + str(blog_num) + ' skipped')
        num_skipped += 1
        
#%% Save documents 
processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'kd_docs'

with open(filename, 'wb') as fp:
    pickle.dump((documents,blogs_included), fp)
    
filename = processed_data_folder + 'doc_sents'

with open(filename, 'wb') as fp:
    pickle.dump(doc_sents, fp)