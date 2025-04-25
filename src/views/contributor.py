"""
© Ocado Group
Created on 16/07/2024 at 11:03:09(+01:00).
"""

from codeforlife.permissions import AllowAny

from ..models import Contributor
from ..serializers import ContributorSerializer
from ._model_view_set import ModelViewSet


# pylint: disable-next=missing-class-docstring,too-many-ancestors
class ContributorViewSet(ModelViewSet[Contributor]):
    http_method_names = ["get"]
    permission_classes = [AllowAny]
    model_class = Contributor
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
