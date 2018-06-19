# insight-articles-project
My project for the Insight Data Science Program. The goal of the project is to automatically generate a series of blog posts which guide you from what you know to what you want to learn. 

# Project organization 

###src>scraping 

kd_crawler - scrapes kd nuggets 

parse_test - Testing whether parsing kd nuggets is possible

read_and_parse - Reads in and cleans local html

get_article_info - Gets article source, author etc. 


###src>topic_modeling 

extract_phrases  - finds bigrams and trigrams 

generate_graph - draws graph of connections between topics 

linear_topic_sequence - finds sequence of topics for webapp 

topic_modeling - performs LDA 

plotly_network - plots networkx graph in plotly
			
