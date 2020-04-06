#!/bin/bash
gunicorn -w 5 --timeout 120 -b 0.0.0.0:5005 server:app
