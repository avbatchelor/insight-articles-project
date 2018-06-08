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

#%% 
#url = "https://www.kdnuggets.com/2018/02/logistic-regression-concise-technical-overview.html"
url = "https://www.kdnuggets.com/tutorials/index.html"
result = requests.get(url)

# Check that it was received 
if result.status_code != 200:
    print('Page ' + str(id) + ' not downloaded.')
    
soup = BeautifulSoup(result.text, 'html.parser')
print(soup)

#%% Titles 
title = soup.title.text

#%% Paragraphs
tags = soup.find_all('p')
for i in range(0,len(tags)):
    a = tags[i].text
    print(a)
    
# Remove related paragraph and paragraphs following that 
    
#%% Links
tags = soup.find_all('a')
for i in range(0,len(tags)):
    a = tags[i].text
    print(a)
    
#%% Tag data
tag = soup.find_all('div', class_ = 'tag-data')
tags = tag[0].text

# Remove 'Tags:' part
# Tokenize  

#%% Related articles 
tag = soup.find_all('ul', class_ = 'three_ul')
tags = tag[0].text
