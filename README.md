# Stable Configurations
Python tool to generate Stable Configurations of Monomers by reducing the problem to NP-Complete SAT. 

#### Uses
Finding Stable Configurations of Thermodynamic Binding Networks

#### System Requirements
+ POSIX-compliant operating system (Linux or MacOS environment) 
+ python3.6 or higher
+ pip3 (Python Package Installer for Python 3)

# Installation instructions

Install the requirements (needed for Command Line Tool):

    $ pip3 install -r requirements.txt

*Optional:* Install the StableConfigs package (needed for importing StableConfig modules into project):

    $ python3 setup.py build
    $ python3 setup.py install

*Use a virtual environment (virtualenv) or add "--user" flag if working on personal environment to end of commands*

## Docker

StableConfigs contains a Dockerfile to support running the server on Docker. In order to use docker you need to have Docker locally on your machine.

Build a docker image:

    Docker build .
    
Find your image id:

    Docker images
    
Run stable configs on docker:

    Docker run {image id}

# Python Usage

    from stableconfigs import StableConfig

    example_path = 'input/basic.txt'
    polymers = StableConfig.get_stable_configs(example_path)

  
# Command line tool
    
    $ python3 -m stableconfigs {path/to/tbn_file.txt}

#### Example input

    basic.txt

    a b*
    a* b
    a
    a* b
    b
    b


#### Example output
    
    $ python3 -m src input/basic.txt

    Found a stable configuration with [ 4 ] polymers:

        Polymer number 1
                ['a', 'b*']
                ['a*', 'b']

        Polymer number 2
                ['a']
                ['a*', 'b']

        Polymer number 3
                ['b']

        Polymer number 4
                ['b']

    Completed in 0.0041961669921875 seconds.

# Citation

#### Authors
Benson Huang, Varun Prabhu, Hasan Saleemi, Anthony Vento, Steven Wang, Kyle Zhou

#### Contributors
Dr. David Soloveichik, Keenan Breik

#### References
Breik K., et. al, “Computing properties of stable configurations of thermodynamic binding networks,” 
Theoretical Computer Science, vol. 785, pp. 17–29, Sept. 2019. [source](https://arxiv.org/pdf/1709.08731.pdf)

Ignatiev A., Morgado A., and Marques-Silva J., "PySAT: Python Toolkit for Prototyping with SAT Oracles," SAT, pp. 428–437, 2018. Online.
[source](https://doi.org/10.1007/978-3-319-94144-8_26)
[github](https://github.com/pysathq/pysat)
