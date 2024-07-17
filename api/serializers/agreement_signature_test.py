"""
© Ocado Group
Created on 12/07/2024 at 17:16:58(+01:00).
"""

from datetime import timedelta

from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User
from django.utils import timezone

from ..models import AgreementSignature
from .agreement_signature import AgreementSignatureSerializer


# pylint: disable-next=missing-function-docstring,too-many-ancestors
class TestAgreementSignatureSerializer(
    ModelSerializerTestCase[User, AgreementSignature]
):
    """Test the Agreement Signature serializers"""

    model_serializer_class = AgreementSignatureSerializer

    def test_validate_signed_at__signed_in_future(self):
        """Can validate the time the signature was signed at."""
        time = timezone.now() + timedelta(hours=10)
        self.assert_validate_field(
            name="signed_at",
            value=time,
            error_code="signed_in_future",
        )
