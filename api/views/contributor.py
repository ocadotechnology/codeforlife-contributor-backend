"""
© Ocado Group
Created on 16/07/2024 at 11:03:09(+01:00).
"""

import requests
from codeforlife.permissions import AllowAny
from codeforlife.request import Request
from codeforlife.response import Response
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet, action
from django.conf import settings
from rest_framework import status

from ..models import Contributor
from ..serializers import ContributorSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class ContributorViewSet(ModelViewSet[User, Contributor]):
    http_method_names = ["get"]  # "post"
    permission_classes = [AllowAny]
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    # TODO: delete custom action and override default create action.
    @action(detail=False, methods=["get"])
    def log_into_github(self, request: Request):
        """
        Creates a new contributor or updates an existing contributor.
        This requires users to authorize us to read their GitHub account.

        https://docs.github.com/en/apps/creating-github-apps/
        writing-code-for-a-github-app/building-a-login
        -with-github-button-with-a-github-app
        """
        # Get code from login request
        code = request.GET.get("code")
        if not code:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get user access Token
        response = requests.post(
            url="https://github.com/login/oauth/access_token",
            headers={
                "Accept": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            params={
                "client_id": settings.GH_CLIENT_ID,
                "client_secret": settings.GH_CLIENT_SECRET,
                "code": code,
            },
            timeout=5,
        )

        if not response.ok:
            return Response(status=response.status_code)
        auth_data = response.json()

        # Code expired
        if "error" in auth_data:
            return Response(
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

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

        serializer = self.get_serializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=self.get_success_headers(serializer.data),
        )
