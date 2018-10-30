# How to run Dashboard

## Configure Kibana and see summary JSON in dashboard

```
./run_kibana.sh
```

And open

http://localhost:5617/app/kibana#/dashboards

## Without Kibana

Check summary is saved:

```
curl -u admin:QZSFKVNUNTMWPHMY 'https://portal-ssl65-41.bmix-dal-yp-c401ad96-667e-4128-af0e-cb3d54fd1cf9.250607799.composedb.com:62863/demo/doc/flux1-task-C0B24665-0100-C335-A06E-0432C264E7B7'
```

expected output

```
{"_index":"demo","_type":"doc","_id":"flux1-task-C0B24665-0100-C335-A06E-0432C264E7B7","_version":3,"found":true,"_source":{"type": "task", "id": "{C0B24665-0100-C335-A06E-0432C264E7B7}", "category": "icm", "timestamp": "2018-08-17T07:04:01.675000+00:00", "start-time": "2018-08-17T07:04:01.675000+00:00", "end-time": "2018-08-17T07:05:04.903000+00:00", "duration-seconds": 63.228, "task-state": "Ready","task-name" : "RadioTask", "state": "Ready", "analytics-id" : "flux1"}}
```
