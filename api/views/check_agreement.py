"""
© Ocado Group
Created on 15/07/2024 at 12:52:50(+01:00).
"""

from typing import Dict

import requests
from codeforlife.permissions import AllowAny
from codeforlife.response import Response
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet

# from django.http import HttpResponse
from rest_framework import status

from ..models import AgreementSignature, Contributor

# from rest_framework.views import APIView


class CheckAgreementViewSet(ModelViewSet[User, Contributor]):
    """
    An endpoint to check if a contributor has signed latest agreement,
    return OKAY if he has otherwise return the latest commit ID.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        """
        Get the latest commit id and compare with contributor's
        agreement signature.
        """
        # Repo information
        github_id = 118008817  # TODO: Change later
        owner = "ocadotechnology"
        repo = "codeforlife-workshop"
        file_name = "CONTRIBUTING.md"

        params: Dict[str, str]
        params = {"path": file_name, "per_page": 1}

        url = f"https://api.github.com/repos/{owner}/{repo}/commits"

        # Send an API request
        response = requests.get(url, params=params, timeout=10)

        # Check the result of the API call
        if response.status_code == 200:
            latest_commit_id = response.json()[0]["sha"]
        else:
            return Response(
                status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
            )

        # Retrieve contributor
        contributor = Contributor.objects.get(id=github_id)
        if not contributor:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Retrieve signature agreement IDs
        signatures = AgreementSignature.objects.filter(contributor=contributor)
        latest_signature = signatures.order_by("-signed_by").first()
        if not latest_signature:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Compare agreement IDs
        if latest_commit_id == latest_signature.agreement_id:
            return Response(status=status.HTTP_200_OK)

        return Response(
            data={"latest_commit_id: ": latest_commit_id},
            status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )
