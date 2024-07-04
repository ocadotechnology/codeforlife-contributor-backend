"""
© Ocado Group
Created on 02/07/2024 at 16:27:55(+01:00).
"""

from datetime import timedelta
from unittest.mock import patch

from codeforlife.tests import ModelSerializerTestCase
from codeforlife.user.models import User
from django.utils import timezone

from ..models import Fruit
from .fruit import FruitSerializer


# pylint: disable-next=missing-class-docstring
class TestFruitSerializer(ModelSerializerTestCase[User, Fruit]):
    model_serializer_class = FruitSerializer

    def test_create(self):
        """Creating a fruit instance sets the expiry date to 3 days from now."""
        now = timezone.now()
        with patch.object(timezone, "now", return_value=now):
            self.assert_create(
                validated_data={"name": "kiwi", "is_citrus": False},
                new_data={"expires_on": now.date() + timedelta(days=3)},
            )
