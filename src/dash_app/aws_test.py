# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.plotly as py
import plotly.graph_objs as go
import networkx as nx
import pickle
import boto3
import io

############################
# Load data

BUCKET_NAME = 'blog-seq-data' # replace with your bucket name

# list of topics
KEY = 'graph_and_labels' # replace with your object key
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
obj_str = obj['Body'].read()     
graph_mat,topic_labels,dist_mat,doc_topic_mat = pickle.loads(obj_str)

topic_list = list(topic_labels.values())

# article info
KEY = 'article_info' # replace with your object key
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
obj_str = obj['Body'].read()     
adf = pickle.loads(obj_str)

# topic sequence 
KEY = 'topic_seq' # replace with your object key
s3 = boto3.client('s3')
obj = s3.get_object(Bucket=BUCKET_NAME, Key=KEY)
obj_str = obj['Body'].read()     
topic_sequence = pickle.loads(obj_str)