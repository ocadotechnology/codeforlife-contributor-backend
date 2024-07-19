"""
© Ocado Group
Created on 16/07/2024 at 14:59:49(+01:00).
"""

from unittest.mock import patch

from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User
from rest_framework import status

from ..models import AgreementSignature, Contributor
from .agreement_signature import AgreementSignatureViewSet


# pylint: disable-next=too-many-ancestors,missing-class-docstring
class TestAgreementSignatureViewSet(
    ModelViewSetTestCase[User, AgreementSignature]
):
    basename = "agreement-signature"
    model_view_set_class = AgreementSignatureViewSet
    fixtures = ["agreement_signatures", "contributors"]

    def setUp(self):
        self.contributor = Contributor.objects.get(pk=1)
        self.agreement1 = AgreementSignature.objects.get(pk=1)
        self.agreement2 = AgreementSignature.objects.get(pk=2)
        self.agreement3 = AgreementSignature.objects.get(pk=3)

    # test: get queryset

    def test_get_queryset__retrieve(self):
        """Includes all of a contributor's agreement-signatures."""
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=self.contributor
            ),
            action="retrieve",
            kwargs={"contributor_pk": self.contributor.pk},
        )

    def test_get_queryset__list(self):
        """Includes all of a contributor's agreement-signatures."""
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=self.contributor
            ),
            action="list",
            kwargs={"contributor_pk": self.contributor.pk},
        )

    def test_get_queryset__check_signed(self):
        """
        Includes all of a contributor's agreement-signatures, ordered by the
        datetime they were signed.
        """
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=self.contributor
            ).order_by("signed_at"),
            action="check_signed",
            kwargs={"contributor_pk": self.contributor.pk},
        )

    # test: actions

    def test_retrieve(self):
        """Can retrieve a single agreement-signature."""
        self.client.retrieve(model=self.agreement1)

    def test_list(self):
        """Check list of all agreement signatures."""
        self.client.list(
            models=[self.agreement1, self.agreement2, self.agreement3]
        )

    # TODO: salman
    def test_create(self):
        """Can create a contributor signature."""
        self.client.create(
            data={
                "contributor": 4,
                "agreement_id": "81efd9e68f161104071f7bef7f9256e4840c1af7",
                "signed_at": "2024-01-02T12:00:00Z",
            },
        )

    # TODO: salman
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

    # TODO: salman
    def test_check_signed__not_signed(self):
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

    # TODO: salman
    def test_check_signed__not_latest_agreement(self):
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

    # TODO: salman
    def test_check_signed__no_contributor(self):
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
