# Testing

To run all tests:

    $ python3.7 -m unittest discover -v

To run individual unit tests:

    $ python3.7 -m unittest test_parser.py
    $ python3.7 -m unittest test_encoder.py
    $ python3.7 -m unittest test_satsolver.py
    $ python3.7 -m unittest test_decoder.py

To run integration tests:

    $ python3.7 -m unittest test_intgeration.py

To run api tests: 

    $... Documentation coming soon

If there are formatting issues, it is likely due to a PYTHONPATH issue

    # export PYTHONPATH={/path/to/StableConfigs}
    export PYTHONPATH=/home/bhuang/SeniorDesign/StableConfigs
