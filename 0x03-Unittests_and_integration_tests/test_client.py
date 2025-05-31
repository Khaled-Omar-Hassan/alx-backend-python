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
