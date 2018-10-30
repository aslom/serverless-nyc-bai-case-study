# How to build and run BAI analytics action


## Building and testing action code locally

Make sure python3 is installed: https://realpython.com/installing-python/

```
python3 -m pip install -r requirements.txt --user
```

Then you can run simulated serverless invocaiton:

```
./simulate_invoke.py
```


## Process events into summary JSON

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

## Create Kafka action to process events

```
YOUR_ID=flux5
ibmcloud fn action create task_summary task_summary.py --param analytics-id $YOUR_ID --param ES_URL https://admin:QZSFKVNUNTMWPHMY@portal-ssl65-41.bmix-dal-yp-c401ad96-667e-4128-af0e-cb3d54fd1cf9.250607799.composedb.com:62863/ --docker aslom/python3action-bai
```

expected output

```
ok: created action task_summary
```

After editing of python code use update:

```
ibmcloud fn action update task_summary task_summary.py --param analytics-id $YOUR_ID --param ES_URL https://admin:QZSFKVNUNTMWPHMY@portal-ssl65-41.bmix-dal-yp-c401ad96-667e-4128-af0e-cb3d54fd1cf9.250607799.composedb.com:62863/ --docker aslom/python3action-bai
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

Your trigger should triggered and your action invoked when events are received.

```
ibmcloud fn activation poll
```


# Building Docker base image with libraries

```
docker build -t docker.io/aslom/python3action-bai:latest .
docker push docker.io/aslom/python3action-bai
```