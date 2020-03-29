# API Server Usage
We provide an API Server that can serve StableConfigs over the network.
The default serve location is at http://localhost:5005/ that handles one POST request on "/"

### Prerequisites
To run the server locally or in product, you need to install the stableconfigs python module on your machine:

    $ python3 setup.py build
    $ python3 setup.py install


## Local Server Deployment
To run the flask server from root directory:

    $ python3 -m stableconfigs -s

## Production Deployment
Gunicorn (pip3 install gunicorn) is a production-ready Python WSGI HTTTP Server. 
To run the server with Gunicorn on your Ubuntu server:
    
    $ cd flaskserver
    $ ./run.sh

## API Request Body and Response Examples

POST request body format (json):
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

POST response body format (json):
```json
{   
    "success": true,
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

POST response error:
```json
{   
    "success": false,
    "error": {
                "type": "EmptyProblemException",
                "message": "EmptyProblemException"
            }
}
```

## Testing API

Running API tests will fail unless local server is running: 

    $ python3.7 -m stableconfigs -s #Start Server
    $ python3.7 -m unittest flaskserver/test_api.py -v