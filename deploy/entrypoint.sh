#!/bin/bash
poetry run gunicorn -c deploy/gunicorn.conf.py
nginx -g 'daemon off;'
