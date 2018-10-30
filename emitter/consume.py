#!/usr/bin/env python3
import sys
from confluent_kafka import Producer, KafkaError, Consumer

consumer_settings = {
            'bootstrap.servers': 'kafka03-prod02.messagehub.services.us-south.bluemix.net:9093',
            'security.protocol': 'SASL_SSL',
            'ssl.ca.location': '/Users/aslom/Documents/awsm/experiments/tut-ex/kafka-python/certs.pem',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': 'token',
            'sasl.password': 'HFrcTJyrKd0GRNkK5NJkATVxktFCnN79Gxa1flhe9GDWJE8s',
            'api.version.request': True,
            'broker.version.fallback': '0.10.2.1',
            'log.connection.close' : False,
            'client.id': 'kafka-python-console-sample-consumer2',
            'group.id': 'kafka-python-console-sample-group2'
}

c = Consumer(**consumer_settings)
c.subscribe(['mytopic'])

running = True

while running:
    msg = c.poll(0.1)
    if msg:
      print(msg.value())
