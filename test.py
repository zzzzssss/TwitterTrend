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
host2='search-tweet-kzsnkupnrbvy6gdiw6vi4qwkaq.us-west-2.es.amazonaws.com'

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    #'timestamp': datetime.now(),
}

es2 = Elasticsearch(
    hosts=[{'host': host2, 'port': 443}],
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
) 
res = es2.index(index="test-index4", doc_type='tweet', id=1, body=doc)