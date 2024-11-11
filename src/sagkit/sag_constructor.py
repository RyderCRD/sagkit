"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-11-12 00:27:11
FilePath: \\sagkit\\src\\sagkit\\sag_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import csv
import time
import argparse
from tqdm import tqdm
from constructors.extended_constructor import Extended_constructor
from constructors.hybrid_constructor import Hybrid_constructor
from constructors.original_constructor import Constructor as Original_constructor


def str_list(value):
    if len(value.split(",")) == 1:
        return [str(value)]
    return [str(i) for i in value.split(",")]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a jobset")
    # parser.add_argument(
    #     "--num_jobsets",
    #     type=int,
    #     default=1,
    #     help="Number of jobsets",
    # )
    parser.add_argument(
        "--jobset_folder",
        type=str,
        default="../../tests/",
        help="Path to the jobset folder",
    )
    parser.add_argument(
        "--constructor_type",
        type=str_list,
        default="original,extended,hybrid",  # Original, Extended, Hybrid
        help="Type of SAG constructor",
    )
    args = parser.parse_args()

    jobset_folder = args.jobset_folder
    jobset_paths = os.listdir(jobset_folder)
    jobset_paths.sort(key=lambda x: (int(x.split("-")[1]), int(x.split("-")[2][:-4])))
    print(jobset_paths)

    for constructor_type in args.constructor_type:
        print(
            "########## Constructing SAG with :",
            constructor_type,
            " construction algorithm ##########",
        )

        type = [constructor_type]

        header = [
            "ET_Ratio",
            "Utilization",
            "Number of States",
            "Number of execution scenarios",
            "Number of non-ET execution scenarios",
            "Valid ratio of non-ET SAG:",
            "Maximum width",
            "Maximum waste idle time",
            "Construction time",
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

            start_time = time.process_time()
            SAG_constructor.construct_SAG(do_merging=True)
            # print("SAG construction time:", time.time() - start_time, "s")
            ET_es_counter, non_ET_es_counter, max_width, waste_time = (
                SAG_constructor.do_statistics()
            )
            end_time = time.process_time()

            with open("../../statistics.csv", "a", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    [
                        ET_ratio,
                        utilization,
                        len(SAG_constructor.state_list),
                        ET_es_counter,
                        non_ET_es_counter,
                        pow(10, non_ET_es_counter - ET_es_counter),
                        max_width,
                        waste_time,
                        end_time - start_time,
                    ]
                )

            # SAG_constructor.save_SAG()
