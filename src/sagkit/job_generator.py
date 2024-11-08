'''
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-11-05 17:53:13
LastEditTime: 2024-11-08 12:08:09
FilePath: \sagkit\src\sagkit\job_generator.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
'''
import os
import random
import argparse

class JobsetGenerator:
    def __init__(self, seed, num_ins, ET_ratio, utilization, num_runnable):
        random.seed(seed)
        self.num_ins = num_ins
        self.ET_ratio = ET_ratio
        self.utilization = utilization
        self.num_runnable = num_runnable
        
    def run(self, output_folder):
        for ins in range(self.num_ins):
            BCAT_list = []
            WCAT_list = []
            BCET_list = []
            WCET_list = []
            DDL_list = []
            priority_list = []
            ET_list = []

            for i in range(self.num_runnable):
                ET_list.append(0 if random.randint(0, 99) < 100-self.ET_ratio else 1)
                BCAT = random.randint(1, 9900)
                BCAT_list.append(BCAT)
                WCAT_list.append(BCAT + random.randint(0, 9))
                BCET = random.randint(2, int(self.utilization/5-7))
                BCET_list.append(BCET)
                WCET_list.append(BCET + random.randint(1, 4))
                DDL_list.append(10000)
                priority_list.append(random.randint(1, 10))

            test_folder = output_folder
            if not os.path.exists(test_folder):
                os.makedirs(test_folder)
                
            with open(test_folder + "/generate_result.txt","w") as dot_file:
                for i in range(self.num_runnable):
                    dot_file.write(str(BCAT_list[i]) + ' ' + str(WCAT_list[i]) + ' ' + str(BCET_list[i]) + ' ' + str(WCET_list[i]) + \
                        ' ' + str(DDL_list[i]) + ' ' + str(priority_list[i]) + ' ' + str(ET_list[i]) + '\n')
            print("Generate input file successfully!")
            print("U = ", sum(WCET_list)/10000)

def int_or_int_list(value):
    try:
        return int(value)
    except ValueError:
        return [int(i) for i in value.split(',')]
     
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a jobset")
    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        help="random seed",
    )
    parser.add_argument(
        "--num_ins",
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
        type=int,
        default=1000,
        help="Number of runnables",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./tests",
        help="Output folder path",
    )

    args = parser.parse_args()
    generator = JobsetGenerator(
        args.seed,
        args.num_ins,
        args.ET_ratio,
        args.utilization,
        args.num_runnable
    )
    generator.run(args.output)