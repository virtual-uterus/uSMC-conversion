# Uterine smooth muscle model conversion

# Table of contents
1. [General description](#general)
2. [Requirements](#requirements)
3. [Usage](#usage)
	1. [Setup](#setup)
	2. [Running the code](#code)
		1. [***model-simulation.py*** script](#sim)
		2. [***PNP-comp.py*** script](#pnp)
		3. [***sensitivity.py*** script](#sense)

<a id="general"></a>
## General description
This project focuses on comparing results from a pregnant and a non-pregnant uterine smooth muscle cell model. Details about the first version of the non-pregnant model can be found in this [paper](https://ieeexplore.ieee.org/document/10782940). 

The project is structure as follows:
```
uSMC-conversion/ (top-level directory)
|-- cells/ (contains the cellML implementations)
|-- scripts/ (contains the Python scripts)
|-- conversion/ (contains the conversion module)
|-- res/ (contains simulation outputs)
|-- tests/ (contains tests)
```

<a id="requirements"></a>
## Requirements
The code was run on Linux Ubuntu 22.04.2 LTS\
The code was developed in [Python](https://www.python.org/) version 3.10.12\
The required packages for Python are found in requirements.txt


<a id="usage"></a>
## Usage

<a id="setup"></a>
### Setup 
First clone the project into *uSMC-conversion* and enter the new directory:
```bash
$ git clone git@github.com/virtual-uterus/uSMC-conversion.git
$ cd uSMC-conversion
```

It is recommended to create a virtual environment in which to run the code. Create a virtual environment and activate it with the following commands:
```bash
$ python3 -m venv ~/venv/conversion-env
$ source ~/venv/conversion-env/bin/activate
```

Now, install the conversion module with the following commands:
```bash
$ pip3 install -e .
```

Run the test to make sure that the code is working properly:
```bash
$ pytest
```

Finally, create the *res/* directory in the uSMC-conversion directory to store the results in:
```bash
$ mkdir res
```

<a id="code"></a>
### Running the code

There are three scripts that can be run, contained in the *scripts/* directory: 
* ***model-simulation.py***
* ***PNP-comp.py***
* ***sensitivity.py***

The estrus parameters of the non-pregnant cell model (Roesler2024) can be modified in the **conversion/constants.py** script. They are loaded before running simulations and override the default values in the **conversion/Roesler2024.py** file.

<a id="simx"></a>
#### ***model-simulation.py*** script
The ***model-simulaion.py*** performs simulations for a single model. There are two subcommands: **single** and **multi**. The first performs a single simulation with the parameters set in the **conversion/constants.py** file. The second performs multiple simulations with varying values of a parameter and only works for the non-pregnant cell model (Roesler2024). 

Run the following commands from inside the *scripts/* directory to view the help message:
```bash
$ python3 model-simulation.py -h
$ python3 model-simulation.py single -h
$ python3 model-simulation.py multi -h
```


<a id="pnp"></a>
#### ***PNP-comp.py*** script
The ***PNP-comp.py*** compares the simulation outputs of the pregnant and the non-pregnant cell models. The script has two positional argument: **p_model** the pregnant model to use, and **metric** that selects the comparison metric to use. Currently, the options are:
* **mae**, for Mean Absolute Error
* **rmse**, for Root Mean Squared Error
* **correl**, for correlation
* **vrd**, for Van Rossum Distance
* **l2**, for L2-norm

When run with no flags, the script will generate a .pkl file in the *res/* directory:
* **P-MODEL_Roesler2024_METRIC_comp.pkl**, where P-MODEL is the pregnant cell model used and METRIC the selected metric. The .pkl file contains a dictionary with the comparison points between the two models.

The **P-MODEL_Roesler2024_METRIC_comp.pkl** file is required to use the **-p** flag.

**Note:** the estrus stages are always in the same order: proestrus, estrus, metestrus, diestrus.

Run the following command from inside the *scripts/* directory to view the help message:
```bash
$ python3 PNP-comp.py -h
```

<a id="sense"></a>
#### ***sensitivity.py*** script

The ***sensitivity.py*** script performs parameter sweeps for the non-pregnant cell model (Roesler2024) and plots the sensitivity of the different parameters across the estrus cycle. There are two subcommands: **sweep** and **plot**. The first performs a the sweep and compares the results with a base simulation. The base-model is computed and can be any one of the pregnant or non-pregnant cells. For the non-pregnant cell model, the estrus phase needs to be specified with the --base-estrus flag. The comparison metrics is computed for each value of the parameter. The results are saved in a .pkl file in the **res/** directory. The naming convention is BASE-MODEL_B-ESTRUS_SWEEP-MODEL_ESTRUS_PARAM_METRIC.pkl, where:
* BASE-MODEL is the base model used,
* B-ESTRUS is only added if BASE-MODEL is a non-pregnant model (Roesler2024),
* SWEEP-MODEL is the model on which the parameter sweep is performed,
* ESTRUS the associated estrus phase (only for a non-pregnant cell model),
* PARAM is the selected parameter, and
* METRIC the selected metric. 

The **plot** subcommand plots the results if they have already been computed. The plot can be for a specific estrus phase or all at once if --estrus is set to all.

Run the following commands from inside the *scripts/* directory to view the help message:
```bash
$ python3 sensitivity.py -h
$ python3 sensitivity.py sweep -h
$ python3 sensitivity.py plot -h
```
