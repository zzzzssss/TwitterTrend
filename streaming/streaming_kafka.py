# Important the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
# from elasticsearch import Elasticsearch
import requests
import json
from kafka import KafkaProducer

# Variables that contains the user credentials to access Twitter API
access_token = '108946322-GxvJPHiMPG9zTPLMnRQkNLfLvp7G8Qx31EYEnBTM'
access_token_secret = '2deVNWy9p8U5F5L8n3FlwrycJ4QOHj9Q9mJF5XDPCu9Vr'
consumer_key = 'fmqy8dresXcowGR8Hd8PbyMbe'
consumer_secret = 'X00DyyCwXOnUBM1VsJEibTqHjEeSVwrl0aVbBIaVo835TuvXeP'


# This is a basic listener that just prints received tweets to stdout
class StdOutListener(StreamListener):
    def on_error(self, status):
        # print status
        pass

    def on_status(self, status):
        try:
            if status.coordinates:
                # print status
                tweet = {'user': status.user.screen_name, 'text': status.text,
                         'location': status.coordinates['coordinates'], 'time': str(status.created_at)}

                # Write record to kafka
                producer.send('tweet', value = tweet)

                print tweet
        except Exception as e:
            print 'Error! {0}: {1}'.format(type(e), str(e))


if __name__ == '__main__':
    

    # Create Kafka Producer client
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['Restaurant','Basketball','Weather','Friday','Cloud','Movie','Panda','God','Trump','Hilarious'])
