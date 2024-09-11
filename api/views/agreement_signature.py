"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

import typing as t

import requests
from codeforlife.permissions import AllowAny
from codeforlife.response import Response
from codeforlife.types import DataDict
from codeforlife.views import action
from django.conf import settings
from rest_framework import status

from ..common import ModelViewSet
from ..models import AgreementSignature
from ..serializers import AgreementSignatureSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class AgreementSignatureViewSet(ModelViewSet[AgreementSignature]):
    http_method_names = ["get", "post"]
    permission_classes = [AllowAny]  # TODO: remove
    serializer_class = AgreementSignatureSerializer

    def get_queryset(self):
        return AgreementSignature.objects.filter(
            contributor=self.request.contributor
        ).order_by("signed_at")

    @action(detail=False, methods=["get"])
    # pylint: disable-next=unused-argument
    def check_signed_latest(self, _):
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

        is_signed, reason = True, ""
        if not last_signature:
            is_signed, reason = False, "no_agreement_signatures"
        elif latest_commit_id != last_signature.agreement_id:
            is_signed, reason = False, "old_agreement_signatures"

        return Response(
            {
                "latest_commit_id": latest_commit_id,
                "is_signed": is_signed,
                "reason": reason,
            }
        )
