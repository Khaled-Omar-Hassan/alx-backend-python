#!/usr/bin/env python3
"""Module For Testing Utils"""

import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch



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
       


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch("utils.requests.get")
    def test_get_json(self, url, data, mock_request_get):
      mock_request_get.return_value.json.return_value = data

      self.assertEqual(get_json(url), data)
      mock_request_get.assert_called_once_with(url)



class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
          
        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()
            call1 = obj.a_property
            call2 = obj.a_property
            self.assertEqual(call1, 42)
            self.assertEqual(call2, 42)
            mock_method.assert_called_once()
            


    




if __name__ == "__main__":
  unittest.main()
