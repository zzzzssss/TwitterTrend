from flask import Flask, render_template, request
from flask_googlemaps import Map
from flask_socketio import SocketIO, send, emit
from elasticsearch import Elasticsearch, RequestsHttpConnection,Urllib3HttpConnection,Connection
import random
import math
import requests
import json

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
socketio = SocketIO(application)
socketConnected = False

esurl='http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/test-index2/tweet'
# es = Elasticsearch(
#     hosts=[{'host': host, 'port': 423}],
#     use_ssl=True,
#     verify_certs=True,
#     connection_class=RequestsHttpConnection
# ) 
# print(es.info())
@application.route('/home', methods=['GET','POST'])
def home():

return render_template('home1.html', marker_list = [], count='')



@application.route('/home', methods=['POST'])
def map():    
creating a map in the view
    try:
        dp_res = request.form['dropdown']
        dp_res2=request.form['dropdown2']
    except:
        return render_template('home1.html', marker_list = [], count='')
    

    selected = dp_res
    maxsize=int(dp_res2)
    print type(selected), dp_res2, maxsize
        
    res = es.search(index="twittertrend", doc_type="tweets", q=selected, size=maxsize)
    locationst=[]

    print("%d documents found" % res['hits']['total'])


    print len(res['hits']['hits'])
    for doc in res['hits']['hits']:
        #print doc
        #print("%s) %s" % (doc['_id'], doc['_source']['text']))
        #print doc['_source']['coordinates']
        text=doc['_source']['text']
        if doc['_source']['coordinates']:
            x= doc['_source']['coordinates']['coordinates']
            locationst.append([x, text])

        # select a random coordinates    
        else:
            
            radius = 2113000.0                       #Choose your own radius
            radiusInDegrees=float(radius/111300)            
            r = radiusInDegrees
            
            #   UScenter = {lat: 40.461881, lng: -99.757229};
            x0 = 40.84
            y0 = -99.757229
         
            u = float(random.uniform(0.0,1.0))
            v = float(random.uniform(0.0,1.0))
          
            w = r * math.sqrt(u)
            t = 2 * math.pi * v
        
            x = w * math.cos(t) 
            y = w * math.sin(t)

            xLat  = x + x0
            yLong = y + y0
            point = (xLat, yLong)
            locationst.append([point, text])

    # number of tweets   
    number = len(locationst)  
    #print locationst[1][0]
    #print locationst[1][1]
    return render_template('home1.html', marker_list= locationst, count=number, selected=selected)


@application.route('/', methods=['GET','POST'])
def sns():
    global socketConnected

    if request.method == 'POST':
        
        js = json.loads(request.data)

        hdr=request.headers.get('x-amz-sns-message-type')
        
        if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
            r = requests.get(js['SubscribeURL'])
            
        if hdr == 'Notification':
            tweet_js = js['Message']
            print tweet_js
            r = requests.post(esurl, data=tweet_js)
            #print r.text
        if socketConnected:
                socketio.emit('realTimeResponse', tweet_js)


    #return render_template('home1.html', marker_list = [], count='')


@socketio.on('realTime')
def handle_my_custom_event(message):
    global socketConnected
    socketConnected = True
    print('received message:' + message)


if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0')
    
