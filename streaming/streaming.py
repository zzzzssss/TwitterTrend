import json
import time
from codecs import open
from dateutil import parser
import tweepy
import boto3

# Variables that contains the user credentials to access Twitter API 
access_token = '108946322-GxvJPHiMPG9zTPLMnRQkNLfLvp7G8Qx31EYEnBTM'
access_token_secret = '2deVNWy9p8U5F5L8n3FlwrycJ4QOHj9Q9mJF5XDPCu9Vr'
consumer_key = 'fmqy8dresXcowGR8Hd8PbyMbe'
consumer_secret = 'X00DyyCwXOnUBM1VsJEibTqHjEeSVwrl0aVbBIaVo835TuvXeP'


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='TwitterTrend')
print(queue.url)

class MyStreamListener(tweepy.StreamListener):  
    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        #streaming data reference: https://dev.twitter.com/overview/api/tweets
        try: 
             # Twitter returns data in JSON format - we need to decode it first
            decoded = json.loads(data)
            if decoded.get('lang') =='en' and decoded.get('coordinates') is not None:
                location=decoded['coordinates']['coordinates']
                timestamp = parser.parse(decoded['created_at']).strftime('%Y-%m-%dT%H:%M:%SZ')
                tweet = {
                'user': decoded['user']['screen_name'],
                'text': decoded['text'],
                'location': location,
                'time': timestamp
                }
                encoded = json.dumps(tweet, ensure_ascii=False)
                queue.send_message(MessageBody=encoded)

        except Exception as e:
            print type(e), str(e)

    def on_error(self, status):
        if status == 420:  # rate limited
            return False
if __name__ == '__main__':
    ls = MyStreamListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = tweepy.Stream(auth, ls)
    stream.filter(track=['Restaurant','Basketball','Weather','Friday','Cloud','Movie','Panda','God','Trump','Hilarious'])


