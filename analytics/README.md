# How to build and run BAI analytics action


## Building and testing action code locally

Mae sure python3 is installed: https://realpython.com/installing-python/

```
python3 -m pip install -r requirements.txt --user
```


## Process event into summary JSON

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
ibmcloud fn action create task_summary task_summary.py --param ES_URL https://admin:IDGYVALTPVDZZVCZ@portal-ssl113-38.bmix-dal-yp-cc659f75-4d33-404d-8934-644c6858f0ca.250607799.composedb.com:58570/ --docker aslom/python3action-bai
```

expected output

```
ok: created action task_summary
```

## Create rule to connect trigger to action

```
ibmcloud fn rule create taskSummaryRule baiEventStreamTestTrigger task_summary
```

expected output

```
ok: created rule taskSummaryRule
```


## Check output

```
ibmcloud fn activation poll
```