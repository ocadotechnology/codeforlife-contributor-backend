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
from rest_framework import status

import settings

from ..models import Contributor
from ..serializers import ContributorSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class ContributorViewSet(ModelViewSet[User, Contributor]):
    http_method_names = ["get", "post"]
    permission_classes = [AllowAny]
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    @action(detail=False, methods=["get"])
    def log_into_github(self, request: Request):
        """Users can login using their existing github account"""
        # Get code from login request
        code = request.GET.get("code")
        if not code:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get user access Token
        access_token_request = requests.post(
            url="https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            params={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": request.GET.get("code"),
            },
            timeout=5,
        )
        if not access_token_request.ok:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        auth_data = access_token_request.json()

        # Code expired
        if "access_token" not in auth_data:
            return Response(
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            )

        access_token = auth_data["access_token"]
        token_type = auth_data["token_type"]

        # Get user's information
        user_data_request = requests.get(
            url="https://api.github.com/user",
            headers={
                "Accept": "application/json",
                "Authorization": f"{token_type} {access_token}",
            },
            timeout=5,
        )

        user_data = user_data_request.json()
        if not user_data["email"]:
            return Response(
                data="Email null",
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

        # Check if user is already a contributor (TODO: Update user info)
        gh_id = user_data["id"]
        if Contributor.objects.filter(pk=gh_id):
            return Response(status=status.HTTP_409_CONFLICT)

        # Create a new contributor
        data = {
            "id": gh_id,
            "email": user_data["email"],
            "name": user_data["name"],
            "location": user_data["location"],
            "html_url": user_data["html_url"],
            "avatar_url": user_data["avatar_url"],
        }

        serializer = ContributorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )
