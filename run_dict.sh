#!/usr/bin/env bash

source .venv/bin/activate

uvicorn english_api:app --host 0.0.0.0 --port $1
