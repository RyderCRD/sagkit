"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-25 23:07:39
FilePath: \\sagkit\\tests\\constructors\\test_hybrid_constructor.py
Description: Unit tests for the Hybrid_constructor class in src/sagkit/utils/hybrid_constructor.py
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.constructors.hybrid_constructor import Hybrid_constructor


class TestHybridConstructor(unittest.TestCase):

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
        self.constructor = Hybrid_constructor(["hybrid"])

    def test_construct_SAG(self):
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        self.constructor.read_jobs(test_file_path)
        self.constructor.construct_SAG()
        self.assertEqual(len(self.constructor.state_list), 4)
        self.assertEqual(self.constructor.state_list[0].id, 0)
        self.assertEqual(self.constructor.state_list[0].depth, 0)
        self.assertEqual(self.constructor.state_list[0].EFT, 0)
        self.assertEqual(self.constructor.state_list[0].LFT, 0)
        self.assertEqual(self.constructor.state_list[1].id, 1)
        self.assertEqual(self.constructor.state_list[1].depth, 1)
        self.assertEqual(self.constructor.state_list[1].EFT, 4)
        self.assertEqual(self.constructor.state_list[1].LFT, 6)
        self.assertEqual(self.constructor.state_list[2].id, 2)
        self.assertEqual(self.constructor.state_list[2].depth, 2)
        self.assertEqual(self.constructor.state_list[2].EFT, 8)
        self.assertEqual(self.constructor.state_list[2].LFT, 11)
        self.assertEqual(self.constructor.state_list[3].id, 3)
        self.assertEqual(self.constructor.state_list[3].depth, 2)
        self.assertEqual(self.constructor.state_list[3].EFT, 4)
        self.assertEqual(self.constructor.state_list[3].LFT, 6)

    def test_count_execution_scenarios(self):
        self.assertEqual(self.constructor.count_execution_scenarios(), (0, 0))
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        self.constructor.read_jobs(test_file_path)
        self.assertEqual(
            self.constructor.count_execution_scenarios(),
            (1.380211241711606, 1.380211241711606),
        )

    def test_count_idle_time(self):
        self.assertEqual(self.constructor.count_idle_time(), 0)
        test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../test_jobs.txt")
        )
        self.constructor.read_jobs(test_file_path)
        self.constructor.construct_SAG()
        self.assertEqual(self.constructor.count_idle_time(), 0)


if __name__ == "__main__":
    unittest.main()
