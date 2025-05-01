"""
© Ocado Group
Created on 09/07/2024 at 11:43:31(+01:00).
"""

from codeforlife.tests import ModelTestCase

from .repository import Repository


class TestRepository(ModelTestCase[Repository]):
    """Test the Repository Model"""

    fixtures = ["contributors", "repositories"]

    def setUp(self):
        self.repository = Repository.objects.get(pk=1)

    def test_str(self):
        """
        Parsing a repository instance to a string
        returns the contributor's primary key and
        the repository's GitHub ID.
        """
        expected = f"{self.repository.contributor.pk}:{self.repository.gh_id}"
        assert str(self.repository) == expected
