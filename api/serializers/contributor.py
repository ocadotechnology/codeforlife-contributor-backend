from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import Contributor


class ContributorSerializer(ModelSerializer[User, Contributor]):
    """Contributor class"""

    class Meta:
        model = Contributor
        fields = "__all__"
