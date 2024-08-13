"""
© Ocado Group
Created on 12/07/2024 at 11:36:23(+01:00).
"""

from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User

from ..models import Contributor
from .contributor import ContributorSerializer


# pylint: disable-next=missing-class-docstring,
class TestContributorSerializer(ModelSerializerTestCase[User, Contributor]):
    model_serializer_class = ContributorSerializer
