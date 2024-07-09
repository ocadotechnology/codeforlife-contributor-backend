"""
© Ocado Group
Created on 09/07/2024 at 11:43:42(+01:00).
"""

from codeforlife.tests import ModelTestCase
from .contributor import Contributor
from .repository import Repository
from .agreement_signature import AgreementSignature

class TestAgreementSignature(ModelTestCase[AgreementSignature]):
    fixtures = ["agreement_signatures"]

    def setUp(self):
        pass
    
    def test_str(self):
        """Parsing a contributor object instance to string returns its name."""
        pass
    
    def test_fields(self):
        """ Check if """
        pass