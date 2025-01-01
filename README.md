<!--
 * @Author: Ruide Cao (caoruide123@gmail.com)
 * @Date: 2024-12-22 02:14:46
 * @LastEditTime: 2024-12-26 02:17:19
 * @FilePath: \\sagkit\\README.md
 * @Description: README
 * Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
-->

<img src="https://www.ryderblog.com/wp-content/uploads/2024/12/sagkit.png" width="200" alt="header pic">

# SAGkit


A lightweight Python toolkit for response-time analysis based on schedule-abstraction graph.
You may also be interested in [Official SAG repository (in C++)](https://github.com/SAG-org/schedule_abstraction-main), [sag-go (in GO)](https://github.com/porya-gohary/sag-go), and [sag-py (in Python)](https://github.com/RaduLucianR/sag-py).

## Install

You may install SAGkit with pip:
```
pip install sagkit
```

or reproduce the results in our paper with a docker image (requires [Docker](https://www.docker.com/)):
```
docker pull caoruide/sagkit
```

## Use

The jobset generator takes the following arguments:
* --ET_ratio: What percentage of jobs are ET. Default is 15.
* --utilization: What percentage of the macrocycle is the expectation of the total execution time. Default is 45.
* --jobset_folder: Which folder to save the jobsets. Default is "./jobsets/".
* --num_job: How many jobs to include in each job set. Default is 1000.
* --num_instance: How many jobsets to generate for each set of parameter combinations. Default is 1.

Note: generate_jobs() of jobset_generator.py is based on the setup in our paper, and it allows the utilization to grow in steps of 5, starting at 45 (45, 50, 55, ..., 75 are valid, 40, 46 are not). You may re-implement this method to generate the desired jobsets if you want them differently.

Generate jobsets:
```
python -m sagkit.jobset_generator [ET_ratio] [utilization] [jobset_folder] [num_job] [num_instance]
```

The SAG constructor takes the following arguments:
* --jobset_folder: Which folder to read the jobsets. Default is "./jobsets/".
* --constructor_type: What constructor(s) to use to do the construction. Default is "original,extended,hybrid".
* --save_dot: Which folder to save the dot files. Default is "./dotfiles/".
* --save_statistics: Which path to save the statistics results. Default is "./statistics.csv".

Construct SAGs:
```
python -m sagkit.sag_constructor [jobset_folder] [constructor_type] [save_dot] [save_statistics]
```

### Example Usage 1 (Manually type in 1 jobset)
1. Create a folder /example/ in the current working directory.

2. Create a file 'example.txt' in the /example/ folder.

3. Write the following content (Fig. 4 example in our paper) into example.txt.
    ```
    0 2 9 10 20 1 1
    1 2 5 6 25 4 0
    4 5 1 2 25 3 0
    3 6 2 3 25 2 0
    ```
    or write any job you want for each line, in the following format:
    ```
    BCAT WCAT BCET WCET deadline priority ET
    ```
    * BCAT (Best-Case Arrival Time): Earliest arrival time for the job.
    * WCAT (Worst-Case Arrival Time): Latest arrival time for the job.
    * BCET (Best-Case Execution Time): Minimum time required for the job to be executed.
    * WCET (Worst-Case Execution Time): Maximum time required for the work to be executed.
    * deadline: Deadline in absolute time.
    * priority:  A smaller value implies higher priority.
    * ET (Event-Triggered): Whether the job is potentially absent, with 0 being impossible and 1 being possible.

4. Go back to the original working directory. Run the constructor:
    ```
    python -m sagkit.sag_constructor --jobset_folder ./example/
    ```

5. The constructed SAGs will be saved in ./dotfiles/ folder. To visualize, paste the contents of each .dot file to:
    ```
    https://dreampuf.github.io/GraphvizOnline (you may want to access in incognito mode.)
    ```

### Example Usage 2 (Automatically generate 84 jobsets)

1. Generate jobsets:
    ```
    python -m sagkit.jobset_generator --ET_ratio 0,10,15,20,30,40,50,60,70,80,90,100 --utilization 45,50,55,60,65,70,75
    ```

2. Construct SAGs (29 hours on my computer):
    ```
    python -m sagkit.sag_constructor --jobset_folder ./jobsets/ --save_statistics ./statistics.csv
    ```

3. View the statistics in ./statistics.csv.

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

## Test

Install SAGkit from source:
```
git clone https://github.com/RyderCRD/sagkit
```

Change direcotry to ./sagkit (over the /src directory):
```
cd sagkit
```
Run all unit tests:
```
python -m unittest discover tests
```

## Contribute

Contributions are welcome! Please feel free to drop your issues and PRs :)
