"""
© Ocado Group
Created on 05/08/2024 at 12:48:13(+01:00).
"""

import typing as t

import requests
from codeforlife.request import BaseHttpRequest
from codeforlife.types import JsonDict
from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from ...models import Contributor
from ...models.session import SessionStore


class GitHubBackend(BaseBackend):
    """Authenticate a user using the code returned by github's callback url."""

    def authenticate(  # type: ignore[override]
        self,
        request: t.Optional[BaseHttpRequest[SessionStore, Contributor]],
        code: t.Optional[str] = None,
        **kwargs,
    ):
        if code is None:
            return None

        # Get user access Token
        response = requests.post(
            url="https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": settings.GH_CLIENT_ID,
                "client_secret": settings.GH_CLIENT_SECRET,
                "code": code,
            },
            timeout=5,
        )
        if not response.ok:
            return None

        access_token: JsonDict = response.json()
        if "error" in access_token:
            return None

        return Contributor.sync_with_github(
            auth=f"{access_token['token_type']} {access_token['access_token']}"
        )

    # pylint: disable-next=arguments-renamed
    def get_user(self, contributor_id: int):
        try:
            return Contributor.objects.get(id=contributor_id)
        except Contributor.DoesNotExist:
            return None
