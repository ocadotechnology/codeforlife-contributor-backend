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
