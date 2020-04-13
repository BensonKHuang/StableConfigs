#!/bin/bash
gunicorn -w 1 --timeout 300 -b 0.0.0.0:5005 tasks:app
