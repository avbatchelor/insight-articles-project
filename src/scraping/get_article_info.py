# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 15:39:43 2018

@author: Alex

Get article info 
"""

#%% Import libraries
from bs4 import BeautifulSoup
import pandas as pd
import os
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\scraping')
import pickle
from read_and_parse import read_local_html

#%%
def get_article_info(soup):
    
    # source 
    source = 'kdnuggets.com'
    
    # title 
    title = soup.title.text
    
    # author 
    paras = soup.find_all('p')
    if "By " in paras[1].text:
        author = paras[1].text
    else:
        author_result = soup.find_all('div', class_ = 'author-link')
        try:
            author = author_result[0].text
        except:
            result = soup.find_all('b')
            if "By" in result[2].text:
                author = result[2].text
            else:
                author= 'Author not found'
        
    
    # link
    link_result = soup.find_all('link', rel='canonical')
    link = link_result[0]['href']
    
    return source, title, author, link

#%% Hard coded variables 
blog_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\raw\\kd_blogs\\'

processed_data_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\processed\\'
filename = processed_data_folder + 'kd_docs'

with open (filename, 'rb') as fp:
    documents, included_blogs = pickle.load(fp)

#%% Loop through all the blog posts 
os.chdir(blog_folder)
num_blog_posts = len(os.listdir(blog_folder))
documents = []
num_skipped = 0
info_list = []

edited_column_names = ['source','title', 'author', 'link']
df = pd.DataFrame(columns = edited_column_names)
    
for blog_num in included_blogs:
    soup = read_local_html(blog_folder,blog_num)
    source, title, author, link = get_article_info(soup)
    info_list.append([source, title, author, link])

#df.append([source, title, author, link])


