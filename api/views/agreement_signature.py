"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

import typing as t

import requests
from codeforlife.permissions import AllowAny
from codeforlife.response import Response
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet, action
from rest_framework import status

import settings

from ..models import AgreementSignature
from ..serializers import AgreementSignatureSerializer


# pylint: disable-next=missing-docstring,too-many-ancestors
class AgreementSignatureViewSet(ModelViewSet[User, AgreementSignature]):
    http_method_names = ["get", "post"]
    permission_classes = [AllowAny]
    serializer_class = AgreementSignatureSerializer

    def get_queryset(self):
        queryset = AgreementSignature.objects.all()
        if "contributor_pk" in self.kwargs:
            queryset = queryset.filter(
                contributor=self.kwargs["contributor_pk"]
            )

        return queryset

    @action(
        detail=False,
        methods=["get"],
        url_path="check-signed/(?P<contributor_pk>.+)",
    )
    # pylint: disable=unused-argument
    def check_signed(self, _, **url_params: str):
        """
        Get the latest commit id and compare with contributor's
        agreement signature.
        """
        # Send an API request
        params: t.Dict[str, str] = {"path": settings.FILE_NAME, "per_page": 1}

        # pylint: disable=line-too-long
        url = f"https://api.github.com/repos/{settings.OWNER}/{settings.REPO_NAME}/commits"

        # Send an API request
        response = requests.get(url, params=params, timeout=10)
        if not response.ok:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get the commit id from json data
        latest_commit_id = response.json()[0]["sha"]

        # Retrieve signature agreement IDs
        signatures = self.get_queryset()
        latest_signature = signatures.order_by("-signed_at").first()
        if not latest_signature:
            return Response(
                data={"outcome: ": "No Agreement Signatures found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Compare agreement IDs
        if latest_commit_id == latest_signature.agreement_id:
            return Response(
                data={"Outcome:": "Successful"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"latest_commit_id: ": latest_commit_id},
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )
