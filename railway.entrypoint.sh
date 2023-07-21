#!/bin/sh

gunicorn --workers 4 -k uvicorn.workers.UvicornWorker ai4collab.asgi:application