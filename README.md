# Stable Configurations
Python tool to generate Stable Configurations of Monomers by reducing the problem to NP-Complete SAT. 


#### Use Cases
+ Finding Stable Configurations of Thermodynamic Binding Networks
+ Finding Stable Configurations with specified instructions

#### System Requirements for Command Line Tool and Native installation
+ POSIX-compliant operating system (Linux or MacOS environment) 
+ python3.6 or higher
+ pip3 (Python Package Installer for Python 3)

Docker instructions are also specified in [Docker Usage](#-docker-usage) section.

# Installation instructions

Install the requirements (needed for Command Line Tool):

    $ pip3 install -r requirements.txt

*Optional:* Install the StableConfigs package (needed for importing StableConfig modules into project):

    $ python3 setup.py build
    $ python3 setup.py install

*Use a virtual environment (virtualenv) or add "--user" flag if working on personal environment to end of commands*


## Python Usage (import in project)

    from stableconfigs import StableConfig

    example_path = 'input/basic.txt'
    polymers = StableConfig.get_stable_configs(example_path)

  
## Command line tool
    
    $ python3 -m stableconfigs {path/to/tbn_file.txt} {optional/path/to/instr.txt}


### Solving General TBN Problems (tbn_file.txt)

The input file to solve tbn problems is as follows:

#### Binding Sites
- Each token represents a binding site: "a"
- Each token that ends with a "&ast;" indicates a compliment binding site: "a&ast;"

#### Monomers
- Each line represents a monomer (space separated binding sites): "a b c d&ast;"
- Ending the line with ":{name}" will uniquely label the monomer : "a b c d&ast; :m1"


### Additional Feature Instructions (instr.txt)

In the instruction file (the second argument), you can provide instructions to check additional properties

#### TOGETHER

Specifying **TOGETHER** attempts to force the specified monomers to bind into a polymer

    TOGETHER {m1} {m2} {m3}

#### FREE

Specifying **FREE** attempts to force the specified monomer(s) to not bind to any other monomer

    FREE {m1}


#### Example 1 input

    basic.txt

    a b*
    a* b
    a
    a* b
    b
    b


#### Example 1 output
    
    $ python3 -m stableconfigs input/basic.txt

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


#### Example 2 input

    stably_together_example.txt

    a :t1
    a* b* :t2
    a b
    b


    stably_together_instructions.txt

    TOGETHER t1 t2


#### Example 2 output
    
    $ python3 -m stableconfigs input/stably_together_example.txt input/stably_together_instructions.txt


    ...
    Found an original stable configuration with [ 3 ] polymers.

    ...
    Found a modified stable configuration with [ 2 ] polymers.

    Entropy is [ 1 ] away from stable configuration

        Polymer number 1
            ['a', 'b']

        Polymer number 2
            ['a']	t2
            ['a*', 'b*']	t1
            ['b']	t3

    Properties:
        TOGETHER ['t2', 't3']

    Completed in 0.008085012435913086 seconds.


# Docker Usage

StableConfigs contains a Dockerfile to support running the program on Docker. In order to use docker you need to have Docker locally on your machine. Using Docker is useful to ensure that the program will work on your machine.

Build a docker image:

    $ Docker build -t stablegen .


Run stable configs on docker and pass local files as arguments by using the "-v" docker option for mounting:

    $ Docker run -v {/absolute/local/path/tbn_file.txt}:/{tbn_file.txt} stablegen {tbn_file.txt}

General TBN Problem Example:

    $ Docker run -v /users/solo/and.txt:/and.txt stablegen and.txt

To run additional instructions, you must provide an additional file:

    $ Docker run -v {absolute/local/path/tbn_file.txt}:/{tbn_file.txt} -v {absolute/local/path/instr.txt}:/{instr.txt} stablegen {tbn_file.txt} {instr.txt} 


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
