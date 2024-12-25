<!--
 * @Author: Ruide Cao (caoruide123@gmail.com)
 * @Date: 2024-12-22 02:14:46
 * @LastEditTime: 2024-12-25 19:58:34
 * @FilePath: \\sagkit\\README.md
 * @Description: README
 * Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
-->
# SAGkit

<img src="doc/sagkit.png" alt="go-sag" width="200">

A toolkit for constructing and analyzing schedule-abstraction graph in Python.
You may also be interested in [Official SAG repository (in C++)](https://github.com/SAG-org/schedule_abstraction-main), [sag-go (in GO)](https://github.com/porya-gohary/sag-go), and [sag-py (in Python)](https://github.com/RaduLucianR/sag-py).

## Install

You may install SAGkit from source (recommended):
```
git clone https://github.com/RyderCRD/sagkit
```

or install with pip:
```
pip install sagkit
```

or reproduce the results in our paper directly with a docker image (requires [Docker](https://www.docker.com/)):
```
docker pull caoruide/sagkit
```

## Use

Change direcotry to ./sagkit (over the /src directory):
```
cd sagkit
```
Run all unit tests:
```
python -m unittest discover tests
```
Normally, all tests will pass correctly. You can then generate jobsets and build the SAGs.
Change direcotry to ./src:
```
cd src
```
The jobset generator takes the following arguments:
* --ET_ratio: What percentage of jobs are ET. Default is 15.
* --utilization: What percentage of the macrocycle is the expectation of the total execution time. Default is 45.
* --jobset_folder: Which folder to save the jobsets. Default is "./jobsets/".
* --num_job: How many jobs to include in each job set. Default is 1000.
* --num_instance: How many jobsets to generate for each set of parameter combinations. Default is 1.

Generate jobsets:
```
python -m sagkit.jobset_generator [ET_ratio] [utilization] [jobset_folder] [num_job] [num_instance]
```

The SAG constructor takes the following arguments:
* --jobset_folder: Which folder to read the jobsets. Default is "./jobsets/".
* --constructor_type: What constructor(s) to use to do the construction. Default are "original,extended,hybrid".
* --save_dot: Which folder to save the dot files. Default is "./dotfiles/".
* --save_statistics: Which path to save the statistics results. Default is "./statistics.csv".

Construct SAGs:
```
python -m sagkit.sag_constructor [jobset_folder] [constructor_type] [save_dot] [save_statistics]
```

## Reproduce

* Step 1: Create a folder named 'results' in the current working directory:
```
mkdir results
```

* Step 2: **Reproduce Fig. 1 and 2**. The .dot files corresponding to the figures ('original.dot' for Fig.1, 'hybrid.dot' for Fig.2) will appear under the /results folder after running the following command:
```
docker run -v "$(pwd)/results:/output" caoruide/sagkit sagkit.sag_constructor --save_dot True --jobset_folder /basic_idea/
```

* Step 3 (optional): **Visualize Fig. 1 and 2**. This step is optional because the .dot files are readable and easy to understand. Paste the contents of each .dot file to:
```
https://dreampuf.github.io/GraphvizOnline (you may want to access in incognito mode.)
```

* Step 4: **Reproduce Fig. 3**. Also, you may visualize the .dot files ('original.dot' for Fig. 3 (a), 'extended.dot' for Fig. 3 (b), 'hybrid.dot' for Fig. 3 (c)) following Step 3. 
```
docker run -v "$(pwd)/results:/output" caoruide/sagkit sagkit.sag_constructor --save_dot True --jobset_folder /example1/
```

* Step 5: **Reproduce Fig. 4**. Also, you may visualize the .dot files ('original.dot' for Fig. 4 (a), 'extended.dot' for Fig. 4 (b), 'hybrid.dot' for Fig. 4 (c)) following Step 3. 
```
docker run -v "$(pwd)/results:/output" caoruide/sagkit sagkit.sag_constructor --save_dot True --jobset_folder /example2/
```

* Step 6: Generate job sets:
```
docker run -v "$(pwd)/results:/output" caoruide/sagkit sagkit.jobset_generator --ET_ratio 0,10,15,20,30,40,50,60,70,80,90,100 --utilization 45,50,55,60,65,70,75    
```

* Step 7: **Reproduce Fig. 5 and Tables 2-4**. This step may take some time (29 hours on my machine). All numerical results corresponding to Figure 5 and Tables 2-4 will be automatically generated in the /results/statistics.csv file. The construction times may vary from Fig. 5 (a), (b), (c) depending on the computational power of the machine.
```
docker run -v "$(pwd)/results:/output" caoruide/sagkit sagkit.sag_constructor  
```

## Contribute

Contributions are welcome! Please feel free to drop your issues and PRs :)