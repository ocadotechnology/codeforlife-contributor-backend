"""
© Ocado Group
Created on 16/07/2024 at 14:54:09(+01:00).
"""

from unittest.mock import Mock, patch

from codeforlife.permissions import AuthHeaderIsGitHubOidcToken

from ..models import AgreementSignature, ContributorEmail
from ..serializers import ContributorEmailCheckSignedLatestAgreementSerializer
from ._model_view_set_test_case import ModelViewSetTestCase
from .contributor_email import ContributorEmailViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorEmailViewSet(ModelViewSetTestCase[ContributorEmail]):
    basename = "contributor-email"
    model_view_set_class = ContributorEmailViewSet
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
        self.email__signed_latest_agreement = contributor_email.email

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
        self.email__not_signed_latest_agreement = contributor_email.email

        # Get the first email of a contributor who has no agreement-signatures.
        contributor_email = ContributorEmail.objects.filter(
            contributor__agreement_signatures__isnull=True
        ).first()
        assert contributor_email
        self.email__no_agreement_signatures = contributor_email.email

    # test: get permissions

    def test_get_permissions__check_signed_latest_agreement(self):
        """
        Only our GitHub pipelines can check if a list of emails have signed the
        latest agreement.
        """
        self.assert_get_permissions(
            permissions=[AuthHeaderIsGitHubOidcToken()],
            action="check_signed_latest_agreement",
        )

    # test: get serializers

    def test_get_serializer_class__check_signed_latest_agreement(self):
        """
        Checking if a list of emails have signed the latest agreement has a
        dedicated serializer.
        """
        self.assert_get_serializer_class(
            ContributorEmailCheckSignedLatestAgreementSerializer,
            action="check_signed_latest_agreement",
        )

    # test: actions

    @patch.object(
        AuthHeaderIsGitHubOidcToken, "has_permission", return_value=True
    )
    def test_check_signed_latest_agreement(
        self, has_github_oidc_token__has_permission: Mock
    ):
        """
        Check a list of contributor-email's have signed the latest agreement.
        """
        with patch.object(
            AgreementSignature,
            "get_latest_sha_from_github",
            return_value=self.latest_agreement_id,
        ) as agreement_signature__get_latest_sha_from_github:
            response = self.client.post(
                self.reverse_action("check_signed_latest_agreement"),
                data=[
                    {"email": self.email__signed_latest_agreement},
                    {"email": self.email__not_signed_latest_agreement},
                    {"email": self.email__no_agreement_signatures},
                ],
            )

            agreement_signature__get_latest_sha_from_github.assert_called_once()
        has_github_oidc_token__has_permission.assert_called_once()

        self.assertListEqual(
            response.json(),
            [
                {
                    "email": self.email__signed_latest_agreement,
                    "has_signed": True,
                },
                {
                    "email": self.email__not_signed_latest_agreement,
                    "has_signed": False,
                },
                {
                    "email": self.email__no_agreement_signatures,
                    "has_signed": False,
                },
            ],
        )
