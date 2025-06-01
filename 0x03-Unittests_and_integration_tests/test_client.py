#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from unittest import TestCase
from unittest.mock import patch, MagicMock
from parameterized import parameterized_class
import requests
import client
import fixtures  


class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient class."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch.object(client, "get_json")
    def test_org(self,  org, mock_get_json):
        """Test that org returns expected JSON payload from get_json."""
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

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock:
            mock.return_value = test_url

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license correctly determines license match."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)



@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(TestCase):
    """Integration test class for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Start patching requests.get to mock API responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Define the behavior of requests.get().json() using side_effect
        def side_effect(url):
            mock_resp = MagicMock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

if __name__ == "__main__":
    unittest.main()
