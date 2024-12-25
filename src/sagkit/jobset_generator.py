"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 17:53:13
LastEditTime: 2024-12-25 21:04:53
FilePath: \\sagkit\\src\\sagkit\\jobset_generator.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import random
import argparse
import traceback
import itertools
from tqdm import tqdm

random.seed(2024)


class Jobset_generator:
    def __init__(self, num_ins, ET_ratio, utilization, num_job):
        self.num_ins = num_ins
        self.ET_ratio = [ET_ratio] if isinstance(ET_ratio, int) else ET_ratio
        self.utilization = (
            [utilization] if isinstance(utilization, int) else utilization
        )
        self.num_job = [num_job] if isinstance(num_job, int) else num_job

    def run(self, jobset_folder):
        param_combinations = list(
            itertools.product(self.ET_ratio, self.utilization, self.num_job)
        )
        num_param_combinations = len(param_combinations)
        for ins in range(self.num_ins):
            with tqdm(
                total=num_param_combinations, desc=f"Instance {ins+1}/{self.num_ins}"
            ) as pbar:
                for _, (ET_ratio, utilization, num_job) in enumerate(
                    param_combinations
                ):
                    try:
                        # Initialize lists
                        BCAT_list = []
                        WCAT_list = []
                        BCET_list = []
                        WCET_list = []
                        DDL_list = []
                        priority_list = []
                        ET_list = []

                        # Generate jobset
                        for j in range(num_job):
                            # Best-case arrival time
                            BCAT = random.randint(1, 9990)
                            BCAT_list.append(BCAT)
                            # Worst-case arrival time
                            WCAT_list.append(BCAT + random.randint(0, 9))
                            # Best-case execution time
                            BCET = random.randint(2, int(utilization / 5 - 7))
                            BCET_list.append(BCET)
                            # Worst-case execution time
                            WCET_list.append(BCET + random.randint(1, 4))
                            # Deadline
                            DDL_list.append(10000)
                            # Priority
                            priority_list.append(random.randint(1, 10))
                            # Hybrid
                            ET_list.append(
                                0 if random.randint(0, 99) < 100 - ET_ratio else 1
                            )

                        # Create output folder if not exists
                        jobset_folder = jobset_folder
                        if not os.path.exists(jobset_folder):
                            os.makedirs(jobset_folder)

                        # Write to file
                        with open(
                            jobset_folder
                            + "/jobset-"
                            + f"{utilization}-"
                            + f"{ET_ratio}"
                            + f"-{num_job}-"
                            + f"{ins+1}"
                            + ".txt",
                            "w",
                        ) as dot_file:
                            for j in range(num_job):
                                dot_file.write(
                                    str(BCAT_list[j])
                                    + " "
                                    + str(WCAT_list[j])
                                    + " "
                                    + str(BCET_list[j])
                                    + " "
                                    + str(WCET_list[j])
                                    + " "
                                    + str(DDL_list[j])
                                    + " "
                                    + str(priority_list[j])
                                    + " "
                                    + str(ET_list[j])
                                    + "\n"
                                )

                        # Update progress bar
                        pbar.update(1)

                    # Catch exceptions
                    except Exception as e:
                        print(e, traceback.format_exc())


def int_or_int_list(value):
    try:
        return int(value)
    except ValueError:
        return [int(i) for i in value.split(",")]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate jobsets")
    parser.add_argument(
        "--ET_ratio",
        type=int_or_int_list,
        default=15,
        help="What percentage of jobs are ET. Default is 15.",
    )
    parser.add_argument(
        "--utilization",
        type=int_or_int_list,
        default=45,
        help="What percentage of the macrocycle is the expectation of the total execution time. Default is 45.",
    )
    parser.add_argument(
        "--jobset_folder",
        type=str,
        default="./jobsets/",
        help='Which folder to save the jobsets. Default is "./jobsets/".',
    )
    parser.add_argument(
        "--num_job",
        type=int_or_int_list,
        default=1000,
        help="How many jobs to include in each job set. Default is 1000.",
    )
    parser.add_argument(
        "--num_instance",
        type=int,
        default=1,
        help="How many jobsets to generate for each set of parameter combinations. Default is 1.",
    )

    args = parser.parse_args()
    generator = Jobset_generator(
        args.num_instance, args.ET_ratio, args.utilization, args.num_job
    )
    generator.run(args.jobset_folder)
    print("Successfully generated jobsets!")
