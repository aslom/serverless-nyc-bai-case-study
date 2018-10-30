#!/usr/local/bin/python3

import os
import sys
import json
import datetime
import dateutil.parser
from datetime import date
from dateutil.relativedelta import relativedelta

import time
from confluent_kafka import Producer, KafkaError, Consumer

def loadEventFromFile(filename, offsetSeconds=None):
    with open(filename, 'r') as eventFile:
        event = json.load(eventFile)
        if offsetSeconds is not None:
            now = datetime.datetime.now(datetime.timezone.utc)
            #timestamp = dateutil.parser.parse(event['timestamp'])
            timestamp = now + relativedelta(seconds=offsetSeconds)
            print("timestamp=", timestamp, "offset=",
                  offsetSeconds, "now=", now)
            event['timestamp'] = timestamp.isoformat()
        return event


def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' %
                         (msg.topic(), msg.partition(), msg.offset()))


def send_event(event):
    global p
    jsonStr = json.dumps(event)
    b = jsonStr.encode('utf-8')
    try:
        p.produce('mytopic',  b, key, -1, delivery_callback)
    except BufferError as e:
        sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                         len(p))
    # Serve delivery callback queue.
    # NOTE: Since produce() is an asynchronous API this poll() call
    #       will most likely not serve the delivery callback for the
    #       last produce()d message.
    p.poll(0)
    # Wait until all messages have been delivered
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()

producer_settings = {
    'bootstrap.servers': 'kafka03-prod02.messagehub.services.us-south.bluemix.net:9093',
    'security.protocol': 'SASL_SSL',
    'ssl.ca.location': '/Users/aslom/Documents/awsm/experiments/tut-ex/kafka-python/certs.pem',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'token',
    'sasl.password': 'HFrcTJyrKd0GRNkK5NJkATVxktFCnN79Gxa1flhe9GDWJE8s',
    'api.version.request': True,
    'broker.version.fallback': '0.10.2.1',
    'log.connection.close': False,
    'client.id': 'kafka-python-console-sample-producer2'
}

# parameters
# type of task
# name of task

p = Producer(**producer_settings)

# for line in sys.stdin:


# https://github.com/confluentinc/confluent-kafka-python/blob/master/examples/producer.py

print("starting")

running = True

counter = 0
while running:
    key = 'key'
    print("counter="+str(counter))
    for i in range(1, 3):
      event = loadEventFromFile('../samples/task'+str(i)+'.json')
      # recompute timestamp
      today = datetime.datetime.now(datetime.timezone.utc)
      event['timestamp'] = today.isoformat()
      event['id'] = '{C0B24665-0200-C4B8-8768-591884F5BA-'+str(i)+'-'+str(counter)+'}'
      event['source']['instance']['id'] =  '{C0B24665-0100-C335-A06E-0432C264E7-'+str(counter)+'}'
      print('event=', event)
      send_event(event)
      print("sent event "+str(i)+" and sleeping")
      time.sleep(5)
    counter = (counter + 1) % 10   # wrap over event IDs
print("finished")
