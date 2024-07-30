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
    http_method_names = ["get", "post"]  # "post"
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
            headers={"Accept": "application/json"},
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
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
                "Authorization": f"{auth_data['token_type']} {auth_data['access_token']}",
            },
            timeout=5,
        )

        user_data = response.json()
        if not user_data["email"]:
            return Response(
                data="Email null",
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

        # Check if user is already a contributor
        gh_id = user_data["id"]
        contributor_data = {
            "id": gh_id,
            "email": user_data["email"],
            "name": user_data["name"],
            "location": user_data["location"],
            "html_url": user_data["html_url"],
            "avatar_url": user_data["avatar_url"],
        }

        try:
            # Update an existing contributor
            contributor = Contributor.objects.get(pk=gh_id)
            serializer = ContributorSerializer(
                contributor, data=contributor_data
            )
        except Contributor.DoesNotExist:
            # Create a new contributor
            serializer = ContributorSerializer(data=contributor_data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )
