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

Running API tests will fail unless a local server is running: 

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

## First Steps to setup build files for deployment:

#### 1. Create a virtual environment and download environment libraries/binaries
    
    $ python3 -m venv ~/env
    $ source ~/env/bin/activate

    (env) $ pip3 install --upgrade pip
    (env) $ pip3 install -r server/requirements.txt

*Note: To Deactivate and exit virtual environment:*

    (env) $ deactivate

#### 2. Install core libraries
You need to install the stableconfigs python module (from root directory) on your machine:

    (env) $ python3 setup.py install

#### 3. Install redis source
To have celery message broker work, you need to install redis on in your directory

    (env) $ ./install-redis.sh 

## [Option 1] Start Server Manually without Supervisor
If you want to quickly run the processes locally, you can simply run the following command line commands. 
This is not a good long term solution, as it doesn't daemonize (detach from shell) the processes. 

##### 1. Start the Redis Server

    (env) $ server/redis-stable/src/redis-server

##### 2. Start the Celery Worker
Run the code from root directory

    (env) $ celery -A server.tasks.celery worker --loglevel=info

##### 3. Start the Gunicorn Worker
    (env) $ cd server/
    (env) $ gunicorn -w 1 --timeout 3000 -b 0.0.0.0:5005 tasks:app

## [Option 2] Start Server Locally with Supervisor Daemon for Production Deployment ...
You will want to start the server locally with supervisor for much faster development speed and actual deployment.
Supervisor will daemonize all the (above) redis, celery, and gunicorn processes, which will be managed by your OS.

#### 1. Modify your codemod script to use your machine's absolute path
You need to modify the following files to use your machine's absolute path. 
In the file `setup-supervisor.sh`, modify the $SRC_DIR and $VENV_DIR variables to point to your machine's absolute path.

    # Change these values to fit your machine's absolute path for source directory and virtual env path 
    SRC_DIR="/path/to/StableConfigs"
    VENV_DIR="/path/to/env"

#### 2. Setup supervisor and copy all configuration files to your machine
Create the supervisor directories, update paths in supervisord.conf files, and copies file over to /etc/supervisor/
*Note: You will likely have to run with sudo permissions to create log directories*

    (env) $ sudo ./setup-supervisor.sh

*Note: If you have to use sudo, you should instead grant user write permissions to the following directories*

- /var/log/supervisor/
- /etc/supervisor/

#### 3. Run supervisor daemon (on your machine)
*Note: You will likely have to run with sudo permissions permissions*
    
    (env) $ sudo ~/env/bin/supervisord -c /etc/supervisor/supervisord.conf

#### 4. Check status of processes (on your machine)
*Note: You will likely have to run with sudo permissions unless group permissions are added*

Enter supervisor mode:

    (env) $ sudo ~/env/bin/supervisorctl 
    supervisor> <command>

    # EQUIVALENT COMMAND: 
    (env) $ ~/env/bin/supervisorctl <command>

*status* - Supervisor Status for all processes:

    supervisor> status
    celery                           RUNNING   pid 53638, uptime 0:02:08
    gunicorn                         RUNNING   pid 53639, uptime 0:02:08
    redis                            RUNNING   pid 53637, uptime 0:02:08

*status <program_name>* - Daemon statuses:

    supervisor> status celery
    celery                           RUNNING   pid 53638, uptime 0:02:12

*restart <program_name>* - Restart process:
    
    supervisor> restart <program_name>

    supervisor> restart celery
    celery: stopped
    celery: started

*reload* - Reload entire supervisor daemon and processes:

    supervisor> reload
    Really restart the remote supervisord process y/N? y
    Restarted supervisord

*shutdown* - Shutdown server completely:

    supervisor> shutdown

*help* - More information on supervisorctl: 

    supervisor> help 

#### 5. (Optional) Tips for Production
While not covered in this documentation, for proper deployment, you should use appropriate deployment techniques, including:
1. Setting up user groups/permissions with supervisor (not running with root)
2. Setting up a proxy server such as nginx to prevent DDoS and other security features
3. Dockerize this workflow for faster container deployment 

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
To start the server again, simply run `(env) $ ~/env/bin/supervisord /etc/supervisor/supervisord.conf`

You can enable autorestart by changing each conf.d/*.conf file by adding the `autorestart=true` flag

#### If the website is currently in deployment and I want to make a change, what do I do?
1. After updating the code, check if all tests are passing:
    
    $ cd tests
    $ python3 -m unittest discover -v

2. After confirming your change, run `python3 setup.py install` in your python virtual environment (will update the build/ folder):

3. Reload your supervisor daemon:

    $ supervisorctl reload

#### Why isn't supervisord working? 

1. You might have a supervisord instance already running. Supervisor manages one configuration file only, which is default to supervisord.conf.
    - Check if you have an instance running using: `sudo supervisorctl status`

2. You may have set up false paths from your script. The `setup-supervisor.sh` script simply creates the directories and codemods the configuration file.

3. Check the logs in /var/log/supervisor/ for information regarding specific processes. 


#### The Supervisor process is sort of messed up. How can I stop the process ...?

You can print out the supervisor daemon processes here and manually kill them:

    $ ps -ef | grep supervisor
    $ pkill -9 <pid>
