#  BAI Case Study for Serverless NYC


## Context

This case study is specifically prepared for 
<a href="https://www.serverlessnyc.com/ibm">IBM tutorial</a> in
<a href="https://www.serverlessnyc.com/">Serverless NYC, A serverless reality check - October 30 2018, New York</a>

For introduction see <a href="https://github.com/beemarie/serverless-nyc-lab">instructions for the IBM Cloud Functions & Apache OpenWhisk lab at Serverless Days NYC 2018</a>


What is BAI?

IBM® Business Automation Insights (BAI) is a platform-level component that provides visualization insights to business owners and that feeds a data lake to infuse artificial intelligence into IBM Digital Business Automation.
[More in docs](https://www.ibm.com/support/knowledgecenter/SSYHZ8_18.0.0/com.ibm.dba.bai/topics/con_bai_overview.html)

## Case study

This case study is designed to show how to use Apache OpenWhisk with IBM Cloud Functions to add custom behavior to BAI.

We simplify several aspects of BAI:
* emitter is not connected to real system but is hardcoded to send task events
* analytics is simplified to maintain task summary as a JSON object in Elasticsearch
* dashboards are custom made for this case study

## Setup - requirements

Makse sure <a href="https://docs.docker.com/install/#supported-platforms">Docker is installed</a> and you have <a href="https://github.com/beemarie/serverless-nyc-lab">IBM Cloud Account and cloud functions CLI installed and working.</a>

Update <a href="kafka.json">JSON with Kafka configuration</a> or use one provided (should be valid during lab).

Update <a href="elastic.json">JSON with Elastic installation</a> or use one provided (should be valid during lab).



## Create event source

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

expected output:

```
ok: invoked /whisk.system/messaging/messageHubProduce with id 95036269326e4a26836269326e7a2667
```


TODO did not work ...

```
    "logs": [
        "2018-10-29T02:52:32.097526275Z stdout: INFO     [02:52:32] <BrokerConnection node_id=7 host=kafka08-prod02.messagehub.services.us-south.bluemix.net:9093 <connecting> [IPv4 ('169.60.0.123', 9093)]>: connecting to kafka08-prod02.messagehub.services.us-south.bluemix.net:9093 [('169.60.0.123', 9093) IPv4]",
        "2018-10-29T02:52:32.116779151Z stdout: INFO     [02:52:32] Using kafka-python 1.4.3",
        "2018-10-29T02:52:32.11679968Z  stdout: INFO     [02:52:32] Validating parameters",
        "2018-10-29T02:52:32.116805046Z stdout: INFO     [02:52:32] Starting attempt 1",
        "2018-10-29T02:52:32.116809771Z stdout: INFO     [02:52:32] Getting producer",
        "2018-10-29T02:52:32.116821274Z stdout: INFO     [02:52:32] Reusing existing producer",
        "2018-10-29T02:52:32.116825845Z stdout: INFO     [02:52:32] Finding topic mytopic",
        "2018-10-29T02:52:32.116829777Z stdout: INFO     [02:52:32] Found topic mytopic with partition(s) {0}",
        "2018-10-29T02:52:32.116833852Z stdout: INFO     [02:52:32] Producing message",
        "2018-10-29T02:52:32.116837756Z stdout: WARNING  [02:52:32] encoding without a string argument",
        "2018-10-29T02:52:32.117036478Z stdout: INFO     [02:52:32] <BrokerConnection node_id=7 host=kafka08-prod02.messagehub.services.us-south.bluemix.net:9093 <authenticating> [IPv4 ('169.60.0.123', 9093)]>: Authenticated as HFrcTJyrKd0GRNkK via PLAIN",
        "2018-10-29T02:52:32.117293828Z stdout: INFO     [02:52:32] <BrokerConnection node_id=7 host=kafka08-prod02.messagehub.services.us-south.bluemix.net:9093 <authenticating> [IPv4 ('169.60.0.123', 9093)]>: Connection complete.",
        "2018-10-29T02:52:32.118021906Z stderr: Traceback (most recent call last):",
        "2018-10-29T02:52:32.11804087Z  stderr: File \"__main__.py\", line 95, in main",
        "2018-10-29T02:52:32.11804627Z  stderr: TypeError: encoding without a string argument"
    ],
  ```

## Process event into summary JSON

TODO

## Configure Kibana and see summary JSON in dashboard

TODO