# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 15:00:26 2018

@author: Alex

# reads and parses local html 

"""

#%% Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import codecs
import os 
from parse_kd import get_article_str
import re

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
def clean_article(article_str):
    article_str = article_str.replace("\(.+\)","")
    # lowercase
    article_str = article_str.lower()

    #Remove any non alphanumeric characters
    article_str = re.sub('[^a-z\s]+','', article_str)
    article_str = re.sub('\s+',' ', article_str)
    
    return article_str

#%% Loop through all the blog posts 
os.chdir(blog_folder)
num_blog_posts = len(os.listdir(blog_folder))
documents = []
num_skipped = 0

for blog_num in range(1,num_blog_posts+1):
    try:
        soup = read_local_html(blog_folder,blog_num)
        article_str = get_article_str(soup)
        cleaned_article = clean_article(article_str)
        documents.append(cleaned_article)
    except:
        print('Blog ' + str(blog_num) + ' skipped')
        num_skipped += 1
    