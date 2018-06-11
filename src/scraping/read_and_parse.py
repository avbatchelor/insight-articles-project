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

#%% Loop through all the blog posts 
os.chdir(blog_folder)
num_blog_posts = len(os.listdir(blog_folder))

for blog_num = range(1:num_blog_posts+1):
    soup = read_local_html(blog_folder,blog_num)
    article_str = get_article_str(soup)
    cleaned_article = clean_article(article_str)
    
    edited_column_names = ['title', 'tags', 'description', 'paragraphs']
    
    'author', 'month_published', 'year_published', , 'related articles', 'awards']
    df = pd.DataFrame(columns = edited_column_names)
    
    

# Change directory to the blog folder 
    
# Find all the filenames 

# Loop through the filenames 
    
# Parse the information 
    
# Write it to a pandas dataframe 