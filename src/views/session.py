"""
© Ocado Group
Created on 05/08/2024 at 17:23:01(+01:00).
"""

from codeforlife.request import BaseHttpRequest
from codeforlife.views import BaseLoginView

from ..forms import GitHubLoginForm
from ..models import Contributor
from ..models.session import SessionStore


class LoginView(
    BaseLoginView[BaseHttpRequest[SessionStore, Contributor], Contributor]
):
    """Login users with their existing github accounts."""

    def get_form_class(self):
        return GitHubLoginForm

    def get_session_metadata(self, user):
        return {"contributor_id": user.id}
