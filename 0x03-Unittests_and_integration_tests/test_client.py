#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
import client


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("case_google", "google", {"login": "google", "id": 1}),
        ("case_abc", "abc", {"login": "abc", "id": 2})
    ])
    @patch("client.get_json")
    def test_org(self, _, org_name, expected_response, mock_get_json):
        """Test that GithubOrgClient.org returns the expected org data."""
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), expected_response)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected repos_url from mocked org"""
        test_url = "https://api.github.com/orgs/test_org/repos"
        payload = {"repos_url": test_url}

        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test_org")

            result = client._public_repos_url
            self.assertEqual(result, test_url)
            mock_org.assert_called_once()


if __name__ == "__main__":
    unittest.main()
