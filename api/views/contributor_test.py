"""
© Ocado Group
Created on 16/07/2024 at 14:54:09(+01:00).
"""

from codeforlife.tests import ModelViewSetTestCase
from codeforlife.user.models import User

from ..models import Contributor
from .contributor import ContributorViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorViewSet(ModelViewSetTestCase[User, Contributor]):
    """Testing contributor view set."""

    basename = "contributor"
    model_view_set_class = ContributorViewSet
    fixtures = ["contributors"]

    def setUp(self):
        self.contributor1 = Contributor.objects.get(pk=1)
        self.contributor2 = Contributor.objects.get(pk=2)
        self.contributor3 = Contributor.objects.get(pk=3)

    def test_list(self):
        """Check list of all contributors."""
        self.client.list(models=list(Contributor.objects.all()))

    def test_retrieve(self):
        """Can retrieve a single contributor."""
        self.client.retrieve(model=self.contributor1)

    def test_create(self):
        """Can create a contributor."""
        self.client.create(
            data={
                "id": 100,
                "email": "contributor1@gmail.com",
                "name": "Test Contributor",
                "location": "Hatfield",
                "html_url": "https://github.com/contributortest",
                "avatar_url": "https://contributortest.github.io/",
            }
        )
