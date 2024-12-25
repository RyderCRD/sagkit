"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 02:14:46
LastEditTime: 2024-12-25 23:53:42
FilePath: \\sagkit\\src\\sagkit\\schedulers\\edf_scheduler.py
Description: Scheduler for the Earliest Deadline First (EDF) algorithm.
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import sys


class EDF_Scheduler:

    # Earliest Deadline First (EDF) algorithm
    # Return True if job1 is prior to job2
    @staticmethod
    def compare(job1, job2) -> bool:
        try:
            if job1.DDL == job2.DDL:
                return job1.priority < job2.priority
            return job1.DDL < job2.DDL
        except Exception as e:
            print(e)
            if e == AttributeError:
                sys.exit("Scheduler Error! Jobs do not have priority attribute!")
            sys.exit("Scheduler Error! Unknown error!")
