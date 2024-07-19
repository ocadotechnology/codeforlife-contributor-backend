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

from ..models import AgreementSignature

# pylint: disable-next=missing-function-docstring,too-many-ancestors


class AgreementSignatureSerializer(ModelSerializer[User, AgreementSignature]):
    """Agreement serializer class"""

    class Meta:
        model = AgreementSignature
        fields = ["id", "contributor", "agreement_id", "signed_at"]

    def validate_signed_at(self, value: datetime):
        """Validate the time in not in future."""
        if value > timezone.now():
            raise serializers.ValidationError(
                "Cannot sign in the future", code="signed_in_future"
            )
        return value

    def get_agreement_commit(self, ref: str):
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
        # pylint: disable=line-too-long
        url = f"https://api.github.com/repos/{settings.OWNER}/{settings.REPO_NAME}/commits/{ref}"

        # Send an API request
        response = requests.get(
            url,
            headers={
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
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
        """
        Validate the new agreement is the new version not the older version.
        """

        # Check validity of the new agreement_ID
        if "agreement_id" in attrs:
            commit = self.get_agreement_commit(attrs["agreement_id"])
            new_agreement_version = commit["commit"]["committer"]["date"]

            # Check if contributor has signed a contribution in the past
            if "contributor" in attrs:
                last_signature = (
                    AgreementSignature.objects.filter(
                        contributor=attrs["contributor"]
                    )
                    .order_by("-signed_at")
                    .first()
                )
                if not last_signature:
                    return attrs

                commit = self.get_agreement_commit(last_signature.agreement_id)

                # Compare the two versions agreement ID.
                old_agreement_version = commit["commit"]["committer"]["date"]
                if new_agreement_version <= old_agreement_version:
                    raise serializers.ValidationError(
                        "You tried to sign an older version of the agreement.",
                        code="old_version",
                    )
        return attrs
