"""
© Ocado Group
Created on 12/07/2024 at 14:07:45(+01:00).
"""

from datetime import datetime

import requests
from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User
from django.utils import timezone
from rest_framework import serializers

import settings

from ..models import AgreementSignature, Contributor

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-ancestors


class AgreementSignatureSerializer(ModelSerializer[User, AgreementSignature]):
    class Meta:
        model = AgreementSignature
        fields = ["id", "contributor", "agreement_id", "signed_at"]

    def validate_signed_at(self, value: datetime):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Cannot sign in the future", code="signed_in_future"
            )

        return value

    def _get_agreement_commit(self, ref: str):
        """
        Get a commit for the agreement using GitHub's API

        https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28#
        get-a-commit

        Args:
            ref: The SHA for the commit.

        Raises:
            ValidationError: If the commit does not exist for the agreement.

        Returns:
            The commit's data.
        """

        # Send an API request
        response = requests.get(
            # pylint: disable-next=line-too-long
            url=f"https://api.github.com/repos/{settings.OWNER}/{settings.REPO_NAME}/commits/{ref}",
            headers={"X-GitHub-Api-Version": "2022-11-28"},
            timeout=5,
        )
        if not response.ok:
            raise serializers.ValidationError(
                "Invalid commit ID", code="invalid_commit_id"
            )

        response_json = response.json()
        for file in response_json.get("files", []):
            if file["filename"] == settings.FILE_NAME:
                return response_json

        raise serializers.ValidationError(
            "Agreement not in commit files", code="agreement_not_in_files"
        )

    def validate(self, attrs):
        contributor: Contributor = attrs["contributor"]
        agreement_id: str = attrs["agreement_id"]

        # Check validity of the new agreement_ID
        commit = self._get_agreement_commit(agreement_id)

        # Check if contributor has signed a contribution in the past
        last_agreement_signature = contributor.last_agreement_signature
        if last_agreement_signature:
            last_commit = self._get_agreement_commit(
                last_agreement_signature.agreement_id
            )

            if (
                commit["commit"]["author"]["date"]
                <= last_commit["commit"]["author"]["date"]
            ):
                raise serializers.ValidationError(
                    "You tried to sign an older version of the agreement.",
                    code="old_version",
                )

        return attrs
