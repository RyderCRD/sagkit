"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 17:18:54
LastEditTime: 2024-12-25 23:53:48
FilePath: \\sagkit\\src\\sagkit\\schedulers\\fp_scheduler.py
Description: Scheduler for the Fixed-Priority (FP) algorithm.
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys


class FP_Scheduler:

    # Fixed-Priority (FP) algorithm
    # Return True if job1 is prior to job2
    @staticmethod
    def compare(job1, job2) -> bool:
        try:
            return job1.priority < job2.priority
        except Exception as e:
            print(e)
            if e == AttributeError:
                sys.exit("Scheduler Error! Jobs do not have priority attribute!")
            sys.exit("Scheduler Error! Unknown error!")
