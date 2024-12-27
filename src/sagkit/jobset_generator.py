"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 17:53:13
LastEditTime: 2024-12-28 01:49:23
FilePath: \\sagkit\\src\\sagkit\\jobset_generator.py
Description: Generate jobsets for the SAG construction algorithms.
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import random
import argparse
import traceback
import itertools
from tqdm import tqdm
from sagkit.utils.job import Job

random.seed(2024)


class Jobset_generator:
    def __init__(self, num_ins, ET_ratio, utilization, num_job):
        self.num_ins = num_ins
        self.ET_ratio = [ET_ratio] if isinstance(ET_ratio, int) else ET_ratio
        self.utilization = (
            [utilization] if isinstance(utilization, int) else utilization
        )
        self.num_job = [num_job] if isinstance(num_job, int) else num_job

    # Generate jobs
    def generate_jobs(self, num_job, utilization, ET_ratio):
        jobs = []
        for j in range(num_job):
            # Best-case arrival time
            BCAT = random.randint(1, 9990)
            # Worst-case arrival time
            WCAT = BCAT + random.randint(0, 9)
            # Best-case execution time
            BCET = random.randint(2, int(utilization / 5 - 7))
            # Worst-case execution time
            WCET = BCET + random.randint(1, 4)
            # Deadline
            DDL = 10000
            # Priority
            priority = random.randint(1, 10)
            # Hybrid
            ET = 0 if random.randint(0, 99) < 100 - ET_ratio else 1
            jobs.append(Job(j, BCAT, WCAT, BCET, WCET, DDL, priority, ET))
        return jobs

    # Generate jobsets
    def generate(self, jobset_folder):
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
                        # Generate jobs
                        jobs = self.generate_jobs(num_job, utilization, ET_ratio)

                        # Create output folder if not exists
                        jobset_folder = jobset_folder
                        if not os.path.exists(jobset_folder):
                            os.makedirs(jobset_folder)

                        # Write to file
                        file_path = f"{jobset_folder}/jobset-{utilization}-{ET_ratio}-{num_job}-{ins+1}.txt"
                        with open(file_path, "w") as jobset_file:
                            for job in jobs:
                                jobset_file.write(str(job) + "\n")

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
    generator.generate(args.jobset_folder)
    print("Successfully generated jobsets!")
