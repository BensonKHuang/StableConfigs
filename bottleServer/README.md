# API Server Usage
We provide an API Server that can serve StableConfigs over the network.
The default serve location is at http://localhost:5005/ that handles one POST request on /

To run the server from root directory:
    python3 -m stableconfigs -s

To run the server with gunicorn on ubuntu:
    cd bottleServer
    ./run.sh

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
    "configs":[
        {
            "polymers":[
                [["a*", "b*"], ["a", "b"]], 
                [["b"]], 
                [["a"]]
            ],
            "polymers_count":3
        }
    ]
}
```
