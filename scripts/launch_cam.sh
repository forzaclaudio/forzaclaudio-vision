#!/bin/bash

if [ -z ${1} ] 
then
  IP=192.168.50.64
else
  echo "Using IP: "${1}
  IP=${1}
fi
PORT=4747

if [ -z ${2} ] 
then
  PORT=4747
else
  echo "Using port: "${2}
  PORT=${2}
fi


droidcam-cli ${IP} ${PORT}
