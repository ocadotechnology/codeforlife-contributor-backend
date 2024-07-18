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

    def check_agreement_version(self, value: str):
        """
        Get the status of a commit using GitHub's API.
        """
        # Repo Information
        owner = settings.OWNER
        repo = settings.REPO_NAME
        file_name = settings.FILE_NAME
        url = f"https://api.github.com/repos/{owner}/{repo}/commits/{value}"

        # Send an API request
        params = {"path": file_name}
        response = requests.get(url, params=params, timeout=10)
        return response

    def validate(self, attrs):
        """
        Validate the new agreement is the new version not the older version.
        """

        # Check validity of the new agreement_ID
        if "agreement_id" in attrs:
            response = self.check_agreement_version(value=attrs["agreement_id"])
            if response.status_code != 200:
                raise serializers.ValidationError(
                    "Invalid commit ID", code="invalid_commit_id"
                )
            new_agreement_version = response.json()["commit"]["committer"][
                "date"
            ]

            # Check if contributor has signed a contribution in the past
            if "contributor" in attrs:
                contributor = attrs["contributor"]
                prev_signatures = AgreementSignature.objects.filter(
                    contributor=contributor
                )
                last_signature = prev_signatures.order_by("-signed_at").first()
                if not last_signature:
                    return attrs

                response = self.check_agreement_version(
                    value=last_signature.agreement_id
                )

                # Compare the two versions agreement ID.
                old_agreement_version = response.json()["commit"]["committer"][
                    "date"
                ]
                if new_agreement_version <= old_agreement_version:
                    raise serializers.ValidationError(
                        "You tried to sign an older version of the agreement.",
                        code="old_version",
                    )
        return attrs
