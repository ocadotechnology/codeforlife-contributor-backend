"""
© Ocado Group
Created on 02/07/2024 at 15:24:20(+01:00).
"""

from codeforlife.permissions import AllowAny
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet

from ..models import Fruit
from ..serializers import FruitSerializer


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class FruitViewSet(ModelViewSet[User, Fruit]):
    http_method_names = ["get", "post"]
    permission_classes = [AllowAny]
    serializer_class = FruitSerializer
    queryset = Fruit.objects.all()
