"""
© Ocado Group
Created on 12/07/2024 at 11:36:23(+01:00).
"""

from ..models import Contributor
from ._model_serializer_test_case import ModelSerializerTestCase
from .contributor import ContributorSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class TestContributorSerializer(ModelSerializerTestCase[Contributor]):
    model_serializer_class = ContributorSerializer
