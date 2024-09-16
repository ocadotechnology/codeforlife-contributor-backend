"""
© Ocado Group
Created on 12/07/2024 at 14:07:45(+01:00).
"""

import typing as t
from datetime import datetime

import requests
from codeforlife.types import JsonDict
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from ..common import ModelSerializer
from ..models import AgreementSignature

# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-many-ancestors


class AgreementSignatureSerializer(ModelSerializer[AgreementSignature]):
    class Meta:
        model = AgreementSignature
        fields = ["id", "agreement_id", "signed_at"]

    def validate_agreement_id(self, value: str):
        if AgreementSignature.get_latest_sha_from_github() != value:
            raise serializers.ValidationError(
                "Can only sign the latest agreement", code="only_latest"
            )

        return value

    def validate_signed_at(self, value: datetime):
        if value > timezone.now():
            raise serializers.ValidationError(
                "Cannot sign in the future", code="signed_in_future"
            )

        return value

    def create(self, validated_data):
        validated_data["contributor"] = self.request.contributor
        return super().create(validated_data)
