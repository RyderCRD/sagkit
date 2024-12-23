"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-22 22:18:10
FilePath: \\sagkit\\tests\\test_jobset_generator.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.jobset_generator import Jobset_generator


class TestJobsetGenerator(unittest.TestCase):

    # Make sure the folder ./temp_jobsets/ does not exist
    @classmethod
    def setUpClass(cls):
        if os.path.exists("./temp_jobsets/"):
            raise Exception("The folder ./temp_jobsets/ already exists")

    # Remove the folder ./temp_jobsets/ and its content
    @classmethod
    def tearDownClass(cls):
        jobset_paths = os.listdir("./temp_jobsets/")
        for jobset_path in jobset_paths:
            os.remove(f"./temp_jobsets/{jobset_path}")
        os.removedirs("./temp_jobsets/")

    # Test the jobset generator
    def test_jobset_generator(self):
        num_ins = 1
        ET_ratio = [0, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        utilization = [45, 50, 55, 60, 65, 70, 75]
        num_runnable = 1000
        output_folder = "./temp_jobsets/"
        jobset_generator = Jobset_generator(
            num_ins, ET_ratio, utilization, num_runnable
        )
        jobset_generator.run(output_folder)
        self.assertTrue(os.path.exists(output_folder))

        jobset_folder = output_folder
        jobset_paths = os.listdir(jobset_folder)
        jobset_paths.sort(
            key=lambda x: (int(x.split("-")[1]), int(x.split("-")[2][:-4]))
        )

        self.assertEqual(len(jobset_paths), 84)
        self.assertEqual(jobset_paths[0], "jobset-45-0.txt")
        self.assertEqual(jobset_paths[1], "jobset-45-10.txt")
        self.assertEqual(jobset_paths[2], "jobset-45-15.txt")
        self.assertEqual(jobset_paths[3], "jobset-45-20.txt")
        self.assertEqual(jobset_paths[4], "jobset-45-30.txt")
        self.assertEqual(jobset_paths[5], "jobset-45-40.txt")
        self.assertEqual(jobset_paths[6], "jobset-45-50.txt")
        self.assertEqual(jobset_paths[7], "jobset-45-60.txt")
        self.assertEqual(jobset_paths[8], "jobset-45-70.txt")
        self.assertEqual(jobset_paths[9], "jobset-45-80.txt")
        self.assertEqual(jobset_paths[10], "jobset-45-90.txt")
        self.assertEqual(jobset_paths[11], "jobset-45-100.txt")
        self.assertEqual(jobset_paths[12], "jobset-50-0.txt")
        self.assertEqual(jobset_paths[-1], "jobset-75-100.txt")


if __name__ == "__main__":
    unittest.main()
