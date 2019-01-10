#!/bin/bash

export FLASK_APP=albrookRESTServer.py
export FLASK_DEBUG=1
flask run --port 5002 --host 0.0.0.0
