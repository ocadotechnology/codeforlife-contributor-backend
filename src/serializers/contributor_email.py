"""
© Ocado Group
Created on 12/07/2024 at 14:07:59(+01:00).
"""

import typing as t

from rest_framework import serializers

from ..models import AgreementSignature, ContributorEmail
from ._model_list_serializer import ModelListSerializer
from ._model_serializer import ModelSerializer

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-many-ancestors


class ContributorEmailCheckSignedLatestAgreementListSerializer(
    ModelListSerializer[ContributorEmail]
):
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        email_indicies = {
            t.cast(str, contributor_email["email"]).lower(): i
            for i, contributor_email in enumerate(representation)
        }

        signed_emails = ContributorEmail.objects.filter(
            email__in=email_indicies.keys(),
            contributor__agreement_signatures__agreement_id=(
                AgreementSignature.get_latest_sha_from_github()
            ),
        ).values_list("email", flat=True)

        for signed_email in signed_emails:
            representation[email_indicies[signed_email]]["has_signed"] = True

        return representation


class ContributorEmailCheckSignedLatestAgreementSerializer(
    ModelSerializer[ContributorEmail]
):
    has_signed = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        model = ContributorEmail
        fields = ["email", "has_signed"]
        extra_kwargs: t.Dict[str, t.Dict[str, t.Any]] = {
            "email": {"validators": []}
        }
        list_serializer_class = (
            ContributorEmailCheckSignedLatestAgreementListSerializer
        )
