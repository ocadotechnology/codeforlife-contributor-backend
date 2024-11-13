"""
© Ocado Group
Created on 08/08/2024 at 15:46:09(+01:00).
"""

import json
from unittest.mock import Mock, patch

import requests
from codeforlife.request import BaseHttpRequest
from codeforlife.tests import TestCase
from django.conf import settings
from rest_framework import status

from ...models import Contributor
from ...models.session import SessionStore
from .github import GitHubBackend


# pylint: disable-next=missing-class-docstring,
class TestGitHubBackend(TestCase):
    fixtures = ["contributors"]

    def setUp(self):
        # Set up initial test data
        self.contributor1 = Contributor.objects.get(id=1)
        self.backend = GitHubBackend()
        self.request = BaseHttpRequest[SessionStore, Contributor]()

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
            contributor = self.backend.authenticate(
                request=self.request, code=code
            )

            assert not contributor
            self._assert_request_github_access_token(requests_post, code)

    def test_login__error(self):
        """Login cannot return an error in the response."""
        code = "7f06468085765cdc1578"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps({"error": ""}).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            contributor = self.backend.authenticate(
                request=self.request, code=code
            )

            assert not contributor
            self._assert_request_github_access_token(requests_post, code)
