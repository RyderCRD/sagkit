"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-26 00:02:55
FilePath: \\sagkit\\tests\\schedulers\\test_fp_scheduler.py
Description: Unit tests for FP_Scheduler class in src/sagkit/schedulers/fp_scheduler.py
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from sagkit.utils.job import Job
from sagkit.schedulers.fp_scheduler import FP_Scheduler


class TestFPScheduler(unittest.TestCase):

    # Initialize the job objects
    def setUp(self):
        self.job_1 = Job(1, 0, 0, 1, 1, 1, 1, 1)
        self.job_2 = Job(2, 0, 0, 1, 1, 1, 2, 1)
        self.job_3 = Job(3, 0, 0, 1, 1, 2, 1, 1)
        self.job_4 = Job(4, 0, 0, 1, 1, 2, 2, 1)

    # Test the compare method
    def test_compare(self):
        self.assertTrue(FP_Scheduler.compare(self.job_1, self.job_2))
        self.assertFalse(FP_Scheduler.compare(self.job_1, self.job_3))
        self.assertTrue(FP_Scheduler.compare(self.job_1, self.job_4))
        self.assertFalse(FP_Scheduler.compare(self.job_2, self.job_3))
        self.assertFalse(FP_Scheduler.compare(self.job_2, self.job_4))
        self.assertTrue(FP_Scheduler.compare(self.job_3, self.job_4))


if __name__ == "__main__":
    unittest.main()
