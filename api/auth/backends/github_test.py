"""
© Ocado Group
Created on 08/08/2024 at 15:46:09(+01:00).
"""

import json
from unittest.mock import Mock, patch

import requests
from codeforlife.request import HttpRequest
from codeforlife.tests import TestCase
from django.conf import settings
from rest_framework import status

from ...models import Contributor
from .github import GitHubBackend


# pylint: disable-next=missing-class-docstring,
class TestGitHubBackend(TestCase):
    fixtures = ["contributors"]

    def setUp(self):
        # Set up initial test data
        self.contributor1 = Contributor.objects.get(id=1)
        self.backend = GitHubBackend()
        self.request = HttpRequest()

        self.gh_access_token_response = requests.Response()
        self.gh_access_token_response.status_code = status.HTTP_200_OK
        self.gh_access_token_response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        self.gh_access_token_response._content = json.dumps(
            {"access_token": "123254", "token_type": "Bearer"}
        ).encode("utf-8")

    def test_get_user__existing_contributor(self):
        """Can get the existing contributor"""
        contributor = self.backend.get_user(contributor_id=self.contributor1.id)
        assert contributor == self.contributor1

    def test_get_user__non_existing_contributor(self):
        """Can check if the contributor does not exist"""
        contributor = self.backend.get_user(contributor_id=999)
        assert not Contributor.objects.filter(id=999).exists()
        assert not contributor

    def _assert_request_github_access_token(self, request: Mock, code: str):
        """Retrieve the use access token in exchange for the code."""
        request.assert_called_once_with(
            url="https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": settings.GH_CLIENT_ID,
                "client_secret": settings.GH_CLIENT_SECRET,
                "code": code,
            },
            timeout=5,
        )

    def _assert_request_github_user(self, request: Mock, auth: str):
        """Retrieve user data using the access token."""
        request.assert_called_once_with(
            url="https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "Authorization": auth,
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=5,
        )

    def test_login__invalid_code(self):
        """Provided code must be valid."""
        code = "7f06468085765cdc1578"

        response = requests.Response()
        response.status_code = status.HTTP_404_NOT_FOUND

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            res = self.backend.authenticate(request=self.request, code=code)

            assert not res
            self._assert_request_github_access_token(requests_post, code)

    def test_login__code_expired(self):
        """Provided code must not expired."""
        code = "7f06468085765cdc1578"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps({"error": ""}).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            res = self.backend.authenticate(request=self.request, code=code)

            assert not res
            self._assert_request_github_access_token(requests_post, code)

    def test_login__token_failure(self):
        """Access token did not get accepted by github."""
        code = "7f06468085765cdc1578"

        response_get = requests.Response()
        response_get.status_code = status.HTTP_401_UNAUTHORIZED

        with patch.object(
            requests, "post", return_value=self.gh_access_token_response
        ) as requests_post:
            with patch.object(
                requests, "get", return_value=response_get
            ) as requests_get:
                res = self.backend.authenticate(request=self.request, code=code)

                assert not res
                self._assert_request_github_access_token(requests_post, code)
                self._assert_request_github_user(requests_get, "Bearer 123254")

    def test_login__invalid_contributor_data(self):
        """
        Github did not provide data needed to log the user in.
        """
        code = "7f06468085765cdc1578"

        response_get = requests.Response()
        response_get.status_code = status.HTTP_200_OK
        response_get.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_get._content = json.dumps({}).encode("utf-8")

        with patch.object(
            requests, "post", return_value=self.gh_access_token_response
        ) as requests_post:
            with patch.object(
                requests, "get", return_value=response_get
            ) as requests_get:
                res = self.backend.authenticate(request=self.request, code=code)

                assert not res
                self._assert_request_github_access_token(requests_post, code)
                self._assert_request_github_user(requests_get, "Bearer 123254")
