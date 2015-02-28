#!/usr/bin/env python3.4

import unittest

from datastructures.python_list import SampleList

class SampleListTest(unittest.TestCase):

    def test_all_functions_roughly_work(self):
        x = SampleList()
        x.append(1)
        x.append(2)
        x.append(4)

        self.assertEqual(x.fill, 3)
        self.assertEqual(x.index(0), 1)
        self.assertEqual(x.index(2), 4)
        self.assertEqual(x.pop(), 4)

    def test_resize(self):
        x = SampleList([1, 2, 3, 4])

        self.assertEqual(x.allocated_length, 4)
        x.append(5)
        self.assertEqual(x.allocated_length, 9)

        # note that range is lazy/generator in python3
        expected = [i for i in range(1, 6)]
        self.assertEqual(x.get_all(), expected)

    def test_edge_cases(self):
        # too lazy to test edge cases
        pass
