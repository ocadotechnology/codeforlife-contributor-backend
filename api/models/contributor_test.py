"""
© Ocado Group
Created on 09/07/2024 at 09:39:50(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .contributor import Contributor


class TestContributor(ModelTestCase[Contributor]):
    """Test the Contributor Model"""

    fixtures = ["contributors"]

    def setUp(self):
        self.contributor1 = Contributor.objects.get(pk=1)
        self.contributor2 = Contributor.objects.get(pk=2)
        self.contributor3 = Contributor.objects.get(pk=3)

    def test_str(self):
        """Parsing a contributor object instance to returns its name."""
        name = self.contributor1.name
        email = self.contributor1.email
        assert str(self.contributor1) == f"{name} <{email}>"

    def test_fields(self):
        """Check the correct fields"""
        assert self.contributor1.email == "contributor1@gmail.com"
        assert self.contributor2.email == "contributor2@gmail.com"
        assert self.contributor3.email == "contributor3@gmail.com"
