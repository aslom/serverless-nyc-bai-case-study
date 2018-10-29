# How to emit events


## BAI Create event source

```
ibmcloud fn package bind /whisk.system/messaging baiEventStream -p kafka_brokers_sasl "[\"kafka03-prod02.messagehub.services.us-south.bluemix.net:9093\"]" -p user HFrcTJyrKd0GRNkK -p password 5NJkATVxktFCnN79Gxa1flhe9GDWJE8s -p kafka_admin_url https://kafka-admin-prod02.messagehub.services.us-south.bluemix.net:443
```

expected output:

```
ok: created binding baiEventStream
```


## Create trigger for kafka topic


```
ibmcloud fn trigger create baiEventStreamTestTrigger -f baiEventStream/messageHubFeed -p topic mytopic -p isJSONData true
```

expected output:

```
ok: created trigger baiEventStreamTestTrigger
```

## Create Kafka actin to print message

```
ibmcloud fn action create kafkaAction analytics/kafkaAction.js
```

expected output

```
ok: created action kafkaAction
```

## Create rule to connect trigger to action

```
ibmcloud fn rule create kafkaActionRule baiEventStreamTestTrigger kafkaAction
```

expected output

```
ok: created rule kafkaActionRule
```

## Test trigger

Send an event to Kafka topic (see above) and check that kafkaAction was activated


```
#EVENT=`emitter/generate.py`
EVENT=`cat emitter/task1.json`
ibmcloud fn action invoke /whisk.system/messaging/messageHubProduce -p kafka_brokers_sasl "[\"kafka03-prod02.messagehub.services.us-south.bluemix.net:9093\"]" -p topic mytopic -p user HFrcTJyrKd0GRNkK -p password 5NJkATVxktFCnN79Gxa1flhe9GDWJE8s -p value $EVENT
```
