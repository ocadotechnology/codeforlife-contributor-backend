"""
© Ocado Group
Created on 05/08/2024 at 17:23:01(+01:00).
"""

import json
import typing as t
from urllib.parse import quote_plus

from codeforlife.request import HttpRequest
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as _LoginView
from django.http import JsonResponse
from rest_framework import status

from ..forms import GitHubLoginForm


class LoginView(_LoginView):
    """Login users with their existing github accounts."""

    request: HttpRequest

    def get_form_class(self):
        return GitHubLoginForm

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["data"] = json.loads(self.request.body)

        return form_kwargs

    def form_valid(self, form: GitHubLoginForm):  # type: ignore
        contributor = form.contributor

        # pylint: disable-next=line-too-long
        self.request.session.clear_expired(
            contributor_id=contributor.pk
        )  # type: ignore

        login(self.request, contributor)  # type: ignore

        self.request.session.save()

        # Get session metadata.
        session_metadata = {"contributor_id": contributor.id}

        # Return session metadata in response and a non-HTTP-only cookie.
        response = JsonResponse(session_metadata)
        response.set_cookie(
            key=settings.SESSION_METADATA_COOKIE_NAME,
            value=quote_plus(
                json.dumps(
                    session_metadata,
                    separators=(",", ":"),
                    indent=None,
                )
            ),
            max_age=(
                None
                if settings.SESSION_EXPIRE_AT_BROWSER_CLOSE
                else settings.SESSION_COOKIE_AGE
            ),
            secure=settings.SESSION_COOKIE_SECURE,
            samesite=t.cast(
                t.Optional[t.Literal["Lax", "Strict", "None", False]],
                settings.SESSION_COOKIE_SAMESITE,
            ),
            domain=settings.SESSION_COOKIE_DOMAIN,
            httponly=False,
        )

        return response

    def form_invalid(self, form: GitHubLoginForm):  # type: ignore
        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)
