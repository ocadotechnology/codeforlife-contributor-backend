"""
© Ocado Group
Created on 16/07/2024 at 14:59:49(+01:00).
"""

import json
from unittest.mock import patch

import requests
from codeforlife.user.models import User
from django.conf import settings
from django.utils import timezone
from rest_framework import status

from ..common import ModelViewSetTestCase
from ..models import AgreementSignature, Contributor
from .agreement_signature import AgreementSignatureViewSet


# pylint: disable-next=too-many-ancestors,missing-class-docstring
class TestAgreementSignatureViewSet(ModelViewSetTestCase[AgreementSignature]):
    basename = "agreement-signature"
    model_view_set_class = AgreementSignatureViewSet
    fixtures = ["agreement_signatures", "contributors"]

    def setUp(self):
        self.contributor1 = Contributor.objects.get(pk=1)
        self.contributor2 = Contributor.objects.get(pk=2)
        self.contributor3 = Contributor.objects.get(pk=3)
        self.agreement1 = AgreementSignature.objects.get(pk=1)

    # test: get queryset

    def test_get_queryset__retrieve(self):
        """Includes all of a contributor's agreement-signatures."""
        self.client.login_as(self.contributor1)
        
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=self.contributor1
            ).order_by("signed_at"),
            action="retrieve",
        )

    def test_get_queryset__list(self):
        """Includes all of a contributor's agreement-signatures."""
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=self.contributor1
            ),
            action="list",
            kwargs={"contributor_pk": self.contributor1.pk},
        )

    def test_get_queryset__check_signed(self):
        """
        Includes all of a contributor's agreement-signatures, ordered by the
        datetime they were signed.
        """
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=self.contributor1
            ).order_by("signed_at"),
            action="check_signed",
            kwargs={"contributor_pk": self.contributor1.pk},
        )

    # test: actions

    def test_retrieve(self):
        """Can retrieve a single agreement-signature."""
        self.client.retrieve(model=self.agreement1)

    def test_list(self):
        """Check list of all agreement signatures."""
        self.client.list(models=list(AgreementSignature.objects.all()))

    def test_create(self):
        """Can create a contributor signature."""
        self.client.create(
            data={
                "contributor": 4,
                "agreement_id": "81efd9e68f161104071f7bef7f9256e4840c1af7",
                "signed_at": timezone.now(),
            },
        )

    def test_check_signed__signed(self):
        """Contributor has signed the latest agreement."""
        agreement_id = "76241fa5e96ce9a620472842fee1ddadfd13cd86"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps([{"sha": agreement_id}]).encode("utf-8")

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": self.contributor1.pk},
                )
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=5,
            )

    def test_check_signed__no_response(self):
        """API cannot process the get request."""
        response = requests.Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": self.contributor3.pk},
                ),
                status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=5,
            )

    def test_check_signed__not_signed(self):
        """Can check if user has NOT signed ANY contribution agreement."""
        agreement_id = "76241fa5e96ce9a620472842fee1ddadfd13cd86"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps([{"sha": agreement_id}]).encode("utf-8")

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            response = self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": self.contributor3.pk},
                ),
                status_code_assertion=status.HTTP_404_NOT_FOUND,
            )

            assert agreement_id == response.json()["latest_commit_id"]

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=5,
            )

    def test_check_signed__not_latest_agreement(self):
        """
        Contributor has signed an agreement but it is not the latest one.
        """
        agreement_id = "76241fa5e96ce9a620472842fee1ddadfd13cd86"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps([{"sha": agreement_id}]).encode("utf-8")

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            response = self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": self.contributor2.pk},
                ),
                # pylint: disable-next=line-too-long
                status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

            assert agreement_id == response.json()["latest_commit_id"]

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=5,
            )
