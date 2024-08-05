"""
© Ocado Group
Created on 05/08/2024 at 12:48:13(+01:00).
"""
import typing as t

import requests
from codeforlife.request import HttpRequest
from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from ...models import Contributor


class GithubBackend:
    """Authenticate a user using the code returned by github's callback url."""

    def authenticate(
        self,
        request: t.Optional[HttpRequest],
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
        auth_data = response.json()

        # Code expired
        if "error" in auth_data:
            return None

        # Get user's information
        response = requests.get(
            url="https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                # pylint: disable-next=line-too-long
                "Authorization": f"{auth_data['token_type']} {auth_data['access_token']}",
            },
            timeout=5,
        )

        contributor_data = response.json()
        contributor, created = Contributor.objects.get_or_create(
            id=contributor_data["id"],
            defaults={
                "email": contributor_data["email"],
                "name": contributor_data["name"],
                "location": contributor_data["location"],
                "html_url": contributor_data["html_url"],
                "avatar_url": contributor_data["avatar_url"],
            },
        )

        return contributor if contributor or created else None

    def get_user(self, user_id: int):
        try:
            return Contributor.objects.get(id=user_id)
        except Contributor.DoesNotExist:
            return None
