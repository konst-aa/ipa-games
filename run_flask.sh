#!/usr/bin/env bash

source .venv/bin/activate

gunicorn -w 4 --bind 0.0.0.0:8000 'main:app'
