"""
© Ocado Group
Created on 12/07/2024 at 17:16:58(+01:00).
"""

from unittest.mock import patch

from ..models import AgreementSignature, ContributorEmail
from ._model_list_serializer_test_case import ModelListSerializerTestCase
from .contributor_email import (
    ContributorEmailCheckSignedLatestAgreementListSerializer,
    ContributorEmailCheckSignedLatestAgreementSerializer,
)


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorEmailCheckSignedLatestAgreementListSerializer(
    ModelListSerializerTestCase[ContributorEmail]
):
    model_serializer_class = (
        ContributorEmailCheckSignedLatestAgreementSerializer
    )
    model_list_serializer_class = (
        ContributorEmailCheckSignedLatestAgreementListSerializer
    )
    fixtures = ["contributors", "contributor_emails", "agreement_signatures"]

    def setUp(self):
        # Assume the latest agreement signature has the latest agreement ID.
        agreement_signature = AgreementSignature.objects.order_by(
            "signed_at"
        ).last()
        assert agreement_signature
        self.latest_agreement_id = agreement_signature.agreement_id

        # Get the first email of a contributor who has signed the latest
        # agreement.
        contributor_email = ContributorEmail.objects.filter(
            contributor__agreement_signatures__agreement_id=(
                self.latest_agreement_id
            )
        ).first()
        assert contributor_email
        self.contributor_email__signed_latest_agreement = contributor_email

        # Get the first email of a contributor who has agreement-signatures but
        # has not signed the latest agreement.
        contributor_email = (
            ContributorEmail.objects.filter(
                contributor__agreement_signatures__isnull=False
            )
            .exclude(
                contributor__agreement_signatures__agreement_id=(
                    self.latest_agreement_id
                )
            )
            .first()
        )
        assert contributor_email
        self.contributor_email__not_signed_latest_agreement = contributor_email

        # Get the first email of a contributor who has no agreement-signatures.
        contributor_email = ContributorEmail.objects.filter(
            contributor__agreement_signatures__isnull=True
        ).first()
        assert contributor_email
        self.contributor_email__no_agreement_signatures = contributor_email

    def test_to_representation(self):
        """
        Representation correctly determines which contributor-emails have signed
        the latest agreement.
        """
        with patch.object(
            AgreementSignature,
            "get_latest_sha_from_github",
            return_value=self.latest_agreement_id,
        ):
            self.assert_to_representation(
                instance=[
                    self.contributor_email__signed_latest_agreement,
                    self.contributor_email__not_signed_latest_agreement,
                    self.contributor_email__no_agreement_signatures,
                ],
                new_data=[
                    {"has_signed": True},
                    {"has_signed": False},
                    {"has_signed": False},
                ],
                non_model_fields={"has_signed"},
            )
