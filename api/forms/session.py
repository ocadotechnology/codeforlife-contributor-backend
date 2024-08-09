"""
© Ocado Group
Created on 05/08/2024 at 15:54:51(+01:00).
"""

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest

from ..models import Contributor


class GitHubLoginForm(forms.Form):
    """Login with an existing github account."""

    contributor: Contributor

    code = forms.CharField(required=True)

    def __init__(self, request: WSGIRequest, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        """Authenticates a contributor.

        Raises:
            ValidationError: If there are form errors.
            ValidationError: If the contributor's credentials were incorrect.
            ValidationError: If the contributor's instance is incorrect.

        Returns:
            The cleaned form data.
        """
        if self.errors:
            raise ValidationError(
                "Found form errors. Skipping authentication.",
                code="form_errors",
            )

        # Needs mocking. Must return a valid Contributor
        contributor = authenticate(
            self.request,
            **{key: self.cleaned_data[key] for key in self.fields.keys()}
        )
        if contributor is None:
            raise ValidationError(
                "The code returned was invalid or expired.",
                code="invalid_login",
            )

        if not isinstance(contributor, Contributor):
            raise ValidationError(
                "Incorrect contributor class.",
                code="incorrect_contributor_class",
            )

        self.contributor = contributor
        return self.cleaned_data
