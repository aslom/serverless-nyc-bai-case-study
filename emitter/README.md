# How to emit events



## Send test events

Send an event to Kafka topic (see above) and check that kafkaAction was activated



```bash
EVENT1=$( base64 task1.json )
EVENT2=$( base64 task2.json )

ibmcloud fn action invoke -v -d /whisk.system/messaging/messageHubProduce -p kafka_brokers_sasl "[\"kafka03-prod02.messagehub.services.us-south.bluemix.net:9093\"]" -p topic mytopic -p user HFrcTJyrKd0GRNkK -p password 5NJkATVxktFCnN79Gxa1flhe9GDWJE8s -p value "$EVENT1" --param base64DecodeValue true

ibmcloud fn action invoke -v -d /whisk.system/messaging/messageHubProduce -p kafka_brokers_sasl "[\"kafka03-prod02.messagehub.services.us-south.bluemix.net:9093\"]" -p topic mytopic -p user HFrcTJyrKd0GRNkK -p password 5NJkATVxktFCnN79Gxa1flhe9GDWJE8s -p value "$EVENT2" --param base64DecodeValue true
```


```
#EVENT=`emitter/generate.py`
EVENT=`cat emitter/task1.json`
ibmcloud fn action invoke /whisk.system/messaging/messageHubProduce -p kafka_brokers_sasl "[\"kafka03-prod02.messagehub.services.us-south.bluemix.net:9093\"]" -p topic mytopic -p user HFrcTJyrKd0GRNkK -p password 5NJkATVxktFCnN79Gxa1flhe9GDWJE8s -p value $EVENT
```
