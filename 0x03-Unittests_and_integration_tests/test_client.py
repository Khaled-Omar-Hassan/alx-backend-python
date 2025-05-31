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

     @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names from payload"""
        # Mock JSON payload returned by get_json
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        # Mock URL that would be returned by _public_repos_url
        test_url = "https://api.github.com/orgs/test_org/repos"

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = test_url

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()
