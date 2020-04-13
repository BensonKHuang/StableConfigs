#!/bin/bash
celery -A server.tasks.celery worker --loglevel=info
