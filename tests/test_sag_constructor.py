"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-25 20:01:05
FilePath: \\sagkit\\tests\\test_sag_constructor.py
Description: 
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.sag_constructor import SAG_constructor


class TestSAGConstructor(unittest.TestCase):

    def test_constructor(self):
        sag_constructor = SAG_constructor()
        self.assertEqual(sag_constructor.jobset_folder, "./jobsets/")
        self.assertEqual(
            sag_constructor.constructor_type, ["original", "extended", "hybrid"]
        )
        self.assertIsNotNone(sag_constructor.save_dot)


if __name__ == "__main__":
    unittest.main()
