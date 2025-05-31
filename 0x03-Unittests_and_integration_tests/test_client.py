#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient class."""

    @patch("client.get_json")
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    def test_org(self, mock_get_json, org):
        """Test that GitHubOrgClient.org returns the expected dict and calls get_json once."""
        # Arrange: make get_json pretend to return {"login": org}
        mock_get_json.return_value = {"login": org}

        # Act: instantiate and access the .org property
        client = GithubOrgClient(org)
        result = client.org  # <-- this calls get_json(...) behind the scenes

        # Assert: .org must return the same dict
        self.assertEqual(result, {"login": org})

        # And get_json must have been called exactly once with the correct URL
        expected_url = GithubOrgClient.ORG_URL.format(org=org)
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
