#!/bin/bash

docker run \
    --rm \
    --net=host \
    -v $1:/usr/share/nginx/html \
    nginx

