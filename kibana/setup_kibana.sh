#!/bin/bash
set -vx

SETUP_HOST=localhost
if [[ $DOCKER_HOST != "" ]]; then
  SETUP_HOST=$(echo $DOCKER_HOST | sed -e 's/\(tcp:\/\/\)*\([a-z0-9\.]*\):[0-9]*/\2/')
fi

ES_INDEX=${ES_INDEX:-demo}

KIBANA_URL=${KIBANA_URL:-http://$SETUP_HOST:5617}
ES_URL=${ES_URL:-http://$SETUP_HOST:9206}

# detect and create full URL ti use with curl
ES_URL=https://admin:QZSFKVNUNTMWPHMY@portal-ssl65-41.bmix-dal-yp-c401ad96-667e-4128-af0e-cb3d54fd1cf9.250607799.composedb.com:62863
ES_USER=admin
ES_PASS=QZSFKVNUNTMWPHMY

KIBANA_URL=http://localhost:5617

ES_URL_INDEX=${ES_URL_INDEX:-$ES_URL/$ES_INDEX}
USER_PAS="-u ${ES_USER}:${ES_PASS}"

echo "Using $KIBANA_URL for Kibana and $ES_URL_INDEX for Elastic Search with $USER_PAS"



# index pattern

curl -f -XPOST $USER_PAS -H 'Content-Type: application/json' -H 'kbn-xsrf: anything' \
  "$KIBANA_URL/api/saved_objects/index-pattern/$ES_INDEX" \
  -d"{\"attributes\":{\"title\":\"$ES_INDEX\",\"timeFieldName\":\"timestamp\"}}"

# Make it the default index
curl -XPOST $USER_PAS -H 'Content-Type: application/json' -H "kbn-xsrf: anything" \
  "$KIBANA_URL/api/kibana/settings/defaultIndex" \
  -d"{\"value\":\"$ES_INDEX\"}"

# sample data

curl -XPUT $USER_PAS -d "@../samples/task1.json" -H 'Content-Type: application/json' -k "$ES_URL_INDEX/doc/{C0B24665-0200-C4B8-8768-591884F5BAD7}?pretty"

curl -XPUT $USER_PAS -d "@../samples/task2.json" -H 'Content-Type: application/json' -k "$ES_URL_INDEX/doc/{C0B24665-0400-CDAD-9209-15858A4C3AF6}?pretty"

curl -XPUT $USER_PAS -d "@../samples/summary1.json" -H 'Content-Type: application/json' -k "$ES_URL_INDEX/doc/flux1-task-{C0B24665-0100-C335-A06E-0432C264E7B7}?pretty"

curl -XPUT $USER_PAS -d "@../samples/summary2.json" -H 'Content-Type: application/json' -k "$ES_URL_INDEX/doc/flux2-task-{C0B24665-0100-C335-A06E-0432C264E7B7}?pretty"


