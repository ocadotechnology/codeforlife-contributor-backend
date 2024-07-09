"""
© Ocado Group
Created on 09/07/2024 at 09:39:50(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .contributor import Contributor


class TestContributor(ModelTestCase[Contributor]):
    fixtures = ["contributors"]

    def setUp(self):
        self.contributor = Contributor.objects.get(pk=111111)

    def test_str(self):
        """Parsing a contributor object instance to string returns its name."""
        assert str(self.contributor) == self.contributor.name

    def test_fields(self):
        """Check if"""
        assert self.contributor.email == "contributor1@gmail.com"
