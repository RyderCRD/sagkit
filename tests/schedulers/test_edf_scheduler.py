"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-22 20:23:22
FilePath: \\sagkit\\tests\\schedulers\\test_edf_scheduler.py
Description: Unit tests for EDFScheduler class in src/sagkit/schedulers/edf_scheduler.py
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.utils.job import Job
from sagkit.schedulers.edf_scheduler import EDF_Scheduler


class TestEDFScheduler(unittest.TestCase):

    def setUp(self):
        self.job_1 = Job(1, 0, 0, 1, 1, 1, 1, 1)
        self.job_2 = Job(2, 0, 0, 1, 1, 1, 2, 1)
        self.job_3 = Job(3, 0, 0, 1, 1, 2, 1, 1)
        self.job_4 = Job(4, 0, 0, 1, 1, 2, 2, 1)

    def test_compare(self):
        self.assertTrue(EDF_Scheduler.compare(self.job_1, self.job_2))
        self.assertTrue(EDF_Scheduler.compare(self.job_1, self.job_3))
        self.assertTrue(EDF_Scheduler.compare(self.job_1, self.job_4))
        self.assertTrue(EDF_Scheduler.compare(self.job_2, self.job_3))
        self.assertTrue(EDF_Scheduler.compare(self.job_2, self.job_4))
        self.assertTrue(EDF_Scheduler.compare(self.job_3, self.job_4))


if __name__ == "__main__":
    unittest.main()
