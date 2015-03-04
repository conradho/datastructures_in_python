#!/usr/bin/env python3.4

import unittest
from unittest.mock import patch

from datastructures.python_dict import (
    SampleDict,
    KeyAlreadyExistsInDictError,
    KeyDoesNotExistInDictError,
)

class SampleDictTest(unittest.TestCase):

    def setUp(self):
        self.sample_dict = SampleDict()
        self.sample_dict.insert(b'a', 2)

    def test_get_value_works(self):
        self.assertEqual(self.sample_dict.get_value(b'a'), 2)

    def test_insert_works(self):
        self.sample_dict.insert(b'b', 3)
        self.assertEqual(self.sample_dict.get_value(b'b'), 3)

    def test_pop_works(self):
        self.assertEqual(self.sample_dict.pop(b'a'), 2)

    def test_errors_if_no_key(self):
        with self.assertRaises(KeyDoesNotExistInDictError):
            self.sample_dict.get_value(b'b')

    def test_errors_on_same_key(self):
        with self.assertRaises(KeyAlreadyExistsInDictError):
            self.sample_dict.insert(b'a', 3)

    def test_does_not_error_on_same_hash_diff_key(self):
        mock_hash = self.sample_dict._hash(b'a')
        with patch(
            'datastructures.python_dict.SampleDict._hash',
            lambda self, key: mock_hash
        ):
            self.sample_dict.insert(b'b', 3)
            self.assertEqual(
                self.sample_dict.get_value(b'b'),
                3
            )
            # check that it did not overwrite 'a'
            self.assertEqual(
                self.sample_dict.get_value(b'a'),
                2
            )
            
    def test_can_insert_a_lot(self):
        for i in range(90):
            # ord('a') == 97 so if we try to insert 97 we actually get a KeyAlreadyExistsInDictError
            key = bytes(chr(i), "UTF-8")
            self.sample_dict.insert(key, i)

    def test_dict_resizes_correctly(self):
        self.sample_dict._resize()
        self.assertEqual(
            len(self.sample_dict.c_dict_array),
            32
        )
        self.assertEqual(
            self.sample_dict.allocated_length,
            32
        )

