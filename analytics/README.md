# BAI Analytics: Process events into summary JSON
*You can imagine that you could do something a little more interesting than hello world.  For this section of the lab, you'll be creating a trigger that will fire whenever a new item is placed on a Kafka topic.  That trigger will be connected to an action (via a rule).  The action will run some code to process the incoming kafka message.*


## BAI Create the event source
- Your first step will be to create a kafka event source. For simplicity in this lab, we are using a kafka instance already created by the instructors. Run the following command in your terminal window:

  ```
  ibmcloud fn package bind /whisk.system/messaging baiEventStream -p kafka_brokers_sasl "[\"kafka03-prod02.messagehub.services.us-south.bluemix.net:9093\"]" -p user HFrcTJyrKd0GRNkK -p password 5NJkATVxktFCnN79Gxa1flhe9GDWJE8s -p kafka_admin_url https://kafka-admin-prod02.messagehub.services.us-south.bluemix.net:443
  ```

  expected output:

  ```
  ok: created binding baiEventStream
  ```


## Create the trigger for a kafka topic

- Create a trigger to listen for messages coming in on the kafka topic

  ```
  ibmcloud fn trigger create baiEventStreamTestTrigger -f baiEventStream/messageHubFeed -p topic mytopic -p isJSONData true
  ```

  expected output:

  ```
  ok: created trigger baiEventStreamTestTrigger
  ```

## Create the Kafka action to process events

- You will be creating a new action from the code provided in `https://github.com/aslom/serverless-nyc-bai-case-study/blob/master/analytics/task_summary.py` Clone the repo, and cd into the folder containing this file:
  
  `git clone git@github.com:aslom/serverless-nyc-bai-case-study.git && cd serverless-nyc-bai-case-study/analytics`
  
    - if you are unable to clone, you could create a file named task_summary.py & paste in the contents from the [file on github](https://raw.githubusercontent.com/aslom/serverless-nyc-bai-case-study/master/analytics/task_summary.py).

- VERY IMPORTANT: to avoid overriding each other's state in Elasticsearch set your own unique analytics ID:
  ```
  YOUR_ID=mynamehere
  ```
- Create the serverless action using the code at task_summary.py. You could look at the code, but at a high level, this action calculates the duration of a particular case management task. You will notice that the action being created is a docker action - this is so that we can include our required libraries.
  ```
  ibmcloud fn action create task_summary task_summary.py --param analytics-id $YOUR_ID --param ES_URL https://admin:QZSFKVNUNTMWPHMY@portal-ssl65-41.bmix-dal-yp-c401ad96-667e-4128-af0e-cb3d54fd1cf9.250607799.composedb.com:62863/ --docker aslom/python3action-bai
  ```

  expected output

  ```
  ok: created action task_summary
  ```

- You will not edit the python code during this lab, but if you wanted to make edits in the future, you would use the `update` command instead of `create`.

  ```
  ibmcloud fn action update task_summary task_summary.py --param analytics-id $YOUR_ID --param ES_URL https://admin:QZSFKVNUNTMWPHMY@portal-ssl65-41.bmix-dal-yp-c401ad96-667e-4128-af0e-cb3d54fd1cf9.250607799.composedb.com:62863/ --docker aslom/python3action-bai
  ```


## Create a rule to connect the trigger to the action

- The trigger you created needs to be connected to the action you created via a rule, so that the action will be run whenever a new item is on the kafka topic:

  ```
  ibmcloud fn rule create taskSummaryRule baiEventStreamTestTrigger task_summary
  ```

  expected output

  ```
  ok: created rule taskSummaryRule
  ```


## Check output

- The instructors will be sending messages to the kafka topic periodically. Your trigger should be fired and your action invoked when events are received.

  ```
  ibmcloud fn activation poll
  ```

# Optional (if time allows)

## Building and testing action code locally

Make sure python3 is installed: https://realpython.com/installing-python/

```
python3 -m pip install -r requirements.txt --user
```

Then you can run simulated serverless invocation:

```
./simulate_invoke.py
```



## Building Docker base image with libraries

Ensure docker is installed. If you want to build the docker base image with libraries, you can use the following commands:
```
docker build -t docker.io/aslom/python3action-bai:latest .
docker push docker.io/aslom/python3action-bai
```
