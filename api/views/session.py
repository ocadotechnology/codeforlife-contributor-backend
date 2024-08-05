"""
© Ocado Group
Created on 05/08/2024 at 17:23:01(+01:00).
"""
import json

from codeforlife.request import HttpRequest
from django.contrib.auth.views import LoginView as _LoginView
from django.http import JsonResponse
from rest_framework import status

from ..forms import GitHubLoginForm


class LoginView(_LoginView):
    """Login users with their existing github accounts."""

    request: HttpRequest

    def get_form_class(self):
        form = self.kwargs["form"]
        if form == "login-with-github":
            return GitHubLoginForm
        raise NameError(f'Unsupported form: "{form}".')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["data"] = json.loads(self.request.body)

        return form_kwargs

    # def form_valid(self, form: GitHubLoginForm):
    #     pass

    def form_invalid(self, form: GitHubLoginForm):  # type: ignore
        return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)
