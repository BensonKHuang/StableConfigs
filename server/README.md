# API Server Usage
We provide an API Server that can serve StableConfigs over the network.
The default serve location is at http://localhost:5005/ 

This has 3 APIs, and uses async and celery distriubted task queue to manage computations:
- start task:  /task POST
- task status: /status/<task_id> GET
- terminate: /terminate/<task_id> DELETE

## API Request Body and Response Examples

### /task POST

*request*
```json
{
    "monomers":[
        ["a", "b"],
        ["a*", "b*"],
        ["a*", ">mon1"],
        ["b*"]
    ],
    "constraints":[
        ["FREE", "mon1"]
    ],
    "gen":2,
    "init_k":2
}
```

*response*
```json
{   
    "task_id": "{task_id}",
}
```

### /status/<task_id> GET


**status_code 200** : Completed 
```json
{   
    "status": "COMPLETE",
    "configs":[
            {
                "polymers":[
                    [["a*", "b*"], ["a", "b"]], 
                    [["b"]], 
                    [["a"]]
                ],
                "polymers_count":3
            }
        ],
    "count":1,
    "entropy": 3
}
```

**status_code 202** : In Progress
```json
{
    "status": "Progress",
    "count": "{current_configuration_number}",
    "k": "{current_min_polymer_k}"
}
```

**status_code 203** : Try Again
```json
{
    "status": "Progress",
    "count": "{current_configuration_number}",
    "k": "{current_min_polymer_k}"
}
```

**status_code 400** : Time Out
```json
{
    "status": "TimedOut",
    "message": "{Exception string...}"
}
```

**status_code 401** : TBNException
```json
{
    "status": "TBNException",
    "message": "{Exception string...}"
}
```

**status_code 402** : Exception
```json
{
    "status": "Exception",
    "message": "{Exception string...}"
}
```

### /terminate/<task_id> DELETE

```json
{
    "status": "terminating task: {task_id}"
}
```

## Testing API

Running API tests will fail unless local server is running: 

    $ python3.7 -m unittest server/tests/test_api.py -v

# Deployment

## Tech Stack
- Supervisor (Manages and runs all backend daemons concurrently)
    - Gunicorn (production-ready Python WSGI HTTP Server)
        - Flask Server
        - StableConfigs
    - Celery (Asynchronous Distirbuted Task Queue)
    - Redis (Message and Results broker for Celery)

### Requirements
- OSX or Unix machine 
- Python >= 3.5

## Start Server locally ...

#### 1. Create a virtual environment
    
    $ python3 -m venv ~/backendenv
    $ source ~/backendenv/bin/activate

    (backendenv) $ pip3 install -r server/requirements.txt

*Note: To Deactivate and exit virtual environment:*

    (backendenv) $ deactivate
    $

#### 2. Install core libraries
You need to install the stableconfigs python module (from root directory) on your machine:

    (backendenv) $ python3 setup.py install

#### 3. Install redis source
To have celery message broker work, you need to install redis on in your directory

    (backendenv) $ ./install-redis.sh 

#### 4. Modify your server/configs/conf.d files to use your machine's absolute path
You need to modify the following files to use your machine's absolute path. 
Run the command to see your path: 

    $ pwd

- `redis.conf`:

    directory={/path/to/StableConfigs/root}/server/redis-stable
    command={/path/to/StableConfigs/root}/server/redis-stable/src/redis-server

- `celeryd.conf`:

    directory={/path/to/StableConfigs/root}
    command={/path/to/virtualenv}/bin/celery -A server.tasks.celery worker --loglevel=info

- `gunicornd.conf`:

    directory={/path/to/StableConfigs/root}/server
    command={/path/to/virtualenv}/bin/gunicorn -w 1 --timeout 3000 -b 0.0.0.0:5005 tasks:app

#### 5. Setup supervisor and copy all configuration files to your machine
Create the supervisor directories and copy the files over to /etc/supervisor/
*Note: You will likely have to run with sudo permissions to create log directories*

    (backendenv) $ sudo ./setup-supervisor.sh 

#### 6. Run supervisor daemon (on your machine)
*Note: You will likely have to run with sudo permissions unless group permissions are added*
    
    (backendenv) $ supervisord /etc/supervisor/supervisord.conf

#### 7. Check status of process (on your machine)
*Note: You will likely have to run with sudo permissions unless group permissions are added*

    (backendenv) $ supervisorctl 
    supervisor> 
    
    #or

    (backendenv) $ supervisorctl <command>

Supervisor commands:

    supervisor> status 
    celery                           RUNNING   pid 53638, uptime 0:02:08
    gunicorn                         RUNNING   pid 53639, uptime 0:02:08
    redis                            RUNNING   pid 53637, uptime 0:02:08

Daemon statuses:

    supervisor> status <program_name>
    celery                           RUNNING   pid 53638, uptime 0:02:12

Restart processes:
    
    supervisor> restart <program_name>

    supervisor> restart celery
    celery: stopped
    celery: started

Reload entire supervisor daemon:

    supervisor> reload
    Really restart the remote supervisord process y/N? y
    Restarted supervisord

Shutdown server completely:

    supervisor> shutdown

More information on supervisorctl: 

    supervisor> help 

## Deploying with Supervisor on a Server

#### 0. Check if you can start the server locally using the previous instructions 
- Create your python virtual environment 
- Install the core library
- Install the Redis Broker

#### 1. Add user group
Assuming you are deploying to a unix environment, we should not deploy with sudo permissions.
We should crearte a user group and set appropriate permissions in our .conf files (commented out)

    $ groupadd supervisor
    $ usermod -a <your-username> -G supervisor

To find your username (on Linux), you can run:

    $ whoami

Relog into your server to propagate user groups (so new group membership takes effect).

#### 2. Edit configuration files
Edit the server/configs/supervisord.conf file:

    [unix_http_server]
    file=/var/run/supervisor.sock ; (the path to the socket file)
    chmod=0770 ; socket file mode (default 0700)
    chown=root:supervisor

#### 3. Setup supervisor and copy all configuration files to your machine

    (backendenv) $ sudo ./setup-supervisor.sh

#### 4. Run supervisor daemon or reload SupervisorCTL

    (backendenv) $ supervisorctl reload


## FAQ (for deployment)

#### What is general flow of API? 
1. `POST /task request` with appropriate request format, which will return you <task_id>
2. `GET /status/<task_id>` will return you status of computation or results if finished
3. `DELETE /terminate/<task_id>` will terminate the computation if it is currently in progress

#### How do I change timeout?
Go to the tasks.py file and change the `TIMEOUT` flag to whatever integer seconds (Currently set to 90)

#### How do I persist results longer?
Currently the default of the redis backend results is set to 300 seconds. 
Go to the tasks.py file and change the `celery.conf.result_expires = 300` to a greater number

#### If the server is shutdown and I want to redeploy, what do I do?
If your server resets, autorestart is not currently enabled.
To start the server again, simply run `(backendenv) $ supervisord /etc/supervisor/supervisord.conf`

You can enable autorestart by changing each conf.d/*.conf file by adding the `autorestart=true` flag

#### If the website is currently in deployment and I want to make a change, what do I do?
1. After updating the code, check if all tests are passing:
    
    $ cd tests
    $ python3 -m unittest discover -v

2. After confirming your change, run `python3 setup.py install` in your python virtual environment (will update the build/ folder):

3. Reload your supervisor daemon:

    $ supervisorctl reload

#### Why isn't supervisord working? 

You might have a supervisord instance already running. Supervisor manages one configuration file only, which is default to supervisord.conf
Check if you have an instance running using: `sudo supervisorctl status`

#### The Supervisor process is sort of messed up. How can I stop the process ...?

You can print out the supervisor daemon processes here and manually kill them:

    $ ps -ef | grep supervisor
    $ pkill -9 <pid>
