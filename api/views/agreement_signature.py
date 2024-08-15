"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

import typing as t

import requests
from codeforlife.permissions import AllowAny
from codeforlife.response import Response
from codeforlife.types import DataDict
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet, action
from django.conf import settings
from rest_framework import status

from ..models import AgreementSignature
from ..serializers import AgreementSignatureSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
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
        if self.action == "check_signed":
            queryset = queryset.order_by("signed_at")

        return queryset

    @action(
        detail=False,
        methods=["get"],
        url_path="check-signed/(?P<contributor_pk>.+)",
    )
    # pylint: disable-next=unused-argument
    def check_signed(self, _, **url_params: str):
        """Check if a contributor has signed the latest agreement."""
        # Get latest agreement commit.
        response = requests.get(
            # pylint: disable-next=line-too-long
            url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
            headers={"X-GitHub-Api-Version": "2022-11-28"},
            params=t.cast(DataDict, {"path": settings.GH_FILE, "per_page": 1}),
            timeout=5,
        )
        if not response.ok:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        latest_commit_id = response.json()[0]["sha"]

        last_signature = self.get_queryset().last()
        if not last_signature:
            return Response(
                data={"latest_commit_id": latest_commit_id},
                status=status.HTTP_404_NOT_FOUND,
            )
        if latest_commit_id == last_signature.agreement_id:
            return Response()

        return Response(
            data={"latest_commit_id": latest_commit_id},
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )
