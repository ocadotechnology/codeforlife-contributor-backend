"""
© Ocado Group
Created on 09/07/2024 at 09:39:50(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .contributor import Contributor


class TestContributor(ModelTestCase[Contributor]):
    """Test the Contributor Model"""

    fixtures = ["contributors", "contributor_emails"]

    def setUp(self):
        self.contributor = Contributor.objects.get(pk=1)

    def test_str(self):
        """
        Parsing a contributor instance to a string returns its name and email.
        """
        name = self.contributor.name
        email = self.contributor.primary_email
        assert str(self.contributor) == f"{name} <{email}>"
