"""
© Ocado Group
Created on 09/07/2024 at 11:43:42(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .agreement_signature import AgreementSignature
from .contributor import Contributor
# from .repository import Repository


class TestAgreementSignature(ModelTestCase[AgreementSignature]):
    """Test the AgreementSignature Model"""

    fixtures = ["agreement_signatures"]

    def setUp(self):
        self.agreement_signature = Contributor.objects.get(pk=1)

    # def test_str(self):
    #     """Parsing a contributor object instance to returns its name."""
    #     pass

    # def test_fields(self):
    #     """Check if"""
    #     pass
