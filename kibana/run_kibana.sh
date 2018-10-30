#!/bin/bash
docker run --rm --name kibana16 -it -p 5617:5601 -v $PWD/config:/usr/share/kibana/config:ro docker.elastic.co/kibana/kibana-oss:6.2.2
