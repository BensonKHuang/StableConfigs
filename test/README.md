# Testing

To run all tests:

    $ python3.7 -m unittest discover -v

To run individual tests:

    $ python3.7 -m unittest test_Parser.py
    $ python3.7 -m unittest test_ProjectPipeline.py


If there are formatting issues, it is likely due to a PYTHONPATH issue

    # export PYTHONPATH={/path/to/StableConfigs}
    export PYTHONPATH=/home/bhuang/SeniorDesign/StableConfigs
