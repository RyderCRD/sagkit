"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-22 20:23:10
FilePath: \\sagkit\\tests\\utils\\test_job.py
Description: Unit tests for State class in src/sagkit/utils/state.py
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.utils.job import Job


class TestJob(unittest.TestCase):

    def setUp(self):
        self.job = Job(1, 1, 1, 1, 1, 1, 1, 1)

    def test_set_to_non_triggered(self):
        self.assertEqual(self.job.BCET, 1)
        self.assertEqual(self.job.WCET, 1)
        self.job.set_to_non_triggered()
        self.assertEqual(self.job.BCET, 0)
        self.assertEqual(self.job.WCET, 0)

    def test_set_to_triggered(self):
        self.job.set_to_non_triggered()
        self.job.set_to_triggered()
        self.assertEqual(self.job.BCET, 1)
        self.assertEqual(self.job.WCET, 1)

    def test_is_priority_eligible(self):
        future_jobs = [Job(2, 2, 2, 2, 2, 2, 2, 2)]
        self.assertTrue(self.job.is_priority_eligible(future_jobs, 1))

    def test_is_potentially_next(self):
        future_jobs = [Job(2, 2, 2, 2, 2, 2, 2, 2)]
        self.assertTrue(self.job.is_potentially_next(future_jobs, 1, 1))


if __name__ == "__main__":
    unittest.main()
