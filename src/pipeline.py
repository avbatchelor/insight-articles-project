# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 22:05:23 2018

@author: Alex

Pipeline 
"""

#%% Import packages
import os 
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\scraping\\') 


#%% 
'''
Input = local HTML
Output = Save article strings and document sentences 
'''
import read_and_parse

#%% 

import get_article_info

#%% 
'''
Topic modeling

'''
#topic_modeling()

#%% Generate graph 
os.chdir('C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\src\\topic modeling\\') 
import generate_graph


#%% Linear topic sequence 
import linear_topic_sequence