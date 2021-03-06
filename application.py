from flask import Flask, render_template, request
from flask_googlemaps import Map
from flask_socketio import SocketIO, send, emit
from elasticsearch import Elasticsearch, RequestsHttpConnection,Urllib3HttpConnection,Connection
import random
import math
import requests
import json
#from requests_aws4auth import AWS4Auth
application = Flask(__name__)
#application.debug=True
socketio = SocketIO(application)
socketConnected = False
queryKeyWord = ''
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'  

esurl='http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/test-index2/tweet'
host='search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com'

# es = Elasticsearch(
#     hosts=[{'host': host, 'port': 423}],
#     http_auth=awsauth,
#     use_ssl=True,
#     verify_certs=True,
#     connection_class=RequestsHttpConnection
# ) 
# print(es.info())



# @application.route('/home', methods=['POST'])
# def map():    
# #creating a map in the view
#     try:
#         dp_res = request.form['dropdown']
#         dp_res2=request.form['dropdown2']
#     except:
#         return render_template('home1.html', marker_list = [], count='')
    

#     selected = dp_res
#     maxsize=int(dp_res2)
#     #print type(selected), dp_res2, maxsize

#     # queryURL = 'http://localhost:9201/tweetmap/_search?q=*:*&size=1000'
#     queryURL = 'http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/test-index2/tweet/_search?q='
#     queryURL=queryURL+selected+'&size='+str(maxsize)
#     print queryURL
#     response = requests.get(queryURL)
#     res = json.loads(response.text)
#     #print res['hits']['hits']
        
#     #res = es.search(index="twittertrend", doc_type="tweets", q=selected, size=maxsize)
#     locationst=[]

#     print("%d documents found" % res['hits']['total'])


#     print len(res['hits']['hits'])
#     for doc in res['hits']['hits']:
#         #print doc
#         #print("%s) %s" % (doc['_id'], doc['_source']['text']))
#         #print doc['_source']['coordinates']
#         text=doc['_source']['text']
#         if doc['_source']['location']:
#             x= doc['_source']['location']
#             locationst.append([x, text])

#         # select a random coordinates    
#         else:
            
#             radius = 2113000.0                       #Choose your own radius
#             radiusInDegrees=float(radius/111300)            
#             r = radiusInDegrees
            
#             #   UScenter = {lat: 40.461881, lng: -99.757229};
#             x0 = 40.84
#             y0 = -99.757229
         
#             u = float(random.uniform(0.0,1.0))
#             v = float(random.uniform(0.0,1.0))
          
#             w = r * math.sqrt(u)
#             t = 2 * math.pi * v
        
#             x = w * math.cos(t) 
#             y = w * math.sin(t)

#             xLat  = x + x0
#             yLong = y + y0
#             point = (xLat, yLong)
#             locationst.append([point, text])

#     # number of tweets   
#     number = len(locationst)  
#     #print locationst[1][0]
#     #print locationst[1][1]
#     return render_template('home1.html', marker_list= locationst, count=number, selected=selected)
    


# @application.route('/', methods=['GET','POST'])
# def sns():
#     global socketConnected

#     if request.method == 'POST':
        
#         js = json.loads(request.data)

#         hdr=request.headers.get('x-amz-sns-message-type')
        
#         if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
#             r = requests.get(js['SubscribeURL'])
            
#         if hdr == 'Notification':
#             tweet_js = js['Message']
#             print type(tweet_js)
#             r = requests.post(esurl, data=tweet_js)
#             #print r.text
#         if socketConnected:
#                 socketio.emit('realTimeResponse', tweet_js)


#     return render_template('TwitterMap.html')

@application.route('/',methods=['GET','POST'])
def home():
    global socketConnected
    global queryKeyWord

    if request.method == 'POST':
        
        js = json.loads(request.data)

        hdr=request.headers.get('x-amz-sns-message-type')
        
        if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
            r = requests.get(js['SubscribeURL'])
            
        if hdr == 'Notification':
            tweet_js = js['Message']

            a=json.loads(js['Message'])
            print a['text']
            
            r = requests.post(esurl, data=tweet_js)
        #####uncomment if want to filter with new coming twitter with keyword
        # if socketConnected and queryKeyWord in a['text']: 
        #         print "filter queryKeyWord backend"
        #         print queryKeyWord
        #         socketio.emit('realTimeResponse', tweet_js)

        #####filter without new coming twitter with keyword
        if socketConnected: 
                print "filter without queryKeyWord backend"
                print queryKeyWord
                socketio.emit('realTimeResponse', tweet_js)

    return render_template('home1.html')


@socketio.on('message')
def handle_message(message):
    global socketConnected
    global queryKeyWord
    if message == 'Init':
        queryURL = 'http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/test-index2/tweet/_search?q=*:*&size=0'
        response = requests.get(queryURL)
        results = json.loads(response.text)

        print("INIT MAP")
    else:
        queryKeyWord = message.replace(' ', '%20')
        socketConnected = True
        queryURL = 'http://search-movie-vpmtwgvr57yoata6seazfnpyfe.us-west-2.es.amazonaws.com/test-index2/tweet/_search?q='
        #show 10 twitter location on map when searching
        queryURL=queryURL+queryKeyWord+'&size=10'
        response = requests.get(queryURL)
        results = json.loads(response.text)
        print("SEARCH " + str(message))

    # locations of each tweet
    tweets = []
    for result in results['hits']['hits']:
        tweet = {'sentiment': result['_source']['sentiment'], 'location': result['_source']['location']}
        tweets.append(tweet)
    print len(tweets) 

    send(json.dumps(tweets))


if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0')
    
