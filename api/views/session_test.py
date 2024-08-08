"""
© Ocado Group
Created on 06/08/2024 at 14:52:07(+01:00).
"""

import json
from unittest.mock import Mock, patch

import requests
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestLoginView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login__invalid_code(self):
        """Provided code must be valid and not expired."""
        response = self.client.post(
            reverse("session-login"),
            data={"code": "7f06468085765cdc1578"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login__form_errors(self):
        """Throw ValidationError if there are form errors."""
        response = self.client.post(
            reverse("session-login"),
            data={"code": ""},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

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

    def test_login__invalid_user(self):
        """
        Github did not provide data needed to log the user in.
        """

        code = "7f06468085765cdc1578"

        response_post = requests.Response()
        response_post.status_code = status.HTTP_200_OK
        response_post.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_post._content = json.dumps(
            {"access_token": "123254", "token_type": "Bearer"}
        ).encode("utf-8")

        response_get = requests.Response()
        response_get.status_code = status.HTTP_200_OK
        response_get.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_get._content = json.dumps({}).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response_post
        ) as requests_post:
            with patch.object(
                requests, "get", return_value=response_get
            ) as requests_get:
                response = self.client.post(
                    reverse("session-login"),
                    data={"code": code},
                    format="json",
                )

                assert response.status_code == status.HTTP_400_BAD_REQUEST

                self._assert_request_github_access_token(requests_post, code)
                self._assert_request_github_user(requests_get, "Bearer 123254")

    def test_login__new_contributor(self):
        """
        Login a new user with their existing github account and
        add record to the database for this contributor.
        """

        code = "7f06468085765cdc1578"

        response_post = requests.Response()
        response_post.status_code = status.HTTP_200_OK
        response_post.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_post._content = json.dumps(
            {"access_token": "123254", "token_type": "Bearer"}
        ).encode("utf-8")

        response_get = requests.Response()
        response_get.status_code = status.HTTP_200_OK
        response_get.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_get._content = json.dumps(
            {
                "id": 999999999999999,
                "email": "contributornew@gmail.com",
                "name": "contributor new",
                "location": "London",
                "html_url": "https://github.com/contributornew",
                "avatar_url": "https://contributornew.github.io/",
            }
        ).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response_post
        ) as requests_post:
            with patch.object(
                requests, "get", return_value=response_get
            ) as requests_get:
                response = self.client.post(
                    reverse("session-login"),
                    data={"code": code},
                    format="json",
                )
                assert response.status_code == status.HTTP_200_OK

                self._assert_request_github_access_token(requests_post, code)
                self._assert_request_github_user(requests_get, "Bearer 123254")

    def test_login__existing_contributor(self):
        """
        Login a returning user with their existing github account and
        sync any updated information for this contributor.
        """

        code = "7f06468085765cdc1578"

        response_post = requests.Response()
        response_post.status_code = status.HTTP_200_OK
        response_post.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_post._content = json.dumps(
            {"access_token": "123254", "token_type": "Bearer"}
        ).encode("utf-8")

        response_get = requests.Response()
        response_get.status_code = status.HTTP_200_OK
        response_get.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_get._content = json.dumps(
            {
                "id": 1,
                "email": "contributor1@gmail.com",
                "name": "contributor one",
                "location": "London",
                "html_url": "https://github.com/contributor1",
                "avatar_url": "https://contributor1.github.io/",
            }
        ).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response_post
        ) as requests_post:
            with patch.object(
                requests, "get", return_value=response_get
            ) as requests_get:
                response = self.client.post(
                    reverse("session-login"),
                    data={"code": code},
                    format="json",
                )

                assert response.status_code == status.HTTP_200_OK

                self._assert_request_github_access_token(requests_post, code)
                self._assert_request_github_user(requests_get, "Bearer 123254")

    def test_login__invalid_contributor_data(self):
        """User data returned by github is not in the correct format."""

        code = "7f06468085765cdc1578"

        response_post = requests.Response()
        response_post.status_code = status.HTTP_200_OK
        response_post.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_post._content = json.dumps(
            {"access_token": "123254", "token_type": "Bearer"}
        ).encode("utf-8")

        response_get = requests.Response()
        response_get.status_code = status.HTTP_200_OK
        response_get.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response_get._content = json.dumps(
            {
                "id": 1,
                "email": "1234",
                "name": "contributor one",
                "location": "London",
                "html_url": "https://github.com/contributor1",
                "avatar_url": "https://contributor1.github.io/",
            }
        ).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response_post
        ) as requests_post:
            with patch.object(
                requests, "get", return_value=response_get
            ) as requests_get:
                response = self.client.post(
                    reverse("session-login"),
                    data={"code": code},
                    format="json",
                )

                assert response.status_code == status.HTTP_400_BAD_REQUEST

                self._assert_request_github_access_token(requests_post, code)
                self._assert_request_github_user(requests_get, "Bearer 123254")
