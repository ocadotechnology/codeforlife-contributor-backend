"""
© Ocado Group
Created on 12/07/2024 at 14:07:59(+01:00).
"""
from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import Contributor


class ContributorSerializer(ModelSerializer[User, Contributor]):
    """Contributor serializer class"""

    class Meta:
        model = Contributor
        fields = "__all__"
