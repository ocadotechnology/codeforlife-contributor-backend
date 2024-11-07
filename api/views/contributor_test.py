"""
© Ocado Group
Created on 16/07/2024 at 14:54:09(+01:00).
"""

from ..models import Contributor
from ._model_view_set_test_case import ModelViewSetTestCase
from .contributor import ContributorViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorViewSet(ModelViewSetTestCase[Contributor]):
    basename = "contributor"
    model_view_set_class = ContributorViewSet
    fixtures = ["contributors"]

    def setUp(self):
        self.contributor1 = Contributor.objects.get(pk=1)

    def test_list(self):
        """Check list of all contributors."""
        self.client.list(models=list(Contributor.objects.all()))

    def test_retrieve(self):
        """Can retrieve a single contributor."""
        self.client.retrieve(model=self.contributor1)
