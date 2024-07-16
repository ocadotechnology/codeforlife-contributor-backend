"""
© Ocado Group
Created on 16/07/2024 at 14:59:49(+01:00).
"""

from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User

from ..models import AgreementSignature
from .agreement_signature import AgreementSignatureViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestAgreementSignatureViewSet(
    ModelViewSetTestCase[User, AgreementSignature]
):
    """Testing agreement signature view set."""

    basename = "agreement"
    model_view_set_class = AgreementSignatureViewSet
    fixtures = ["agreement_signature", "contributors"]
