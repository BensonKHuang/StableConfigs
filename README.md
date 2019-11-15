# StableConfigs
Repository for tool to generate Stable Configurations of Monomers by reducing the problem to NP-Complete SAT. 

### Authors
+ Benson Huang
+ Varun Prabhu
+ Hasan Saleemi
+ Anthony Vento
+ Steven Wang
+ Kyle Zhou

### Uses
+ Finding Stable Configurations of Thermodynamic Binding Networks

### System Requirements
+ Linux or MacOS environment 
+ python3.6 or higher 


### Installation instructions

*coming soon*

### Command line tool
    
    $ python3.7 -m src {path/to/tbn_file.txt}


##### Example input

    basic.txt

    a b*
    a* b
    a
    a* b
    b
    b


##### Example output
    
    $ python3.7 -m src input/basic.txt

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

    Completed in 0.005658149719238281 seconds.


### Contributors
+ Dr. David Soloveichik
+ Keenan Breit

### Sources

    Breik K., et. al, “Computing properties of stable configurations of thermodynamic 
    binding networks,” Theoretical Computer Science, vol. 785, pp. 17–29, Sept. 2019.
    https://arxiv.org/pdf/1709.08731.pdf
