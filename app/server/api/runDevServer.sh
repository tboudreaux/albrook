#!/bin/bash

export FLASK_APP=server
export FLASK_DEBUG=1
flask run --port 5002 --host 0.0.0.0
