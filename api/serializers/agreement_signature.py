"""
© Ocado Group
Created on 12/07/2024 at 14:07:45(+01:00).
"""

from datetime import datetime

from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User
from django.utils import timezone
from rest_framework import serializers

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
