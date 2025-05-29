#!/usr/bin/env python3
"""Module For Testing Utils"""

import unittest
from utils import access_nested_map
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    
    @parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, map, seq, expected):
        self.assertEqual(access_nested_map(map, seq), expected)



    @parameterized.expand([
      ({}, ("a",)),
      ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, map, seq):
       self.assertRaises(KeyError, access_nested_map, map, seq)
       




if __name__ == "__main__":
  unittest.main()
