"""
© Ocado Group
Created on 13/09/2024 at 12:01:04(+03:00).
"""

import typing as t

from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request as _Request

from ..models import Contributor


# pylint: disable-next=abstract-method
class Request(_Request):
    """A HTTP request."""

    user: t.Union[Contributor, AnonymousUser]  # type: ignore[assignment]

    @property
    def anon_user(self):
        """The anonymous user that made the request."""
        return t.cast(AnonymousUser, self.user)

    @property
    def contributor(self):
        """The contributor that made the request."""
        return t.cast(Contributor, self.user)
