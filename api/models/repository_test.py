"""
© Ocado Group
Created on 09/07/2024 at 11:43:31(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .agreement_signature import AgreementSignature
from .contributor import Contributor
from .repository import Repository


class TestRepository(ModelTestCase[Repository]):
    """Test the Repository Model"""

    fixtures = ["repositories"]

    def setUp(self):
        self.repository = Repository.objects.get(pk=111)

    # def test_str(self):
    #     """Parsing a contributor object instance to string returns its name."""
    #     assert str(self.repository) == self.repository.name

    # def test_fields(self):
    #     """Check if"""
    #     pass
