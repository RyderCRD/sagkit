"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-22 20:23:51
FilePath: \\sagkit\\tests\\constructors\\test_extended_constructor.py
Description: Unit tests for the Extended_constructor class in src/sagkit/utils/extended_constructor.py
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.constructors.extended_constructor import Extended_constructor


class TestExtendedConstructor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        test_jobs = open(test_file_path, "w")
        test_jobs.write("1 2 3 4 5 6 0\n")
        test_jobs.write("2 3 4 5 6 7 1\n")
        test_jobs.close()

    @classmethod
    def tearDownClass(cls):
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        os.remove(test_file_path)

    def setUp(self):
        self.constructor = Extended_constructor(["extended"], True)

    def test_read_jobs(self):
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        self.constructor.read_jobs(test_file_path)
        self.assertEqual(len(self.constructor.job_list), 2)
        self.assertEqual(self.constructor.job_list[0].id, 0)
        self.assertEqual(self.constructor.job_list[0].BCAT, 1)
        self.assertEqual(self.constructor.job_list[0].WCAT, 2)
        self.assertEqual(self.constructor.job_list[0].BCET, 3)
        self.assertEqual(self.constructor.job_list[0].WCET, 4)
        self.assertEqual(self.constructor.job_list[0].BCET_REC, 3)
        self.assertEqual(self.constructor.job_list[0].WCET_REC, 4)
        self.assertEqual(self.constructor.job_list[0].DDL, 5)
        self.assertEqual(self.constructor.job_list[0].priority, 6)
        self.assertFalse(self.constructor.job_list[0].is_ET)

        self.assertEqual(self.constructor.job_list[1].id, 1)
        self.assertEqual(self.constructor.job_list[1].BCAT, 2)
        self.assertEqual(self.constructor.job_list[1].WCAT, 3)
        self.assertEqual(self.constructor.job_list[1].BCET, 0)
        self.assertEqual(self.constructor.job_list[1].WCET, 5)
        self.assertEqual(self.constructor.job_list[1].BCET_REC, 4)
        self.assertEqual(self.constructor.job_list[1].WCET_REC, 5)
        self.assertEqual(self.constructor.job_list[1].DDL, 6)
        self.assertEqual(self.constructor.job_list[1].priority, 7)
        self.assertTrue(self.constructor.job_list[1].is_ET)

    def test_count_execution_scenarios(self):
        self.assertEqual(self.constructor.count_execution_scenarios(), (0, 0))
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        self.constructor.read_jobs(test_file_path)
        self.assertEqual(
            self.constructor.count_execution_scenarios(),
            (1.380211241711606, 1.6812412373755872),
        )

    def test_count_idle_time(self):
        self.assertEqual(self.constructor.count_idle_time(), 0)
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        self.constructor.read_jobs(test_file_path)
        self.assertEqual(
            self.constructor.count_execution_scenarios(),
            (1.380211241711606, 1.6812412373755872),
        )
        self.assertEqual(self.constructor.count_idle_time(), 0)


if __name__ == "__main__":
    unittest.main()
