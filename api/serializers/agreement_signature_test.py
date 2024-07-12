"""
© Ocado Group
Created on 12/07/2024 at 17:16:58(+01:00).
"""

from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User

from ..models import AgreementSignature
from .agreement_signature import AgreementSignatureSerializer


class TestAgreementSignatureSerializer(
    ModelSerializerTestCase[User, AgreementSignature]
):
    """Test the Agreement Signature serializers"""

    model_serializer_class = AgreementSignatureSerializer
