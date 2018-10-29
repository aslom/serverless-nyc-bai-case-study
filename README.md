#  BAI Case Study for Tutorial IBM Cloud Functions & Apache OpenWhisk lab at Serverless Days NYC 2018


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

## Feedback

Feel free to reach out with any questions!

## Setup required

Makse sure <a href="https://docs.docker.com/install/#supported-platforms">Docker is installed</a> and you have IBM Cloud Account and cloud functions CLI installed and working.

## Optional setup

Not required but you could use your own Kafka or Elasticsearch.

To use your own Kafka update <a href="kafka.json">JSON with Kafka configuration</a>.

To use your own Elasticsearch update  <a href="elastic.json">JSON with Elastic installation</a> or use one provided (should be valid during lab).

### Sign up for IBM Cloud Account
*IBM Cloud Functions is based on the Apache OpenWhisk project.  We'll be using IBM Cloud Functions for today's lab, but the concepts could apply to any managed Serverless offering.*

1. [Sign up for an IBM Cloud Account](https://ibm.biz/BdYYJG) [https://ibm.biz/BdYYJG]
2. This link may redirect to IBM Coders - you don't need to accept the terms or join IBM Coders.  At that point, you can just go directly to [https://bluemix.net](https://bluemix.net) & sign in to confirm your IBM Cloud account was created.

### Install IBM Cloud CLI & IBM Cloud Functions Plugin
*In this section, you will install the IBM Cloud CLI and the IBM Cloud Functions Plugin to the CLI, as well as do some account set up and configuration. This will enable you to interact with IBM Cloud Functions from a command line interface.*

1. Install the IBM Cloud CLI 
    1. From Shell:
	    * Mac/Linux: In your terminal window, run `curl -sL https://ibm.biz/idt-installer | bash`
	    * Windows 10 Pro, run `Set-ExecutionPolicy Unrestricted; iex(New-Object Net.WebClient).DownloadString('http://ibm.biz/idt-win-installer')`

    2. Alternatively, you can use an installer:
        * Link to installer: [Link to installer](https://console.bluemix.net/docs/cli/reference/ibmcloud/download_cli.html#install_use)

2. Configure your environment
    * Select your API: `ibmcloud api https://api.ng.bluemix.net`
    * Login: `ibmcloud login`
    * You should have an org created already. Target your org with the command `ibmcloud target --cf`
    * You do not have a space; let's create one. In this example, we'll call our space dev, but you can choose anything you want: `ibmcloud cf create-space dev`
    * Ensure your org & space is correctly targeted using `ibmcloud target --cf`
    * Confirm cloud-functions plugin is installed: `ibmcloud fn` should return some help information.
        * If the plugin is not installed, install it: `ibmcloud plugin install cloud-functions`

### Create your first action (Hello World) using the CLI!
*Your first goal is to create a simple hello world action.  This action will return the string 'Hello World' when it is in invoked.*

1. Create a folder for your action to live in: `mkdir myFolder && cd myFolder`
2. Create a file called helloworld.js: `touch helloworld.js`
3. Use your favorite editor to paste the following code into helloworld.js:

	```
	function main(params) {  
		if (params.name) {    
			return { greeting: `Hello ${params.name}` };  
		}  
			return { greeting: 'Hello stranger!' };
		}
	```
4. This code will return "Hello stranger" if no name parameter is given, otherwise it will say hello to the supplied name. Let's create a new action using this file: `ibmcloud fn action create helloWorld helloworld.js`
5. Let's invoke the action hosted on IBM Cloud Functions, using -r to wait for a result: `ibmcloud fn action invoke helloWorld -r`
6. You should see a response like:

	```
	{
	    "greeting": "Hello stranger!"
	}
	```
7. Let's invoke the action with a parameter of your name: `ibmcloud fn action invoke helloWorld -p name Belinda -r`
8. You should see a response like:

	```
	{
	    "greeting": "Hello Belinda"
	}
	```




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

expected output:

```
ok: invoked /whisk.system/messaging/messageHubProduce with id 95036269326e4a26836269326e7a2667
```


## Process event into summary JSON

TODO

## Configure Kibana and see summary JSON in dashboard

TODO
