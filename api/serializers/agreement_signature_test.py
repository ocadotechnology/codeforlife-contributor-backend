"""
© Ocado Group
Created on 12/07/2024 at 17:16:58(+01:00).
"""

import json
from datetime import timedelta
from unittest.mock import ANY, patch

import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import status

from ..common import ModelSerializerTestCase
from ..models import AgreementSignature, Contributor
from .agreement_signature import AgreementSignatureSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestAgreementSignatureSerializer(
    ModelSerializerTestCase[AgreementSignature]
):
    model_serializer_class = AgreementSignatureSerializer
    fixtures = ["contributors", "agreement_signatures"]

    def setUp(self):
        self.contributor = Contributor.objects.get(pk=1)

    def test_validate_agreement_id__only_latest(self):
        """Can only sign the latest agreement."""
        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps([{"sha": "b"}]).encode("utf-8")

        with patch.object(
                requests, "get", return_value=response
        ) as requests_get:
            self.assert_validate_field(
                name="agreement_id",
                value="a",
                error_code="only_latest",
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=ANY,
            )

    def test_validate_signed_at__signed_in_future(self):
        """Cannot sign in the future."""
        self.assert_validate_field(
            name="signed_at",
            value=timezone.now() + timedelta(hours=10),
            error_code="signed_in_future",
        )

    def test_create(self):
        """Can successfully create a contributor."""
        self.assert_create(
            validated_data={
                "signed_at": timezone.now() - timedelta(seconds=10),
                "agreement_id": "t9hoswlwi6rme2wlgvmhunl6r1gjfsnc910u7p3k",
            },
            context={
                "request": self.request_factory.post(user=self.contributor)
            },
        )
