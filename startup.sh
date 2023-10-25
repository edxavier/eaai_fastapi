#!/bin/bash

DIR=/root/eaai_fastapi
VENV=/root/flask_venv/bin/activate
BIND=/tmp/uvicorn.sock

cd $DIR
source $VENV

exec uvicorn ap:app --port 8081 --uds=$BIND
