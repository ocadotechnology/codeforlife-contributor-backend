"""
© Ocado Group
Created on 12/07/2024 at 17:16:58(+01:00).
"""

from datetime import timedelta

from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User
from django.utils import timezone

from ..models import AgreementSignature, Contributor
from .agreement_signature import AgreementSignatureSerializer


# pylint: disable-next=missing-function-docstring,too-many-ancestors
class TestAgreementSignatureSerializer(
    ModelSerializerTestCase[User, AgreementSignature]
):
    """Test the Agreement Signature serializers"""

    model_serializer_class = AgreementSignatureSerializer
    fixtures = ["contributors", "agreement_signatures"]

    def setUp(self):
        self.contributor = Contributor.objects.get(pk=1)

    def test_validate_signed_at__signed_in_future(self):
        """Can validate the time the signature was signed at."""
        time = timezone.now() + timedelta(hours=10)
        self.assert_validate_field(
            name="signed_at",
            value=time,
            error_code="signed_in_future",
        )

    def test_validate__invalid_commit_id(self):
        """Can check the validity of the agreement ID"""
        self.assert_validate(
            attrs={
                "contributor": 1,
                "agreement_id": "1234567890",
                "signed_at": "2024-02-02T12:00:00Z",
            },
            error_code="invalid_commit_id",
        )

    def test_validate__agreement_not_in_files(self):
        """Can check if Agreement not in commit files"""
        self.assert_validate(
            attrs={
                "contributor": 1,
                "agreement_id": "be894d07641a174b9000c177b92b82bd357d2e63",
                "signed_at": "2024-02-02T12:00:00Z",
            },
            error_code="agreement_not_in_files",
        )

    def test_validate__old_version(self):
        """Can check if contributor tried to sign an older version."""
        self.assert_validate(
            attrs={
                "contributor": 1,
                "agreement_id": "81efd9e68f161104071f7bef7f9256e4840c1af7",
                "signed_at": "2024-06-02T12:00:00Z",
            },
            error_code="old_version",
        )
