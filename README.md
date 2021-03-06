#  BAI Case Study for Tutorial IBM Cloud Functions & Apache OpenWhisk lab at Serverless Days NYC 2018

<a href="https://docs.google.com/presentation/d/1zer_AC0ZgP2cJekqyLdnYKd60cQq5mVMW6oTXP_8meU/edit?usp=sharing">Overview Slides</a>

## Context

This case study is specifically prepared for 
<a href="https://www.serverlessnyc.com/ibm">IBM tutorial</a> in
<a href="https://www.serverlessnyc.com/">Serverless NYC, A serverless reality check - October 30 2018, New York</a>

What is BAI?

IBM® Business Automation Insights (BAI) is a platform-level component that provides visualization insights to business owners and that feeds a data lake to infuse artificial intelligence into IBM Digital Business Automation.
[More in docs](https://www.ibm.com/support/knowledgecenter/SSYHZ8_18.0.0/com.ibm.dba.bai/topics/con_bai_overview.html)

## Case study

This case study is designed to show how to use Apache OpenWhisk with IBM Cloud Functions to add custom behavior to BAI.

We simplify several aspects of BAI:
* emitter is not connected to a real system but is hardcoded to send sample task events
* analytics is simplified and modified to group task summaries by actions 
* summaries are stored as JSON objects in Elasticsearch
* dashboards are a simplified version of BAI dashboards

## Feedback

Share Feedback  - we would apprecate if you take one minute to fill very short google form: https://ibm.biz/BdY3B8

Adn feel free to reach out with any questions!
Twitter @aslom https://twitter.com/aslom


## Sign up for IBM Cloud Account
*IBM Cloud Functions is based on the Apache OpenWhisk project.  We'll be using IBM Cloud Functions for today's lab, but the concepts could apply to any managed Serverless offering.*

1. [Sign up for an IBM Cloud Account](https://ibm.biz/BdY3BT) [https://ibm.biz/BdY3BT]
2. This should redirect you to IBM Cloud as a part of the sign up process, but if not you can go directly there at [https://bluemix.net](https://bluemix.net)
3. Sign in to confirm your account was created.

## Install IBM Cloud CLI & IBM Cloud Functions Plugin
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
    * You should have a space that was created automatically for you as well, called dev.  If it was, then the `ibmcloud target --cf` command would show that this space was targeted, and you can skip the steps for creating a space.
      * If you do not have a space; let's create one. In this example, we'll call our space dev, but you can choose anything you want: `ibmcloud cf create-space dev`
      * Ensure your org & space is correctly targeted using `ibmcloud target --cf`
    * Confirm cloud-functions plugin is installed: `ibmcloud fn` should return some help information.
        * If the plugin is not installed, install it: `ibmcloud plugin install cloud-functions`

## Create your first action (Hello World) using the CLI!
*Your first goal is to create a simple hello world action.  This action will return the string 'Hello World' when it is in invoked.*

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

## Create BAI analytics action

Now that you have a basic hello action working, you are ready to go to the main part of our tutorial: let's move to [BAI Case study](analytics/README.md).


## Optional setup

It is not required for this lab due to time constraints, but in the future you could use your own Kafka or Elasticsearch.

To use your own Kafka, update <a href="kafka.json">JSON with Kafka configuration</a>.

To use your own Elasticsearch, update  <a href="elastic.json">JSON with Elasticsearch installation</a> or use the one provided (should be valid during lab).
