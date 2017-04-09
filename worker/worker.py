import json
import boto3
from multiprocessing import Pool
from watson_developer_cloud import AlchemyLanguageV1
import random


alchemy_language = AlchemyLanguageV1(api_key='3946e2353ef5132f59f5fc47536fb8ac67882707')


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='TwitterTrend')


client = boto3.client('sns')
response = client.create_topic(Name = 'tweets')
topicArn = response['TopicArn']
#subscribeResponse = client.subscribe(TopicArn = topicArn, Protocol = 'http', Endpoint = 'http://54.202.67.200:5000/')
#subscribeResponse = client.subscribe(TopicArn = topicArn, Protocol = 'http', Endpoint = 'http://52.26.22.105:5000/')

#sns = boto3.resource('sns')
#IMPORTANT: sns and aws region needs to be the same: here both are us-west-2 Oregon
#topic = sns.Topic('arn:aws:sns:us-west-2:217770466492:TwitterSentiment') 


def worker():
    while True:
        for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20): #message.body type: unicode
            try:
                tweet = json.loads(message.body)   #tweet type:dict
                #print tweet
                #response = alchemy_language.sentiment(text=tweet['text'])   #tweet['text']: unicode
                #if response['status'] == 'OK':
                emotional=['positive','negative','neutral']
                tweet['sentiment'] = random.choice(emotional)
                print tweet['sentiment'] 
                    #encoded = json.dumps(tweet, ensure_ascii=False)
                    # Publish to Amazon SNS
                client.publish(TopicArn = topicArn, Message=json.dumps(tweet, ensure_ascii=True))
            #except:
                #pass

            finally:
                message.delete()

if __name__ == '__main__':
    worker()
     #pool = Pool(3)
     #pool.map(worker, range(3))




