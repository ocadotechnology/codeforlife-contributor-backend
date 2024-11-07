"""
© Ocado Group
Created on 05/08/2024 at 15:54:51(+01:00).
"""

from codeforlife.forms import BaseLoginForm
from django import forms

from ..models import Contributor


class GitHubLoginForm(BaseLoginForm[Contributor]):
    """Login with an existing github account."""

    code = forms.CharField(required=True)

    def get_invalid_login_error_message(self):
        return "The code returned was invalid or expired."
