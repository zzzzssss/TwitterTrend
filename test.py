from flask import Flask, render_template, request
from flask_googlemaps import Map
from flask_socketio import SocketIO, send, emit
from elasticsearch import Elasticsearch, RequestsHttpConnection,Urllib3HttpConnection,Connection
import random
import math
import requests
import json

#from awses.connection import AWSConnection
#from aws_requests_auth.aws_auth import AWSRequestsAuth
# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
socketio = SocketIO(application)
#es=Elasticsearch()
host='search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com'
doc={
	"text": "#God has given you an ability unique to you alone. Walk in that\u2026 https://t.co/uQo9omf35k", 
	"location": [-72.96151239, 41.29106458],
	 "user": "DvineExpression", 
	 "sentiment": "positive",
	  "time": "2017-04-08T19:03:01Z"
	  }

# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     #'timestamp': datetime.now(),
# }

es2 = Elasticsearch(
    hosts=[{'host': host, 'port': 443}],
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
) 
res = es2.index(index="test-index2", doc_type='tweet', body=doc)