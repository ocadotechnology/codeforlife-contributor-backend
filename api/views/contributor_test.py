"""
© Ocado Group
Created on 16/07/2024 at 14:54:09(+01:00).
"""

from unittest.mock import patch

import requests
from codeforlife.request import Request
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

    # def test_log_into_github__no_code(self):
    #     """Login API call does not return a code."""
    #     code = "3e074f3e12656707cf7f"
    #     request = Request
    #     # request.GET= {"code": code}

    #     with patch.object(Request, "GET", return_value=request):
    #         self.client.get(
    #             self.reverse_action(
    #                 "log_into_github",
    #             ),
    #             status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    # def test_log_into_github__no_access_token(self):
    #     """POST API call did not return an access token"""
    #     code = "3e074f3e12656707cf7f"
    #     response = requests.Response()
    #     response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     request = Request
    #     request.GET = {"code": code}
    #     with patch.object(
    #         requests, "post", return_value=response
    #     ) as requests_get:
    #         self.client.get(
    #             self.reverse_action(
    #                 "log_into_github",
    #             ),
    #             status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )

    #         requests_get.assert_called_once_with(
    #             url="https://github.com/login/oauth/access_token",
    #             headers={"Accept": "application/json"},
    #             params={
    #                 "client_id": settings.GITHUB_CLIENT_ID,
    #                 "client_secret": settings.GITHUB_CLIENT_SECRET,
    #                 "code": code,
    #             },
    #             timeout=5,
    #         )
