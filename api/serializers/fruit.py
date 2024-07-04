"""
© Ocado Group
Created on 02/07/2024 at 15:21:47(+01:00).
"""

from datetime import timedelta

from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User
from django.utils import timezone

from ..models import Fruit


# pylint: disable-next=missing-class-docstring
class FruitSerializer(ModelSerializer[User, Fruit]):
    class Meta:
        model = Fruit
        fields = ["id", "name", "is_citrus", "expires_on"]
        extra_kwargs = {
            "id": {"read_only": True},
            "expires_on": {"read_only": True},
        }

    def create(self, validated_data):
        validated_data["expires_on"] = timezone.now().date() + timedelta(days=3)
        return super().create(validated_data)
