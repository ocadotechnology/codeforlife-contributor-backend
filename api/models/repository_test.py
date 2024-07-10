"""
© Ocado Group
Created on 09/07/2024 at 11:43:31(+01:00).
"""

from codeforlife.tests import ModelTestCase
from django.db import IntegrityError

from .contributor import Contributor
from .repository import Repository


class TestRepository(ModelTestCase[Repository]):
    """Test the Repository Model"""

    fixtures = ["contributors", "repositories"]

    def setUp(self):
        self.repository = Repository.objects.get(pk=1)
        self.contributor1 = Contributor.objects.get(pk=1)
        self.contributor2 = Contributor.objects.get(pk=2)

    def test_str(self):
        """Parsing a contributor object instance to returns its name."""
        expected = f"{self.repository.contributor}: {self.repository.gh_id}"
        assert str(self.repository) == expected

    def test_default_value(self):
        """check default value of points if not assigned"""
        new_contributor = Contributor.objects.create(
            id=425525,
            email="newcontributor@gmail.com",
            name="new contributor",
            location="london",
            html_url="https://github.com/newcontributor",
            avatar_url="https://contributornew.github.io/",
        )
        repository = Repository.objects.create(
            contributor=new_contributor, gh_id=432079567
        )
        assert repository.points == 0

    def test_unique_fields(self):
        """Test the unique fields functionality"""
        new_contributor = Contributor.objects.create(
            id=5134,
            email="newcontributor@gmail.com",
            name="new contributor",
            location="london",
            html_url="https://github.com/newcontributor",
            avatar_url="https://contributornew.github.io/",
        )
        Repository.objects.create(contributor=new_contributor, gh_id=432079567)

        with self.assertRaises(IntegrityError):
            Repository.objects.create(
                contributor=self.contributor1, gh_id=10274252
            )
