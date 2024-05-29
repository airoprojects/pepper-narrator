#!/bin/bash

# Use  ./build.bash [version] [Dockerfile] [--no-cache]

UPAR="--build-arg UID=`id -u` --build-arg GID=`id -g`"

IMAGENAME=pepper-hri

VERSION=0.8
if [ ! "$1" == "" ]; then
  VERSION=$1
fi

DOCKERFILE=Dockerfile
if [ ! "$2" == "" ]; then
  DOCKERFILE=$2
fi

docker build $UPAR $3 -t $IMAGENAME:$VERSION -f $DOCKERFILE .

docker tag $IMAGENAME:$VERSION $IMAGENAME:latest

