#!/bin/bash
gunicorn3 -w 3 --timeout 3000 -b 0.0.0.0:5005 server:app
