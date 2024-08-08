"""
© Ocado Group
Created on 06/08/2024 at 14:52:07(+01:00).
"""

import json
from unittest.mock import patch

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
        """Login a user as an existing github user."""
        self.client.post(
            reverse("session-login"),
            data={"code": "7f06468085765cdc1578"},
            format="json",
        )

    def test_login(self):
        """Login a user as an existing github user."""
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
                self.client.post(
                    reverse("session-login"),
                    data={"code": code},
                    format="json",
                )

                requests_post.assert_called_once_with(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": settings.GH_CLIENT_ID,
                        "client_secret": settings.GH_CLIENT_SECRET,
                        "code": code,
                    },
                    timeout=5,
                )

                requests_get.assert_called_once_with(
                    url="https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": "Bearer 123254",
                        "X-GitHub-Api-Version": "2022-11-28",
                    },
                    timeout=5,
                )
