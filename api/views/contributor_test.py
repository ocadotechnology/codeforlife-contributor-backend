"""
© Ocado Group
Created on 16/07/2024 at 14:54:09(+01:00).
"""

import json
from unittest.mock import patch

import requests
from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User
from rest_framework import status

import settings

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

    def test_create(self):
        """Can create a contributor."""
        self.client.create(
            data={
                "id": 100,
                "email": "contributor1@gmail.com",
                "name": "Test Contributor",
                "location": "Hatfield",
                "html_url": "https://github.com/contributortest",
                "avatar_url": "https://contributortest.github.io/",
            }
        )

    def test_log_into_github__no_code(self):
        """Login API call does not return a code."""
        code = ""
        self.client.get(
            self.reverse_action(
                "log_into_github",
            ),
            {"code": code},
            status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def test_log_into_github__no_access_token(self):
        """POST API call did not return an access token"""
        code = "3e074f3e12656707cf7f"

        response = requests.Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            self.client.get(
                self.reverse_action(
                    "log_into_github",
                ),
                {"code": code},
                status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            requests_post.assert_called_once_with(
                url="https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                params={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                },
                timeout=5,
            )

    def test_log_into_github__code_expired(self):
        """POST API call failed due to expired code."""
        code = "3e074f3e12656707cf7f"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps({}).encode("utf-8")

        with patch.object(
            requests, "post", return_value=response
        ) as requests_post:
            self.client.get(
                self.reverse_action(
                    "log_into_github",
                ),
                {"code": code},
                # pylint: disable-next=line-too-long
                status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

            requests_post.assert_called_once_with(
                url="https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                params={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                },
                timeout=5,
            )

    def test_log_into_github__null_email(self):
        """User must have their email public on github"""
        code = "3e074f3e12656707cf7f"

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
        response_get._content = json.dumps({"email": ""}).encode("utf-8")

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
                    {"code": code},
                    # pylint: disable-next=line-too-long
                    status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                )

                requests_post.assert_called_once_with(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": settings.GITHUB_CLIENT_ID,
                        "client_secret": settings.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    timeout=5,
                )
                requests_get.assert_called_once_with(
                    url="https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": "Bearer 123254",
                    },
                    timeout=5,
                )

    def test_log_into_github__existing_contributor(self):
        """User already exists as a contributor"""
        # TODO: update the user info
        code = "3e074f3e12656707cf7f"

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
                    {"code": code},
                    status_code_assertion=status.HTTP_200_OK,
                )

                requests_post.assert_called_once_with(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": settings.GITHUB_CLIENT_ID,
                        "client_secret": settings.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    timeout=5,
                )
                requests_get.assert_called_once_with(
                    url="https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": "Bearer 123254",
                    },
                    timeout=5,
                )

    def test_log_into_github__new_contributor(self):
        """Add user to the contributor data table"""
        code = "3e074f3e12656707cf7f"

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
                    {"code": code},
                )

                requests_post.assert_called_once_with(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": settings.GITHUB_CLIENT_ID,
                        "client_secret": settings.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    timeout=5,
                )
                requests_get.assert_called_once_with(
                    url="https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": "Bearer 123254",
                    },
                    timeout=5,
                )

    def test_log_into_github__invalid_serializer(self):
        """User data from Github is not in the valid format."""
        code = "3e074f3e12656707cf7f"

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
                "email": "1223533",
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
                    {"code": code},
                    # pylint: disable-next=line-too-long
                    status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
                )

                requests_post.assert_called_once_with(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": settings.GITHUB_CLIENT_ID,
                        "client_secret": settings.GITHUB_CLIENT_SECRET,
                        "code": code,
                    },
                    timeout=5,
                )
                requests_get.assert_called_once_with(
                    url="https://api.github.com/user",
                    headers={
                        "Accept": "application/json",
                        "Authorization": "Bearer 123254",
                    },
                    timeout=5,
                )
