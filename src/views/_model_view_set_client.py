"""
© Ocado Group
Created on 13/09/2024 at 12:00:50(+03:00).
"""

# pylint: disable=duplicate-code

import json
import typing as t
from unittest.mock import ANY, call, patch

import requests
from codeforlife.request import BaseRequest
from codeforlife.tests import BaseAPIRequestFactory, BaseModelViewSetClient
from django.conf import settings
from django.db.models import Model
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Contributor
from ..models.session import SessionStore

AnyModel = t.TypeVar("AnyModel", bound=Model)

if t.TYPE_CHECKING:  # pragma: no cover
    from ._model_view_set_test_case import ModelViewSetTestCase


# pylint: disable-next=too-many-ancestors,arguments-differ
class ModelViewSetClient(
    BaseModelViewSetClient[
        "ModelViewSetTestCase[AnyModel]",
        BaseAPIRequestFactory[
            BaseRequest[SessionStore, Contributor], Contributor
        ],
    ],
    t.Generic[AnyModel],
):
    """Client used to make test requests."""

    request_factory_class = BaseAPIRequestFactory

    # pylint: disable-next=arguments-differ
    def login(  # type: ignore[override]
        self, contributor: t.Union[int, Contributor]
    ):
        # Logout current user (if any) before logging in next user.
        self.logout()

        contributor = (
            contributor
            if isinstance(contributor, Contributor)
            else Contributor.objects.get(pk=contributor)
        )

        code = "example_code"

        # TODO: mock api calls
        access_token = {"token_type": "Bearer", "access_token": "example_token"}
        access_token_response = requests.Response()
        access_token_response.status_code = status.HTTP_200_OK
        access_token_response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        access_token_response._content = json.dumps(access_token).encode(
            "utf-8"
        )

        get_contributor_response = requests.Response()
        get_contributor_response.status_code = status.HTTP_200_OK
        get_contributor_response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        get_contributor_response._content = json.dumps(
            {
                "id": contributor.id,
                "name": contributor.name,
                "location": contributor.location,
                "html_url": contributor.html_url,
                "avatar_url": contributor.avatar_url,
            }
        ).encode("utf-8")

        list_emails_response = requests.Response()
        list_emails_response.status_code = status.HTTP_200_OK
        list_emails_response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        list_emails_response._content = json.dumps(
            [
                {
                    "verified": True,
                    "email": email.email,
                    "primary": email.is_primary,
                    "visibility": "public" if email.is_public else None,
                }
                for email in contributor.emails.all()
            ]
        ).encode("utf-8")

        with patch.object(
            requests, "post", return_value=access_token_response
        ) as post:
            with patch.object(
                requests,
                "get",
                side_effect=[get_contributor_response, list_emails_response],
            ) as get:
                assert APIClient.login(self, code=code), "Failed to login."

                post.assert_called_once_with(
                    url="https://github.com/login/oauth/access_token",
                    headers={"Accept": "application/json"},
                    params={
                        "client_id": settings.GH_CLIENT_ID,
                        "client_secret": settings.GH_CLIENT_SECRET,
                        "code": code,
                    },
                    timeout=ANY,
                )

                # pylint: disable-next=line-too-long
                auth = f"{access_token['token_type']} {access_token['access_token']}"

                get.assert_has_calls(
                    [
                        call(
                            url="https://api.github.com/user",
                            headers={
                                "Accept": "application/json",
                                "X-GitHub-Api-Version": "2022-11-28",
                                "Authorization": auth,
                            },
                            timeout=ANY,
                        ),
                        call(
                            url="https://api.github.com/user/emails",
                            headers={
                                "Accept": "application/vnd.github+json",
                                "X-GitHub-Api-Version": "2022-11-28",
                                "Authorization": auth,
                            },
                            params={"per_page": 100},
                            timeout=ANY,
                        ),
                    ]
                )

        return Contributor.objects.get(session=self.session.session_key)
