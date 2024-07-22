"""
© Ocado Group
Created on 12/07/2024 at 17:16:58(+01:00).
"""

import json
from datetime import timedelta
from unittest.mock import call, patch

import requests
from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User
from django.conf import settings
from django.utils import timezone
from rest_framework import status

from ..models import AgreementSignature, Contributor
from .agreement_signature import AgreementSignatureSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestAgreementSignatureSerializer(
    ModelSerializerTestCase[User, AgreementSignature]
):
    model_serializer_class = AgreementSignatureSerializer
    fixtures = ["contributors", "agreement_signatures"]

    def setUp(self):
        self.contributor = Contributor.objects.get(pk=1)

    def test_validate_signed_at__signed_in_future(self):
        """Cannot sign in the future."""
        self.assert_validate_field(
            name="signed_at",
            value=timezone.now() + timedelta(hours=10),
            error_code="signed_in_future",
        )

    def test_validate__invalid_commit_id(self):
        """Agreement id must be an existing commit SHA on GitHub."""
        agreement_id = "1234567890"

        response = requests.Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.assert_validate(
                attrs={
                    "contributor": self.contributor,
                    "agreement_id": agreement_id,
                    "signed_at": timezone.now(),
                },
                error_code="invalid_commit_id",
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits/{agreement_id}",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                timeout=5,
            )

    def test_validate__agreement_not_in_files(self):
        """Can check if Agreement not in commit files"""
        agreement_id = "be894d07641a174b9000c177b92b82bd357d2e63"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps({"files": []}).encode("utf-8")

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.assert_validate(
                attrs={
                    "contributor": self.contributor,
                    "agreement_id": agreement_id,
                    "signed_at": timezone.now(),
                },
                error_code="agreement_not_in_files",
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits/{agreement_id}",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                timeout=5,
            )

    def test_validate__old_version(self):
        """Can check if contributor tried to sign an older version."""

        agreement_id = "81efd9e68f161104071f7bef7f9256e4840c1af7"
        now = timezone.now()

        current_response = requests.Response()
        current_response.status_code = status.HTTP_200_OK
        current_response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        current_response._content = json.dumps(
            {
                "files": [{"filename": settings.GH_FILE}],
                "commit": {"author": {"date": str(now - timedelta(days=1))}},
            }
        ).encode("utf-8")

        last_response = requests.Response()
        last_response.status_code = status.HTTP_200_OK
        last_response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        last_response._content = json.dumps(
            {
                "files": [{"filename": settings.GH_FILE}],
                "commit": {"author": {"date": str(now)}},
            }
        ).encode("utf-8")

        last_agreement_signature = self.contributor.last_agreement_signature
        assert last_agreement_signature

        with patch.object(
            requests, "get", side_effect=[current_response, last_response]
        ) as requests_get:
            self.assert_validate(
                attrs={
                    "contributor": self.contributor,
                    "agreement_id": agreement_id,
                    "signed_at": now - timedelta(days=1),
                },
                error_code="old_version",
            )

            requests_get.assert_has_calls(
                [
                    call(
                        # pylint: disable-next=line-too-long
                        url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits/{agreement_id}",
                        headers={"X-GitHub-Api-Version": "2022-11-28"},
                        timeout=5,
                    ),
                    call(
                        # pylint: disable-next=line-too-long
                        url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits/{last_agreement_signature.agreement_id}",
                        headers={"X-GitHub-Api-Version": "2022-11-28"},
                        timeout=5,
                    ),
                ]
            )
