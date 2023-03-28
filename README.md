# Quadrocopter

Small command line tool that allows to verify if the safe Quadrocopter flight path exists for given input data.

## Program installation

Recommended python version: 3.11

Before running program, all the requirements have to be installed first. Although the list of dependencies is short,
it is recommended to use virtual environment for this installation.
Please follow the below commands to perform the installation:

    $ python3 -m venv .venv
    $ source .venv/bin/activate

To verify if python is running from virtual environment just type below command (output should be similar to below):
    
    $ which python3
    /path/to/quadrocopter/.venv/bin/python3

Then finally install dependencies just run

    $ python3 -m pip install -r requirements.txt
    
## Running CLI

### Input data from file

Program allows to read input data from file in below format:

    <number of transmitters: int>
    <transmitter 1 X coordinate: int> <transmitter 1 Y coordinate: int> <transmitter 1 M range radius: int>
    ...
    <transmitter n X coordinate: int> <transmitter n Y coordinate: int> <transmitter n M range radius: int>
    <starting point X coordinate: int> <starting point Y coordinate: int>
    <finish point X coordinate: int> <finish point Y coordinate: int>

Some examples can be found under `tests/fixtures` directory.

Having defined a file with input data, let's call it `init_data.txt` we can run the program by simply typing below command:

    $ python3 -m quadrocopter init_data.txt

Program will print output with information about the results of the validation.

#### Example success messages

When safe Quadrocopter flight is possible, message will be printed as below:

    $ python3 -m quadrocopter tests/fixtures/example-9.txt 
    For given start_point=Point(x=7, y=10), stop_point=Point(x=20, y=12) and transmitters=[Transmitter(x=10, y=10, m=3), Transmitter(x=15, y=15, m=2), Transmitter(x=20, y=15, m=4), Transmitter(x=20, y=8, m=5), Transmitter(x=15, y=10, m=2)]
    Safe flight is POSSIBLE 🚀

However, if safe Quadrocopter flight is not possible, message will be printed as below:

    $ python3 -m quadrocopter tests/fixtures/example-11.txt
    For given start_point=Point(x=5, y=5), stop_point=Point(x=7, y=10) and transmitters=[Transmitter(x=10, y=10, m=3), Transmitter(x=15, y=15, m=2), Transmitter(x=20, y=15, m=4), Transmitter(x=20, y=8, m=5), Transmitter(x=15, y=10, m=2)]
    Safe flight is NOT POSSIBLE ❌ 

#### Example error messages

When given file will not be found in the filesystem, the below message will be printed:

    $ python3 -m quadrocopter tests/fixtures/example-20.txt
    Error: file 'tests/fixtures/example-20.txt' does not exist ⛔️ 

### Input data from command line prompt

Program allows to read input data typed in manually in the prompt. The format is the same as input data file format
described in the `Input data from file` section. Program will be handful with informing each time what kind of input
is needed.

    python3 -m quadrocopter
    Type transmitters count: 
    Type transmitter1 coordinates (space separated: x y m): 
    Type transmitter2 coordinates (space separated: x y m): 
    Type transmitter3 coordinates (space separated: x y m): 
    Type transmitter4 coordinates (space separated: x y m): 
    Type transmitter5 coordinates (space separated: x y m): 
    Type transmitter6 coordinates (space separated: x y m): 
    Type starting point coordinates (space separated: x y): 
    Type finish point coordinates (space separated: x y): 

#### Example success messages

When safe Quadrocopter flight is possible, message will be printed as below:

    $ python3 -m quadrocopter                              
    Type transmitters count: 6
    Type transmitter1 coordinates (space separated: x y m): 6 11 4
    Type transmitter2 coordinates (space separated: x y m): 8 17 3
    Type transmitter3 coordinates (space separated: x y m): 19 19 2
    Type transmitter4 coordinates (space separated: x y m): 19 11 4
    Type transmitter5 coordinates (space separated: x y m): 15 7 6
    Type transmitter6 coordinates (space separated: x y m): 12 19 4
    Type starting point coordinates (space separated: x y): 10 19
    Type finish point coordinates (space separated: x y): 19 14
    For given start_point=Point(x=10, y=19), stop_point=Point(x=19, y=14) and transmitters=[Transmitter(x=6, y=11, m=4), Transmitter(x=8, y=17, m=3), Transmitter(x=19, y=19, m=2), Transmitter(x=19, y=11, m=4), Transmitter(x=15, y=7, m=6), Transmitter(x=12, y=19, m=4)]
    Safe flight is POSSIBLE 🚀 

However, if safe Quadrocopter flight is not possible, message will be printed as below:

    $ python3 -m quadrocopter
    Type transmitters count: 6
    Type transmitter 1 coordinates (space separated: x y m): 6 11 4
    Type transmitter 2 coordinates (space separated: x y m): 8 17 3
    Type transmitter 3 coordinates (space separated: x y m): 19 19 2
    Type transmitter 4 coordinates (space separated: x y m): 19 11 4
    Type transmitter 5 coordinates (space separated: x y m): 15 7 6
    Type transmitter 6 coordinates (space separated: x y m): 12 19 4
    Type starting point coordinates (space separated: x y): 5 19
    Type finish point coordinates (space separated: x y): 19 14
    For given start_point=Point(x=5, y=19), stop_point=Point(x=19, y=14) and transmitters=[Transmitter(x=6, y=11, m=4), Transmitter(x=8, y=17, m=3), Transmitter(x=19, y=19, m=2), Transmitter(x=19, y=11, m=4), Transmitter(x=15, y=7, m=6), Transmitter(x=12, y=19, m=4)]
    Safe flight is NOT POSSIBLE ❌ 
