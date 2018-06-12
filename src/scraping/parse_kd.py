# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 14:01:08 2018

@author: Alex

Testing whether parsing kd nuggets is possible

"""

#%% Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

#%%
def get_article_str(soup):
    
    #%% Titles 
    title = soup.title.text
    
    #%% Tag data
    tag = soup.find_all('div', class_ = 'tag-data')
    tags = tag[0].text
    tags = tags.replace('Tags: ','')
            
    #%% Paragraphs
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
        
    #%% Create an article string 
    article_str = title + ' ' + tags + ' ' + description + ' ' + main_text
    
    return article_str

#%%


#%% 
    
'''    
    
    # Author is second paragraph 
    #author = tags[1].text
    #author = author.replace("By ", "")
    
    # 
    
    
# Remove related paragraph and paragraphs following that 
    
#%% Links
tags = soup.find_all('a')
for i in range(0,len(tags)):
    a = tags[i].text
    
    

    
    print(a)
    

    


#%% Related articles 
def related_articles(soup):
    tag = soup.find_all('ul', class_ = 'three_ul')
    tags = tag[0].text
    
    return article_titles
    
    '''