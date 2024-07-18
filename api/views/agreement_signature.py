"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

from typing import Dict

import requests
from codeforlife.permissions import AllowAny
from codeforlife.response import Response
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet, action
from rest_framework import status

import settings

from ..models import AgreementSignature, Contributor
from ..serializers import AgreementSignatureSerializer


# pylint: disable-next=too-many-ancestors
class AgreementSignatureViewSet(ModelViewSet[User, AgreementSignature]):
    """
    An endpoint to check if a contributor has signed latest agreement,
    return OKAY if he has otherwise return the latest commit ID.
    """

    # http_method_names = ["get", "post"]
    queryset = AgreementSignature.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AgreementSignatureSerializer

    def get_latest_commit_id(self, commits=None):
        """Fetch the latest commit using github's api."""
        owner = settings.OWNER
        repo = settings.REPO_NAME
        file_name = settings.FILE_NAME

        params: Dict[str, str]
        if commits:
            params = {"path": file_name, "per_page": commits}
        else:
            params = {"path": file_name}

        url = f"https://api.github.com/repos/{owner}/{repo}/commits"

        # Send an API request
        response = requests.get(url, params=params, timeout=10)

        return response

    @action(
        detail=False,
        methods=["get"],
        url_path="check-signed/(?P<contributor_pk>.+)",
    )
    def check_signed(self, _, **url_params: str):
        """
        Get the latest commit id and compare with contributor's
        agreement signature.
        """
        # Repo information
        github_pk = url_params["contributor_pk"]

        # Send an API request
        response = self.get_latest_commit_id(commits=1)

        # Check the result of the API call
        if response.status_code == 200:
            latest_commit_id = response.json()[0]["sha"]
        else:
            return Response(
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            )

        # Retrieve contributor
        try:
            contributor = Contributor.objects.get(pk=github_pk)
        except Contributor.DoesNotExist:
            return Response(  # pragma: no cover
                data={"outcome: ": "Contributor does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Retrieve signature agreement IDs
        signatures = AgreementSignature.objects.filter(contributor=contributor)
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
