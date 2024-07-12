from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import Contributor


class ContributorSerializer(ModelSerializer[User, Contributor]):
    """Contributor class"""

    class Meta:
        """Specify fields for the serializer"""

        model = Contributor
        fields = "__all__"
