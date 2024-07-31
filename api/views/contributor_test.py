"""
© Ocado Group
Created on 16/07/2024 at 14:54:09(+01:00).
"""

import json
from unittest.mock import patch

import requests
from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User
from django.conf import settings
from rest_framework import status

from ..models import Contributor
from .contributor import ContributorViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorViewSet(ModelViewSetTestCase[User, Contributor]):
    """Testing contributor view set."""

    basename = "contributor"
    model_view_set_class = ContributorViewSet
    fixtures = ["contributors"]

    def setUp(self):
        self.contributor1 = Contributor.objects.get(pk=1)

    def test_list(self):
        """Check list of all contributors."""
        self.client.list(models=list(Contributor.objects.all()))

    def test_retrieve(self):
        """Can retrieve a single contributor."""
        self.client.retrieve(model=self.contributor1)

    def test_log_into_github__no_code(self):
        """Login API call does not return a code."""
        self.client.get(
            self.reverse_action("log_into_github"),
            data={"code": ""},
            status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def verify_api_call(self, request, url):
        """API call is correctly executed."""
        request.assert_called_once_with(
            url=url,
            headers={
                "Accept": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            params={
                "client_id": settings.GH_CLIENT_ID,
                "client_secret": settings.GH_CLIENT_SECRET,
                "code": "3e074f3e12656707cf7f",
            },
            timeout=5,
        )

    def test_log_into_github__no_access_token(self):
        """0Auth API call did not return an access token"""
        response = requests.Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            self.client.get(
                self.reverse_action("log_into_github"),
                data={"code": "3e074f3e12656707cf7f"},
                status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            self.verify_api_call(
                requests_post, "https://github.com/login/oauth/access_token"
            )

    def test_log_into_github__code_expired(self):
        """Access token was not generated due to expired code."""
        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps({"error": "bad request."}).encode(
            "utf-8"
        )

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            self.client.get(
                self.reverse_action(
                    "log_into_github",
                ),
                data={"code": "3e074f3e12656707cf7f"},
                # pylint: disable-next=line-too-long
                status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

            self.verify_api_call(
                requests_post, "https://github.com/login/oauth/access_token"
            )

    def test_log_into_github__existing_contributor(self):
        """User already logged-in in the past and exists as a contributor"""
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
                self.client.get(
                    self.reverse_action(
                        "log_into_github",
                    ),
                    data={"code": "3e074f3e12656707cf7f"},
                    status_code_assertion=status.HTTP_201_CREATED,
                )

                self.verify_api_call(
                    requests_post, "https://github.com/login/oauth/access_token"
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

    def test_log_into_github__new_contributor(self):
        """
        User is logging-in for the first time and will be added
        to the contributor data table
        """
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
                self.client.get(
                    self.reverse_action(
                        "log_into_github",
                    ),
                    data={"code": "3e074f3e12656707cf7f"},
                )

                self.verify_api_call(
                    requests_post, "https://github.com/login/oauth/access_token"
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
