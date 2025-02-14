"""
© Ocado Group
Created on 16/07/2024 at 14:59:49(+01:00).
"""

import json
from unittest.mock import ANY, patch

import requests
from django.conf import settings
from django.utils import timezone
from rest_framework import status

from ..models import AgreementSignature, Contributor
from ._model_view_set_test_case import ModelViewSetTestCase
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
        contributor = self.contributor1
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=contributor
            ).order_by("signed_at"),
            action="retrieve",
            request=self.client.request_factory.get(user=contributor),
        )

    def test_get_queryset__list(self):
        """Includes all of a contributor's agreement-signatures."""
        contributor = self.contributor1
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=contributor
            ).order_by("signed_at"),
            action="list",
            request=self.client.request_factory.get(user=contributor),
        )

    def test_get_queryset__check_signed(self):
        """
        Includes all of a contributor's agreement-signatures, ordered by the
        datetime they were signed.
        """
        contributor = self.contributor1
        self.assert_get_queryset(
            values=AgreementSignature.objects.filter(
                contributor=contributor
            ).order_by("signed_at"),
            action="check_signed",
            request=self.client.request_factory.get(user=contributor),
        )

    # test: actions

    def test_retrieve(self):
        """Can retrieve a single agreement-signature."""
        contributor = self.contributor1
        agreement_signature = contributor.agreement_signatures.first()
        assert agreement_signature

        self.client.login(contributor)
        self.client.retrieve(model=agreement_signature)

    def test_list(self):
        """Check list of all agreement signatures."""
        contributor = self.contributor1
        agreement_signatures = list(
            contributor.agreement_signatures.order_by("signed_at")
        )
        assert agreement_signatures

        self.client.login(contributor)
        self.client.list(models=agreement_signatures)

    def test_create(self):
        """Can create a contributor signature."""
        contributor = self.contributor1
        agreement_id = "81efd9e68f161104071f7bef7f9256e4840c1af7"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps([{"sha": agreement_id}]).encode("utf-8")

        self.client.login(contributor)

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.client.create(
                data={
                    "agreement_id": agreement_id,
                    "signed_at": timezone.now(),
                },
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=ANY,
            )

    def _test_check_signed_latest(
        self, contributor: Contributor, is_signed: bool, reason: str = ""
    ):
        latest_commit_id = "76241fa5e96ce9a620472842fee1ddadfd13cd86"

        response = requests.Response()
        response.status_code = status.HTTP_200_OK
        response.encoding = "utf-8"
        # pylint: disable-next=protected-access
        response._content = json.dumps([{"sha": latest_commit_id}]).encode(
            "utf-8"
        )

        self.client.login(contributor)

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            response = self.client.get(
                self.reverse_action("check-signed-latest")
            )

            self.assertDictEqual(
                response.json(),
                {
                    "latest_commit_id": latest_commit_id,
                    "is_signed": is_signed,
                    "reason": reason,
                },
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=ANY,
            )

    def test_check_signed_latest(self):
        """Contributor has signed the latest agreement."""
        self._test_check_signed_latest(self.contributor1, is_signed=True)

    def test_check_signed_latest__github_api_error(self):
        """GitHub API cannot process the get request."""
        response = requests.Response()
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        self.client.login(self.contributor3)

        with patch.object(
            requests, "get", return_value=response
        ) as requests_get:
            self.client.get(
                self.reverse_action("check-signed-latest"),
                status_code_assertion=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

            requests_get.assert_called_once_with(
                # pylint: disable-next=line-too-long
                url=f"https://api.github.com/repos/{settings.GH_ORG}/{settings.GH_REPO}/commits",
                headers={"X-GitHub-Api-Version": "2022-11-28"},
                params={"path": settings.GH_FILE, "per_page": 1},
                timeout=ANY,
            )

    def test_check_signed_latest__no_agreement_signatures(self):
        """Can check if user has NOT signed ANY contribution agreement."""
        self._test_check_signed_latest(
            self.contributor3, is_signed=False, reason="no_agreement_signatures"
        )

    def test_check_signed_latest__old_agreement_signatures(self):
        """
        Contributor has signed an agreement but it is not the latest one.
        """
        self._test_check_signed_latest(
            self.contributor2,
            is_signed=False,
            reason="old_agreement_signatures",
        )
