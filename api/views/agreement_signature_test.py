"""
© Ocado Group
Created on 16/07/2024 at 14:59:49(+01:00).
"""

from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User
from rest_framework import status

from ..models import AgreementSignature
from .agreement_signature import AgreementSignatureViewSet


# pylint: disable-next=too-many-ancestors
class TestAgreementSignatureViewSet(
    ModelViewSetTestCase[User, AgreementSignature]
):
    """Testing agreement signature view set."""

    basename = "agreement-signature"
    model_view_set_class = AgreementSignatureViewSet
    fixtures = ["agreement_signatures", "contributors"]

    def setUp(self):
        self.agreement1 = AgreementSignature.objects.get(pk=1)
        self.agreement2 = AgreementSignature.objects.get(pk=2)
        self.agreement3 = AgreementSignature.objects.get(pk=3)

    def test_list(self):
        """Check list of all agreement signatures."""
        self.client.list(
            models=[self.agreement1, self.agreement2, self.agreement3]
        )

    def test_retrieve(self):
        """Can retrieve a single contributor."""
        self.client.retrieve(model=self.agreement1)

    def test_create(self):
        """Can create a contributor signature."""
        self.client.create(
            data={
                "contributor": 4,
                "agreement_id": "4e694741a4501f224435c6adf23dd6f0122ccbf4",
                "signed_at": "2024-01-02T12:00:00Z",
            }
        )

    def test_check_signed(self):
        """
        Can check if user has signed the latest contribution agreement.
        """

        self.client.get(
            self.reverse_action(
                "check_signed",
                kwargs={"contributor_pk": 1},
            ),
            status_code_assertion=status.HTTP_200_OK,
        )

    def test_not_signed(self):
        """
        Can check if user has NOT signed ANY contribution agreement.
        """
        self.client.get(
            self.reverse_action(
                "check_signed",
                kwargs={"contributor_pk": 3},
            ),
            status_code_assertion=status.HTTP_404_NOT_FOUND,
        )

    def test_not_latest_agreement(self):
        """
        Can check if user has signed an contribution agreement
        but it is not the latest one.
        """
        self.client.get(
            self.reverse_action(
                "check_signed",
                kwargs={"contributor_pk": 2},
            ),
            status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
        )

    def test_no_contributor(self):
        """
        Can check if user is not a contributor at all.
        """
        self.client.get(
            self.reverse_action(
                "check_signed",
                kwargs={"contributor_pk": 190},
            ),
            status_code_assertion=status.HTTP_404_NOT_FOUND,
        )
