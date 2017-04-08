'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk 

'''
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

#socketConnected = False


#host='search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com'
esurl='http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/twittertrend'
#host='http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com'
#client = Elasticsearch([host])
#print (client.info())
#es = Elasticsearch(['http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/twittertrend'])
# es = Elasticsearch(
#     hosts=[{'host': host, 'port': 443}],
#     use_ssl=True,
#     verify_certs=True,
#     connection_class=RequestsHttpConnection
# ) 
#print(es.info())



# @application.route('/', methods=['POST'])
# def map():    
# creating a map in the view
    # try:
    #     dp_res = request.form['dropdown']
    #     dp_res2=request.form['dropdown2']
    # except:
    #     return render_template('home1.html', marker_list = [], count='')
    

    # selected = dp_res
    # maxsize=int(dp_res2)
    # print type(selected), dp_res2, maxsize
        
    # res = es.search(index="twittertrend", doc_type="tweets", q=selected, size=maxsize)
    # locationst=[]

    # print("%d documents found" % res['hits']['total'])


    # print len(res['hits']['hits'])
    # for doc in res['hits']['hits']:
    #     #print doc
    #     #print("%s) %s" % (doc['_id'], doc['_source']['text']))
    #     #print doc['_source']['coordinates']
    #     text=doc['_source']['text']
    #     if doc['_source']['coordinates']:
    #         x= doc['_source']['coordinates']['coordinates']
    #         locationst.append([x, text])

    #     # select a random coordinates    
    #     else:
            
    #         radius = 2113000.0                       #Choose your own radius
    #         radiusInDegrees=float(radius/111300)            
    #         r = radiusInDegrees
            
    #         #   UScenter = {lat: 40.461881, lng: -99.757229};
    #         x0 = 40.84
    #         y0 = -99.757229
         
    #         u = float(random.uniform(0.0,1.0))
    #         v = float(random.uniform(0.0,1.0))
          
    #         w = r * math.sqrt(u)
    #         t = 2 * math.pi * v
        
    #         x = w * math.cos(t) 
    #         y = w * math.sin(t)

    #         xLat  = x + x0
    #         yLong = y + y0
    #         point = (xLat, yLong)
    #         locationst.append([point, text])

    # # number of tweets   
    # number = len(locationst)  
    # #print locationst[1][0]
    # #print locationst[1][1]
    # return render_template('home1.html', marker_list= locationst, count=number, selected=selected)


@application.route('/', methods=['GET','POST'])
def home():
    global socketConnected

    if request.method == 'POST':
        
        js = json.loads(request.data)

        
        hdr=request.headers.get('x-amz-sns-message-type')
        
        if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
            r = requests.get(js['SubscribeURL'])
            
        if hdr == 'Notification':
            tweet = js['Message']
            print type(tweet)
            #client.index(index="twittertrend", doc_type="tweets", id=js['MessageId'], body= tweet)
            #es.index(index="twittertrend", doc_type="tweets", id=js['MessageId'], body= tweet)
            r = requests.post(esurl, tweets=json.dumps(tweet, ensure_ascii=True))
            print r
        # if socketConnected:
        #         socketio.emit('realTimeResponse', tweet)


    return render_template('home1.html', marker_list = [], count='')

@socketio.on('realTime')
def handle_my_custom_event(message):
    global socketConnected
    socketConnected = True
    print('received message:' + message)


if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0')
    
