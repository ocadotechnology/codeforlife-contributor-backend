"""
© Ocado Group
Created on 09/07/2024 at 11:43:31(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .agreement_signature import AgreementSignature
from .contributor import Contributor
from .repository import Repository


class TestRepository(ModelTestCase[Repository]):
    fixtures = ["repositories"]

    def setUp(self):
        pass

    def test_str(self):
        """Parsing a contributor object instance to string returns its name."""
        pass

    def test_fields(self):
        """Check if"""
        pass
