import json
import typing as t
from unittest.mock import ANY, call, patch

import requests
from codeforlife.tests import ModelViewSetClient as _ModelViewSetClient
from codeforlife.tests import ModelViewSetTestCase as _ModelViewSetTestCase
from django.conf import settings
from django.db.models import Model
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Contributor
from .api_request_factory import APIRequestFactory
from .model_view_set import ModelViewSet

AnyModel = t.TypeVar("AnyModel", bound=Model)


class ModelViewSetClient(_ModelViewSetClient, t.Generic[AnyModel]):
    def __init__(self, enforce_csrf_checks: bool = False, **defaults):
        super().__init__(enforce_csrf_checks, **defaults)

        self.request_factory = APIRequestFactory(  # type: ignore[assignment]
            enforce_csrf_checks, **defaults
        )

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

    def login_as(self, contributor: Contributor):  # type: ignore[override]
        return self.login(contributor)


class ModelViewSetTestCase(_ModelViewSetTestCase, t.Generic[AnyModel]):
    model_view_set_class: t.Type[  # type: ignore[assignment]
        ModelViewSet[AnyModel]
    ]
    client: ModelViewSetClient[AnyModel]
    client_class: t.Type[ModelViewSetClient[AnyModel]] = ModelViewSetClient

    @classmethod
    def get_model_class(cls) -> t.Type[AnyModel]:
        """Get the model view set's class.

        Returns:
            The model view set's class.
        """
        # pylint: disable-next=no-member
        return t.get_args(cls.__orig_bases__[0])[  # type: ignore[attr-defined]
            0
        ]

    @classmethod
    def get_request_user_class(cls):
        return Contributor

    def _get_client_class(self):
        # TODO: unpack type args in index after moving to python 3.11
        # pylint: disable-next=too-few-public-methods
        class _Client(
            self.client_class[self.get_model_class()]  # type: ignore[misc]
        ):
            _test_case = self

        return _Client
