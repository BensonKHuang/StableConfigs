### David's instructions for running the server locally ###

# Alternatively: just use Docker from main directory
docker compose up -d



####################

# create local environment (in venv directory)
python -m venv venv     

# start this local environment
# it automatically ends when shell quits, or run `deactivate`
source venv/bin/activate    

# Install required packages for the server
pip install -r server/requirements.txt

# Insall stableconfigs python package itself which is used by the server
python setup.py install

# Download and compile redis
cd server
./install-redis.sh
cd ..

# Start all the processes: I run these commands in separate shells since they don't return

## Start redis:
redis-stable/src/redis-server

## Start celery:
celery -A server.tasks.celery worker --loglevel=info

## Start gunicorn:
cd server/
gunicorn -w 1 --timeout 3000 -b 0.0.0.0:5005 tasks:app

# Exit python environment (don't really need to do this)
deactivate
