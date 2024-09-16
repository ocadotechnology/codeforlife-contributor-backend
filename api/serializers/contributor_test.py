"""
© Ocado Group
Created on 12/07/2024 at 11:36:23(+01:00).
"""

from ..common import ModelSerializerTestCase
from ..models import Contributor
from .contributor import ContributorSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorSerializer(ModelSerializerTestCase[Contributor]):
    model_serializer_class = ContributorSerializer
