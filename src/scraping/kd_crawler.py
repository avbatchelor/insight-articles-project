# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 17:48:20 2018

@author: Alex

Scrapes kd nuggets
"""

#%% Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

#%% Start at the index page 
#url = "https://www.kdnuggets.com/2018/02/logistic-regression-concise-technical-overview.html"
# url = "https://www.kdnuggets.com/tutorials/index.html"

def getHTML(url):
    # request url 
    result = requests.get(url)
    
    # Check that it was received 
    if result.status_code != 200:
        print('Page ' + str(id) + ' not downloaded.')
        
    soup = BeautifulSoup(result.text, 'html.parser')
    
    return soup

#%% Scrape and write 
def scrape_and_write(blog_folder,blog_num,link):
    # request url 
    result = requests.get(link)
    
    # make filename
    filename = blog_folder + 'kd_blog' + str(blog_num).zfill(4) + '.html'
    
    # write result 
    with open(filename, "wb") as f:
        f.write(result.content)


#%% Loop through years and months 
first_year = 2015
last_year = 2018 
blog_folder = 'C:\\Users\\Alex\\Documents\\GitHub\\insight-articles-project\\data\\raw\\kd_blogs\\'
blog_num = 0

for year in range(first_year,last_year+1):
    year_str = str(year)
    
    # Create month range 
    if year == 2015:
        month_range = range(5,12+1)
    elif year == 2018:
        month_range = range(1,6+1)
    else:
        month_range = range(1,12+1)
        
    # Loop through years and months
    for month in month_range:
        month_str = str(month).zfill(2)
        # Make link
        prefix = 'https://www.kdnuggets.com/'
        month_index_link = prefix + year_str + '/' + month_str + '/' + 'tutorials.html'
        
        # Print index url 
        print(month_index_link)
        
        # get html 
        soup = getHTML(month_index_link)
    
        # Find all the links within monthly index pages  
        for paragraph in soup.find_all("ul", class_="three_ul"):
            for a in paragraph("a"):
                link = a.get('href')
                if 'kdnuggets.com/tag/' not in link:
                    print(link)
                    
                    # Scrape the html for that link 
                    blog_soup = getHTML(link)
                
                    # Scrape and save the html for that link 
                    blog_num += 1
                    scrape_and_write(blog_folder,blog_num,link)
                    time.sleep(0.5)
        
 