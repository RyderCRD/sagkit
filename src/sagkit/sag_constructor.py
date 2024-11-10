"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 21:09:02
LastEditTime: 2024-11-10 00:23:53
FilePath: \\sagkit\\src\\sagkit\\sag_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys
import time
import argparse
import traceback
from tqdm import tqdm
from utils import Job, State
from constructors.extended_constructor import Extended_constructor
from constructors.hybrid_constructor import Hybrid_constructor
from constructors.original_constructor import Original_constructor


def int_or_int_list(value):
    try:
        return int(value)
    except ValueError:
        return [int(i) for i in value.split(",")]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a jobset")
    parser.add_argument(
        "--num_jobsets",
        type=int,
        default=1,
        help="Number of jobsets",
    )
    parser.add_argument(
        "--jobset_folder",
        type=str,
        default="../../tests/",
        help="Path to the jobset folder",
    )
    parser.add_argument(
        "--constructor_type",
        type=int_or_int_list,
        default=1,
        help="Type of SAG constructor",
    )
    args = parser.parse_args()

    for i in tqdm(range(args.num_jobsets)):

        origin_SAG_constructor = Original_constructor(
            header="origin", do_merging=True, do_spliting=False, do_extending=False
        )
        splited_SAG_constructor = Hybrid_constructor(
            header="splited", do_merging=True, do_spliting=True, do_extending=False
        )
        extended_SAG_constructor = Extended_constructor(
            header="extended", do_merging=True, do_spliting=False, do_extending=True
        )

        jobset_path = args.jobset_folder + "jobset_" + f"{i}" + ".txt"
        origin_SAG_constructor.read_jobs(jobset_path)
        splited_SAG_constructor.read_jobs(jobset_path)
        extended_SAG_constructor.read_jobs(jobset_path)

        start_time = time.time()
        origin_SAG_constructor.construct_SAG(do_merging=True, do_spliting=False)
        print("Origin SAG construction time:", time.time() - start_time, "s")
        # origin_SAG_constructor.save_SAG()

        start_time = time.time()
        splited_SAG_constructor.construct_SAG(do_merging=True, do_spliting=True)
        print("Splited SAG construction time:", time.time() - start_time, "s")
        # splited_SAG_constructor.save_SAG()

        start_time = time.time()
        extended_SAG_constructor.construct_SAG(do_merging=True, do_spliting=False)
        print("Extended SAG construction time:", time.time() - start_time, "s")
        # extended_SAG_constructor.save_SAG()
