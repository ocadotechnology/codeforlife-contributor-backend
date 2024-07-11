from codeforlife.serializers import ModelSerializer
from codeforlife.user.models import User

from ..models import AgreementSignature

class ContributorSerializer(ModelSerializer[User, AgreementSignature]):
    class Meta:
        model = AgreementSignature
        fields = "__all__"