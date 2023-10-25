#!/bin/bash

DIR=/root/eaai_fastapi
VENV=/root/eaai_venv/bin/activate
BIND=/tmp/uvicorn.sock

cd $DIR
source $VENV
 
exec uvicorn app:app --port 8081 --host 0.0.0.0 
