import json
import boto3
from multiprocessing import Pool
from watson_developer_cloud import AlchemyLanguageV1


alchemy_language = AlchemyLanguageV1(api_key='3946e2353ef5132f59f5fc47536fb8ac67882707')


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='TwitterTrend')


sns = boto3.resource('sns')
#IMPORTANT: sns and aws region needs to be the same: here both are us-west-2 Oregon
topic = sns.Topic('arn:aws:sns:us-west-2:217770466492:TwitterSentiment') 


def worker():
    while True:
        for message in queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20): #message.body type: unicode
            try:
                tweet = json.loads(message.body)   #tweet type:dict
                response = alchemy_language.sentiment(text=tweet['text'])   #tweet['text']: unicode
                if response['status'] == 'OK':
                    tweet['sentiment'] = response['docSentiment']['type']
                    print tweet['sentiment'] 
                    encoded = json.dumps(tweet, ensure_ascii=False)
                    # Publish to Amazon SNS
                    topic.publish(Message=encoded)
                     

            finally:
                message.delete()



if __name__ == '__main__':
    worker()
#     pool = Pool(3)
#     pool.map(worker, range(3))




