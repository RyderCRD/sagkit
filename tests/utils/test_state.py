"""
Author: Ruide Cao (caoruide123@gmail.com)
Date: 2024-12-22 16:32:13
LastEditTime: 2024-12-22 20:22:27
FilePath: \\sagkit\\tests\\utils\\test_state.py
Description: Unit tests for State class in src/sagkit/utils/state.py
Copyright (c) 2024 by Ruide Cao, All Rights Reserved. 
"""

import os
import sys
import unittest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from sagkit.utils.state import State


class TestState(unittest.TestCase):

    def test_is_leaf(self):
        state = State(1, 1, 1, [])
        self.assertTrue(state.is_leaf())

    def test_str(self):
        state = State(1, 1, 1, [])
        self.assertEqual(str(state), "State 1 [1, 1]")

    def test_init(self):
        state = State(1, 1, 1, [])
        self.assertEqual(state.id, 1)
        self.assertEqual(state.EFT, 1)
        self.assertEqual(state.LFT, 1)
        self.assertEqual(state.depth, 0)
        self.assertEqual(state.job_path, [])
        self.assertEqual(state.next_jobs, [])
        self.assertEqual(state.next_states, [])


if __name__ == "__main__":
    unittest.main()
