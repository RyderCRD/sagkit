"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 17:53:13
LastEditTime: 2024-11-10 13:31:39
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

random.seed(1)


class Jobset_generator:
    def __init__(self, num_ins, ET_ratio, utilization, num_runnable):
        self.num_ins = num_ins
        self.ET_ratio = [ET_ratio] if isinstance(ET_ratio, int) else ET_ratio
        self.utilization = (
            [utilization] if isinstance(utilization, int) else utilization
        )
        self.num_runnable = (
            [num_runnable] if isinstance(num_runnable, int) else num_runnable
        )

    def run(self, output_folder):
        param_combinations = list(
            itertools.product(self.ET_ratio, self.utilization, self.num_runnable)
        )
        num_param_combinations = len(param_combinations)
        for ins in range(self.num_ins):
            with tqdm(
                total=num_param_combinations, desc=f"Instance {ins+1}/{self.num_ins}"
            ) as pbar:
                for i, (ET_ratio, utilization, num_runnable) in enumerate(
                    param_combinations
                ):
                    try:
                        BCAT_list = []
                        WCAT_list = []
                        BCET_list = []
                        WCET_list = []
                        DDL_list = []
                        priority_list = []
                        ET_list = []

                        for j in range(num_runnable):
                            ET_list.append(
                                0 if random.randint(0, 99) < 100 - ET_ratio else 1
                            )
                            BCAT = random.randint(1, 9900)
                            BCAT_list.append(BCAT)
                            WCAT_list.append(BCAT + random.randint(0, 9))
                            BCET = random.randint(2, int(utilization / 5 - 7))
                            BCET_list.append(BCET)
                            WCET_list.append(BCET + random.randint(1, 4))
                            DDL_list.append(10000)
                            priority_list.append(random.randint(1, 10))

                        output_folder = output_folder
                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder)

                        with open(
                            output_folder + "/jobset-"
                            # + f"{i + ins * num_param_combinations}-"
                            + f"{ET_ratio}-" + f"{utilization}" + ".txt",
                            "w",
                        ) as dot_file:
                            for j in range(num_runnable):
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
                        pbar.update(1)
                    except Exception as e:
                        print(e, traceback.format_exc())


def int_or_int_list(value):
    try:
        return int(value)
    except ValueError:
        return [int(i) for i in value.split(",")]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a jobset")
    parser.add_argument(
        "--num_instance",
        type=int,
        default=1,
        help="Number of instances",
    )
    parser.add_argument(
        "--ET_ratio",
        type=int_or_int_list,
        default=15,
        help="Event-triggered ratio",
    )
    parser.add_argument(
        "--utilization",
        type=int_or_int_list,
        default=45,
        help="Utilization",
    )
    parser.add_argument(
        "--num_runnable",
        type=int_or_int_list,
        default=1000,
        help="Number of runnables",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="../../tests",
        help="Output folder path",
    )

    args = parser.parse_args()
    generator = Jobset_generator(
        args.num_instance, args.ET_ratio, args.utilization, args.num_runnable
    )
    generator.run(args.output)
    print("Successfully generated jobsets!")
