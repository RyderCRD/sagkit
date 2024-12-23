"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-12-22 22:28:41
FilePath: \\sagkit\\src\\sagkit\\sag_constructor.py
Description: 
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
    def __init__(self):
        self.jobset_folder = "./jobsets/"
        self.constructor_type = ["original", "extended", "hybrid"]
        self.save_dot = False

    def construct(self):
        # Read jobsets and sort them
        jobset_folder = self.jobset_folder
        jobset_paths = os.listdir(jobset_folder)
        jobset_paths.sort(
            key=lambda x: (int(x.split("-")[1]), int(x.split("-")[2][:-4]))
        )
        print(jobset_paths)

        # Remove old statistics file if it exists
        if os.path.exists("../../statistics.csv"):
            os.remove("../../statistics.csv")

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
                "Number of actual execution scenarios",
                "Number of analyzed execution scenarios",
                "Valid ratio of analyzed SAG:",
                "Maximum width",
                "Maximum idle time",
                "Construction time (ns)",
            ]

            with open("../../statistics.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(type)
                writer.writerow(header)

            for jobset_path in tqdm(jobset_paths):
                utilization = int(jobset_path.split("-")[1])
                ET_ratio = int(jobset_path.split("-")[2][:-4])
                jobset_path = jobset_folder + jobset_path

                if constructor_type == "original":
                    SAG_constructor = Original_constructor(
                        header=constructor_type, do_merging=True
                    )
                elif constructor_type == "extended":
                    SAG_constructor = Extended_constructor(
                        header=constructor_type, do_merging=True
                    )
                elif constructor_type == "hybrid":
                    SAG_constructor = Hybrid_constructor(
                        header=constructor_type, do_merging=True
                    )
                else:
                    print(constructor_type)
                    raise ValueError("Invalid constructor type!")

                # jobset_path = args.jobset_folder + "jobset_" + f"{i}" + ".txt"
                SAG_constructor.read_jobs(jobset_path)

                start_time = time.process_time_ns()
                SAG_constructor.construct_SAG(do_merging=True)
                end_time = time.process_time_ns()
                # print("SAG construction time:", time.time() - start_time, "s")
                actual_es_counter, analyzed_es_counter, max_width, idle_time = (
                    SAG_constructor.do_statistics()
                )

                with open("../../statistics.csv", "a", newline="") as csvfile:
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

                if self.save_dot:
                    SAG_constructor.save_SAG()


def str_list(value):
    if len(value.split(",")) == 1:
        return [str(value)]
    return [str(i) for i in value.split(",")]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a jobset")
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
        type=bool,
        default=False,
        help="Whether to save SAG as dot file",
    )
    args = parser.parse_args()

    sag_constructor = SAG_constructor()
    sag_constructor.jobset_folder = args.jobset_folder
    sag_constructor.constructor_type = args.constructor_type
    sag_constructor.save_dot = args.save_dot
    sag_constructor.construct()
