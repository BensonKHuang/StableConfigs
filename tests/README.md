# Test Suite

To run all tests (including API tests, which will fail if Server is not running):

    $ python3.7 -m unittest discover -v

To run individual unit tests:

    $ python3.7 -m unittest test_parser.py -v
    $ python3.7 -m unittest test_encoder.py -v
    $ python3.7 -m unittest test_satsolver.py -v
    $ python3.7 -m unittest test_decoder.py -v

To run integration tests:

    $ python3.7 -m unittest test_intgeration.py -v

Running API tests will fail unless local server is running: 

    $ python3.7 -m stableconfigs -s #Start Server
    $ python3.7 -m unittest test_api.py -v

If there are formatting issues, it is likely due to a PYTHONPATH issue

    # export PYTHONPATH={/path/to/StableConfigs}
    export PYTHONPATH=/home/bhuang/SeniorDesign/StableConfigs
