#!/usr/bin/env python3

import os
import sys
import json
import datetime
import dateutil.parser
from datetime import date
from dateutil.relativedelta import relativedelta
import time

#import hello_yatg_web
import print_input


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


if __name__ == '__main__':
    #dict = {}
    #dict['body'] = {}
    #dict['name'] = 'Alek2'
    #dict = {'messages': [{'partition': 0, 'key': None, 'offset': 20, 'topic': 'mytopic', 'value': {'source': {'parent': {'instance': {'id': '{C0B24665-0000-C41D-905D-91B662F2CBF7}', 'name': 'VLD_ValidatorCase_000000100001'}, 'type': 'case', 'id': '{EE103375-9756-4D0D-891E-E2A3DD4157FD}', 'name': 'VLD_ValidatorCase'}, 'name': 'RadioTask', 'instance': {'id': '{C0B24665-0100-C335-A06E-0432C264E7B7}', 'name': 'RadioTask'}, 'id': '{66C798B2-7D34-4045-8CFA-780B18C71782}', 'type': 'task', 'icm': {'audit-sequence': 12219.0, 'case-instance-name': '000000100001', 'state': 'Ready', 'case-id': '{C0B24665-0000-C41D-905D-91B662F2CBF7}', 'source-class-display-name': 'RadioTask', 'version': '1534489444675', 'case-type-name': 'VLD_ValidatorCase', 'solution-name': 'Validator', 'source-class-id': '{66C798B2-7D34-4045-8CFA-780B18C71782}', 'case-instance-id': '{C0B24665-0000-C41D-905D-91B662F2CBF7}', 'case-folder-id': '{C0B24665-0000-C41D-905D-91B662F2CBF7}', 'is-task-container': False, 'case-type-id': '{EE103375-9756-4D0D-891E-E2A3DD4157FD}'}}, 'timestamp': '2018-08-17T07:04:04.675Z', 'kafka': {'key': '\"TaskEvent_C0B24665-0000-C41D-905D-91B662F2CBF7\"'}, 'business-events-envelope-version': '1.0.1', 'id': '{C0B24665-0200-C4B8-8768-591884F5BAD7}', 'category': 'icm:TaskEvent', 'type': 'icm:TaskEvent:Ready', 'user': {'id': 'intgpeadmin'}, 'business-events-extension-version': 'icm/1.0.0'}}]}
    dict = {'messages': [{'partition': 0, 'key': None,
                          'offset': 20, 'topic': 'ingress', 'value': {}}]}
    dict['messages'][0]['value'] = loadEventFromFile('../emitter/task1.json')
    dict['ES_URL'] = 'https://admin:IDGYVALTPVDZZVCZ@portal-ssl113-38.bmix-dal-yp-cc659f75-4d33-404d-8934-644c6858f0ca.250607799.composedb.com:58570/'
    resp = print_input.main(dict)
    print('first event respone=', resp)
    dict['messages'][0]['value'] = loadEventFromFile('../emitter/task2.json')
    resp = print_input.main(dict)
    print('second event response=', resp)
