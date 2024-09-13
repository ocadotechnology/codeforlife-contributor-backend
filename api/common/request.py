import typing as t

from django.contrib.auth.models import AnonymousUser
from rest_framework.request import Request as _Request

from ..models import Contributor


class Request(_Request):
    user: t.Union[Contributor, AnonymousUser]  # type: ignore[assignment]

    @property
    def anon_user(self):
        """The anonymous user that made the request."""
        return t.cast(AnonymousUser, self.user)

    @property
    def contributor(self):
        """The contributor that made the request."""
        return t.cast(Contributor, self.user)
