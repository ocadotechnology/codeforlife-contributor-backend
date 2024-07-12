"""
© Ocado Group
Created on 12/07/2024 at 14:07:45(+01:00).
"""

from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import AgreementSignature


class AgreementSignatureSerializer(ModelSerializer[User, AgreementSignature]):
    """Agreement serializer"""

    class Meta:
        """Specify fields for the serializer"""

        model = AgreementSignature
        fields = "__all__"
