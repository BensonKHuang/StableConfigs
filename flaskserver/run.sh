#!/bin/bash
gunicorn3 -w 5 --timeout 80 -b 0.0.0.0:5005 server:app
