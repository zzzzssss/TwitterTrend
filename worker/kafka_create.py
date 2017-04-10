## Example create kafka topic
##from kafka.producer import SimpleProducer
from kafka import KafkaProducer
from time import sleep
from datetime import datetime

##kafka = KafkaClient("localhost:9092")
##producer = SimpleProducer(kafka)
producer = KafkaProducer(bootstrap_servers='localhost:9092')

while 1:
	# "kafkaesque" is the name of our topic
	
	producer.send("kafkaesque", str.encode("Metamorphosis! " + str(datetime.now().time()) ))
	sleep(1)