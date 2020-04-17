# API Server Usage
We provide an API Server that can serve StableConfigs over the network.
The default serve location is at http://localhost:5005/ 

This has 3 APIs, and uses async and celery distriubted task queue to manage computations:
    - start task:  /task POST
    - task status: /status/<task_id> GET
    - terminate: /terminate/<task_id> DELETE
 

## Start Server ...

### Requirements
- OSX or Unix machine 

#### Create a virtual environment (from the server directory)
    
    $ virtualenv stableenv
    $ source stableenv/bin/activate
    (stableenv) $ pip install -r requirements.txt

#### Install core libraries
You need to install the stableconfigs python module (from root directory) on your machine:

    (stableenv) $ python3 setup.py install

#### Start Redis Server 
    $ ./run-redis.sh

#### Start Celery Broker worker
    $ ./celery.sh

#### Start gunicorn wsgi - flask server
Gunicorn (pip3 install gunicorn) is a production-ready Python WSGI HTTTP Server. 
To run the server with Gunicorn on your Ubuntu server:

    $ ./gunicorn.sh

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