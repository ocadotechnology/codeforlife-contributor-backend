"""
© Ocado Group
Created on 16/07/2024 at 11:03:09(+01:00).
"""

from codeforlife.permissions import AllowAny
from codeforlife.user.models import User
from codeforlife.views import ModelViewSet

from ..models import Contributor
from ..serializers import ContributorSerializer


# pylint: disable-next=too-many-ancestors
class ContributorViewSet(ModelViewSet[User, Contributor]):
    """
    List, create, update, delete Contributors on the view.
    """

    http_method_names = ["get", "post"]
    permission_classes = [AllowAny]
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
