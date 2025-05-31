#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
import client


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch.object(client, "get_json")
    def test_org(self,  org, mock_get_json):
        mock_get_json.return_value = {"login": org}
        client_instance = client.GithubOrgClient(org)
        self.assertEqual(client_instance.org, {"login": org})
        mock_get_json.assert_called_once_with(
            client.GithubOrgClient.ORG_URL.format(org=org)
        )


if __name__ == "__main__":
    unittest.main()
