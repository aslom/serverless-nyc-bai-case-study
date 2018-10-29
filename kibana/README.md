# How to run Dashboard

## Configure Kibana and see summary JSON in dashboard

TODO

Check summary is saved:

```
$ curl -u admin:IDGYVALTPVDZZVCZ 'https://portal-ssl113-38.bmix-dal-yp-cc659f75-4d33-404d-8934-644c6858f0ca.250607799.composedb.com:58570/demo/doc/task-\{C0B24665-0100-C335-A06E-0432C264E7B7\}'

{"_index":"demo","_type":"doc","_id":"task-{C0B24665-0100-C335-A06E-0432C264E7B7}","_version":2,"found":true,"_source":{"type": "task", "id": "{C0B24665-0100-C335-A06E-0432C264E7B7}", "category": "icm", "timestamp": "2018-08-17T07:04:04.675000+00:00", "start-time": "2018-08-17T07:04:04.675000+00:00", "end-time": "2018-08-17T07:04:04.675000+00:00", "duration-seconds": 0.0, "task-state": "Ready", "state": "Ready"}}
```
