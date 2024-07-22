"""
© Ocado Group
Created on 16/07/2024 at 14:59:49(+01:00).
"""

import json
import typing as t
from datetime import timedelta
from unittest.mock import call, patch

import requests
from codeforlife.tests import ModelViewSetTestCase
from codeforlife.types import DataDict
from codeforlife.user.models import User
from django.utils import timezone
from rest_framework import status

import settings

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

    def test_create(self):
        """Can create a contributor signature."""
        self.client.create(
            data={
                "contributor": 4,
                "agreement_id": "81efd9e68f161104071f7bef7f9256e4840c1af7",
                "signed_at": timezone.now() - timedelta(days=1),
            },
        )

    def test_check_signed__signed(self):
        """
        Contributor has signed the latest agreement.
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
            self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": 1},
                ),
                status_code_assertion=status.HTTP_200_OK,
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params=t.cast(
                    DataDict, {"path": settings.GH_FILE, "per_page": 1}
                ),
                timeout=5,
            )

    def test_check_signed__no_response(self):
        """
        API cannot process the get request.
        """
        agreement_id = "76241fa5e96ce9a620472842fee1ddadfd13cd86"
        response = requests.Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": 3},
                ),
                status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params=t.cast(
                    DataDict, {"path": settings.GH_FILE, "per_page": 1}
                ),
                timeout=5,
            )

    def test_check_signed__not_signed(self):
        """
        Can check if user has NOT signed ANY contribution agreement.
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
            self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": 3},
                ),
                status_code_assertion=status.HTTP_404_NOT_FOUND,
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params=t.cast(
                    DataDict, {"path": settings.GH_FILE, "per_page": 1}
                ),
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
            self.client.get(
                self.reverse_action(
                    "check_signed",
                    kwargs={"contributor_pk": 2},
                ),
                # pylint: disable-next=line-too-long
                status_code_assertion=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params=t.cast(
                    DataDict, {"path": settings.GH_FILE, "per_page": 1}
                ),
                timeout=5,
            )
