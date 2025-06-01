#!/usr/bin/env python3
"""Test suite for GithubOrgClient class."""

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class
import client
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch.object(client, "get_json")
    def test_org(self, org, mock_get_json):
        """Test that org returns expected JSON payload from get_json."""
        mock_get_json.return_value = {"login": org}
        client_instance = GithubOrgClient(org)
        self.assertEqual(client_instance.org, {"login": org})
        mock_get_json.assert_called_once_with(
            client.GithubOrgClient.ORG_URL.format(org=org)
        )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns expected repo names from payload."""
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mock_repos_payload

        test_url = "https://api.github.com/orgs/test_org/repos"

        with patch.object(
            GithubOrgClient, "_public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = test_url

            client_instance = GithubOrgClient("test_org")
            result = client_instance.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
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
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
    for org_payload, repos_payload, expected_repos,
    apache2_repos in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and return controlled fixture responses."""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_response = MagicMock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = None
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns correct list of repo names."""
        client_instance = GithubOrgClient("google")
        self.assertEqual(client_instance.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license."""
        client_instance = GithubOrgClient("google")
        self.assertEqual(
            client_instance.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
        
    def test_public_repos(self):
        """Test public_repos returns correct list of repo names."""
        client_instance = GithubOrgClient("google")
        repos = client_instance.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by 'apache-2.0' license."""
        client_instance = GithubOrgClient("google")
        repos = client_instance.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
