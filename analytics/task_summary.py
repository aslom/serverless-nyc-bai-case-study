#!/usr/bin/env python3

import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import certifi
import os

from elasticsearch import Elasticsearch
import json
import datetime
import dateutil.parser
from datetime import date
from dateutil.relativedelta import relativedelta
import time

import ssl
default_sslContext = ssl._create_unverified_context()

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings()

client = None
index = os.getenv('ES_INDEX', 'demo')

EVENT_SUFFIX = 'Event'
SUMMARY_SUFFIX = 'Summary'
ACM_PREFIX = 'icm'


def get(eventType, eventId):
    json = client.get(index=index, doc_type='doc', id=eventType+'-'+eventId)
    return json['_source']


def put(eventType, eventId, json):
    client.index(index=index, doc_type='doc',
                 id=eventType+'-'+eventId, body=json)


def exists(eventType, eventId):
    return client.exists(index=index, doc_type='doc', id=eventType+'-'+eventId)


def getIfExists(eventType, eventId):
    if exists(eventType, eventId):
        return get(eventType, eventId)
    else:
        return None


def delete(eventType, eventId):
    # return client.delete(index=index, doc_type=eventType, id=eventId)
    return client.delete(index=index, doc_type='doc', id=eventType+'-'+eventId)


def create_or_load_summary(objectType, objectId):
    summaryType = objectType.lower()  # + SUMMARY_SUFFIX
    if exists(summaryType, objectId):
        summary = get(summaryType, objectId)
        print('processor loaded summaryType=', summaryType,
              'objectId=', objectId, 'summary=', summary)
        return summary
    else:
        summary = None
        summary = json.loads('{ }')
        summary['type'] = objectType.lower()
        summary['id'] = objectId
        print('processor creates summaryType=', summaryType,
              'objectId=', objectId, 'summary=', summary)
        return summary


def save_summary(summary):
    summaryType = summary['type']
    objectId = summary['id']
    print("saving "+summaryType+"-"+objectId+" summary=", summary)
    put(summaryType, objectId, summary)


def make_error(msg):
    print('processor error', msg)
    res = {'result': 'error', 'message': msg}
    return res


def main(dict):
    print('dict=', dict)
    if 'analytics-id' not in dict:
        return make_error('processor missing analytics-id')
    else:
        analytics_id = dict['analytics-id']
    if 'ES_URL' in dict:
        esUrl = dict['ES_URL']
        esUser = dict.get('ES_USER')
        esPass = dict.get('ES_PASS')
    else:
        esUrl = os.getenv('ES_URL', 'http://localhost:9200')
        esUser = os.getenv('ES_USER')
        esPass = os.getenv('ES_PASS')
    print('esUrl=', esUrl, 'esUser=', esUser, 'esPass=', esPass)
    http_auth = None
    if esUser is not None:
        http_auth = (esUser, esPass)
    global client
    client = Elasticsearch([esUrl],  verify_certs=False, http_auth=http_auth)
    resp = {}
    messages = dict['messages']
    size = len(messages)
    for i in range(size):
        msg = messages[i]
        #print('msg=', msg)
        event = msg.get('value')
        #print('event=', event)
        if event is None:
            return make_error('processor missing message value')
        eventCategory = event.get('category')
        if eventCategory is None:
            return make_error('processor skipping missing category event ' + event)
        print('processor eventCategory=', eventCategory)
        supportedEventCategories = ["icm:TaskEvent"]
        if eventCategory not in supportedEventCategories:
            return make_error('processor skipping unrecognized category for event ' + event)
        print("event=", json.dumps(event, sort_keys=True, indent=4))
        # create or load summary
        # if "source.instance.id" not in event:
        #    return None
        objectId = event['source']['instance']['id']
        print('processor objectId=', objectId)
        eventType = event.get('type')
        print('processor eventType1=', eventType)
        if eventType.startswith(ACM_PREFIX):
            eventType = eventType[(len(ACM_PREFIX)+1):]
        print('processor eventType2=', eventType)
        lst = eventType.split(":", 1)
        state = event.get('state')
        if len(lst) > 1:
            if state is None:
                state = lst[1]
            print('processor state1=', state)
            eventType = lst[0]   # remove anything after first :
            print('processor eventType3=', eventType)
        objectType = eventType
        # remove "Event" suffix
        if objectType.endswith(EVENT_SUFFIX):
            objectType = objectType[:len(EVENT_SUFFIX)-1]
        print('processor objectType1=', objectType)
        summary = create_or_load_summary(objectType, objectId)
        if summary is None:
            return
        summary['analytics-id'] = analytics_id
        # duration, {object}Duration => taskDuration
        # JSON.stringify({'now': new Date()})
        summary['category'] = 'icm'
        timestamp = dateutil.parser.parse(event['timestamp'])
        #summary['@timestamp'] = timestamp.isoformat()
        summary['timestamp'] = timestamp.isoformat()
        startTime = summary.get('start-time')
        if startTime is not None:
            startTime = dateutil.parser.parse(startTime)
        if ((startTime is None) or (timestamp < startTime)):
            startTime = timestamp
        print('processor startTime', startTime)
        summary['start-time'] = startTime.isoformat()
        # elif timestamp < startTime:
        #  startTime = timestamp
        endTime = summary.get('end-time')
        if endTime is not None:
            endTime = dateutil.parser.parse(endTime)
        if ((endTime is None) or (timestamp > endTime)):
            endTime = timestamp
        print('processor endTime', endTime)
        summary['end-time'] = endTime.isoformat()
        durationSeconds = (endTime - startTime).total_seconds()
        # (getTime -getTime) / 1000.0
        summary['duration-seconds'] = durationSeconds
        # state, {object}State => taskState
        # if event.get('state') is not None:
        #  state = event.get('state')
        print('processor state2=', state)
        objectTypeLowerCase = objectType.lower()
        if state is not None:
            summary[objectTypeLowerCase+'-state'] = summary['state'] = state
        # name, task-name
        if get_path(event, 'source.instance.name'):
            summary[objectTypeLowerCase +
                    '-name'] = summary['name'] = get_path(event, 'source.instance.name')
        if get_path(event, 'source.name'):
            summary[objectTypeLowerCase +
                    '-type-name'] = summary['type-name'] = get_path(event, 'source.name')
        # user.id
        if get_path(event, 'user.id'):
            summary['user-id'] = get_path(event, 'user.id')
        #print("summary=", json.dumps(summary, sort_keys=True, indent=4))
        save_summary(summary)
        # update summary with event timestamp
    resp['result'] = 'ok'
    return resp


def get_path(obj, path):
    path_list = path.split(".")
    size = len(path_list)
    current = obj
    val = None
    for i in range(size):
        name = path_list[i]
        val = current.get(name)
        if val is None:
            return None
        current = val
        if i < (size - 1) and not isinstance(val, dict):
            return None
    return val


# TODO write unit tests ...
if __name__ == '__main__':
    event = {'a': {'b': {'c': '1'}}}
    print(get_path(event, 'e'))
    print(get_path(event, 'a'))
    print(get_path(event, 'a.b'))
    print(get_path(event, 'a.b.c'))
