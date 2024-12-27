"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-12-28 01:28:20
FilePath: \\sagkit\\src\\sagkit\\sag_constructor.py
Description: Construct SAGs with specified construction algorithms.
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import csv
import time
import argparse
from tqdm import tqdm
from sagkit.constructors.extended_constructor import Extended_constructor
from sagkit.constructors.hybrid_constructor import Hybrid_constructor
from sagkit.constructors.original_constructor import Constructor as Original_constructor


class SAG_constructor:
    def __init__(
        self,
        jobset_folder="./jobsets/",
        constructor_type=["original", "extended", "hybrid"],
        save_dot="./dotfiles/",
        save_statistics="./statistics.csv",
    ):
        self.jobset_folder = jobset_folder
        self.constructor_type = constructor_type
        self.save_dot = save_dot
        self.save_statistics = save_statistics

    # Construct SAGs with specified construction algorithms
    def construct(self):

        # Read all jobsets in the jobset folder
        jobset_folder = self.jobset_folder
        jobset_paths = os.listdir(jobset_folder)

        # Sort jobsets by utilization, ET_ratio, num_runnable, and instance number
        try:
            jobset_paths.sort(
                key=lambda x: (
                    int(x.split("-")[1]),
                    int(x.split("-")[2]),
                    int(x.split("-")[3]),
                    int(x.split("-")[4][:-4]),
                )
            )
            print(jobset_paths)
        # In case jobset file names are not in the automatic format, do not sort
        except IndexError:
            pass

        # Remove old statistics file if it exists
        if self.save_statistics and os.path.exists(self.save_statistics):
            os.remove(self.save_statistics)

        # Construct SAGs with different construction algorithms
        for constructor_type in self.constructor_type:
            print(
                "########## Constructing SAG with :",
                constructor_type,
                "construction algorithm ##########",
            )

            type = [constructor_type]

            header = [
                "Utilization",
                "ET_Ratio",
                "Number of States",
                "Number of actual execution scenarios (log10)",
                "Number of analyzed execution scenarios (log10)",
                "Valid ratio of analyzed SAG (log10)",
                "Maximum width",
                "Maximum idle time",
                "Construction time (ns)",
            ]

            # Write header to statistics file
            if self.save_statistics:
                with open(self.save_statistics, "a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(type)
                    writer.writerow(header)

            # Construct SAGs on each jobset
            for jobset_path in tqdm(jobset_paths):
                if len(jobset_path.split("-")) > 1:
                    utilization = int(jobset_path.split("-")[1])
                    ET_ratio = int(jobset_path.split("-")[2])
                    runnable_number = int(jobset_path.split("-")[3])
                    instance_number = int(jobset_path.split("-")[4][:-4])
                else:
                    self.save_statistics = False

                jobset_path = jobset_folder + jobset_path

                if constructor_type == "original":
                    SAG_constructor = Original_constructor(header=constructor_type)
                elif constructor_type == "extended":
                    SAG_constructor = Extended_constructor(header=constructor_type)
                elif constructor_type == "hybrid":
                    SAG_constructor = Hybrid_constructor(header=constructor_type)
                else:
                    print(constructor_type)
                    raise ValueError("Invalid constructor type!")

                # jobset_path = args.jobset_folder + "jobset_" + f"{i}" + ".txt"
                SAG_constructor.read_jobs(jobset_path)

                start_time = time.process_time_ns()
                SAG_constructor.construct_SAG()
                end_time = time.process_time_ns()
                # print("SAG construction time:", time.time() - start_time, "s")
                actual_es_counter, analyzed_es_counter, max_width, idle_time = (
                    SAG_constructor.do_statistics()
                )

                # Write statistics to statistics file
                if self.save_statistics:
                    with open(self.save_statistics, "a", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(
                            [
                                utilization,
                                ET_ratio,
                                len(SAG_constructor.state_list),
                                actual_es_counter,
                                analyzed_es_counter,
                                # pow(10, analyzed_es_counter - actual_es_counter),
                                analyzed_es_counter - actual_es_counter,
                                max_width,
                                idle_time,
                                end_time - start_time,
                            ]
                        )

                # Save SAG as dot file
                if self.save_dot:
                    if not os.path.exists(self.save_dot):
                        os.makedirs(self.save_dot)
                    SAG_constructor.save_SAG(self.save_dot, jobset_path.split("/")[-1])


def str_list(value):
    if len(value.split(",")) == 1:
        return [str(value)]
    return [str(i) for i in value.split(",")]


# Main function
if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description="Construct SAGs")
    parser.add_argument(
        "--jobset_folder",
        type=str,
        default="./jobsets/",
        help="Path to the jobset folder",
    )
    parser.add_argument(
        "--constructor_type",
        type=str_list,
        default="original,extended,hybrid",  # Original, Extended, Hybrid
        help="Type of SAG constructor",
    )
    parser.add_argument(
        "--save_dot",
        type=str,
        default="./dotfiles/",
        help="Whether to save SAG as dot file",
    )
    parser.add_argument(
        "--save_statistics",
        type=str,
        default="",
        help="Where to save the statistics file",
    )
    args = parser.parse_args()

    # Construct SAGs
    sag_constructor = SAG_constructor(
        args.jobset_folder, args.constructor_type, args.save_dot, args.save_statistics
    )
    sag_constructor.construct()
