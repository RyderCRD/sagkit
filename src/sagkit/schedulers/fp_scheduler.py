"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 17:18:54
LastEditTime: 2024-12-22 20:04:38
FilePath: \\sagkit\\src\\sagkit\\schedulers\\fp_scheduler.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)


class FP_Scheduler:

    # Compare the priority of two jobs
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
